import re
from dataclasses import dataclass, field
from collections import deque
from tqdm import tqdm

from adventofcode2022 import read_file
import math

from itertools import combinations, chain, permutations

FILE_PATH = "./input/day16.csv"


def parse_file(file_content: str) -> list:
    re_ = r"Valve (.*) has flow rate=(.*); .* valves? (.*)"
    rows = [list(re.findall(re_, row)[0]) for row in file_content.split("\n")]
    return {ele[0]: Valve(ele[0], int(ele[1]), ele[2].split(", ")) for ele in rows}


@dataclass(order=True)
class Valve:
    id: str
    flow_rate: int
    link: list = field(default_factory=list)
    opened: bool = False

    def __post_init__(self):
        object.__setattr__(self, "sort_index", self.flow_rate)


def memoize(func):
    data = {}

    def _memoize(*args, **kwargs):
        if args in data:
            return data[args]
        else:
            result = func(*args, **kwargs)
            data[args] = result
            return result

    return _memoize


class ValveGraph:
    def __init__(self, valves_info, start="AA", time=30, constant=2, verbose=False):
        self.edges: dict[Valve] = valves_info
        self.viable_edges: list[str] = self.get_viable_edges()
        self.curr: Valve = valves_info[start]
        self.curr_elephant: Valve = valves_info[start]
        self.total_flow = 0
        self.time = time
        self.time_elephant = time
        self.constant = constant
        self.verbose = verbose

    def get_viable_edges(self, edges_scope=None):
        viable_edges = [k for k, v in self.edges.items() if v.flow_rate > 0 and not v.opened]
        if edges_scope:
            viable_edges = [id_ for id_ in edges_scope if id_ in viable_edges]
        return viable_edges

    def print_(self, text):
        if self.verbose:
            print(text)

    @memoize
    def _run_bfs(self, current, time, edges_scope, early_exit=None):
        return

    def run_bfs(self, current, time, edges_scope, early_exit=None):
        self.update_flow_rate()

        queue = deque()
        queue.appendleft(current)

        costs = {}
        costs[current.id] = [0, 0]  # (time_cost, potential_flow, opp_cost)

        while queue:
            current = queue.popleft()
            if early_exit and current.id == early_exit:
                break

            for next_ in current.link:
                new_cost = costs[current.id][0] + 1

                if next_ not in costs or new_cost < costs[next_][0]:
                    potential_flow = (time - new_cost - 1) * self.edges[next_].flow_rate
                    costs[next_] = [new_cost, potential_flow]
                    queue.append(self.edges[next_])

        for valve_id in costs.keys():  # calculate opp costs
            if valve_id in self.viable_edges:
                all_other_keys = [
                    costs[valve_][1] / ((costs[valve_][0]) ** self.constant)
                    for valve_ in costs.keys()
                    if valve_ != valve_id and valve_ in self.viable_edges
                ]
                opp_cost = sum(all_other_keys)
                costs[valve_id].append(opp_cost)

        return {k: v for k, v in costs.items() if k in self.viable_edges}

    def update_flow_rate(self):
        self.print_(f"t={self.time}, flow_rate={self.total_flow}")

    def move(self, curr_ref, edges_scope, enforce_target_valve=None):

        if curr_ref == "curr":
            time_var = "time"
        elif curr_ref == "curr_elephant":
            time_var = "time_elephant"
        # if self.time > 0:
        if getattr(self, time_var) > 0:
            costs_info = self.run_bfs(
                current=getattr(self, curr_ref),
                time=getattr(self, time_var),
                edges_scope=edges_scope,
                early_exit=enforce_target_valve,
            )
            if enforce_target_valve:
                best_valve = enforce_target_valve
            else:
                opp_cost_info = {k: v[2] for k, v in costs_info.items()}
                best_valve = min(opp_cost_info, key=opp_cost_info.get)

            self.print_(f"{curr_ref} move and open {best_valve}")

            setattr(self, time_var, getattr(self, time_var) - costs_info.get(best_valve)[0] - 1)
            setattr(self, curr_ref, self.edges[best_valve])
            setattr(getattr(self, curr_ref), "opened", True)
            self.total_flow += costs_info[best_valve][1]

            self.viable_edges = self.get_viable_edges(edges_scope=edges_scope)

        else:
            self.print_("Time is up!")

    def simulate(self, curr_ref, edges_scope=None, brute_force=False):
        if curr_ref == "curr":
            time_var = "time"
        elif curr_ref == "curr_elephant":
            time_var = "time_elephant"

        self.viable_edges = self.get_viable_edges(edges_scope=edges_scope)
        if brute_force:
            while getattr(self, time_var) > 0 and len(self.viable_edges) > 0:
                for next_valve in edges_scope:
                    self.move(curr_ref=curr_ref, edges_scope=edges_scope, enforce_target_valve=next_valve)
        else:
            while getattr(self, time_var) > 0 and len(self.viable_edges) > 0:
                self.move(curr_ref=curr_ref, edges_scope=edges_scope)

    def simulate_with_elephant(self, person_elephant_paths: list[list]):
        self.simulate("curr", person_elephant_paths[0], brute_force=True)

        self.simulate("curr_elephant", person_elephant_paths[1], brute_force=True)
        self.print_(f"{person_elephant_paths} gives {self.total_flow}")
        return self.total_flow


file_content = read_file(FILE_PATH)
valves_info = parse_file(file_content)
graph = ValveGraph(valves_info=parse_file(read_file(FILE_PATH)))
graph.simulate("curr")
print(graph.total_flow)

# part 2
valves_info = parse_file(file_content)
non_zero_valves = [k for k, valve in valves_info.items() if valve.flow_rate > 0]

split_combination = []
# https://stackoverflow.com/questions/44730234/generate-all-possible-splits-of-a-list-in-python
subsets = [v for a in range(len(non_zero_valves)) for v in combinations(non_zero_valves, a)]
for i in range(1, len(subsets) // 2 + 1):
    split_combination.append([list(chain(subsets[i])), [e for e in non_zero_valves if e not in subsets[i]]])

total_flow_highest = 0

graph2 = ValveGraph(valves_info=parse_file(file_content), time=26, verbose=True)
# total_flow_ = graph2.simulate_with_elephant([["JJ", "BB", "CC"], ["DD", "HH", "EE"]])
# if total_flow_ > total_flow_highest:
#     total_flow_highest = total_flow_
#     print(total_flow_highest)

for split in split_combination:
    for visit_order_person in permutations(split[0]):
        for visit_order_elephant in permutations(split[1]):
            graph2 = ValveGraph(valves_info=parse_file(file_content), time=26)

            total_flow_ = graph2.simulate_with_elephant([visit_order_person, visit_order_elephant])
            if total_flow_ > total_flow_highest:
                total_flow_highest = total_flow_
                print(total_flow_highest)


print(total_flow_highest)
