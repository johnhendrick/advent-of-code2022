from adventofcode2022 import read_file


def parse_file(file_content):
    row = file_content.split("\n")
    # pair = [(ele.split(" ")) for ele in row]
    return row


file_path = "./input/day02.csv"


guide = parse_file(read_file(file_path))


def get_score(pairs: list) -> int:
    SCORING = {
        "A X": 4,
        "B Y": 5,
        "C Z": 6,
        "A Y": 8,
        "A Z": 3,
        "B X": 1,
        "B Z": 9,
        "C X": 7,
        "C Y": 2,
    }
    score = 0
    for ele in pairs:
        score += SCORING.get(ele, None)

    return score


score = get_score(guide)
print(score)


# Part 2
def resolve_XYZ(pair: str):
    lose_rules = {"C": "B", "B": "A", "A": "C"}
    win_rules = {v: k for k, v in lose_rules.items()}

    if pair[-1] == "Y":
        choice = pair[0]
    elif pair[-1] == "X":
        choice = lose_rules.get(pair[0])
    elif pair[-1] == "Z":
        choice = win_rules.get(pair[0])

    return pair[:2] + choice


def get_tactical_score(pairs: list[str]) -> int:
    SCORING = {
        "A A": 4,
        "B B": 5,
        "C C": 6,
        "A B": 8,
        "A C": 3,
        "B A": 1,
        "B C": 9,
        "C A": 7,
        "C B": 2,
    }
    score = 0
    for ele in pairs:
        pair = resolve_XYZ(ele)
        score += SCORING.get(pair, None)

    return score


tactical_score = get_tactical_score(guide)
print(tactical_score)
