from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon
from PyQt5.QtCore import Qt, QRect, QPoint



class mask:
    def __init__(self):
        self.code = None
        self.points = []

    def draw(self, pixmap):
        pass

    def distance(self, pos, ind):
        return ((self.points[ind].x() - pos.x())**2 + (self.points[ind].y() - pos.y())**2)**0.5

    def min_dist(self, pos):
        min_ind = 0
        min_dist = self.distance(pos, 0)
        for i in range(1, len(self.points)):
            dist = self.distance(pos, i)
            if dist < min_dist:
                min_dist = dist
                min_ind = i
        return min_ind, min_dist

    def click_on_point(self, pos):
        ind, dist = self.min_dist(pos)
        return dist <= 10, ind

class polygon_mask(mask):
    def __init__(self):
        super(polygon_mask, self).__init__()
        self.type = 'polygon'
        self.polygon = QPolygon()

    def setPoint(self, ind, point):
        self.points[ind] = point
        self.polygon = QPolygon(self.points)

    def add_points(self, point):
        self.points.append(point)
        self.polygon = QPolygon(self.points)

    def draw(self, pixmap):
        painter = QPainter(pixmap)
        painter.drawPolygon(self.polygon)
        painter.setPen((QPen(Qt.black, 10.0)))
        painter.drawPoints(self.polygon)


class rectangle_mask(mask):

    def __init__(self):
        super(rectangle_mask, self).__init__()
        self.type = 'rectangle'
        self.rect = QRect()

    def rectangle(self, p1, p2):
        self.rect = QRect(p1, p2)
        self.points.clear()
        self.calc_points()

    def calc_points(self):
        self.points.append(self.rect.topLeft())
        self.points.append(self.rect.topRight())
        self.points.append(self.rect.bottomRight())
        self.points.append(self.rect.bottomLeft())

    def setPoint(self, ind, point):
        if ind == 0:
            self.points[0] = point
        elif ind == 1:
            self.points[0] = QPoint(self.points[0].x(), point.y())
            self.points[2] = QPoint(point.x(), self.points[2].y())
        elif ind == 2:
            self.points[2] = point
        elif ind == 3:
            self.points[0] = QPoint(point.x(), self.points[0].y())
            self.points[2] = QPoint(self.points[2].x(), point.y())
        self.rectangle(self.points[0], self.points[2])


    def draw(self, pixmap):
        painter = QPainter(pixmap)
        painter.drawRect(self.rect)
        painter.setPen((QPen(Qt.black, 10.0)))
        polygon = QPolygon(self.points)
        painter.drawPoints(polygon)

