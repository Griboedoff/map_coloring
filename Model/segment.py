import math


class Segment:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @classmethod
    def from_list(cls, l):
        return cls(tuple(l[0]), tuple(l[1]))

    def to_json(self):
        return '[{}, {}]'.format(self.start, self.end)

    def __len__(self):
        return math.sqrt(math.pow(self.start[0] - self.end[0], 2) +
                         math.pow(self.start[1] - self.end[1], 2))

    def __str__(self):
        return "{} {}".format(self.start, self.end)

    def __eq__(self, other):
        if isinstance(other, Segment):
            return (other.start == self.start and other.end == self.end or
                    other.start == self.end and other.end == self.start)
        return False

    def __hash__(self):
        return int((self.start[0] * 397) ** self.start[1] +
                   (self.end[0] * 397) ** self.end[1])
