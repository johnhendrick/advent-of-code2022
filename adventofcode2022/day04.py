from adventofcode2022 import read_file


def parse_file(file_content) -> list:
    row = file_content.split("\n")
    tasks = [ele.split(",") for ele in row]
    return tasks


FILE_PATH = "./input/day04.csv"

tasks = parse_file(read_file(FILE_PATH))


def transform_to_tuple(task: str) -> tuple:
    _range = task.split("-")
    assert len(_range) == 2

    return tuple([int(ele) for ele in _range])


def check_subset(left: tuple, right: tuple) -> bool:
    if left[0] == right[0] or left[1] == right[1]:
        return True
    elif left[0] < right[0] and left[1] > right[1]:
        return True
    elif left[0] > right[0] and left[1] < right[1]:
        return True
    else:
        return False


def count_subset(tasks: list) -> int:
    count = 0
    for task_pair in tasks:
        _left, _right = task_pair
        left, right = transform_to_tuple(_left), transform_to_tuple(_right)
        if check_subset(left, right):
            count += 1
    return count


print(count_subset(tasks))

# Part 2


def check_any_overlap(left: tuple, right: tuple) -> bool:
    left_set = set(range(left[0], left[1] + 1))
    right_set = set(range(right[0], right[1] + 1))

    if left_set.intersection(right_set).__len__() > 0:
        return True
    else:
        return False


def count_intersect(tasks: list) -> int:
    count = 0
    for task_pair in tasks:
        _left, _right = task_pair
        left, right = transform_to_tuple(_left), transform_to_tuple(_right)
        if check_any_overlap(left, right):
            count += 1
    return count


print(count_intersect(tasks))
