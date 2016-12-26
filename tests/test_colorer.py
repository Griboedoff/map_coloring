import os
import sys
from unittest import TestCase, main


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from model.colorer import Colorer
from model.map import Map
from model.palette import Palette


class TestColorer(TestCase):
    def setUp(self):
        self.two_colors_map = Map.from_file("./test_maps/2color.json")
        self.four_colors_map = Map.from_file("./test_maps/4color.json")
        self.piece_country_map = Map.from_file(
            "./test_maps/2country_with_pieces.json")
        self.two_colors_map.calc_incident_countries()
        self.piece_country_map.calc_incident_countries()
        self.four_colors_map.calc_incident_countries()
        self.palette = Palette.from_json('palette.json')

    def test_two_color_map(self):
        colorer = Colorer(self.two_colors_map, self.palette)
        colorer.color_map()
        self.assertEqual(colorer.colors_count, 2 - 1)

    def test_four_color_map(self):
        colorer = Colorer(self.four_colors_map, self.palette)
        colorer.color_map()
        self.assertEqual(colorer.colors_count, 4 - 1)

    def test_pieces_map(self):
        colorer = Colorer(self.piece_country_map, self.palette)
        colorer.color_map()
        self.assertEqual(colorer.colors_count, 2 - 1)


if __name__ == '__main__':
    main()
