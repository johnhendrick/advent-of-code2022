from adventofcode2022 import read_file

FILE_PATH = "./input/day13.csv"


def parse_file(file_content, skip_blank=True) -> list:
    if skip_blank:
        _rows = [row.split("\n") for row in file_content.split("\n\n")]
    else:
        file_content = file_content.replace("\n\n", "\n")
        return [eval(row) for row in file_content.split("\n")]
    rows = []
    for pair in _rows:
        rows.append([eval(pair[0]), eval(pair[1])])
    return rows


signal = parse_file(read_file(FILE_PATH))


def as_list(x):
    if isinstance(x, list):
        return x
    elif isinstance(x, int):
        return [x]
    else:
        raise Exception("type out of scope")


def compare_signal(left, right):
    left_list, right_list = list(left), list(right)
    # exit conditions
    try:
        left_ele = left_list.pop(0)
    except IndexError:
        print("Left side ran out of items")
        return True
    try:
        right_ele = right_list.pop(0)
    except IndexError:
        print("Right side ran out of items")
        return False

    if isinstance(left_ele, int) and isinstance(right_ele, int):
        if left_ele < right_ele:
            print("Left side is smaller")
            return True
        elif left_ele > right_ele:
            print("Right side is smaller")
            return False
        else:
            return compare_signal(left_list, right_list)

    elif isinstance(left_ele, int) + isinstance(right_ele, int) == 1:
        # one of them is not int
        return compare_signal(as_list(left_ele), as_list(right_ele))
    elif isinstance(left_ele, list) and isinstance(right_ele, list):
        if left_ele == right_ele:
            return compare_signal(left_list, right_list)
        else:
            return compare_signal(left_ele, right_ele)

    else:
        raise Exception("unresolved")


count = 0
for i, pair in enumerate(signal):
    if compare_signal(*pair):
        count += i + 1
print(count)

# part 2
div = [[[2]], [[6]]]
signal2 = parse_file(read_file(FILE_PATH), skip_blank=False) + div


def bubble_sort(arr) -> None:
    n = len(arr)
    # if the array is already sorted, it doesn't need
    swapped = False
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if not compare_signal(arr[j], arr[j + 1]):
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
        if not swapped:
            return


bubble_sort(signal2)
locations = [i + 1 for i, x in enumerate(signal2) if x in div]
print(locations[0] * locations[1])
