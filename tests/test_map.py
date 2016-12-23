import os
import sys
from unittest import TestCase, main

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from model.country import Country
from model.map import Map



class TestMap(TestCase):
    def setUp(self):
        self.c1 = Country.from_json([[[0, 0], [200, 200], [100, 300]]])
        self.c2 = Country.from_json([[[0, 0], [200, 0], [200, 200]]])

        self.c3 = Country.from_json([[[0, 0], [0, 300], [100, 300]]])
        self.c4 = Country.from_json([[[200, 200], [100, 300], [500, 500]]])
        self.c_map = Map([self.c1, self.c2, self.c3, self.c4])

    def test_calc_incident_countries(self):
        self.c_map.calc_incident_countries()
        self.assertTrue(self.c2.is_neighbour(self.c1))
        self.assertTrue(self.c4.is_neighbour(self.c1))

    def test_set_sizes(self):
        self.assertTrue(self.c_map.width, 500)
        self.assertTrue(self.c_map.height, 500)


if __name__ == '__main__':
    main()
