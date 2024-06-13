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

PandasObject = Union[DataFrame, Series]


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


reg_df("pirr")(UtilsAccessor)
reg_ser("pirr")(UtilsAccessor)
