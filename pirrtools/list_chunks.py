from typing import List, Iterable, Any, Union, Optional
import numpy as np

def chunk(iterable: Iterable[Union[int, str, float]], chunk_size: int, equalize: bool=False) -> List[List[Optional[Union[int, str, float]]]]:
    """
    This function splits an iterable into chunks of a specified size.
    If the `equalize` flag is set to True, it will try to make the lengths of the elements
    that share the same position within their respective sub-lists as similar as possible.

    :param iterable: The input iterable
    :type iterable: Iterable[Union[int, str, float]]
    :param chunk_size: The desired size of the chunks
    :type chunk_size: int
    :param equalize: A flag indicating whether to equalize the lengths of elements, defaults to False
    :type equalize: bool, optional
    :return: A list of lists where each sub-list is of length equal to the passed integer
    :rtype: List[List[Optional[Union[int, str, float]]]]

    .. note::
       - The `numpy` module is used for efficient array manipulation (https://numpy.org/doc/stable/)
       - If `equalize` is set to True, the function sorts the iterable by length before chunking, then transposes the list.

    .. code-block:: python

       >>> chunk([1, 2, 3, 4, 5, 6], 2)
       [[1, 2], [3, 4], [5, 6]]
       >>> chunk([1, 2, 3, 4, 5, 6], 2, True)
       [[1, 2], [3, 4], [5, 6]]
    """

    iterable = list(iterable)
    if equalize:
        iterable.sort(key=lambda x: len(str(x)))
    n = int(np.ceil(len(iterable) / chunk_size))
    return [iterable[i::n] for i in range(n)]


def align_columns(iterable_of_iterables: Iterable[Iterable[Any]]) -> List[str]:
    """
    Given an iterable of iterables, this function finds the maximum length of string representation
    of each element in the corresponding position of the sublists. It then returns a list of strings where 
    each string is a representation of each corresponding sub iterable with format width for each element 
    of the sub iterable equal to the corresponding max length for that element's position.
    
    :param iterable_of_iterables: An iterable of iterables
    :type iterable_of_iterables: Iterable[Iterable[Any]]
    :return: A list of strings with equal lengths, which when printed out on separate lines, the columns will be aligned.
    :rtype: List[str]

    .. note::
       The `zip` function is used to make an iterator that aggregates elements from each of the iterables.
       Refer: https://docs.python.org/3.3/library/functions.html#zip
       
    .. code-block:: python

       >>> align_columns([['apple', 'cherry'], ['dates', 'elderberry'], ['banana']])
       ['apple  cherry    ', 
        'dates  elderberry', 
        'banana            ']
    """

    max_lengths = [
        max(len(str(elem)) for elem in col)
        for col in zip(*[iterable + [None] * (len(max(iterable_of_iterables, key=len)) - len(iterable)) 
                         for iterable in iterable_of_iterables])
    ]

    output = [
        " ".join((str(elem) if elem is not None else '').ljust(length) for elem, length in zip(iterable + [None] * (len(max_lengths) - len(iterable)), max_lengths))
        for iterable in iterable_of_iterables
    ]

    return output
