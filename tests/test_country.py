import os
import sys
from unittest import TestCase, main

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from model.country import Country


class TestCountry(TestCase):
    def setUp(self):
        self.c1 = Country.from_json([[[0, 0], [200, 200], [100, 300]]])
        self.c2 = Country.from_json([[[0, 0], [200, 0], [200, 200]]])

    def test_hard_colored(self):
        self.c1.set_color(1)
        self.assertTrue(self.c1.hard_colored)
        self.assertEqual(self.c1.color, 1)


if __name__ == '__main__':
    main()
