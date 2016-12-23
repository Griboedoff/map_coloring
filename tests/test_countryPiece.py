import os
import sys
from unittest import TestCase, main

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from model.country import CountryPiece



class TestCountryPiece(TestCase):
    def setUp(self):
        self.non_convex_piece = CountryPiece(
            [(0, 0), (0, 2), (1, 1), (2, 2), (2, 0)])
        self.convex_piece = CountryPiece([(0, 0), (0, 2), (2, 2), (2, 0)])

    def test_to_json(self):
        self.assertEqual("[[0, 0], [0, 2], [1, 1], [2, 2], [2, 0]]",
                         self.non_convex_piece.to_json())

    def test__calc_area(self):
        self.assertEqual(3, self.non_convex_piece._calc_area())
        self.assertEqual(4, self.convex_piece._calc_area())


if __name__ == '__main__':
    main()
