import argparse
import sys

from PyQt5 import QtWidgets

from model.map import Map
from visualizer import Vizualizer


def create_parser():
    """Argument parse"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--map', type=str,
                        help='Map file')
    parser.add_argument("-p", '--paints', type=str,
                        help='Paints config file')
    parser.add_argument('-e', '--encoding', type=str, default='utf8',
                        help='Encoding for files')
    return parser.parse_args()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    map1 = Map.from_file('maps/very_big_map.json', 'utf8')
    # map1 = Map.from_file('maps/test_map.json', 'utf8')

    viz = Vizualizer(map1)

    sys.exit(app.exec_())
