import json

from typing import List

from model.country import Country


class Map:
    def __init__(self, countries):
        self.countries = countries  # type: List[Country]
        self.size = (0, 0)
        self.set_sizes()

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @classmethod
    def from_file(cls, file, encoding):
        with open(file, 'r', encoding=encoding) as f:
            parsed_json = json.load(f, encoding=encoding)
        return cls([Country.from_json(segments) for segments in parsed_json])

    def to_json(self):
        return json.dumps([[[point for point in piece.points]
                            for piece in country.pieces]
                           for country in self.countries])

    def calc_incident_countries(self):
        checked = set()
        for country in self.countries:
            for seg in filter(lambda s: s not in checked, country.segments):
                for other_country in filter(
                        lambda c: c != country and seg in c, self.countries):
                    country.add_incident(other_country)
                checked.add(seg)

    def set_sizes(self):
        max_w = 0
        max_h = 0
        for country in self.countries:
            max_w = max(max_w, max(x for (x, _) in country.points))
            max_h = max(max_h, max(y for (_, y) in country.points))
        self.size = (max_w, max_h)
