import sys

from model.colorer import Colorer
from model.country import Country
from model.map import Map
from model.palette import Palette

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
        self.colorer = Colorer(countries_map,
                               Palette({(255, 0, 0): 1,
                                        (0, 255, 0): 1,
                                        (0, 0, 255): 1,
                                        (255, 255, 0): 1,
                                        (255, 0, 255): 1,
                                        (0, 255, 255): 1,
                                        (0, 128, 0): 1,
                                        (0, 0, 128): 1,
                                        (128, 0, 0): 1}))
        self.colorer.color_map()
        self.map = self.colorer.countries_map
        self.countries_to_polygons = self._build_polygon_map(self.map)
        self.highlighted_country = None
        self.initUI()

    def _build_polygon_map(self, map):
        return {country: self._get_polygons(country)
                for country in map.countries}

    def initUI(self):
        self.setGeometry(0, 0, self.map.width, self.map.height)
        self.show()

    def mousePressEvent(self, QMouseEvent):
        for (country, polygons) in self.countries_to_polygons.items():
            for polygon in polygons:
                if polygon.containsPoint(QMouseEvent.pos(), 0):
                    self.highlighted_country = country
        self.repaint()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self._draw_countries(painter)
        self._highlight_country(painter)
        painter.end()

    def _highlight_country(self, painter: QtGui.QPainter):
        if self.highlighted_country:
            painter.setBrush(QtGui.QBrush(QtGui.QColor(
                *self.colorer.colors_match[self.highlighted_country.color])))
            pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
            pen.setWidth(3)
            painter.setPen(pen)
            self._draw_polygons(
                painter, self.countries_to_polygons[self.highlighted_country])

    def _draw_countries(self, painter: QtGui.QPainter):
        for (country, polygons) in self.countries_to_polygons.items():
            pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(QtGui.QColor(
                *self.colorer.colors_match[country.color]))
            self._draw_polygons(painter, polygons)

    def _draw_polygons(self, painter, polygons):
        for polygon in polygons:
            painter.drawPolygon(polygon)

    @staticmethod
    def _get_polygons(country: Country):
        return [QtGui.QPolygon([QtCore.QPoint(*x) for x in piece.points])
                for piece in country.country_pieces]
