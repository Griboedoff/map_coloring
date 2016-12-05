import sys

from PyQt5 import QtWidgets

from Model.map import Map
from visualizer import Vizualizer

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    map1 = Map.from_file('maps/very_big_map.json', 'utf8')
    viz = Vizualizer(map1)

    sys.exit(app.exec_())
