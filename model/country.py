from model.exceptions import OneSegmentBorderException
from model.segment import Segment


class Country:
    def __init__(self, country_pieces):
        self.country_pieces = country_pieces
        self.color = None
        self.incident_countries = set()
        self.area = sum((cp.area for cp in self.country_pieces))

    @property
    def segments(self):
        for piece in self.country_pieces:
            for segment in piece.segments_set:
                yield segment

    @property
    def points(self):
        for piece in self.country_pieces:
            yield from piece.points

    @classmethod
    def from_json(cls, json):
        return cls([CountryPiece(points) for points in json])

    def is_neighbour(self, country):
        return country in self.incident_countries

    def has_one_border_with(self, border_segment):
        for piece in self.country_pieces:
            if border_segment in piece.segments:
                return True
        return False

    def add_incident(self, other_country):
        self.incident_countries.add(other_country)
        other_country.incident_countries.add(self)

    def to_json(self):
        return '[{}]'.format(', '.join(map(lambda x: x.to_json,
                                           self.country_pieces)))

    def __contains__(self, item):
        for piece in self.country_pieces:
            if item in piece:
                return True
        return False

    def __str__(self):
        return '\n'.join(map(str, self.country_pieces))


class CountryPiece:
    def __init__(self, points):
        if len(points) <= 2:
            raise OneSegmentBorderException(*points)
        self.points = points
        self.segments_set = {Segment(points[i], points[(i + 1) % len(points)])
                             for i in range(len(points))}
        self.area = self._calc_area()

    def to_json(self):
        return '[{}]'.format(', '.join(map(lambda x: '{}{}'.format(*x),
                                           self.points)))

    def _calc_area(self):
        area = 0
        j = len(self.points) - 1
        for i in range(len(self.points)):
            area += ((self.points[j][1] + self.points[i][1]) *
                     (self.points[j][0] - self.points[i][0]))
        return abs(area / 2)

    def __str__(self):
        return ' | '.join(map(str, self.points))

    def __contains__(self, item):
        return item in self.segments_set
