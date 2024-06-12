import pandas as pd
import json
from pandas import Index, MultiIndex, DataFrame, Series
from typing import Union
from pathlib import Path
from pandas.api.extensions import register_dataframe_accessor as reg_df
from pandas.api.extensions import register_series_accessor as reg_ser


PandasObject = Union[DataFrame, Series]


def _save_index(index: Union[MultiIndex, Index], path: Path, name: str):
    """
    Save the index to a feather file.

    Not a public function.  Internal use only.

    Args:
        index (Union[MultiIndex, Index]): The index to be saved.
        path (Path): The path to save the index.
    """
    level_names = index.names
    if level_names is None:
        level_names = [None] * index.nlevels

    with open(path / f"{name}_index.json", "w") as f:
        json.dump(level_names, f)

    index.to_frame(index=False).rename(columns=str).to_feather(path / f"{name}_index.feather")


def _load_index(path: Path, name: str) -> Index:
    """
    Load the index from a feather file.

    Not a public function.  Internal use only.

    Args:
        path (Path): The path to load the index from.

    Returns:
        Index: The loaded index.
    """
    with open(path / f"{name}_index.json", "r") as f:
        level_names = json.load(f)

    index_df = pd.read_feather(path / f"{name}_index.feather").set_axis(level_names, axis=1)
    index = MultiIndex.from_frame(index_df, names=level_names)
    if index.nlevels == 1:
        index = index.get_level_values(0)
    return index

def _save_values(df: PandasObject, path: Path):
    """
    Save the values of the DataFrame or Series to a feather file.

    Not a public function.  Internal use only.

    Args:
        df (PandasObject): The DataFrame or Series to be saved.
        path (Path): The path to save the values.
    """            
    pd.DataFrame(df.values).rename(columns=str).to_feather(path / f"values.feather")

def _load_values(path: Path) -> pd.DataFrame:
    """
    Load the values of the DataFrame or Series from a feather file.

    Not a public function.  Internal use only.

    Args:
        path (Path): The path to load the values from.

    Returns:
        pd.DataFrame: The loaded values.
    """
    return pd.read_feather(path / f"values.feather")

def _save_cache(df: PandasObject, path: Union[str, Path]):
    """
    Save the DataFrame or Series to a feather file.

    Args:
        df (PandasObject): The DataFrame or Series to be saved.
        path (Union[str, Path]): The path to save the feather file.
    """
    path = Path(path)
    if path.exists():
        raise FileExistsError("The path already exists.")
    path.mkdir(parents=True)

    if isinstance(df, DataFrame):
        _save_index(df.index, path, "index")
        _save_index(df.columns, path, "columns")
        _save_values(df, path)
    else:
        _save_index(df.index, path, "index")
        _save_values(df, path)
        with open(path / "series.json", "w") as f:
            json.dump(df.name, f)

def load_cache(path: Union[str, Path]) -> PandasObject:
    """
    Load the DataFrame or Series from a directory of files.

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
        with open(path / "series.json", "r") as f:
            name = json.load(f)
            if isinstance(name, list):
                name = tuple(name)
        values.name = name
        values.index = index

    return values


class UtilsAccessor:
    """
    Accessor for utility functions.
    """

    def __init__(self, pandas_obj: PandasObject):
        """
        Initialize the UtilsAccessor.

        Args:
            pandas_obj (PandasObject): The pandas DataFrame or Series object to be accessed.
        """
        self._validate(pandas_obj)
        self._obj = pandas_obj
    
    @staticmethod
    def _validate(obj: PandasObject):
        """
        Validate the input object.

        Args:
            obj (PandasObject): The object to be validated.
        
        Raises:
            AttributeError: .
        """
        if not isinstance(obj, (DataFrame, Series)):
            raise AttributeError("The object must be a pandas DataFrame or Series.")
        
    def to_cache(self, path: Union[str, Path]):
        """
        Save the DataFrame or Series to a directory.

        Args:
            path (Union[str, Path]): The path to save the directory of files.
        """
        _save_cache(self._obj, path)

reg_df('pirr')(UtilsAccessor)
reg_ser('pirr')(UtilsAccessor)
