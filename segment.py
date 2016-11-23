import math


class Segment:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __len__(self):
        return math.sqrt(math.pow(self.start[0] - self.end[0], 2) +
                         math.pow(self.start[1] - self.end[1], 2))

    def __hash__(self):
        return int(hash(self.start) * 397) ** hash(self.end)

    @classmethod
    def from_list(cls, l):
        return cls(tuple(l[0]), tuple(l[1]))
