import json

from model.exceptions import NotEnoughColorsInPalette


class Palette:
    def __init__(self, colors_dict):
        self.colors_dict = colors_dict

    def get_n_cheapest_color(self, n):
        if n > len(self.colors_dict):
            raise NotEnoughColorsInPalette(n, len(self.colors_dict))

        items = self.colors_dict.items()
        return sorted(items, key=lambda x: x[1][0])[:n]

    def __len__(self):
        return len(self.colors_dict)

    @classmethod
    def from_json(cls, file):
        with open(file, 'r') as f:
            parsed_json = json.loads(f.read())
        return cls(
            {Palette._parse_tuple_from_str(k): Palette.build_color_info(v)
             for (k, v) in parsed_json.items()})

    @staticmethod
    def build_color_info(d):
        return d["price"], d['name']

    @staticmethod
    def _parse_tuple_from_str(string):
        return tuple(map(int, string.split(' ')))
