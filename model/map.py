import json

from typing import List

from model.country import Country


class Map:
    def __init__(self, countries):
        self.countries = countries  # type: List[Country]
        self.set_sizes()

    @classmethod
    def from_file(cls, file, encoding):
        with open(file, 'r', encoding=encoding) as f:
            parsed_json = json.load(f, encoding=encoding)
        return cls([Country.from_json(segments) for segments in parsed_json])

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
        self.width = max_w
        self.height = max_h
