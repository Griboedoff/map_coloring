import argparse
import sys

from PyQt5 import QtWidgets

from GUI.visualizer import Visualizer
from editor.editor_window import EditorWindow
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
    parser.add_argument('--encoding', type=str, default='utf8',
                        help='Encoding for files')
    parser.add_argument('-e', '--editor', action='store_true',
                        help='Run map editor')
    return parser.parse_args()


if __name__ == '__main__':
    parser = create_parser()
    app = QtWidgets.QApplication(sys.argv)
    if parser.editor:
        editor = EditorWindow()
    else:
        try:
            loaded_map = Map.from_file(parser.map, parser.encoding)
        except IOError as e:
            print("error loading {} file\n{}".format(parser.map, e))
            exit(1)
        viz = Visualizer(loaded_map, Palette.from_json(parser.palette))

    sys.exit(app.exec_())
