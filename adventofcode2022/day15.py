import re
from dataclasses import dataclass, field
from itertools import repeat
from tqdm import tqdm

from adventofcode2022 import read_file

FILE_PATH = "./input/day15.csv"


def parse_file(file_content: str) -> dict:
    rows = [re.findall(r"=(-?[0-9]*)", row) for row in file_content.split("\n")]
    return {(int(ele[0]), int(ele[1])): (int(ele[2]), int(ele[3])) for ele in rows}


@dataclass(order=True, frozen=True)
class Location:
    sort_index: int = field(init=False, repr=False)
    x: int
    y: int

    def __post_init__(self):
        object.__setattr__(self, "sort_index", self.x)


class Sensor:
    def __init__(self, pos: Location, nearest_beacon: Location):
        self.pos = pos
        self.nearest_beacon = nearest_beacon
        self.radius = abs(left.x - right.x) + abs(left.y - right.y)  # manhattan dist

    def integral_y(self, row, only_boundary=False) -> list:
        if abs(row - self.pos.y) > self.radius:
            return []

        blank_ys = [
            -self.radius + abs(self.pos.y - row) + self.pos.x,
            self.radius - abs(self.pos.y - row) + self.pos.x,
        ]
        blank_ys.sort()
        if only_boundary:
            return [Location(*ele) for ele in zip(blank_ys, repeat(row))]
        else:
            return [Location(*ele) for ele in zip(range(blank_ys[0], blank_ys[1] + 1), repeat(row))]


def get_blank_beacon_spaces(row, sensors, beacon_locations):
    no_beacon = []
    for sensor in tqdm(sensors):
        sensor_scope_cleaned = []
        sensor_scope = sensor.integral_y(row)
        for ele in sensor_scope:
            if ele not in beacon_locations:
                sensor_scope_cleaned.append(ele)
        no_beacon += sensor_scope_cleaned
    return len(set(no_beacon))


sensor_beacon = parse_file(read_file(FILE_PATH))
sensors = [Sensor(Location(*s_loc), Location(*b_loc)) for s_loc, b_loc in sensor_beacon.items()]
beacon_locations = list(set([sensor.nearest_beacon for sensor in sensors]))
print(get_blank_beacon_spaces(2000000, sensors, beacon_locations))


def get_potential_beacon(row, sensors, max_coor) -> Location:
    collect_range = []
    for sensor in sensors:
        _range = sensor.integral_y(row, only_boundary=True)
        if len(_range) > 1:
            collect_range.append(range_limiter(_range, max_x=max_coor))
    final_range = union_range(collect_range)
    if len(final_range) > 1:
        return Location(final_range[0][1].x + 1, row)


def range_limiter(range_: list[Location], max_x: int) -> list[Location]:
    left, right = range_[0], range_[1]
    if left.x < 0:
        left = Location(0, right.y)
    if right.x > max_x:
        right = Location(max_x, right.y)
    return [left, right]


def union_range(ranges: list[list[Location]]):
    union_ = []
    for begin, end in sorted(ranges, key=lambda z: z[0]):
        if union_ and union_[-1][1].x >= begin.x - 1:
            union_[-1][1] = max(union_[-1][1], end)
        else:
            union_.append([begin, end])
    return union_


MAX_COOR = 4000000  # part 2
for y in tqdm(range(0, MAX_COOR + 1)):
    val = get_potential_beacon(y, sensors, max_coor=MAX_COOR)
    if val:
        break
print(val.x * 4000000 + val.y)
