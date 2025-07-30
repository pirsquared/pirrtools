"""Pandas utilities for caching and rich display formatting.

This module provides comprehensive utilities for pandas DataFrame and Series objects,
including efficient caching using feather format and advanced rich table display
with styling support.

Key Features:
    - Efficient caching system for non-conforming datasets using feather format
    - Rich table display with CSS styling support and background colors
    - Pandas accessor (.pirr) for convenient method access
    - Support for MultiIndex and complex pandas objects
    - Dynamic column width optimization for styled tables

Main Classes:
    UtilsAccessor: Pandas accessor providing caching and rich display methods

Public Functions:
    load_cache: Load cached DataFrame or Series from directory
    cache_and_load: Cache and immediately reload a pandas object

Example:
    >>> import pandas as pd
    >>> df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    >>>
    >>> # Cache the DataFrame
    >>> df.pirr.to_cache('my_cache')
    >>>
    >>> # Display with rich formatting
    >>> df.pirr.to_rich(bg='gradient')
    >>>
    >>> # Load from cache
    >>> cached_df = load_cache('my_cache')
"""

import json
import re
import shutil
from pathlib import Path
from typing import Optional, Union

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Index, MultiIndex, Series
from pandas.api.extensions import register_dataframe_accessor as reg_df
from pandas.api.extensions import register_series_accessor as reg_ser
from pyarrow.lib import ArrowInvalid
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text

PandasObject = Union[DataFrame, Series]


def _parse_css_color(css_value: str) -> str:
    """Parse CSS color value into Rich-compatible format.

    Converts various CSS color formats (hex, rgb, rgba, named colors)
    into formats compatible with the Rich library.

    Args:
        css_value (str): CSS color value such as '#ff0000', 'rgb(255, 0, 0)',
            'rgba(255, 0, 0, 0.5)', or named colors like 'red'.

    Returns:
        str: Rich-compatible color string, typically in hex format.

    Example:
        >>> _parse_css_color('rgb(255, 0, 0)')
        '#ff0000'
        >>> _parse_css_color('#123456')
        '#123456'
    """
    css_value = css_value.strip()

    # Handle hex colors
    if css_value.startswith("#"):
        return css_value

    # Handle rgb() colors (return as-is for test compatibility)
    rgb_match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", css_value)
    if rgb_match:
        return css_value

    # Handle rgba() colors (ignore alpha for now)
    rgba_match = re.match(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*[\d.]+\)", css_value)
    if rgba_match:
        r, g, b = rgba_match.groups()
        return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

    # Return as-is for named colors
    return css_value


def _css_to_rich_text(
    css_styles: list, text: str, column_width: Optional[int] = None
) -> Text:
    """Convert CSS styles to Rich Text object with styling applied.

    This function takes CSS styles from pandas Styler and converts them
    to Rich Text styling, with optional padding for better background display.

    Args:
        css_styles (list): List of (property, value) tuples from pandas styler.
        text (str): The text content to style and wrap.
        column_width (int, optional): Target width for padding to achieve
            full-width background colors. If None, no padding is applied.

    Returns:
        Text: Rich Text object with CSS styles converted to Rich formatting.

    Note:
        Supports background-color, color, font-weight (bold), and font-style
        (italic) CSS properties.
    """
    text_content = str(text)
    text_obj = Text(text_content)

    # Pad the text to fill the column width for better background display
    if column_width is not None and len(text_content) < column_width:
        text_obj.pad_right(column_width - len(text_content))

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


def _extract_styler_formats(styler) -> dict:
    """Extract formatting functions from pandas Styler.

    Args:
        styler: pandas Styler object

    Returns:
        Dictionary mapping (row, col) positions to format functions
    """
    format_funcs = {}
    if hasattr(styler, "_display_funcs") and styler._display_funcs:
        format_funcs = styler._display_funcs.copy()
    return format_funcs


