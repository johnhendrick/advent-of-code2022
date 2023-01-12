from adventofcode2022 import read_file
from itertools import repeat

FILE_PATH = "./input/day14.csv"


def parse_file(file_content: str) -> list:
    rows = [row.split(" -> ") for row in file_content.split("\n")]
    rocks = [[eval(ele_) for ele_ in ele] for ele in rows]
    return rocks


rock_points = parse_file(read_file(FILE_PATH))


def draw_line(start: tuple[int], end: tuple[int]) -> list[tuple]:
    line = []
    for i, ele in enumerate(start):
        if ele != end[i]:
            if ele > end[i]:
                _line = list(range(end[i], ele + 1))
            else:
                _line = list(range(ele, end[i] + 1))

        else:
            _line = repeat(ele)
        line.append(_line)
    return list(zip(line[0], line[1]))


def draw_rocks(rock_points: list[list]) -> list[tuple]:
    # get all rocks coordinates from rock points
    rock_coors = set()
    for rock in rock_points:
        for i in range(len(rock) - 1):
            line: list = draw_line(rock[i], rock[i + 1])
            rock_coors.update(line)
    return rock_coors


class Sand:
    def __init__(self, terrain: set[tuple()], add_floor: bool = False, lowest_ceil: int = 0):
        self.pos: list = [500, 0]
        self.settled: bool = False
        self.lowest_ceil: int = lowest_ceil
        self.terrain = self._get_terrain(terrain, add_floor)

    def _get_terrain(self, terrain, add_floor):
        if add_floor:
            self.lowest_ceil += 2
            floor_line = draw_rocks([[(0, self.lowest_ceil), (1000, self.lowest_ceil)]])
            terrain.update(floor_line)
        return terrain

    def move_step(self):
        if tuple([self.pos[0], self.pos[1] + 1]) not in self.terrain:
            self.pos = [self.pos[0], self.pos[1] + 1]
        elif tuple([self.pos[0] - 1, self.pos[1] + 1]) not in self.terrain:
            self.pos = [self.pos[0] - 1, self.pos[1] + 1]
        elif tuple([self.pos[0] + 1, self.pos[1] + 1]) not in self.terrain:
            self.pos = [self.pos[0] + 1, self.pos[1] + 1]
        else:
            self.settled = True

    def simulate_sand(self) -> bool:
        while not self.settled:
            self.move_step()
            if self.pos[1] == self.lowest_ceil:  # fallen off
                return False
        return True


def get_lowest_terrain(terrain):
    return max(terrain, key=lambda x: x[1])[1]


def pour_sand(add_floor: bool) -> int:
    terrain = draw_rocks(rock_points)
    lowest_ceil = get_lowest_terrain(terrain)
    count = 0
    no_sand_in_abyss = True
    last_sand_pos = None

    while no_sand_in_abyss and last_sand_pos != [500, 0]:

        sand = Sand(terrain, add_floor=add_floor, lowest_ceil=lowest_ceil)
        no_sand_in_abyss = sand.simulate_sand()
        last_sand_pos = sand.pos

        if no_sand_in_abyss:
            terrain.add(tuple(sand.pos))
            count += 1
    return count


print(pour_sand(add_floor=0))
print(pour_sand(add_floor=True))
