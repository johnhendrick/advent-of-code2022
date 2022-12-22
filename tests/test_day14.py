import pytest

from adventofcode2022.day14 import draw_line


@pytest.mark.parametrize(
    "start, end, expected",
    [((498, 4), (498, 6), [(498, 4), (498, 5), (498, 6)]), ((498, 6), (496, 6), [(498, 6), (497, 6), (496, 6)])],
)
def test_draw_line(start, end, expected):
    line = draw_line(start, end)
    assert set(line) == set(expected)
    assert len(line) == len(expected)
