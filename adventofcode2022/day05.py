from adventofcode2022 import read_file
import pandas as pd


def parse_crates(row: str) -> list:
    size = len(row) // 4

    _content = []
    for i in range(size + 1):
        _content.append(row[i * 4 : (i + 1) * 4 :])
    # _content = [row[:3], row[4:7], row[-3:]]
    content = [None if ele.strip() == "" else ele[1] for ele in _content]
    return content


def parse_tasks(raw_task: list) -> tuple:

    task = raw_task[5:]
    task = task.split(" from ")
    task = [task[0], task[1].split(" to ")]
    return task


def parse_file(file_content) -> list:
    row = file_content.split("\n\n")
    row[0], row[1] = row[0].split("\n"), row[1].split("\n")
    row[0] = [parse_crates(ele) for ele in row[0]]
    row[0] = tranpose(row[0])

    row[1] = [parse_tasks(ele) for ele in row[1]]
    return row


def tranpose(raw_crates_shape: list) -> pd.DataFrame:
    df = pd.DataFrame(raw_crates_shape[:-1], columns=[pos.strip() for pos in raw_crates_shape[-1]])
    _data = df.to_dict(orient="list")
    data = {k: [ele for ele in v[::-1] if ele] for k, v in _data.items()}
    return data


def execute(crates, tasks, reverse=True, verbose=True):

    for task in tasks:
        task_size = int(task[0])
        for move in range(task_size):
            item = crates[task[1][0]].pop()
            crates[task[1][1]].append(item)
            if verbose:
                print(f"Moved {item} from {task[1][0]} to {task[1][1]}")

        if reverse:
            # do a partial reverse
            crates[task[1][1]][-task_size:] = crates[task[1][1]][-task_size:][::-1]

    return crates


def get_top(crates):
    string = ""
    for k, v in crates.items():
        string += v[-1]
    return string


file_path = "./input/day05.csv"

crates, tasks = parse_file(read_file(file_path))

crates = execute(crates, tasks, reverse=False, verbose=False)
print(get_top(crates))

# Part 2
crates_2, tasks = parse_file(read_file(file_path))
crates_2 = execute(crates_2, tasks, reverse=True, verbose=False)
print(get_top(crates_2))
