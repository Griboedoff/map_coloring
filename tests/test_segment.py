import os
import sys
from unittest import TestCase, main

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from model.segment import Segment



class TestSegment(TestCase):
    def test_to_json(self):
        s = Segment((10, 0), (20, 0))
        self.assertEqual(s.to_json(), "[[10, 0], [20, 0]]")

    def test_equals(self):
        s1 = Segment((10, 0), (20, 0))
        s2 = Segment((20, 0), (10, 0))
        self.assertTrue(s1 == s2)


if __name__ == '__main__':
    main()
