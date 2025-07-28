"""
This module contains test functions to be used with the pytest framework.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from pirrtools.pandas import cache_and_load, load_cache


def test_simple_dataframe(tmp_path):
    """
    Test function for caching and loading a simple DataFrame.

    Args:
        tmp_path (str): Temporary directory path.

    Returns:
        None
    """
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    loaded_df = cache_and_load(df, tmp_path / "simple_df")
    pd.testing.assert_frame_equal(df, loaded_df)


def test_simple_series(tmp_path):
    """
    Test function for caching and loading a simple Series.

    Args:
        tmp_path (str): Temporary directory path.

    Returns:
        None
    """
    series = pd.Series([1, 2, 3], name="test_series")
    loaded_series = cache_and_load(series, tmp_path / "simple_series")
    pd.testing.assert_series_equal(series, loaded_series)


def test_dataframe_with_multiindex(tmp_path):
    """
    Test function for caching and loading a DataFrame with a MultiIndex.

    Args:
        tmp_path (str): Temporary directory path.

    Returns:
        None
    """
    arrays = [["bar", "bar", "baz", "baz"], ["one", "two", "one", "two"]]
    index = pd.MultiIndex.from_arrays(arrays, names=["first", "second"])
    df = pd.DataFrame({"A": [1, 2, 3, 4], "B": [5, 6, 7, 8]}, index=index)
    loaded_df = cache_and_load(df, tmp_path / "multiindex_df")
    pd.testing.assert_frame_equal(df, loaded_df)


def test_series_with_multiindex(tmp_path):
    """
    Test function for caching and loading a Series with a MultiIndex.

    Args:
        tmp_path (str): Temporary directory path.

    Returns:
        None
    """
    arrays = [["bar", "bar", "baz", "baz"], ["one", "two", "one", "two"]]
    index = pd.MultiIndex.from_arrays(arrays, names=["first", "second"])
    series = pd.Series([1, 2, 3, 4], index=index, name="multiindex_series")
    loaded_series = cache_and_load(series, tmp_path / "multiindex_series")
    pd.testing.assert_series_equal(series, loaded_series)


def test_dataframe_with_various_dtypes(tmp_path):
    """
    Test function for caching and loading a DataFrame with various data types.

    Args:
        tmp_path (str): Temporary directory path.

    Returns:
        None
    """
    df = pd.DataFrame(
        {
            "ints": [1, 2, 3],
            "floats": [1.1, 2.2, 3.3],
            "strings": ["a", "b", "c"],
            "bools": [True, False, True],
            "dates": pd.date_range("2021-01-01", periods=3),
        }
    )
    loaded_df = cache_and_load(df, tmp_path / "various_dtypes_df")
    pd.testing.assert_frame_equal(df, loaded_df)


def test_series_with_various_dtypes(tmp_path):
    """
    Test function for caching and loading a Series with various data types.

    Args:
        tmp_path (str): Temporary directory path.

    Returns:
        None
    """
    series = pd.Series(
        [1, 2.2, "three", True, pd.Timestamp("2021-01-01")],
        name="various_dtypes_series",
    )
    with pytest.raises(
        ValueError, match="The DataFrame or Series contains an unsupported data type."
    ):
        cache_and_load(series, tmp_path / "various_dtypes_series")


def test_empty_dataframe(tmp_path):
    """
    Test function for caching and loading an empty DataFrame.

    Args:
        tmp_path (str): Temporary directory path.

    Returns:
        None
    """
    df = pd.DataFrame()
    with pytest.raises(ValueError, match="The DataFrame or Series is empty."):
        cache_and_load(df, tmp_path / "empty_df")


def test_empty_series(tmp_path):
    """
    Test function for caching and loading an empty Series.

    Args:
        tmp_path (str): Temporary directory path.

    Returns:
        None
    """
    series = pd.Series([], dtype=float)
    with pytest.raises(ValueError, match="The DataFrame or Series is empty."):
        cache_and_load(series, tmp_path / "empty_series")


def test_dataframe_with_nan_values(tmp_path):
    """
    Test function for caching and loading a DataFrame with NaN values.

    Args:
        tmp_path (str): Temporary directory path.

    Returns:
        None
    """
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [4, 5, np.nan]})
    loaded_df = cache_and_load(df, tmp_path / "nan_values_df")
    pd.testing.assert_frame_equal(df, loaded_df)


def test_series_with_nan_values(tmp_path):
    """
    Test function for caching and loading a Series with NaN values.

    Args:
        tmp_path (str): Temporary directory path.

    Returns:
        None
    """
    series = pd.Series([1, np.nan, 3], name="nan_values_series")
    loaded_series = cache_and_load(series, tmp_path / "nan_values_series")
    pd.testing.assert_series_equal(series, loaded_series)


def test_save_cache_existing_path(tmp_path):
    """
    Test function for saving cache to an existing path.

    Args:
        tmp_path (str): Temporary directory path.

    Returns:
        None
    """
    # Create a sample DataFrame
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    # Create a unique subdirectory in tmp_path
    cache_path = tmp_path / "cache"
    cache_path.mkdir(parents=True, exist_ok=True)

    # Simulate the existing path by creating a file in the cache_path
    (cache_path / "dummy_file.txt").touch()

    # Check that saving to an existing path raises a FileExistsError
    with pytest.raises(
        FileExistsError, match="The path already exists and is not empty."
    ):
        df.pirr.to_cache(cache_path)


def test_save_cache_existing_path_overwrite(tmp_path):
    """
    Test function for saving cache to an existing path with overwrite flag set to True.

    Args:
        tmp_path (str): Temporary directory path.

    Returns:
        None
    """
    # Create a sample DataFrame
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    # Create a unique subdirectory in tmp_path
    cache_path = tmp_path / "cache"
    cache_path.mkdir(parents=True, exist_ok=True)

    # Simulate the existing path by creating a file in the cache_path
    (cache_path / "dummy_file.txt").touch()

    # overwrite flag is set to True
    loaded_df = cache_and_load(df, cache_path, overwrite=True)
    pd.testing.assert_frame_equal(df, loaded_df)


def test_load_cache_nonexistent_path():
    """
    Test function for loading cache from a nonexistent path.

    Returns:
        None
    """
    # Create a path that does not exist
    path = Path("nonexistent_path")

    # Check that loading from a nonexistent path raises a FileNotFoundError
    with pytest.raises(FileNotFoundError, match="The path does not exist."):
        load_cache(path)
