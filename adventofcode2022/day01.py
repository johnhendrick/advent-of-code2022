from adventofcode2022 import read_file


def parse_file(file_content):
    _group = file_content.split("\n\n")
    group = [(ele.split("\n")) for ele in _group]
    group_cleaned = [list(map(lambda x: int(x), ele)) for ele in group]
    return group_cleaned


FILE_PATH = "./input/day01.csv"


calories = parse_file(read_file(FILE_PATH))
calories_sum = [sum(elf) for elf in calories]

print(max(calories_sum))


# Part 2

sorted_calories_sum = sorted(calories_sum, reverse=True)
print(sum(sorted_calories_sum[:3]))
