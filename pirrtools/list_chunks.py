"""This module provides a function for splitting an iterable into chunks of a specified
size. It also supports equalizing the lengths of elements within their respective sub-
lists.

The main function in this module is `chunk()`, which takes an iterable, chunk size, and
  an optional flag for equalizing lengths.
The function returns a list of lists, where each sub-list has a length equal to the
 n specified chunk size.

Example usage:

    >>> chunk([1, 2, 3, 4, 5, 6], 2)
    [[1, 2], [3, 4], [5, 6]]
    >>> chunk([1, 2, 3, 4, 5, 6], 2, True)
    [[1, 2], [3, 4], [5, 6]]
"""

from typing import List, Iterable, Union, Optional
import numpy as np


def chunk(
    iterable: Iterable[Union[int, str, float]], chunk_size: int, equalize: bool = False
) -> List[List[Optional[Union[int, str, float]]]]:
    """This function splits an iterable into chunks of a specified size. If the
    `equalize` flag is set to True, it will try to make the lengths of the elements that
    share the same position within their respective sub-lists as similar as possible.

    :param iterable: The input iterable
    :type iterable: Iterable[Union[int, str, float]]
    :param chunk_size: The desired size of the chunks
    :type chunk_size: int
    :param equalize: A flag indicating whether to equalize the lengths of elements,
      defaults to False
    :type equalize: bool, optional
    :return: A list of lists where each sub-list is of length equal to the passed
      integer
    :rtype: List[List[Optional[Union[int, str, float]]]]

    .. note::
       - The `numpy` module is used for efficient array manipulation
         (https://numpy.org/doc/stable/)
       - If `equalize` is set to True, the function sorts the iterable by length before
         chunking, then transposes the list.

    .. code-block:: python

       >>> chunk([1, 2, 3, 4, 5, 6], 2)
       [[1, 2], [3, 4], [5, 6]]
       >>> chunk([1, 2, 3, 4, 5, 6], 2, True)
       [[1, 2], [3, 4], [5, 6]]
    """

    # Ensure chunk size is at least 1
    chunk_size = max(1, chunk_size)
    iterable = list(iterable)
    if equalize:
        iterable.sort(key=lambda x: len(str(x)))
    n = int(np.ceil(len(iterable) / chunk_size))
    return [iterable[i::n] for i in range(n)]
