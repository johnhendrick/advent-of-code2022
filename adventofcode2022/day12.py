import heapq as hq
from collections import defaultdict
from adventofcode2022 import read_file

FILE_PATH = "./input/day12.csv"


def parse_file(file_content) -> list:
    str_content = file_content.replace("S", "a").replace("E", "{")
    rows = [list(row) for row in str_content.split("\n")]
    return rows


class Graph:
    def __init__(self):
        self.edges: dict[tuple, list[tuple]] = defaultdict(list)

    def neighbors(self, id: tuple) -> list[tuple]:
        return self.edges[id]

    def run_dijkstra(self, start: tuple, goal: tuple):
        queue = []
        hq.heapify(queue)
        hq.heappush(queue, (0, start))
        came_from, costs = {}, {}
        came_from[start] = None
        costs[start] = 0

        while len(queue) != 0:
            current = hq.heappop(queue)[1]
            if current == goal:  # early exit
                break

            for next_ in self.edges[current]:
                new_cost = costs[current] + 1.0  # uniform weight

                if next_ not in costs or new_cost < costs[next_]:
                    costs[next_] = new_cost
                    hq.heappush(queue, (new_cost, next_))
                    came_from[next_] = current
        return came_from, costs[goal]


def build_graph(height_map: list[list]) -> dict:
    graph = Graph()
    shape = len(height_map), len(height_map[0])  # row, col
    for i, row in enumerate(height_map):
        for j, char in enumerate(row):
            graph.edges[(i, j)] = get_edges(i, j, shape)  # all edges

    for node_loc, edge_locs in graph.edges.items():  # prune edges
        pruned_edges = []
        node_char = height_map[node_loc[0]][node_loc[1]]
        for edge_loc in edge_locs:
            char = height_map[edge_loc[0]][edge_loc[1]]

            if ord(char) - ord(node_char) < 2:
                pruned_edges.append(edge_loc)

        graph.edges[node_loc] = pruned_edges  # update
    return graph


def get_edges(row, col, shape):
    up = (row - 1, col) if row - 1 >= 0 else None
    down = (row + 1, col) if row + 1 <= shape[0] - 1 else None
    left = (row, col - 1) if col - 1 >= 0 else None
    right = (row, col + 1) if col + 1 <= shape[1] - 1 else None
    edges = []
    for ele in [up, down, left, right]:
        if ele:
            edges.append(ele)
    return edges


height_map = parse_file(read_file(FILE_PATH))
graph = build_graph(height_map)
_, steps = graph.run_dijkstra((20, 0), (20, 46))  # (0,0) (2,5) # (20,0) (20,46)
print(steps)

# part2
def get_low_positions(height_map: list[list]) -> list[tuple]:
    positions = []
    for i, row in enumerate(height_map):
        for j, col in enumerate(row):
            if col == "a":
                positions.append((i, j))
    return positions


all_dist = []
low_positions = get_low_positions(height_map)
for low_pos in low_positions:
    try:
        _, steps = graph.run_dijkstra(low_pos, (20, 46))
        all_dist.append(steps)
    except:
        pass

print(min(all_dist))
