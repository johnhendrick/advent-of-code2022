from adventofcode2022 import read_file
from collections import deque
import sympy as sym
import re

FILE_PATH = "./input/day21.csv"


def parse_file(file_content: str) -> list:
    tasks_ = [row.split(": ") for row in file_content.split("\n")]
    tasks_ = {task[0]: int(task[1]) if task[1].isdigit() else task[1] for task in tasks_}
    return tasks_, deque([k for k, task in tasks_.items() if isinstance(task, str)])


while unknown:
    try:
        monke = unknown.pop()
        task = tasks[monke]
        for key in tasks.keys():
            if isinstance(tasks[key], int):
                task = task.replace(key, str(tasks[key]))
        value = eval(task)
        tasks[monke] = int(value)
    except NameError:
        unknown.appendleft(monke)

tasks, unknown = parse_file(read_file(FILE_PATH))
print(tasks["root"])  # part 1


def replace(eqn: str):
    vars_ = re.findall(r"\w{4}", eqn)
    if vars_ == ["humn"] or len(vars_) == 0:
        if "humn" not in eqn:
            return eval(eqn)
        return eqn
    else:
        for var in vars_:
            if var != "humn":
                eqn = eqn.replace(var, f"({tasks.get(var)})")
        return replace(eqn)


tasks, unknown = parse_file(read_file(FILE_PATH))
tasks["humn"] = "humn_"
root_eqn = tasks["root"].split(" + ")
solve_eqn = [replace(root_eqn[0]), replace(root_eqn[1])]
eqn = sym.parsing.sympy_parser.parse_expr(solve_eqn[0] + "-" + str(solve_eqn[1]))
result = sym.solve(eqn, sym.symbols("humn"))
print(int(result[0]))  # part 2
