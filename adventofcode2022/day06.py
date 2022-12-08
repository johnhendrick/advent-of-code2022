from adventofcode2022 import read_file

file_path = "./input/day06.csv"

signal = read_file(file_path)


def min_zero(num):
    if num > 0:
        return num
    else:
        return 0


def find_marker_pos(signal: str, check_length=4) -> int:

    for i, char in enumerate(signal):
        # check next 4 are unique
        last_n = set(signal[min_zero(i - check_length) : i])
        if len(last_n) == check_length:
            return i

    raise Exception("No marker found")


print(find_marker_pos(signal))
# Part 2
print(find_marker_pos(signal, check_length=14))
