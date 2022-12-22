import pytest

from adventofcode2022.day15 import Location


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            [
                [Location(12, 10), Location(88, 10)],
                [Location(6, 10), Location(10, 10)],
                [Location(1, 10), Location(5, 10)],
                [Location(7, 10), Location(10, 10)],
            ],
            [
                [Location(1, 10), Location(5, 10)],
                [Location(6, 10), Location(10, 10)],
                [Location(7, 10), Location(10, 10)],
                [Location(12, 10), Location(88, 10)],
            ],
        )
    ],
)
def test_sort_location(input, expected):
    result = sorted(input, key=lambda z: z[0])
    assert result == expected
