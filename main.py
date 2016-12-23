import argparse
import sys

from PyQt5 import QtWidgets

from GUI.visualizer import Vizualizer
from model.map import Map
from model.palette import Palette


def create_parser():
    """Argument parse"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--map', type=str,
                        default='maps/very_big_map.json',
                        help='Map file')
    parser.add_argument("-p", '--palette', type=str, default='palette.json',
                        help='Palette config file')
    parser.add_argument('-e', '--encoding', type=str, default='utf8',
                        help='Encoding for files')
    return parser.parse_args()


if __name__ == '__main__':
    parser = create_parser()
    app = QtWidgets.QApplication(sys.argv)
    map1 = Map.from_file(parser.map, parser.encoding)
    # map1 = Map.from_file('maps/test_map.json', 'utf8')

    viz = Vizualizer(map1, Palette.from_json(parser.palette))

    sys.exit(app.exec_())
