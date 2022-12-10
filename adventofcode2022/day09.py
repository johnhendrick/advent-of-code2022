import math
import numpy as np

from adventofcode2022 import read_file


def parse_file(file_content) -> list:
    rows = file_content.split("\n")
    rows = [(_row.split(" ")[0], int(_row.split(" ")[1])) for _row in rows]
    return rows


FILE_PATH = "./input/day09.csv"
moves = parse_file(read_file(FILE_PATH))


move_ref = {"U": 0, "D": 0, "L": 1, "R": 1}
move_sign = {"U": 1, "D": -1, "L": -1, "R": 1}  # up down flipped


def move_check(head, tail) -> tuple[bool, bool]:
    dist = np.linalg.norm(np.array(head) - np.array(tail))
    if dist == 2:
        return True, False
    elif dist > 2:
        return True, True
    else:
        return False, None


def move_tail(head: list, tail: list) -> list:
    # head after moving
    move_bool, move_diagonal = move_check(head, tail)
    if move_bool:
        for j in range(2):
            poss_diff = head[j] - tail[j]
            vector = int(math.copysign(1, poss_diff))
            if move_diagonal:
                tail[j] += vector
            else:
                if abs(poss_diff) == 2:
                    tail[j] += vector
    return tail


def traverse_multi_knot(moves, tail_knots=9):
    head_pos = [0, 0]
    tails_pos = [[0, 0] for _ in range(tail_knots)]
    last_knot_locs = {(0, 0)}
    for move, val in moves:
        for _ in range(val):
            head_pos[move_ref[move]] += move_sign[move]

            for tail_knot in range(tail_knots):
                if tail_knot == 0:
                    tails_pos[tail_knot] = move_tail(head_pos, tails_pos[tail_knot])
                else:
                    tails_pos[tail_knot] = move_tail(tails_pos[tail_knot - 1], tails_pos[tail_knot])

            last_knot_locs.add(tuple(tails_pos[-1]))

    return last_knot_locs


print(len(traverse_multi_knot(moves, tail_knots=1)))
print(len(traverse_multi_knot(moves, tail_knots=9)))