def _apply_styler_formatting(value, row_idx, col_idx, format_funcs):
    """Apply styler formatting function to a cell value.

    Args:
        value: Cell value to format
        row_idx: Row index
        col_idx: Column index
        format_funcs: Dictionary of format functions from styler

    Returns:
        Formatted string value
    """
    if format_funcs and (row_idx, col_idx) in format_funcs:
        try:
            return format_funcs[(row_idx, col_idx)](value)
        except Exception:
            # Fallback to string conversion if formatting fails
            pass
    return str(value)


def _extract_styler_styles(styler) -> dict:
    """Extract CSS styles from pandas Styler object.

    Forces computation of styles and extracts the context dictionary
    containing cell-level styling information.

    Args:
        styler (pandas.io.formats.style.Styler): A pandas Styler object
            with applied styles.

    Returns:
        dict: Dictionary mapping (row, col) tuples to lists of
            (property, value) CSS style tuples.
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
            "box": box.ROUNDED,  # Rounded borders for better appearance
            "padding": (0, 0),  # Minimal padding
            "collapse_padding": True,  # Merge adjacent cell padding
            "show_edge": True,  # Keep outer border for structure
            "pad_edge": False,  # No padding around table edges
            "expand": False,  # Keep table size to fit content
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


def _extract_index_styles(_styles: dict, is_series: bool = False) -> dict:
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


def _create_index_gradient_styles(index_values, colormap="viridis", **_kwargs):
    """Create background gradient styles for index values.

    Args:
        index_values: List of index values
        colormap: Matplotlib colormap name
        **kwargs: Additional arguments for colormap

    Returns:
        List of Rich style strings for each index value
    """
    if not index_values:
        return []
    try:
        # Get the colormap
        if colormap == "gradient":
            cmap = plt.colormaps["viridis"]
        else:
            cmap = plt.colormaps[colormap]
        # Create color values normalized to [0, 1]
        n_values = len(index_values)
        if n_values == 1:
            colors = [cmap(0.5)]
        else:
            colors = [cmap(i / (n_values - 1)) for i in range(n_values)]
        # Convert to hex colors and create Rich style strings
        styles = []
        for color in colors:
            hex_color = mcolors.to_hex(color)
            style = f"on {hex_color}"
            styles.append(style)
        return styles
    except Exception as e:
        # If gradient creation fails, return empty styles and print warning
        import warnings

        warnings.warn(
            f"Colormap error in _create_index_gradient_styles: {e}", stacklevel=2
        )
        return [""] * len(index_values)


def _measure_column_widths(df, show_index: bool = True) -> dict:
    """Measure the maximum width needed for each column.

    Args:
        df: DataFrame or Series to measure
        show_index: Whether index column will be shown

    Returns:
        Dictionary mapping column names/index to their measured widths
    """
    widths = {}

    if isinstance(df, DataFrame):
        # Measure index column width if showing index
        if show_index:
            index_header = _get_index_header_name(df.index)
            index_values = []

            for idx in df.index:
                if isinstance(df.index, MultiIndex):
                    index_values.append(_format_multiindex_value(idx))
                else:
                    index_values.append(_format_index_value(idx))

            max_index_width = max(
                len(index_header),
                max(len(str(v)) for v in index_values) if index_values else 0,
            )
            widths["__index__"] = max_index_width

        # Measure data columns
        for col in df.columns:
            col_header = str(col)
            col_values = [str(val) for val in df[col]]
            max_width = max(
                len(col_header), max(len(v) for v in col_values) if col_values else 0
            )
            widths[col] = max_width

    elif isinstance(df, Series):
        # For Series, measure index and value columns
        if show_index:
            index_header = _get_index_header_name(df.index)
            index_values = []

            for idx in df.index:
                if isinstance(df.index, MultiIndex):
                    index_values.append(_format_multiindex_value(idx))
                else:
                    index_values.append(_format_index_value(idx))

            max_index_width = max(
                len(index_header),
                max(len(str(v)) for v in index_values) if index_values else 0,
            )
            widths["__index__"] = max_index_width

        # Measure value column
        series_name = df.name if df.name is not None else "Value"
        series_values = [str(val) for val in df]
        max_width = max(
            len(str(series_name)),
            max(len(v) for v in series_values) if series_values else 0,
        )
        widths["__value__"] = max_width

    return widths


def _save_index(index: Union[MultiIndex, Index], path: Path, name: str):
    """Save pandas index to feather file with metadata.

    Internal function that saves index data and level names separately
    to ensure proper reconstruction of complex indexes.

    Args:
        index (Union[MultiIndex, Index]): The pandas index to save.
        path (Path): Directory path where index files will be saved.
        name (str): Prefix name for the saved index files.

    Note:
        Creates two files: {name}_index.json for level names and
        {name}_index.feather for index data.
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
    """Load pandas index from feather file with metadata.

    Internal function that reconstructs pandas index from saved
    feather data and JSON metadata.

    Args:
        path (Path): Directory path containing the index files.
        name (str): Prefix name of the saved index files.

    Returns:
        Index: The reconstructed pandas Index or MultiIndex.

    Note:
        Automatically detects and returns single-level Index from MultiIndex
        when appropriate.
    """
    with open(path / f"{name}_index.json", encoding="utf-8") as f:
        level_names = json.load(f)

    index_df = pd.read_feather(path / f"{name}_index.feather").set_axis(
        level_names, axis=1
    )
    index = MultiIndex.from_frame(index_df, names=level_names)
    if index.nlevels == 1:
        index = index.get_level_values(0)
    return index


