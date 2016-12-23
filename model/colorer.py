from model.map import Map
from model.palette import Palette


class Colorer:
    def __init__(self, countries_map: Map, palette: Palette):
        self.palette = palette
        self.countries_map = countries_map
        self.colors_count = 0
        self.colors_match = {}
        self.total_cost = 0
        self.min_cost = None

    def color_name(self, color):
        return self.palette.colors_dict[color][1]

    def get_color_cost(self, color):
        return self.palette.colors_dict[self.colors_match[color]][0]

    def color_map(self):
        for country in sorted(filter(
                lambda c: not c.hard_colored, self.countries_map.countries),
                key=lambda x: any(filter(lambda y: y.hard_colored,
                                         x.incident_countries))):
            neigh_color = {self._select_color(c) for c in
                           country.incident_countries}
            country.color = self.select_color(neigh_color)
        self.colors_match = {
            color_num: color_def[0]
            for color_def, color_num in
            zip(self.palette.get_n_cheapest_color(self.colors_count + 1),
                range(self.colors_count + 1))}
        self.count_cost()

    @staticmethod
    def _select_color(c):
        return c.color if (c.hard_colored or c.color is not None) else -1

    def count_cost(self):
        self.total_cost = sum(map(
            lambda c: c.area * self.get_color_cost(c.color),
            self.countries_map.countries))
        if not self.min_cost:
            self.min_cost = self.total_cost
        self.min_cost = min(self.min_cost, self.total_cost)

    def select_color(self, neigh_color):
        max_color_index = max(max(neigh_color), self.colors_count) + 1
        for color_index in range(0, max_color_index):
            if color_index not in neigh_color:
                return color_index
        self.colors_count += 1
        return self.colors_count
