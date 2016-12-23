import sys

from model.colorer import Colorer
from model.country import Country
from model.map import Map

try:
    from PyQt5 import QtGui, QtWidgets, QtCore
except Exception as e:
    print('PyQt5 not found: "{}"'.format(e),
          file=sys.stderr)
    sys.exit(1)


class Vizualizer(QtWidgets.QWidget):
    def __init__(self, countries_map: Map, palette):
        super(Vizualizer, self).__init__()
        countries_map.calc_incident_countries()
        self.colorer = Colorer(countries_map, palette)
        self.update_map()
        self.highlighted_country = None
        self.initUI()

    @property
    def countries_map(self):
        return self.colorer.countries_map

    def update_map(self):
        self.colorer.color_map()
        self.countries_to_polygons = self._build_polygon_map(
            self.countries_map)

    def initUI(self):
        self.setGeometry(0, 0,
                         self.countries_map.width, self.countries_map.height)
        self.show()

    def init_pop_up_menu(self, menu, country):
        actions = {}
        forbidden_color = {c.color for c in filter(lambda x: x.hard_colored,
                                                   country.incident_countries)}
        forbidden_color.add(country.color)

        for color, name in filter(lambda x: x[0] not in forbidden_color,
                                  self.colorer.colors_match.items()):
            actions[menu.addAction(self.colorer.color_name(name))] = color
        if country.hard_colored:
            menu.addSeparator()
            self.reset_action = menu.addAction("reset")

        return actions

    def mousePressEvent(self, q_mouse_event: QtGui.QMouseEvent):
        if q_mouse_event.button() == QtCore.Qt.RightButton:
            self.select_country(q_mouse_event)
            if not self.highlighted_country:
                return
            self.run_context_menu(q_mouse_event)
        else:
            self.select_country(q_mouse_event)
        self.repaint()

    def select_country(self, q_mouse_event):
        for (country, polygons) in self.countries_to_polygons.items():
            for polygon in polygons:
                if polygon.containsPoint(q_mouse_event.pos(), 0):
                    self.highlighted_country = country

    def run_context_menu(self, q_mouse_event):
        pop_up_menu = QtWidgets.QMenu(self)
        actions = self.init_pop_up_menu(pop_up_menu, self.highlighted_country)
        action = pop_up_menu.exec(q_mouse_event.pos())
        if action:
            if action in actions:
                self.highlighted_country.set_color(actions[action])
            elif action == self.reset_action:
                self.highlighted_country.hard_set_color = False
            self.update_map()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self._draw_countries(painter)
        self._highlight_country(painter)
        self._draw_costs(painter)
        painter.end()

    def _draw_costs(self, painter):
        painter.setPen(QtGui.QPen(QtCore.Qt.white))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
        painter.drawRect(0, 0, 200, 30)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        painter.drawText(0, 15, 'cur cost = ' + str(self.colorer.total_cost))
        painter.drawText(0, 30, 'min cost = ' + str(self.colorer.min_cost))

    def _highlight_country(self, painter: QtGui.QPainter):
        if self.highlighted_country:
            painter.setBrush(QtGui.QBrush(QtGui.QColor(
                *self.colorer.colors_match[self.highlighted_country.color])))
            pen = QtGui.QPen(QtCore.Qt.white)
            pen.setWidth(3)
            painter.setPen(pen)
            self._draw_polygons(
                painter, self.countries_to_polygons[self.highlighted_country])

    def _draw_countries(self, painter: QtGui.QPainter):
        for (country, polygons) in self.countries_to_polygons.items():
            pen = QtGui.QPen(QtCore.Qt.black)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(QtGui.QColor(
                *self.colorer.colors_match[country.color]))
            self._draw_polygons(painter, polygons)

    @staticmethod
    def _draw_polygons(painter, polygons):
        for polygon in polygons:
            painter.drawPolygon(polygon)

    @staticmethod
    def _build_polygon_map(countries_map):
        return {country: Vizualizer._get_polygons(country)
                for country in countries_map.countries}

    @staticmethod
    def _get_polygons(country: Country):
        return [QtGui.QPolygon([QtCore.QPoint(*x) for x in piece.points])
                for piece in country.country_pieces]