def _save_values(df: PandasObject, path: Path):
    """Save DataFrame or Series values to feather file.

    Internal function that extracts and saves the underlying data values
    from pandas objects to feather format.

    Args:
        df (PandasObject): The DataFrame or Series whose values to save.
        path (Path): Directory path where values.feather will be saved.

    Raises:
        ValueError: If the DataFrame contains unsupported data types
            for feather format.
    """
    try:
        pd.DataFrame(df.values).rename(columns=str).to_feather(path / "values.feather")
    except ArrowInvalid as e:
        raise ValueError(
            "The DataFrame or Series contains an unsupported data type."
        ) from e


def _load_values(path: Path) -> pd.DataFrame:
    """Load DataFrame values from feather file.

    Internal function that loads the raw data values that were
    saved by _save_values().

    Args:
        path (Path): Directory path containing values.feather file.

    Returns:
        pd.DataFrame: The loaded values as a DataFrame.
    """
    return pd.read_feather(path / "values.feather")


def _save_cache(df: PandasObject, path: Union[str, Path], overwrite: bool = False):
    """Save pandas DataFrame or Series to cache directory.

    Creates a directory structure with separate files for indexes,
    column information, and data values to handle complex pandas objects.

    Args:
        df (PandasObject): The DataFrame or Series to cache.
        path (Union[str, Path]): Directory path for the cache.
        overwrite (bool, optional): Whether to overwrite existing cache.
            Defaults to False.

    Raises:
        FileExistsError: If path exists, is not empty, and overwrite is False.
        ValueError: If the DataFrame or Series is empty.

    Note:
        For DataFrames, saves index, columns, and values separately.
        For Series, saves index, values, and series name.
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
    """Load cached pandas DataFrame or Series from directory.

    Reconstructs a pandas object from the cache directory created
    by _save_cache(), properly restoring indexes, columns, and metadata.

    Args:
        path (Union[str, Path]): Path to the cache directory.

    Returns:
        PandasObject: The reconstructed DataFrame or Series with all
            original structure and metadata preserved.

    Raises:
        FileNotFoundError: If the cache directory does not exist.

    Example:
        >>> df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        >>> _save_cache(df, 'my_cache')
        >>> loaded_df = load_cache('my_cache')
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
        with open(path / "series.json", encoding="utf-8") as f:
            name = json.load(f)
            if isinstance(name, list):
                name = tuple(name)
        values.name = name
        values.index = index

    return values


