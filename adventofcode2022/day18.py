import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
from adventofcode2022 import read_file

FILE_PATH = "./input/day18.csv"


def parse_file(file_content: str) -> list:
    return set([tuple([int(ele) for ele in row.split(",")]) for row in file_content.split("\n")])


def get_neighbours(cube: list[int]):
    fix = [(0, 1, 2), (0, 2, 1), (1, 2, 0)]
    neighbour_coors = []

    for fixed_coor1, fixed_coor2, update_coor in fix:
        empty = [0, 0, 0]
        empty[fixed_coor1] = cube[fixed_coor1]
        empty[fixed_coor2] = cube[fixed_coor2]
        empty[update_coor] = cube[update_coor] + 1
        neighbour_coors.append(tuple(empty))
        empty[update_coor] = cube[update_coor] - 1
        neighbour_coors.append(tuple(empty))
    return neighbour_coors


def is_inside(loc: tuple, all_coors: list[tuple]) -> bool:
    try:
        x_min = min(set(filter(lambda l: (l[1], l[2]) == (loc[1], loc[2]), all_coors)), key=lambda l: l[0])[0]
        y_min = min(set(filter(lambda l: (l[2], l[0]) == (loc[2], loc[0]), all_coors)), key=lambda l: l[1])[1]
        z_min = min(set(filter(lambda l: (l[1], l[0]) == (loc[1], loc[0]), all_coors)), key=lambda l: l[2])[2]
        x_max = max(set(filter(lambda l: (l[1], l[2]) == (loc[1], loc[2]), all_coors)), key=lambda l: l[0])[0]
        y_max = max(set(filter(lambda l: (l[2], l[0]) == (loc[2], loc[0]), all_coors)), key=lambda l: l[1])[1]
        z_max = max(set(filter(lambda l: (l[1], l[0]) == (loc[1], loc[0]), all_coors)), key=lambda l: l[2])[2]

        for ele, boundary in zip(loc, [(x_min, x_max), (y_min, y_max), (z_min, z_max)]):
            if ele < boundary[0] or ele > boundary[1]:
                return False
        return True
    except:
        return False


def find_surface_areas(
    cube_coors: set[tuple], all_coors: set[tuple] = None, check_holes: bool = True, internal_mode=False
) -> (list[tuple], list[tuple]):

    surface_area = 0
    internal_cubes = set()
    if all_coors is None:
        all_coors = cube_coors

    for cube in cube_coors:
        cube_neighbours = get_neighbours(cube)

        if internal_mode:
            sides = len(set(cube_neighbours).intersection(all_coors))
        else:
            sides = 6
            sides -= len(set(cube_neighbours).intersection(all_coors))

        surface_area += sides

        if check_holes:
            found_spaces = set(cube_neighbours).difference(cube_coors)
            for ele in found_spaces:
                if is_inside(ele, cube_coors):
                    internal_cubes.add(ele)
    return surface_area, internal_cubes


def plot_data(coors, z=5):
    filtered_coors = list(filter(lambda x: x[2] == z, coors))
    data = np.array(filtered_coors).T
    return data


def plot_slice(coors, hole_coors, z=5):
    fig, ax = plt.subplots()
    x, y, _ = plot_data(coors, z=z)
    ax.scatter(x, y, c="silver", marker="s", s=100.0)
    x_holes, y_holes, _ = plot_data(hole_coors, z=z)
    ax.scatter(x_holes, y_holes, c="lightcoral", marker="s", s=100.0)

    minor_locator = MultipleLocator(1)
    ax.yaxis.set_major_locator(minor_locator)
    ax.xaxis.set_major_locator(minor_locator)
    ax.grid()
    ax.set_title(f"{z=}")


coors_ = parse_file(read_file(FILE_PATH))
surface_areas, internal_holes = find_surface_areas(coors_)
print(surface_areas)  # part 1

surface_areas_internal, _ = find_surface_areas(internal_holes, coors_, check_holes=False, internal_mode=True)
print(f"Net SA: {surface_areas - surface_areas_internal}")  # part 2
plot_slice(coors_, internal_holes, z=14)
plt.show()
