import math
import sys
import uuid

from model.country import Country, CountryPiece
from model.map import Map

try:
    from PyQt5 import QtGui, QtWidgets, QtCore
except Exception as e:
    print('PyQt5 not found: "{}"'.format(e), file=sys.stderr)
    sys.exit(1)


class EditorWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setted_points = []
        self.countries = []
        self.points = []
        self.pieces = []
        self._sticky_point_mode = False
        self.closest = None
        self.setMouseTracking(True)
        self.mouse_pos = None
        self._finish_piece = False

    def add_country(self):
        if self.points:
            self.pieces.append(CountryPiece(self.points))
            self.points = []
        if self.pieces:
            self.countries.append(Country(self.pieces))
            self.pieces = []
        self.trigger_sticky_point_mode()
        self.repaint()

    def add_piece(self):
        if self.points:
            self.pieces.append(CountryPiece(self.points))
            self.points = []
        self.repaint()

    def trigger_sticky_point_mode(self):
        self._sticky_point_mode ^= True
        if not self._sticky_point_mode:
            self.closest = None

    def finish_piece(self):
        self._finish_piece = True

    def save(self):
        self.add_country()
        name = "./maps/map_{}.json".format(str(uuid.uuid4()))
        new_map = Map(self.countries)
        with open(name, 'w') as f:
            f.write(new_map.to_json())
        msg = QtWidgets.QMessageBox()
        msg.setText("Saved to {}".format(name))
        msg.setWindowTitle("Saved")
        msg.exec_()

    def mousePressEvent(self, q_mouse_event):
        self.setted_points.append(q_mouse_event.pos())
        if self._sticky_point_mode:
            self.points.append(self.point_to_tuple(self.closest))
            self.trigger_sticky_point_mode()
        if self._finish_piece:
            self._finish_piece = False
            self.points.append(self.point_to_tuple(self.closest))
            self.add_piece()
            return
        self.points.append(self.point_to_tuple(q_mouse_event.pos()))
        self.repaint()

    def mouseMoveEvent(self, q_mouse_event):
        self.mouse_pos = q_mouse_event.pos()
        if self._sticky_point_mode or self._finish_piece:
            self.closest = min(self.setted_points, key=lambda p: math.sqrt(
                pow(q_mouse_event.pos().x() - p.x(), 2) + pow(
                    q_mouse_event.pos().y() - p.y(), 2)))
        self.repaint()

    def paintEvent(self, q_paint_event: QtGui.QPaintEvent):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.draw_field(painter)
        if self._sticky_point_mode and self.closest:
            painter.setPen(QtCore.Qt.darkRed)
            painter.setBrush(QtCore.Qt.red)
            painter.drawEllipse(self.closest, 2, 2)
            painter.drawLine(self.closest, self.mouse_pos)
        elif self._finish_piece and self.closest and self.setted_points:
            painter.drawLine(self.closest, self.setted_points[-1])
        elif self.setted_points and self.points:
            painter.drawLine(self.setted_points[-1], self.mouse_pos)

        painter.end()

    def draw_field(self, painter):
        for country in self.countries:
            for piece in country.pieces:
                self._draw_poly(piece.points, painter, QtCore.Qt.lightGray,
                                QtCore.Qt.black)
        for piece in self.pieces:
            self._draw_poly(piece.points, painter, QtCore.Qt.magenta,
                            QtCore.Qt.white)
        if self.points:
            self._draw_poly(self.points, painter, QtCore.Qt.magenta,
                            QtCore.Qt.white)

    @staticmethod
    def _draw_points(points, painter):
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.darkBlue)
        for point in points:
            painter.drawEllipse(QtCore.QPoint(*point), 2, 2)

    @staticmethod
    def _draw_poly(points, painter, inner_color, border_color):
        painter.setBrush(inner_color)
        painter.setPen(border_color)
        painter.drawPolygon(EditorWidget._get_polygon(points))
        EditorWidget._draw_points(points, painter)

    @staticmethod
    def _get_polygons(pieces):
        return [pieces._get_polygon(piece) for piece in pieces]

    @staticmethod
    def _get_polygon(points):
        return QtGui.QPolygon([QtCore.QPoint(*x) for x in points])

    @staticmethod
    def point_to_tuple(p):
        return p.x(), p.y()
