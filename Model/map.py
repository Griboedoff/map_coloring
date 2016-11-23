import json

from typing import List

from Model.country import Country
from Model.segment import Segment


class Map:
    def __init__(self, countries):
        self.countries = countries  # type: List[Country]

    @classmethod
    def from_file(cls, file, encoding):
        with open(file, 'r', encoding=encoding) as f:
            parsed_json = json.loads(f.read(), encoding=encoding)
        return cls([Country([Segment.from_list(x) for x in segments])
                    for segments in parsed_json])

    def calc_incident_countries(self):
        checked = set()
        for country in self.countries:
            for seg in country.segments:
                if seg not in checked:
                    for inc_country in self.countries:
                        if inc_country != country and seg in inc_country:
                            country.incident_countries.add(inc_country)
                            inc_country.incident_countries.add(country)
                checked.add(seg)
