from pirrtools.list_chunks import chunk


def test_chunk_basic_case_1():
    assert chunk([1, 2, 3, 4, 5, 6], 2) == [[1, 4], [2, 5], [3, 6]]


def test_chunk_basic_case_2():
    assert chunk([1, 2, 3, 4, 5, 6], 2, True) == [[1, 4], [2, 5], [3, 6]]


def test_chunk_basic_case_3():
    assert chunk([1, 2, 3, 4, 5, 6, 7], 3) == [[1, 4, 7], [2, 5], [3, 6]]


def test_chunk_basic_case_4():
    assert chunk([1, 2, 3, 4, 5, 6, 7], 3, True) == [[1, 4, 7], [2, 5], [3, 6]]


def test_chunk_basic_case_5():
    assert chunk(["apple", "banana", "cherry", "dates", "elderberry"], 2) == [
        ["apple", "dates"],
        ["banana", "elderberry"],
        ["cherry"],
    ]


def test_chunk_basic_case_6():
    assert chunk(["apple", "banana", "cherry", "dates", "elderberry"], 2, True) == [
        ["apple", "cherry"],
        ["dates", "elderberry"],
        ["banana"],
    ]


def test_chunk_edge_case_1():
    assert chunk([], 3) == []


def test_chunk_edge_case_2():
    assert chunk([1], 2) == [[1]]


def test_chunk_edge_case_3():
    assert chunk([1, 2], 1) == [[1], [2]]


def test_chunk_edge_case_4():
    assert chunk([1, 2], 1, True) == [[1], [2]]


def test_chunk_edge_case_5():
    assert chunk([1, 2, 3], 0) == [[1], [2], [3]]  # Chunk size of 0 treated as 1


def test_chunk_edge_case_6():
    assert chunk([1, 2, 3], 1) == [[1], [2], [3]]


def test_chunk_edge_case_7():
    assert chunk([1, 2, 3], 4) == [[1, 2, 3]]
