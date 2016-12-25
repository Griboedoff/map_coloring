import json


class Segment:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @classmethod
    def from_list(cls, l):
        return cls(tuple(l[0]), tuple(l[1]))

    def to_json(self):
        return json.dumps([self.start, self.end])

    def __str__(self):
        return "{} {}".format(self.start, self.end)

    def __eq__(self, other):
        if isinstance(other, Segment):
            return sorted([self.start, self.end]) == sorted(
                [other.start, other.end])
        return False

    def __hash__(self):
        return int((self.start[0] * 397) ** self.start[1] +
                   (self.end[0] * 397) ** self.end[1])
