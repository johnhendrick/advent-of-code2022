from adventofcode2022.day02 import get_score, get_tactical_score

sample_input = ["A Y", "B X", "C Z"]


def test_get_score():

    score = get_score(sample_input)
    assert score == 15


def test_get_tactical_score():
    score = get_tactical_score(sample_input)
    assert score == 12
