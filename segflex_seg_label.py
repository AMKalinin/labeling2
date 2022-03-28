from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QRect #, QVector
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar, 
                            QStatusBar)

from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon

import segflex_mask_as_object as mask
from segflex_lable_dialog import drawing_dialog as dialog

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

        self.maska = mask.mask()
        self.index = None

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
                self.index = None
                if not self.maska.points:
                    flag = False
                else:
                    flag, ind = self.maska.click_on_point(event.pos())
                if flag:
                    self.index = ind
                else:
                    self.maska.add_points(event.pos())
                    self.update()
                    self.update_base(self.base_pixmap)

            elif self.mode == 'draw rect':
                self.index = None
                if not self.maska.points:
                    flag = False
                else:
                    flag, ind = self.maska.click_on_point(event.pos())
                if flag:
                    self.index = ind
                else:
                    self.start_p = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if self.mode == 'draw polygon':
                if self.index is not None:
                    self.maska.setPoint(self.index, event.pos())
                    self.update()
                    self.update_base(self.base_pixmap)

            elif self.mode == 'draw rect':
                if self.index is not None:
                    self.maska.setPoint(self.index, event.pos())
                    self.update()
                    self.update_base(self.base_pixmap)
                else:
                    self.maska.rectangle(self.start_p, event.pos())
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
        elif (self.mode == 'draw polygon') or (self.mode == 'move point') or (self.mode == 'draw rect'):
            pixmap = self.new_polygon_pixmap
            self.maska.draw(pixmap)
        painter.drawPixmap(0, 0, pixmap)

    def select_lable(self):
        self.lable_dialog = dialog(self)
        self.lable_dialog.exec_()