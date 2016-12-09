from model.map import Map
from model.palette import Palette


class Colorer:
    def __init__(self, countries_map: Map, palette: Palette):
        self.palette = palette
        self.countries_map = countries_map
        self.colors_count = 0
        self.colors_match = {}

    def color_map(self):
        for country in self.countries_map.countries:
            neigh_color = {c.color for c in country.incident_countries}
            country.color = self.select_color(neigh_color)
        self.colors_match = {
            i[1]: i[0][0] for i in
            zip(self.palette.get_n_cheapest_color(self.colors_count + 1),
                range(self.colors_count + 1))}

    def select_color(self, neigh_color):
        for color_index in range(0, self.colors_count + 1):
            if color_index not in neigh_color:
                return color_index
        self.colors_count += 1
        return self.colors_count
