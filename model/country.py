import json

from model.exceptions import OneSegmentBorderException
from model.segment import Segment


class Country:
    def __init__(self, country_pieces):
        self._country_pieces = country_pieces
        self.color = None
        self._hard_set_color = False
        self.incident_countries = set()
        self.area = self.calc_area()

    @property
    def pieces(self):
        yield from self._country_pieces

    @property
    def hard_colored(self):
        return self._hard_set_color

    @property
    def segments(self):
        for piece in self._country_pieces:
            for segment in piece.segments_set:
                yield segment

    @property
    def points(self):
        for piece in self._country_pieces:
            yield from piece.points

    @classmethod
    def from_json(cls, json_obj):
        return cls([CountryPiece(points) for points in json_obj])

    def add_piece(self, piece):
        self._country_pieces.append(piece)
        self.area = self.calc_area()

    def calc_area(self):
        return sum((cp.area for cp in self._country_pieces))

    def set_color(self, color):
        self.color = color
        self._hard_set_color = True

    def is_neighbour(self, country):
        return country in self.incident_countries

    def add_incident(self, other_country):
        self.incident_countries.add(other_country)
        other_country.incident_countries.add(self)

    def __contains__(self, item):
        for piece in self._country_pieces:
            if item in piece:
                return True
        return False

    def __str__(self):
        return '{} {}'.format(self.color,
                              '\n'.join(map(str, self._country_pieces)))


class CountryPiece:
    def __init__(self, points):
        if len(points) <= 2:
            raise OneSegmentBorderException(*points)
        self.points = points
        self.segments_set = {Segment(points[i], points[(i + 1) % len(points)])
                             for i in range(len(points))}
        self.area = self._calc_area()

    def _calc_area(self):
        area = 0
        for i in range(len(self.points)):
            area += ((self.points[i - 1][0] * self.points[i][1]) -
                     (self.points[i - 1][1] * self.points[i][0]))
        return abs(area / 2)

    def __str__(self):
        return ' | '.join(map(str, self.points))

    def __contains__(self, item):
        return item in self.segments_set
