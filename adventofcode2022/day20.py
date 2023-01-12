from adventofcode2022 import read_file

FILE_PATH = "./input/day20.csv"


def parse_file(file_content: str) -> list:
    return tuple(int(row) for row in file_content.split("\n"))


class CircularQueue:
    def __init__(self, seq: tuple, multiplier=1):
        self.sequence = [(item * multiplier, i) for i, item in enumerate(seq)]  # value, original pos
        self.max = len(seq)
        self.ops = self.sequence.copy()
        self.zero = (0, seq.index(0))

    def move(self, item: tuple):
        loc = self.sequence.index(item)
        item_ = self.sequence.pop(loc)
        new_pos = (loc + item_[0]) % (self.max - 1)

        if new_pos == 0:
            self.sequence.append(item_)
        else:
            self.sequence.insert(new_pos, item_)

    def run(self, rounds=1):
        for _ in range(rounds):
            for ele in self.ops:
                if ele[0] != 0:
                    self.move(ele)
        self.get_val()

    def get_val(self, val=0):
        for num in [1000, 2000, 3000]:
            index_ = (num + self.sequence.index(self.zero)) % self.max
            val += self.sequence[index_][0]
        print(val)


sequence = parse_file(read_file(FILE_PATH))
seq = CircularQueue(sequence)
seq.run()  # part 1

seq2 = CircularQueue(sequence, multiplier=811589153)
seq2.run(rounds=10)  # # part 2
