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
            parsed_json = json.loads(f.read(), encoding=encoding)
        return cls([Country.from_json(segments) for segments in parsed_json])

    def calc_incident_countries(self):
        checked = set()
        for country in self.countries:
            for seg in country.segments:
                if seg not in checked:
                    for other_country in self.countries:
                        if other_country != country and seg in other_country:
                            country.add_incident(other_country)
                checked.add(seg)

    def set_sizes(self):
        max_w = 0
        max_h = 0
        for country in self.countries:
            for point in country.points:
                if point[0] > max_w:
                    max_w = point[0]
                if point[1] > max_h:
                    max_h = point[1]
        self.width = max_w
        self.height = max_h
