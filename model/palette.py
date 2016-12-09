from model.exceptions import NotEnoughColorsInPalette


class Palette:
    def __init__(self, colors_dict):
        self.colors_dict = colors_dict

    def get_n_cheapest_color(self, n):
        if n > len(self.colors_dict):
            raise NotEnoughColorsInPalette(n, len(self.colors_dict))

        return sorted(self.colors_dict.items(), key=lambda x: x[1])[:n]

    def __len__(self):
        return len(self.colors_dict)

    @classmethod
    def from_json(cls, json):
        return cls({Palette._parse_tuple_from_str(k): v for (k, v) in json})

    @staticmethod
    def _parse_tuple_from_str(string):
        return tuple(map(int, string.split(' ')))
