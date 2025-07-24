"""
This module provides utility functions for caching and loading pandas DataFrame and
Series objects using feather format. It includes functions for saving and loading
indexes, values, and managing cache directories.

Functions:
    - _save_index(index, path, name): Save the index to a feather file (internal use).
    - _load_index(path, name): Load the index from a feather file (internal use).
    - _save_values(df, path): Save the values of the DataFrame or Series to a feather
      file (internal use).
    - _load_values(path): Load the values of the DataFrame or Series from a feather file
      (internal use).
    - _save_cache(df, path, overwrite=False): Save the DataFrame or Series to a cache
      directory.
    - load_cache(path): Load the DataFrame or Series from a cache directory.
    - cache_and_load(obj, path, overwrite=False): Cache and load a DataFrame or Series.

Classes:
    - UtilsAccessor: Accessor for utility functions to save and load pandas objects.

Example:
    >>> import pandas as pd
    >>> from pirrtools import cache_and_load
    >>> df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    >>> path = 'cache_dir'
    >>> cached_df = cache_and_load(df, path)
    >>> print(cached_df)

Note:
    This module is part of the pirrtools package and is intended for internal use. The
      primary
    functions are not meant to be called directly by users.
"""

import json
import shutil
from typing import Union
from pathlib import Path
import pandas as pd
from pandas import Index, MultiIndex, DataFrame, Series
from pandas.api.extensions import register_dataframe_accessor as reg_df
from pandas.api.extensions import register_series_accessor as reg_ser
from pyarrow.lib import ArrowInvalid
import re
from rich.table import Table
from rich.console import Console
from rich import box
from rich.text import Text

PandasObject = Union[DataFrame, Series]


def _parse_css_color(css_value: str) -> str:
    """Extract color from CSS property value.

    Args:
        css_value: CSS color value like '#ff0000', 'rgb(255, 0, 0)', etc.

    Returns:
        Rich-compatible color string
    """
    css_value = css_value.strip()

    # Handle hex colors
    if css_value.startswith("#"):
        return css_value

    # Handle rgb() colors
    rgb_match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", css_value)
    if rgb_match:
        r, g, b = rgb_match.groups()
        return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

    # Handle rgba() colors (ignore alpha for now)
    rgba_match = re.match(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*[\d.]+\)", css_value)
    if rgba_match:
        r, g, b = rgba_match.groups()
        return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

    # Return as-is for named colors
    return css_value


def _css_to_rich_text(css_styles: list, text: str) -> Text:
    """Convert CSS styles to Rich Text object with full-width background.

    Args:
        css_styles: List of (property, value) tuples from pandas styler
        text: The text content to wrap

    Returns:
        Rich Text object with styling applied
    """
    text_obj = Text(str(text))

    if not css_styles:
        return text_obj

    # Apply styles to the Text object
    for prop, value in css_styles:
        if prop == "background-color":
            color = _parse_css_color(value)
            text_obj.stylize(f"on {color}")
        elif prop == "color":
            color = _parse_css_color(value)
            text_obj.stylize(color)
        elif prop == "font-weight" and value == "bold":
            text_obj.stylize("bold")
        elif prop == "font-style" and value == "italic":
            text_obj.stylize("italic")

    return text_obj


def _extract_styler_styles(styler) -> dict:
    """Extract CSS styles from pandas Styler object.

    Args:
        styler: pandas Styler object

    Returns:
        Dictionary mapping (row, col) to CSS styles
    """
    # Force computation of styles
    styler._compute()

    # Extract the context dictionary
    return dict(styler.ctx)


def _has_background_styles(styles: dict) -> bool:
    """Check if any styles contain background colors.

    Args:
        styles: Dictionary of styles from _extract_styler_styles

    Returns:
        True if any background-color styles are found
    """
    for style_list in styles.values():
        for prop, value in style_list:
            if prop == "background-color" and value.strip().lower() not in [
                "",
                "transparent",
                "inherit",
                "initial",
            ]:
                return True
    return False


