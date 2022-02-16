from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar, 
                            QStatusBar)

from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygonF, QPainterPath, QRegion

import os
import h5py
import numpy as np
import cv2
import segflex_classifier as classifier
import copy
import re


class Canvas(QLabel):
    def __init__(self, parent=None, pixmap=None, mask=None):
        super().__init__()
        self.control_pencil = False
        self.pixmap = pixmap.copy()
        self.setPixmap(self.pixmap)
        self.set_pencil_instruments()
        #self.mask = copy.copy(mask)
        #print("inner mask", self.mask, "outer mask", mask)
        self.init_mask()
    
    def init_mask(self):
        #self.mask = QPolygonF()
        #self.mask_points_f = []
        self.mask_points = []
        #print("deep pixmap = ",id(self.pixmap), id(pixmap)) 
    
    def update_mask(self, point):
        #self.mask_points_f.append(QPointF(point))
        #self.mask.append(QPointF(point))
        self.mask_points.append(point)

    def set_pencil_instruments(self):
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            self.update_mask(self.lastPoint)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing & self.control_pencil:
            painter = QPainter(self.pixmap)
            painter.setPen(QPen(self.brushColor, self.brushSize,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update_mask(self.lastPoint)
            self.setPixmap(self.pixmap)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.setPixmap(self.pixmap)

    def draw_polygon(self):
        painter = QPainter(self.pixmap)
        painter.drawPolygon(self.mask)

    def fill_polygon(self):
        pass
    """
        self.pen = QtGui.QPen(QtGui.QColor(0,0,0))                      # set lineColor
        self.pen.setWidth(3)                                            # set lineWidth
        self.brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
        painter = QPainter(self.pixmap)
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawLine(QPointF(0,0), QPointF(400,400))
        #print(self.lastPoint, self.mask_points_f[0])
        painter.drawLine(QPointF(self.lastPoint), self.mask_points_f[0])
        print(QPointF(self.lastPoint), self.mask_points_f[0])
        self.update_mask(self.mask[0])
        #self.mask_points_f.append(self.mask_points_f[0])
        #region = QRegion(self.mask)
        self.painter_path = QPainterPath(self.mask_points_f[0])
        self.painter_path.addPolygon(self.mask)
        painter.fillPath(self.painter_path, Qt.black)
        self.setPixmap(self.pixmap)
    """



class drawing_dialog(QDialog):
    def __init__(self, parent=None,
                        identifier=None,
                        project_path=None,
                        canvas_pixmap=None,
                        canvas_geometry=None,
                        window_geometry=None):
        QDialog.__init__(self, parent)

        self.instrument_name = "<QPolygon>"
        self.object_class = "__" + classifier.code_100[0] + "__"
        self.project_path = project_path
        self.identifier = identifier
        self.adjust_window(window_geometry)
        self.create_place_connect_classes_buttons()
        self.create_canvas(canvas_pixmap, canvas_geometry)
        self.create_control_buttons()

    def create_place_connect_classes_buttons(self):

        self.new_object_button = QPushButton("Новый объект класса")
        self.new_object_button.setCheckable(False)
        self.new_object_button.setChecked(False)
        self.new_object_button.clicked.connect(self.on_new_object_button)
        #self.layout.addWidget(self.new_object_button, 1, 1)

        self.control_pencil_button = QPushButton("Включить/выключить рисование")
        self.control_pencil_button.setCheckable(True)
        self.control_pencil_button.setChecked(False)
        self.control_pencil_button.toggled["bool"].connect(self.on_control_pencil_button)
        self.layout.addWidget(self.control_pencil_button, 1, 2)

        self.draw_polygon_button = QPushButton("Нарисовать полигон")
        self.draw_polygon_button.clicked.connect(self.on_draw_polygon_button)
        self.layout.addWidget(self.draw_polygon_button, 1, 3)

        self.fill_polygon_button = QPushButton("Заполнить полигон")
        self.fill_polygon_button.clicked.connect(self.on_fill_polygon_button)
        self.layout.addWidget(self.fill_polygon_button, 1, 4)

        with h5py.File(self.project_path, 'r') as hdf:
            self.classes_list = hdf.attrs[classifier.HDF_FILE_ATTR_CLASSES]
            print("classes in project = ", self.classes_list)
            i = 1 
            for el in self.classes_list:
                button = QPushButton(el)
                button.setCheckable(True)
                button.setChecked(False)
                button.toggled["bool"].connect(self.on_toggled_classes_buttons)
                self.layout.addWidget(button, i, 0)
                i += 1

    

    def on_draw_polygon_button(self):
        if self.canvas.mask:
            self.canvas.draw_polygon()
    
    def on_fill_polygon_button(self):
        #self.painter_path = QPainterPath(self.)
        self.canvas.fill_polygon()

    def on_new_object_button(self): #ne nujna - vhodit v sohranit
        #if self.canvas.mask_points:
        #    self.on_save_mask_button()
        with h5py.File(self.project_path, 'r+') as hdf:
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
            image_srcs = group_srcs[str(self.identifier)]
            current_object_index = int(image_srcs.attrs[classifier.HDF_IMAGE_ATTR_INDEX])
            image_srcs.attrs[classifier.HDF_IMAGE_ATTR_INDEX] = str(current_object_index + 1)


    def on_control_pencil_button(self, status):
        #print(status)
        if status == True:
            self.canvas.control_pencil = True
        else:
            self.canvas.control_pencil = False

    def on_toggled_classes_buttons(self, status):
        if status == True:
            self.new_object_button.setCheckable(True)
            self.new_object_button.setChecked(False)
        else:
            self.new_object_button.setCheckable(False)
            self.new_object_button.setChecked(False)

    def create_control_buttons(self):
        
        print_mask_btn = QPushButton("Напечатать маску")
        print_mask_btn.clicked.connect(self.on_print_mask_button)

        clear_mask_btn = QPushButton("Очистить маску")
        clear_mask_btn.clicked.connect(self.on_clear_mask_button)

        test_save_btn = QPushButton("Тест сохранения")
        test_save_btn.clicked.connect(self.on_test_save_btn)

        save_object_to_attrs_button = QPushButton("Сохранить объект как атрибут")
        save_object_to_attrs_button.clicked.connect(self.on_save_object_to_attrs_button)

        self.layout.addWidget(test_save_btn, 0, 2)
        self.layout.addWidget(print_mask_btn, 0, 1)
        self.layout.addWidget(clear_mask_btn, 0, 0)
        self.layout.addWidget(save_object_to_attrs_button, 0, 3)

    def on_save_object_to_attrs_button(self):
        if self.canvas.mask_points:
            with h5py.File(self.project_path, 'r+') as hdf:
                group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
                image_srcs = group_srcs[str(self.identifier)]
                current_attr_index = int(image_srcs.attrs[classifier.HDF_IMAGE_ATTR_INDEX])
                current_attr_index += 1
                image_srcs.attrs[str(current_attr_index)] = (self.identify_object_class() + 
                                                            self.identify_drawing_instrument() + 
                                                            self.prepare_coords_string_for_saving())
                image_srcs.attrs[classifier.HDF_IMAGE_ATTR_INDEX] = str(current_attr_index)
            self.canvas.mask_points.clear()
        #self.
        #self.canvas.mask_points_f.clear()
        #self.canvas.mask.clear()                                  

    def on_test_save_btn(self):
        object_as_str_to_save_in_attrs = (self.identify_object_class() + 
                                            self.identify_drawing_instrument() + 
                                            self.prepare_coords_string_for_saving())
        print(object_as_str_to_save_in_attrs)
    """
        with h5py.File(self.project_path, 'r+') as hdf:
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
            image_srcs = group_srcs[str(self.identifier)]
            current_object_index = int(image_srcs.attrs[classifier.HDF_IMAGE_ATTR_INDEX])
            image_srcs.attrs[str(current_object_index)] = str(self.canvas.mask_points)
            print(image_srcs.attrs[str(current_object_index)])
        self.canvas.mask_points.clear()
        self.canvas.mask_points_f.clear()
        self.canvas.mask.clear()
        self.new_object_button.setCheckable(True)
        self.new_object_button.setChecked(False)
    """
    def on_print_mask_button(self):
        with h5py.File(self.project_path, 'r+') as hdf:
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
            image_srcs = group_srcs[str(self.identifier)]
            number_of_objects = int(image_srcs.attrs[classifier.HDF_IMAGE_ATTR_INDEX]) #objects starting from 1
            for i in range(1, number_of_objects):
                print("im object # ", i,  image_srcs.attrs[str(i)], "\n")
            #number_of_objects += 1
            #image_srcs.attrs[current_object_index] = str(self.canvas.mask_points)
        #print(self.canvas.mask_points)
    
    def on_clear_mask_button(self): 
        self.canvas.mask.clear()

    def adjust_window(self, geometry):
        self.setWindowTitle("Разметка изображения")
        #self.setGeometry(geometry)  #SETGEOMETRY портит координаты
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def create_canvas(self, canvas_pixmap, canvas_geometry):
        self.canvas = Canvas(pixmap=canvas_pixmap)
        self.layout.addWidget(self.canvas, 2,2)

    def identify_object_class(self):
        return self.object_class

    def identify_drawing_instrument(self):
        return self.instrument_name

    def prepare_coords_string_for_saving(self):
        base = str(self.canvas.mask_points)
        rtn = re.sub(r'PyQt5.QtCore.QPoint', '', base) 
        #print(rtn)

        return rtn
    