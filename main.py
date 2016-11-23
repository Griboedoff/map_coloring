import sys

from PyQt5 import QtWidgets

from map import Map
from visualizer import Vizualizer

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    map1 = Map.from_file('test_map.json', 'utf8')
    viz = Vizualizer(map1)

    sys.exit(app.exec_())
