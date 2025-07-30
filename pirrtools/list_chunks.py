"""Utilities for splitting iterables into chunks.

This module provides functionality for dividing iterables into smaller,
more manageable chunks of specified sizes. It includes options for
equalizing chunk contents based on element properties.

The primary function `chunk()` distributes elements across a calculated
number of sublists, with optional sorting to balance element characteristics.

Example:
    >>> chunk([1, 2, 3, 4, 5, 6], 2)
    [[1, 4], [2, 5], [3, 6]]

    >>> chunk(['a', 'bb', 'ccc', 'dddd'], 2, equalize=True)
    [['a', 'ccc'], ['bb', 'dddd']]  # Sorted by length first
"""

from collections.abc import Iterable
from typing import Optional, Union

import numpy as np


def chunk(
    iterable: Iterable[Union[int, str, float]], chunk_size: int, equalize: bool = False
) -> list[list[Optional[Union[int, str, float]]]]:
    """Split an iterable into chunks distributed across sublists.

    This function divides an iterable into a calculated number of sublists,
    distributing elements evenly by taking every nth element for each sublist.
    When equalize is True, elements are first sorted by string length to
    balance the characteristics of elements within each chunk.

    Args:
        iterable (Iterable[Union[int, str, float]]): The input iterable to chunk.
        chunk_size (int): The target number of elements to distribute across.
            This determines the number of sublists created.
        equalize (bool, optional): Whether to sort elements by string length
            before chunking to balance element characteristics. Defaults to False.

    Returns:
        List[List[Optional[Union[int, str, float]]]]: A list of sublists where
            elements are distributed evenly. The number of sublists is calculated
            as ceil(len(iterable) / chunk_size).

    Examples:
        Basic chunking (elements distributed, not grouped sequentially):
            >>> chunk([1, 2, 3, 4, 5, 6], 2)
            [[1, 4], [2, 5], [3, 6]]

        With equalization (sorted by string length first):
            >>> chunk(['a', 'bb', 'ccc', 'dddd'], 2, equalize=True)
            [['a', 'ccc'], ['bb', 'dddd']]

        Handling uneven division:
            >>> chunk([1, 2, 3, 4, 5], 2)
            [[1, 3, 5], [2, 4]]

    Note:
        The function ensures chunk_size is at least 1 to avoid division by zero.
        The distribution pattern takes every nth element where n is calculated
        as ceil(len(iterable) / chunk_size).
    """

    # Ensure chunk size is at least 1 to avoid division by zero
    chunk_size = max(1, chunk_size)
    iterable = list(iterable)

    # Sort by string length if equalization is requested
    if equalize:
        iterable.sort(key=lambda x: len(str(x)))

    # Calculate step size for distribution
    n = int(np.ceil(len(iterable) / chunk_size))

    # Create sublists by taking every nth element starting from each position
    return [iterable[i::n] for i in range(n)]
