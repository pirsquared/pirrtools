def test_chunk():
    assert chunk([1, 2, 3, 4, 5, 6], 2) == [[1, 4], [2, 5], [3, 6]]
    assert chunk([1, 2, 3, 4, 5, 6], 2, True) == [[1, 4], [2, 5], [3, 6]]
    assert chunk([1, 2, 3, 4, 5, 6, 7], 3) == [[1, 4, 7], [2, 5], [3, 6]]
    assert chunk([1, 2, 3, 4, 5, 6, 7], 3, True) == [[1, 4, 7], [2, 5], [3, 6]]
    assert chunk(["apple", "banana", "cherry", "dates", "elderberry"], 2) == [['apple', 'dates'], ['banana', 'elderberry'], ['cherry']]
    assert chunk(["apple", "banana", "cherry", "dates", "elderberry"], 2, True) == [["apple", "cherry"], ["dates", "elderberry"], ["banana"]]


def test_align_columns():
    assert align_columns([['apple', 'cherry'], ['dates', 'elderberry'], ['banana']]) == ['apple  cherry    ',
                                                                                         'dates  elderberry',
                                                                                         'banana           ']
    assert align_columns([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == ['1 2 3',
                                                                '4 5 6',
                                                                '7 8 9']
    assert align_columns([[10, 20, 30], [40, 50, 60], [70, 80, 90]]) == ['10 20 30',
                                                                         '40 50 60',
                                                                         '70 80 90']
