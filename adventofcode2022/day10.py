from adventofcode2022 import read_file


def parse_file(file_content) -> list:
    rows = file_content.split("\n")
    rows = [(_row, 0) if _row == "noop" else tuple([_row.split(" ")[0], int(_row.split(" ")[1])]) for _row in rows]
    return rows


FILE_PATH = "./input/day10.csv"
command = parse_file(read_file(FILE_PATH))


def checkpoint_(cycle: int, register: int, cycles=[20, 60, 100, 140, 180, 220]):
    if cycle in cycles:
        signals.append(cycle * register)


def crt_check(cycle, sprite_pos) -> bool:
    crt_row = (cycle - 1) % 40
    if sprite_pos - 1 <= crt_row and sprite_pos + 1 >= crt_row:
        return True


def exec_program(command) -> int:
    crt, cycle, register = 0, 0, 1
    overlap = ""
    for row in command:
        if row[0] == "noop":
            cycle += 1
            checkpoint_(cycle, register)
            overlap += "#" if crt_check(cycle, register) else "."
        else:
            cycle += 1
            checkpoint_(cycle, register)
            overlap += "#" if crt_check(cycle, register) else "."

            cycle += 1
            checkpoint_(cycle, register)
            overlap += "#" if crt_check(cycle, register) else "."
            register += row[1]
    return overlap


signals = []
overlap = exec_program(command)

print(sum(signals))
for i in range(6):
    print(overlap[i * 40 : (i + 1) * 40])
# RBPARAGF
