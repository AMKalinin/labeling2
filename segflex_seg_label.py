from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint#, QVector
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar, 
                            QStatusBar)

from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon

import os
import h5py
import numpy as np
import cv2
import segflex_classifier as classifier
import segflex_draw_window as draw
import re
from ast import literal_eval as make_tuple


class Label(QLabel):
    def __init__(self, parent=None):
        super().__init__()

        self.base_pixmap = QPixmap()
        self.overlayed_pixmap = QPixmap()
        self.new_polygon_pixmap = QPixmap()

        self.polygon_for_iterations = QPolygon()
        self.new_polygon = QPolygon()
        self.new_polygon_points = []

        self.mode = 'display base'

    def update_base(self, pixmap):
        self.base_pixmap = pixmap.copy()
        self.overlayed_pixmap = pixmap.copy()
        self.new_polygon_pixmap = pixmap.copy()

        #self.update()

    def overlay_mask(self, polygon):
        self.polygon_for_iterations = polygon

        self.mode = 'display mask'
        self.repaint()

    def restore_srcs(self):
        self.mode = 'display base'
        self.repaint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.mode == 'draw polygon':
                self.new_polygon_points.append(event.pos())
                #self.new_polygon = QPolygon(self.new_polygon_points)
                self.update()
                self.update_base(self.base_pixmap)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(1))
        pixmap = QPixmap()
        if self.mode == 'display base':
            pixmap = self.base_pixmap
        elif self.mode == 'display mask':
            pixmap = self.overlayed_pixmap
            painter2 = QPainter(pixmap)
            painter2.drawPolygon(self.polygon_for_iterations)
            self.overlayed_pixmap = pixmap
            self.toggle_show_hide_mask = False
        elif self.mode == 'draw polygon':
            pixmap = self.new_polygon_pixmap
            self.new_polygon = QPolygon(self.new_polygon_points)
            painter3 = QPainter(pixmap)
            painter3.drawPolygon(self.new_polygon)
        painter.drawPixmap(0, 0, pixmap)

        