def read_file(file_path: str):
    with open(file_path) as f:
        return f.read()


def parse_file(file_content):
    row = file_content.split("\n")
    return row


file_path = "./input/day03.csv"

rucksack = parse_file(read_file(file_path))


def split_middle(content: str) -> tuple:

    mid = int(len(content) / 2)
    left, right = content[:mid], content[mid:]
    return left, right


def compare(left: str, right: str) -> str:
    exists_both = list(set(left).intersection(right))
    assert len(exists_both) == 1

    return exists_both[0]


def score_lookup(char: str) -> int:

    if char.isupper():
        val = ord(char) - ord("A") + 27
    else:
        val = ord(char) - ord("a") + 1
    return val


def get_priorities(rucksack):

    score = 0
    for content in rucksack:
        left, right = split_middle(content)
        common = compare(left, right)
        score += score_lookup(common)
    return score


print(get_priorities(rucksack))

# Part 2
def compare_three(left: str, mid: str, right: str) -> str:
    exists_all = list(set(left).intersection(mid).intersection(right))
    assert len(exists_all) == 1

    return exists_all[0]


def get_badge_priorities(rucksack):

    score = 0
    for i in range(0, len(rucksack), 3):
        content = rucksack[i : i + 3]
        common = compare_three(*content)
        score += score_lookup(common)
    return score


print(get_badge_priorities(rucksack))
