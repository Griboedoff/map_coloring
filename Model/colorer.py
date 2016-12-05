from model.map import Map


class Colorer:
    def __init__(self, countries_map: Map, ):
        self.countries_map = countries_map
        self.colors_count = 1

    def color_map(self):
        for country in self.countries_map.countries:
            neigh_color = {c.color for c in country.incident_countries}
            country.color = self.select_color(neigh_color)

    def select_color(self, neigh_color):
        for color_index in range(1, self.colors_count + 1):
            if color_index not in neigh_color:
                return color_index
        self.colors_count += 1
        return self.colors_count
