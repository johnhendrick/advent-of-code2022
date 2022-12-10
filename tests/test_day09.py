import pytest

from adventofcode2022.day09 import move_tail


@pytest.mark.parametrize(
    "head, tail, expected",
    [([1, 1], [0, 0], False), ([1, 2], [0, 0], True), ([1, 0], [0, 0], False), ([2, 0], [0, 0], True)],
)
def test_move_tail(head, tail, expected):
    assert move_tail(head, tail) == expected
