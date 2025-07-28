"""
This module contains test functions to be used with the pytest framework.
"""

from pirrtools.list_chunks import chunk


def test_chunk_basic_case_1():
    """
    Test case for the chunk function with a basic input.
    """
    assert chunk([1, 2, 3, 4, 5, 6], 2) == [[1, 4], [2, 5], [3, 6]]


def test_chunk_basic_case_2():
    """
    Test case for the chunk function with a basic case and step size of 2.

    The input list [1, 2, 3, 4, 5, 6] is chunked into sublists of size 2 with a step
    size of 2.
    The expected output is [[1, 4], [2, 5], [3, 6]].

    """
    assert chunk([1, 2, 3, 4, 5, 6], 2, True) == [[1, 4], [2, 5], [3, 6]]


def test_chunk_basic_case_3():
    """
    Test case for the chunk function with a basic case.

    The input list [1, 2, 3, 4, 5, 6, 7] is chunked into sublists of size 3.
    The expected output is [[1, 4, 7], [2, 5], [3, 6]].

    """
    assert chunk([1, 2, 3, 4, 5, 6, 7], 3) == [[1, 4, 7], [2, 5], [3, 6]]


def test_chunk_basic_case_4():
    """
    Test case for the chunk function with a basic case.

    This test verifies that the chunk function correctly splits a list into sublists of
    specified size.

    The expected output is [[1, 4, 7], [2, 5], [3, 6]].

    """
    assert chunk([1, 2, 3, 4, 5, 6, 7], 3, True) == [[1, 4, 7], [2, 5], [3, 6]]


def test_chunk_basic_case_5():
    """
    Test case for the `chunk` function with a basic case.

    This test case verifies that the `chunk` function correctly splits a list into
    chunks of size 2.
    It checks if the output matches the expected chunked list.

    """
    assert chunk(["apple", "banana", "cherry", "dates", "elderberry"], 2) == [
        ["apple", "dates"],
        ["banana", "elderberry"],
        ["cherry"],
    ]


def test_chunk_basic_case_6():
    """
    Test case for the chunk function with a basic case.

    The function tests the behavior of the chunk function when given a list of strings
    and a chunk size of 2. It asserts that the returned value matches the expected
    output.

    """
    assert chunk(["apple", "banana", "cherry", "dates", "elderberry"], 2, True) == [
        ["apple", "cherry"],
        ["dates", "elderberry"],
        ["banana"],
    ]


def test_chunk_edge_case_1():
    """
    Test case for the `chunk` function with an empty list.

    The `chunk` function should return an empty list when given an empty input list.

    """
    assert chunk([], 3) == []


def test_chunk_edge_case_2():
    """
    Test case for the `chunk` function with an edge case.

    This test verifies that the `chunk` function correctly handles the edge case
    where the input list has only one element and the chunk size is 2.

    The expected behavior is that the `chunk` function should return a list
    containing a single sublist with the input element.

    """
    assert chunk([1], 2) == [[1]]


def test_chunk_edge_case_3():
    """
    Test case for the `chunk` function with an edge case.

    This test case verifies that the `chunk` function correctly handles the scenario
    where the input list has two elements and the chunk size is 1. It checks whether
    the function returns a list of two sublists, each containing one element from the
    input list.

    """
    assert chunk([1, 2], 1) == [[1], [2]]


def test_chunk_edge_case_4():
    """
    Test case for the `chunk` function with an edge case.

    This test case verifies that the `chunk` function correctly handles the scenario
    where the input list has only two elements and the chunk size is set to 1.

    The expected result is a list of two sublists, each containing one element from
    the input list.

    """
    assert chunk([1, 2], 1, True) == [[1], [2]]


def test_chunk_edge_case_5():
    """
    Test case for chunk function with edge case of chunk size 0.
    The chunk size of 0 is treated as 1, so the input list should be split into
      individual elements.
    """
    assert chunk([1, 2, 3], 0) == [[1], [2], [3]]  # Chunk size of 0 treated as 1


def test_chunk_edge_case_6():
    """
    Test for the `chunk` function with an edge case where the input list has only one
    element. It verifies that the function correctly returns a list of lists, where each
    sub-list contains a single element from the input list.
    """
    assert chunk([1, 2, 3], 1) == [[1], [2], [3]]


def test_chunk_edge_case_7():
    """
    Test case for the `chunk` function with an edge case where the size of the chunk is
    greater than the length of the list.
    """
    assert chunk([1, 2, 3], 4) == [[1, 2, 3]]
