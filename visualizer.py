import sys

from Model.colorer import Colorer
from Model.country import Country
from Model.map import Map

try:
    from PyQt5 import QtGui, QtWidgets, QtCore
except Exception as e:
    print('PyQt5 not found: "{}"'.format(e),
          file=sys.stderr)
    sys.exit(1)


class Vizualizer(QtWidgets.QWidget):
    def __init__(self, countries_map: Map):
        super(Vizualizer, self).__init__()
        countries_map.calc_incident_countries()
        self.colorer = Colorer(countries_map)
        self.colorer.color_map()
        self.map = self.colorer.countries_map

        self.color_set = [QtGui.QColor(255, 0, 0),
                          QtGui.QColor(0, 255, 0),
                          QtGui.QColor(0, 0, 255),
                          QtGui.QColor(255, 255, 0),
                          QtGui.QColor(255, 0, 255),
                          QtGui.QColor(0, 255, 255),
                          QtGui.QColor(0, 128, 0),
                          QtGui.QColor(0, 0, 128),
                          QtGui.QColor(128, 0, 0)]
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
        painter.setBrush(self.color_set[country.color])
        painter.drawPolygon(self._get_polygon(country))

    @staticmethod
    def _get_polygon(country: Country):
        points = [QtCore.QPoint(*x) for x in country.points]
        return QtGui.QPolygon(points)
