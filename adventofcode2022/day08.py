from adventofcode2022 import read_file


def parse_file(file_content) -> list:
    rows = file_content.split("\n")
    rows = [[int(ele) for ele in _row] for _row in rows]
    return rows


def check_edge(coor: tuple, shape: tuple) -> bool:
    if 0 in coor or coor[0] == shape[0] - 1 or coor[1] == shape[1] - 1:
        return True
    else:
        return False


def check_visible(look_out: list) -> bool:
    # trees are visible to the edge of map
    visibility = [look_out[0] > ele for ele in look_out[1:]]
    return all(visibility)


def count_visible_trees(look_out: list) -> int:
    tree, remaining = look_out[0], look_out[1:]
    count = 0

    for ele in remaining:
        count += 1
        if ele >= tree:
            break
    return count


def count_visible(tree_map: list[list]) -> tuple:
    shape = (len(tree_map), len(tree_map[0]))
    count_visible, scenic_scores = 0, []

    for i in range(shape[0]):
        for j in range(shape[1]):
            if check_edge((i, j), shape):
                count_visible += 1
            else:
                up = [row[j] for row in tree_map[: i + 1]][::-1]
                down = [row[j] for row in tree_map[i:]]
                left = tree_map[i][: j + 1][::-1]
                right = tree_map[i][j:]

                up_visible = check_visible(up)
                down_visible = check_visible(down)
                left_visible = check_visible(left)
                right_visible = check_visible(right)

                if any([up_visible, down_visible, left_visible, right_visible]):
                    count_visible += 1

                up_score = count_visible_trees(up)
                down_score = count_visible_trees(down)
                left_score = count_visible_trees(left)
                right_score = count_visible_trees(right)
                scenic_scores.append(up_score * down_score * left_score * right_score)

    return count_visible, max(scenic_scores)


FILE_PATH = "./input/day08.csv"
tree_map = parse_file(read_file(FILE_PATH))
print(count_visible(tree_map))
