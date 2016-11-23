import json

from segment import Segment
from country import Country


class Map:
    def __init__(self, countries):
        self.countries = countries

    @classmethod
    def from_file(cls, file, encoding):
        with open(file, 'r', encoding=encoding) as f:
            parsed_json = json.loads(f.read(), encoding=encoding)
        return cls([Country([Segment.from_list(x) for x in segments])
                    for segments in parsed_json])