def _optimize_table_for_backgrounds(
    has_backgrounds: bool, minimize_gaps: bool = False
) -> dict:
    """Get optimized table settings for background display.

    Args:
        has_backgrounds: Whether the table has background colors
        minimize_gaps: Force minimal gaps even without backgrounds

    Returns:
        Dictionary of table settings
    """
    if has_backgrounds or minimize_gaps:
        return {
            "box": box.MINIMAL,  # Minimal borders to reduce gaps
            "padding": (0, 0),  # Minimal padding
            "collapse_padding": True,  # Merge adjacent cell padding
            "show_edge": True,  # Keep outer border for structure
            "pad_edge": False,  # No padding around table edges
            "expand": True,  # Allow table to expand to fill width
        }
    else:
        return {
            "box": box.ROUNDED,  # Default nice rounded borders
            "padding": (0, 1),  # Standard padding
            "collapse_padding": False,
            "show_edge": True,
            "pad_edge": True,
            "expand": False,  # Don't expand by default
        }


def _format_index_value(value) -> str:
    """Format index value for display.

    Args:
        value: Index value to format

    Returns:
        Formatted string representation
    """
    if pd.isna(value):
        return ""
    return str(value)


def _format_multiindex_value(values) -> str:
    """Format MultiIndex tuple for display.

    Args:
        values: Tuple of index values

    Returns:
        Formatted string with separator
    """
    formatted = [_format_index_value(v) for v in values]
    return " | ".join(formatted)


def _get_index_header_name(index) -> str:
    """Get appropriate header name for index column.

    Args:
        index: pandas Index object

    Returns:
        Header name string
    """
    if hasattr(index, "names") and index.names:
        # MultiIndex or named index
        if isinstance(index, MultiIndex):
            names = [name or f"Level_{i}" for i, name in enumerate(index.names)]
            return " | ".join(names)
        else:
            return index.names[0] or "Index"
    else:
        return "Index"


def _extract_index_styles(styles: dict, is_series: bool = False) -> dict:
    """Extract styles that apply to index from pandas styler.

    Args:
        styles: Extracted styles dictionary
        is_series: Whether this is for a Series (different indexing)

    Returns:
        Dictionary mapping index position to styles
    """
    index_styles = {}

    if is_series:
        # For Series, index styles might be in column -1 or similar
        # This is complex and pandas doesn't always style indices
        pass
    else:
        # For DataFrames, index styles are rare but possible
        # This would require pandas styler that explicitly styles index
        pass

    return index_styles


def _save_index(index: Union[MultiIndex, Index], path: Path, name: str):
    """Save the index to a feather file.

    Not a public function.  Internal use only.

    Args:
        index (Union[MultiIndex, Index]): The index to be saved.
        path (Path): The path to save the index.
    """
    level_names = index.names
    if level_names is None:
        level_names = [None] * index.nlevels

    with open(path / f"{name}_index.json", "w", encoding="utf-8") as f:
        json.dump(level_names, f)

    index.to_frame(index=False).rename(columns=str).to_feather(
        path / f"{name}_index.feather"
    )


def _load_index(path: Path, name: str) -> Index:
    """Load the index from a feather file.

    Not a public function.  Internal use only.

    Args:
        path (Path): The path to load the index from.

    Returns:
        Index: The loaded index.
    """
    with open(path / f"{name}_index.json", "r", encoding="utf-8") as f:
        level_names = json.load(f)

    index_df = pd.read_feather(path / f"{name}_index.feather").set_axis(
        level_names, axis=1
    )
    index = MultiIndex.from_frame(index_df, names=level_names)
    if index.nlevels == 1:
        index = index.get_level_values(0)
    return index


def _save_values(df: PandasObject, path: Path):
    """Save the values of the DataFrame or Series to a feather file.

    Not a public function.  Internal use only.

    Args:
        df (PandasObject): The DataFrame or Series to be saved.
        path (Path): The path to save the values.
    """
    try:
        pd.DataFrame(df.values).rename(columns=str).to_feather(path / "values.feather")
    except ArrowInvalid as e:
        raise ValueError(
            "The DataFrame or Series contains an unsupported data type."
        ) from e


def _load_values(path: Path) -> pd.DataFrame:
    """Load the values of the DataFrame or Series from a feather file.

    Not a public function.  Internal use only.

    Args:
        path (Path): The path to load the values from.

    Returns:
        pd.DataFrame: The loaded values.
    """
    return pd.read_feather(path / "values.feather")


