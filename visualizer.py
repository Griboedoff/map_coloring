import random
import sys

from country import Country
from map import Map

try:
    from PyQt5 import QtGui, QtWidgets, QtCore
except Exception as e:
    print('PyQt5 not found: "{}"'.format(e),
          file=sys.stderr)
    sys.exit(1)


class Vizualizer(QtWidgets.QWidget):
    def __init__(self, map: Map):
        super(Vizualizer, self).__init__()
        self.map = map
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 700, 700)
        self.show()

    def mousePressEvent(self, QMouseEvent):
        self.repaint()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self._draw_countries(painter)
        painter.end()

    def _draw_countries(self, painter):
        for country in self.map.countries:
            self._draw_country(painter, country)

    def _draw_country(self, painter: QtGui.QPainter, country):
        painter.setBrush(self._get_qt_color(country.color))
        painter.drawPolygon(self._get_polygon(country))

    @staticmethod
    def _get_qt_color(color):
        return QtGui.QColor(random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255))

    @staticmethod
    def _get_polygon(country: Country):
        points = [QtCore.QPoint(*x) for x in country.points]
        return QtGui.QPolygon(points)
