import re
import math

from adventofcode2022 import read_file

FILE_PATH = "./input/day11.csv"


def parse_file(file_content) -> list:
    rows = [row.split("\n") for row in file_content.split("\n\n")]
    notes = []
    for note in rows:
        for i in range(len(note)):
            if i != 2:
                note[i] = [int(ele) for ele in re.findall(r"\d+", note[i])]
                note[i] = note[i][0] if len(note[i]) == 1 and i != 1 else note[i]
            else:
                note[i] = note[i][19:]
        notes.append(note)
    return notes


class Monkey:
    def __init__(
        self,
        items: list = None,
        operation: str = "",
        divide: int = 1,
        true_action: int = 1,
        false_action: int = 1,
        worry_factor: float = 1 / 3,
        lcm: int = 1,
    ):
        self.items = items
        self.inspect_count = 0
        self.operation = operation
        self.divide = divide
        self.target = {True: true_action, False: false_action}  # monkey id
        self.worry_factor = worry_factor
        self.lcm = lcm

    def _inspect(self, item) -> tuple[bool, int]:
        self.inspect_count += 1

        old = item  # eval()
        new = math.floor(eval(self.operation) * self.worry_factor) % self.lcm
        if new % self.divide == 0:
            return True, new
        else:
            return False, new

    def throw(self, verbose=False) -> int:
        item = self.items.pop(0)
        inspect_bool, new = self._inspect(item)
        target_monke = self.target[inspect_bool]

        if verbose:
            print(f"Throwing {new} to {target_monke}")
        return target_monke, new

    def receive(self, item: int):
        self.items.append(item)


def get_prime_lcm(notes, num=1):
    primes = [note[3] for note in notes]
    for prime in primes:
        num *= prime
    return num


def simulate(rounds=1, worry_factor=1 / 3):
    notes = parse_file(read_file(FILE_PATH))
    lcm = get_prime_lcm(notes)
    all_monke = {_monke[0]: Monkey(*_monke[1:], worry_factor, lcm) for _monke in notes}

    for _ in range(rounds):
        for monke_index in range(len(all_monke)):
            # items in Monkey
            monke = all_monke[monke_index]
            n_items = len(monke.items)

            for _ in range(n_items):
                receiver, new_item = monke.throw()
                all_monke[receiver].receive(new_item)
    return all_monke


def get_score(dict_of_monkes: dict[int, Monkey]) -> None:
    active_monkeys = []

    for _, monke in dict_of_monkes.items():
        active_monkeys.append(monke.inspect_count)

    active_monkeys.sort(reverse=True)
    print(active_monkeys[0] * active_monkeys[1])


get_score(simulate(rounds=20))  # part 1
get_score(simulate(rounds=10000, worry_factor=1))  # part 2