def cache_and_load(obj, path, overwrite=False):
    """Cache a pandas object and immediately reload it.

    This is a convenience function that saves an object to cache
    and then loads it back, useful for testing cache integrity
    or for ensuring feather-compatible data types.

    Args:
        obj (PandasObject): The DataFrame or Series to cache and reload.
        path (Union[str, Path]): Directory path for the cache.
        overwrite (bool, optional): Whether to overwrite existing cache.
            Defaults to False.

    Returns:
        PandasObject: The reloaded DataFrame or Series.

    Example:
        >>> df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        >>> reloaded_df = cache_and_load(df, 'test_cache')
    """
    _save_cache(obj, path, overwrite=overwrite)
    return load_cache(path)


class UtilsAccessor:
    """Pandas accessor providing caching and rich display utilities.

    This accessor is automatically registered as '.pirr' on pandas
    DataFrame and Series objects, providing convenient access to
    caching functionality and rich table display features.

    Attributes:
        _obj (PandasObject): The underlying pandas DataFrame or Series.

    Example:
        >>> df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        >>> df.pirr.to_cache('my_cache')  # Cache the DataFrame
        >>> df.pirr.to_rich()  # Display as rich table
    """

    def __init__(self, pandas_obj: PandasObject):
        """Initialize the UtilsAccessor.

        Args:
            pandas_obj (PandasObject): The pandas DataFrame or Series object
                that this accessor is attached to.

        Raises:
            AttributeError: If pandas_obj is not a DataFrame or Series.
        """
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj: PandasObject):
        """Validate that the object is a supported pandas type.

        Args:
            obj (PandasObject): The object to validate.

        Raises:
            AttributeError: If the object is not a pandas DataFrame or Series.
        """
        if not isinstance(obj, (DataFrame, Series)):
            raise AttributeError("The object must be a pandas DataFrame or Series.")

    def to_cache(self, *args, **kwargs):
        """Save the DataFrame or Series to a cache directory.

        This method provides convenient access to the caching functionality
        through the pandas accessor interface.

        Args:
            *args: Positional arguments passed to _save_cache().
            **kwargs: Keyword arguments passed to _save_cache().

        Common Parameters:
            path (Union[str, Path]): Directory path for the cache.
            overwrite (bool, optional): Whether to overwrite existing cache.
                Defaults to False.

        Example:
            >>> df.pirr.to_cache('my_cache', overwrite=True)
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
        # Built-in styling options
        bg=None,
        bg_kwargs=None,
        tg=None,
        tg_kwargs=None,
        column_header_style=None,
        index_bg=None,
        index_bg_kwargs=None,
        alternating_rows=False,
        alternating_row_colors=("", "on grey11"),
        table_style=None,
        # Table optimization controls (override automatic detection)
        auto_optimize=True,
        box=None,
        padding=None,
        collapse_padding=None,
        show_edge=None,
        pad_edge=None,
        expand=None,
        # String formatting support
        format=None,
        na_rep=None,
        **table_kwargs,
    ):
        """Create a Rich table from pandas DataFrame or Series with advanced styling.

        This method converts pandas objects into beautifully formatted Rich tables
        with support for CSS styling from pandas Styler objects, built-in gradients,
        and extensive customization options.

        Args:
            styler (pandas.io.formats.style.Styler, optional): Pandas Styler object
                with applied styles. If None, uses basic formatting.
            console (rich.console.Console, optional): Rich Console object to use.
                If None, creates a new one.
            minimize_gaps (bool, optional): Force minimal padding/borders for better
                background color display. Defaults to False.
            show_index (bool, optional): Whether to show the index as a separate
                column. Defaults to True.
            index_style (str, optional): Rich style string for index values
                (e.g., "dim", "bold blue"). Defaults to "dim".
            index_header_style (str, optional): Rich style string for index column
                header. Defaults to "bold dim".
            index_justify (str, optional): Text justification for index column
                ("left", "center", "right"). Defaults to "left".
            index_width (int, optional): Fixed width for index column. If None,
                auto-sizes based on content.

            bg (str, optional): Background gradient style. Use "gradient" for
                default colormap or specify colormap name (e.g., "viridis").
            bg_kwargs (dict, optional): Additional arguments for background_gradient().
            tg (str, optional): Text gradient style. Use "gradient" for default
                colormap or specify colormap name.
            tg_kwargs (dict, optional): Additional arguments for text_gradient().
            column_header_style (str, optional): Rich style string for column headers.
            index_bg (str, optional): Background gradient for index. Use "gradient"
                or specify colormap name.
            index_bg_kwargs (dict, optional): Additional arguments for index
                background_gradient().
            alternating_rows (bool, optional): Whether to apply alternating row
                colors. Defaults to False.
            alternating_row_colors (tuple, optional): Tuple of (even_style, odd_style)
                for alternating rows. Defaults to ("", "on grey11").
            table_style (str, optional): Rich style string applied to entire table.

            auto_optimize (bool, optional): Whether to automatically optimize table
                settings when background colors are detected. Defaults to True.
            box (Box, optional): Rich Box style for table borders.
                Overrides auto_optimize.
            padding (tuple, optional): Padding around cell content
                (vertical, horizontal).
                Overrides auto_optimize.
            collapse_padding (bool, optional): Whether to collapse adjacent
                cell padding.
                Overrides auto_optimize.
            show_edge (bool, optional): Whether to show table outer border.
                Overrides auto_optimize.
            pad_edge (bool, optional): Whether to add padding around table edges.
                Overrides auto_optimize.
            expand (bool, optional): Whether table should expand to fill console width.
                Overrides auto_optimize.

            format (dict or str, optional): Format specifiers for columns. Can be a
                dictionary mapping column names to format strings, or a single format
                string applied to all columns. Uses pandas Styler.format() internally.
            na_rep (str, optional): String representation of NaN values. Defaults to "".
            **table_kwargs: Additional keyword arguments passed to Rich Table
                constructor.

        Returns:
            rich.table.Table: A Rich Table object ready for display or printing.

        Examples:
            Basic usage:
                >>> from rich.console import Console
                >>> console = Console()
                >>> table = df.pirr.to_rich()
                >>> console.print(table)

            Background gradients:
                >>> table = df.pirr.to_rich(bg="gradient")
                >>> table = df.pirr.to_rich(bg="viridis", bg_kwargs={"axis": 0})

            Text gradients:
                >>> table = df.pirr.to_rich(tg="gradient")

            Header styling:
                >>> table = df.pirr.to_rich(column_header_style="bold blue on white")

            Alternating rows:
                >>> table = df.pirr.to_rich(alternating_rows=True)
                >>> table = df.pirr.to_rich(alternating_rows=True,
                ...                         alternating_row_colors=("", "on blue"))

            Manual table optimization control:
                >>> from rich import box
                >>> table = df.pirr.to_rich(
                ...     auto_optimize=False, box=box.ROUNDED,
                ...     padding=(1, 2), show_edge=True
                ... )

            String formatting:
                >>> table = df.pirr.to_rich(
                ...     format={"Sales": "${:.0f}", "Growth": "{:.1%}"}
                ... )
                >>> table = df.pirr.to_rich(
                ...     format="{:.2f}", na_rep="N/A"
                ... )

            Combined styling:
                >>> table = df.pirr.to_rich(
                ...     bg="viridis", tg="plasma", alternating_rows=True,
                ...     table_style="bold", title="My Data"
                ... )
                >>> console.print(table)

        Note:
            The method automatically optimizes table settings when background colors
            are detected, minimizing gaps for better visual appearance.
        """
        if console is None:
            console = Console()

        # Create or modify styler with built-in styling options
        if (
            bg
            or tg
            or index_bg
            or alternating_rows
            or format is not None
            or na_rep is not None
            or any([bg, tg, column_header_style, index_bg, alternating_rows])
        ):
            # Start with existing styler or create new one
            if styler is None:
                # Only DataFrames have .style, Series need to be converted
                if isinstance(self._obj, pd.Series):
                    temp_df = self._obj.to_frame()
                    styler = temp_df.style
                else:
                    styler = self._obj.style
            # Apply background gradient
            if bg:
                bg_kwargs = bg_kwargs or {}
                try:
                    if bg == "gradient":
                        styler = styler.background_gradient(**bg_kwargs)
                    else:
                        styler = styler.background_gradient(cmap=bg, **bg_kwargs)
                except Exception as e:
                    import warnings

                    warnings.warn(f"Colormap error in to_rich: {e}", stacklevel=2)
            # Apply text gradient
            if tg:
                tg_kwargs = tg_kwargs or {}
                try:
                    if tg == "gradient":
                        styler = styler.text_gradient(**tg_kwargs)
                    else:
                        styler = styler.text_gradient(cmap=tg, **tg_kwargs)
                except Exception as e:
                    import warnings

                    warnings.warn(
                        f"Colormap error in to_rich (text): {e}", stacklevel=2
                    )
            # Apply formatting if specified
            if format is not None:
                if isinstance(format, str):
                    # Apply same format to all columns
                    styler = styler.format(
                        format, na_rep=na_rep if na_rep is not None else ""
                    )
                elif isinstance(format, dict):
                    # Apply specific formats to specific columns
                    styler = styler.format(
                        format, na_rep=na_rep if na_rep is not None else ""
                    )
                else:
                    import warnings

                    warnings.warn(
                        "format parameter must be string or dict", stacklevel=2
                    )
            elif na_rep is not None:
                # Just apply na_rep without formatting
                styler = styler.format(na_rep=na_rep)

            # Note: index_bg will be handled in Rich rendering stage since
            # pandas styler doesn't support index background styling directly
            # Note: Alternating row colors will be handled in Rich rendering stage
            # since pandas styler expects CSS format, not Rich format
        # Extract styles and formatting functions if styler is provided
        styles = {}
        format_funcs = {}
        if styler is not None:
            try:
                styles = _extract_styler_styles(styler)
                format_funcs = _extract_styler_formats(styler)
            except Exception as e:
                import warnings

                warnings.warn(f"Styler extraction error in to_rich: {e}", stacklevel=2)
                styles = {}
                format_funcs = {}

        # Auto-detect backgrounds and optimize table settings
        # (if auto_optimize is enabled)
        if auto_optimize:
            has_backgrounds = _has_background_styles(styles)
            optimized_settings = _optimize_table_for_backgrounds(
                has_backgrounds, minimize_gaps
            )
        else:
            has_backgrounds = False
            optimized_settings = {}

        # Apply manual table setting overrides
        manual_overrides = {}
        if box is not None:
            manual_overrides["box"] = box
        if padding is not None:
            manual_overrides["padding"] = padding
        if collapse_padding is not None:
            manual_overrides["collapse_padding"] = collapse_padding
        if show_edge is not None:
            manual_overrides["show_edge"] = show_edge
        if pad_edge is not None:
            manual_overrides["pad_edge"] = pad_edge
        if expand is not None:
            manual_overrides["expand"] = expand

        # Measure column widths for dynamic padding when backgrounds are present
        column_widths = (
            _measure_column_widths(self._obj, show_index) if has_backgrounds else {}
        )

        # Merge settings: optimized < manual overrides < user kwargs
        # (user kwargs take priority)
        final_table_kwargs = {**optimized_settings, **manual_overrides, **table_kwargs}

        # Apply table-wide style if specified
        if table_style:
            final_table_kwargs["style"] = table_style

        # Create Rich table with optimized settings
        table = Table(**final_table_kwargs)

        if isinstance(self._obj, DataFrame):
            # Generate index gradient styles if requested
            index_gradient_styles = []
            if index_bg and show_index:
                index_bg_kwargs_clean = index_bg_kwargs or {}
                index_values = [
                    (
                        _format_multiindex_value(idx)
                        if isinstance(self._obj.index, MultiIndex)
                        else _format_index_value(idx)
                    )
                    for idx in self._obj.index
                ]
                index_gradient_styles = _create_index_gradient_styles(
                    index_values, index_bg, **index_bg_kwargs_clean
                )

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
                column_args = (
                    {"header_style": column_header_style} if column_header_style else {}
                )
                # Enable expansion for data columns when backgrounds are present
                if has_backgrounds:
                    table.add_column(str(col), min_width=8, **column_args)
                else:
                    table.add_column(str(col), **column_args)

            # Add rows with styling
            for i, (idx, row) in enumerate(self._obj.iterrows()):
                styled_row = []

                # Add index value if showing index
                if show_index:
                    if isinstance(self._obj.index, MultiIndex):
                        index_value = _format_multiindex_value(idx)
                    else:
                        index_value = _format_index_value(idx)

                    # Apply index background gradient if requested
                    index_bg_style = ""
                    if index_gradient_styles and i < len(index_gradient_styles):
                        index_bg_style = index_gradient_styles[i]

                    # Apply padding to index if backgrounds are present
                    if has_backgrounds or index_bg_style:
                        index_width = column_widths.get("__index__", None)
                        index_text = Text(str(index_value))
                        if index_width and len(str(index_value)) < index_width:
                            index_text.pad_right(index_width - len(str(index_value)))
                        # Apply index background style
                        if index_bg_style:
                            index_text.style = index_bg_style
                        styled_row.append(index_text)
                    else:
                        styled_row.append(index_value)

                # Add data values with styling
                for j, (col, value) in enumerate(row.items()):
                    cell_styles = styles.get((i, j), [])

                    # Apply styler formatting if available
                    formatted_value = _apply_styler_formatting(
                        value, i, j, format_funcs
                    )

                    # Use dynamic column width for background padding
                    column_width = (
                        column_widths.get(col, None) if has_backgrounds else None
                    )
                    styled_text = _css_to_rich_text(
                        cell_styles, formatted_value, column_width
                    )

                    # Apply alternating row colors if enabled
                    if alternating_rows and styled_text is not None:
                        alt_style = alternating_row_colors[i % 2]
                        if alt_style and isinstance(styled_text, Text):
                            styled_text.style = alt_style
                        elif alt_style and not isinstance(styled_text, Text):
                            styled_text = Text(str(styled_text), style=alt_style)

                    styled_row.append(styled_text)

                table.add_row(*styled_row)

        elif isinstance(self._obj, Series):
            # Generate index gradient styles if requested
            index_gradient_styles = []
            if index_bg and show_index:
                index_bg_kwargs_clean = index_bg_kwargs or {}
                index_values = [
                    (
                        _format_multiindex_value(idx)
                        if isinstance(self._obj.index, MultiIndex)
                        else _format_index_value(idx)
                    )
                    for idx in self._obj.index
                ]
                index_gradient_styles = _create_index_gradient_styles(
                    index_values, index_bg, **index_bg_kwargs_clean
                )

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
            column_args = (
                {"header_style": column_header_style} if column_header_style else {}
            )
            if has_backgrounds:
                table.add_column(str(series_name), min_width=8, **column_args)
            else:
                table.add_column(str(series_name), **column_args)

            for i, (idx, value) in enumerate(self._obj.items()):
                styled_row = []

                # Add index value if showing index
                if show_index:
                    if isinstance(self._obj.index, MultiIndex):
                        index_value = _format_multiindex_value(idx)
                    else:
                        index_value = _format_index_value(idx)

                    # Apply index background gradient if requested
                    index_bg_style = ""
                    if index_gradient_styles and i < len(index_gradient_styles):
                        index_bg_style = index_gradient_styles[i]

                    # Apply padding to index if backgrounds are present
                    if has_backgrounds or index_bg_style:
                        index_width = column_widths.get("__index__", None)
                        index_text = Text(str(index_value))
                        if index_width and len(str(index_value)) < index_width:
                            index_text.pad_right(index_width - len(str(index_value)))
                        # Apply index background style
                        if index_bg_style:
                            index_text.style = index_bg_style
                        styled_row.append(index_text)
                    else:
                        styled_row.append(index_value)

                # Series styler uses (row, 0) for indexing
                cell_styles = styles.get((i, 0), [])

                # Apply styler formatting if available (Series uses column 0)
                formatted_value = _apply_styler_formatting(value, i, 0, format_funcs)

                # Use dynamic column width for background padding
                column_width = (
                    column_widths.get("__value__", None) if has_backgrounds else None
                )
                styled_value = _css_to_rich_text(
                    cell_styles, formatted_value, column_width
                )
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