def _save_cache(df: PandasObject, path: Union[str, Path], overwrite: bool = False):
    """Save the DataFrame or Series to a feather file.

    Args:
        df (PandasObject): The DataFrame or Series to be saved.
        path (Union[str, Path]): The path to save the feather file.
        overwrite (bool): A flag indicating whether to overwrite the existing file,
          defaults to False.
    """
    path = Path(path)
    if path.exists():
        if overwrite:
            shutil.rmtree(path)
        elif any(path.iterdir()):
            raise FileExistsError("The path already exists and is not empty.")
    if df.empty:
        raise ValueError("The DataFrame or Series is empty.")

    path.mkdir(parents=True, exist_ok=True)

    try:
        if isinstance(df, DataFrame):
            _save_index(df.index, path, "index")
            _save_index(df.columns, path, "columns")
            _save_values(df, path)
        else:
            _save_index(df.index, path, "index")
            _save_values(df, path)
            with open(path / "series.json", "w", encoding="utf-8") as f:
                json.dump(df.name, f)
    except Exception as e:
        shutil.rmtree(path)
        raise e


def load_cache(path: Union[str, Path]) -> PandasObject:
    """Load the DataFrame or Series from a directory of files.

    Args:
        path (Union[str, Path]): The path to load the cached data from.

    Returns:
        PandasObject: The loaded DataFrame or Series.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError("The path does not exist.")

    if (path / "columns_index.feather").exists():
        index = _load_index(path, "index")
        columns = _load_index(path, "columns")
        values = _load_values(path)
        values.index = index
        values.columns = columns
    else:
        index = _load_index(path, "index")
        values = _load_values(path).squeeze()
        with open(path / "series.json", "r", encoding="utf-8") as f:
            name = json.load(f)
            if isinstance(name, list):
                name = tuple(name)
        values.name = name
        values.index = index

    return values


def cache_and_load(obj, path, overwrite=False):
    """Cache and load a Pandas DataFrame or Series.

    Args:
        obj (PandasObject): The DataFrame or Series to be cached and loaded.
        path (Path): The path to save and load the cache.
        overwrite (bool): A flag indicating whether to overwrite the existing cache,
          defaults to False.

    Returns:
        PandasObject: The loaded DataFrame or Series.
    """
    _save_cache(obj, path, overwrite=overwrite)
    return load_cache(path)


class UtilsAccessor:
    """Accessor for utility functions."""

    def __init__(self, pandas_obj: PandasObject):
        """Initialize the UtilsAccessor.

        Args:
            pandas_obj (PandasObject): The pandas DataFrame or Series object to be
              accessed.
        """
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj: PandasObject):
        """Validate the input object.

        Args:
            obj (PandasObject): The object to be validated.

        Raises:
            AttributeError: .
        """
        if not isinstance(obj, (DataFrame, Series)):
            raise AttributeError("The object must be a pandas DataFrame or Series.")

    def to_cache(self, *args, **kwargs):
        """Save the DataFrame or Series to a directory.

        Args:
            path (Union[str, Path]): The path to save the directory of files.
            overwrite (bool): A flag indicating whether to overwrite the existing
              directory, defaults to False.
        """
        _save_cache(self._obj, *args, **kwargs)

    def to_rich(
        self,
        styler=None,
        console=None,
        minimize_gaps=False,
        show_index=True,
        index_style="dim",
        index_header_style="bold dim",
        index_justify="left",
        index_width=None,
        **table_kwargs,
    ):
        """Create a Rich table from pandas DataFrame or Series with optional styling.

        Args:
            styler: pandas Styler object with applied styles. If None, uses basic formatting.
            console: Rich Console object to use. If None, creates a new one.
            minimize_gaps: Force minimal padding/borders for better background display.
            show_index: Whether to show the index as a separate column.
            index_style: Style string for index values (e.g., "dim", "bold blue").
            index_header_style: Style string for index column header.
            index_justify: Text justification for index column ("left", "center", "right").
            index_width: Fixed width for index column (None for auto-sizing).
            **table_kwargs: Additional arguments passed to Rich Table constructor.

        Returns:
            Rich Table object that can be printed or displayed.

        Examples:
            # Basic usage with index
            df.pirr.to_rich()

            # Hide index
            df.pirr.to_rich(show_index=False)

            # Custom index styling
            df.pirr.to_rich(index_style="bold blue", index_justify="right")

            # With pandas styling (auto-optimizes for backgrounds)
            styled = df.style.background_gradient()
            df.pirr.to_rich(styler=styled)

            # Force minimal gaps
            df.pirr.to_rich(minimize_gaps=True)

            # With custom table options
            df.pirr.to_rich(title="My Data", border_style="blue")
        """
        if console is None:
            console = Console()

        # Extract styles if styler is provided
        styles = {}
        if styler is not None:
            styles = _extract_styler_styles(styler)

        # Auto-detect backgrounds and optimize table settings
        has_backgrounds = _has_background_styles(styles)
        optimized_settings = _optimize_table_for_backgrounds(
            has_backgrounds, minimize_gaps
        )

        # Merge optimized settings with user-provided kwargs (user kwargs take priority)
        final_table_kwargs = {**optimized_settings, **table_kwargs}

        # Create Rich table with optimized settings
        table = Table(**final_table_kwargs)

        if isinstance(self._obj, DataFrame):
            # Add index column if requested
            if show_index:
                index_header = _get_index_header_name(self._obj.index)
                table.add_column(
                    index_header,
                    style=index_style,
                    header_style=index_header_style,
                    justify=index_justify,
                    width=index_width,
                )

            # Add data columns
            for col in self._obj.columns:
                # Enable expansion for data columns when backgrounds are present
                if has_backgrounds:
                    table.add_column(str(col), min_width=8)
                else:
                    table.add_column(str(col))

            # Add rows with styling
            for i, (idx, row) in enumerate(self._obj.iterrows()):
                styled_row = []

                # Add index value if showing index
                if show_index:
                    if isinstance(self._obj.index, MultiIndex):
                        index_value = _format_multiindex_value(idx)
                    else:
                        index_value = _format_index_value(idx)
                    styled_row.append(index_value)

                # Add data values with styling
                for j, (col, value) in enumerate(row.items()):
                    cell_styles = styles.get((i, j), [])
                    styled_text = _css_to_rich_text(cell_styles, value)
                    styled_row.append(styled_text)

                table.add_row(*styled_row)

        elif isinstance(self._obj, Series):
            # For Series, always show index (it's the main identifier)
            if show_index:
                index_header = _get_index_header_name(self._obj.index)
                table.add_column(
                    index_header,
                    style=index_style,
                    header_style=index_header_style,
                    justify=index_justify,
                    width=index_width,
                )

            # Add value column
            series_name = self._obj.name if self._obj.name is not None else "Value"
            if has_backgrounds:
                table.add_column(str(series_name), min_width=8)
            else:
                table.add_column(str(series_name))

            for i, (idx, value) in enumerate(self._obj.items()):
                styled_row = []

                # Add index value if showing index
                if show_index:
                    if isinstance(self._obj.index, MultiIndex):
                        index_value = _format_multiindex_value(idx)
                    else:
                        index_value = _format_index_value(idx)
                    styled_row.append(index_value)

                # Series styler uses (row, 0) for indexing
                cell_styles = styles.get((i, 0), [])
                styled_value = _css_to_rich_text(cell_styles, value)
                styled_row.append(styled_value)

                table.add_row(*styled_row)

        return table


reg_df("pirr")(UtilsAccessor)
reg_ser("pirr")(UtilsAccessor)


def create_class(level: int):
    class I_N:
        def __init__(self, pandas_obj):
            self._validate(pandas_obj)
            self._obj = pandas_obj
            self._grp = self._obj.groupby(level=level)

        @staticmethod
        def _validate(obj):
            if not isinstance(obj, (pd.DataFrame, pd.Series)):
                raise AttributeError("The object must be a pandas DataFrame or Series.")
            if level + 1 > obj.index.nlevels:
                raise AttributeError(
                    f"The object must have at least {level + 1} index level(s)."
                )

        def __getattr__(self, name):
            return getattr(self._grp, name)

        def __dir__(self):
            return dir(self._grp)

    I_N.__name__ = f"I{level}"
    return I_N


for i in range(0, 2):
    cls = create_class(i)
    reg_df(cls.__name__.lower())(cls)
    reg_ser(cls.__name__.lower())(cls)
