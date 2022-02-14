from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar, 
                            QStatusBar)

from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen

import os
import h5py
import numpy as np
import cv2
import segflex_classifier as classifier
import copy

class Canvas(QLabel):
    def __init__(self, parent=None, pixmap=None, mask=None):
        super().__init__()
        self.pixmap = pixmap.copy()
        self.setPixmap(self.pixmap)
        self.set_pencil_instruments()
        #self.mask = copy.copy(mask)
        #print("inner mask", self.mask, "outer mask", mask)
        self.init_mask()
    
    def init_mask(self):
        self.mask = []
        #print("deep pixmap = ",id(self.pixmap), id(pixmap)) 
    
    def update_mask(self, point):
        self.mask.append(point)

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
        if (event.buttons() & Qt.LeftButton) & self.drawing:
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

    """
    def paintEvent(self, event):
        # create a canvas
        canvasPainter = QPainter(self)
         
        # draw rectangle  on the canvas
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
    """



class drawing_dialog(QDialog):
    def __init__(self, parent=None,
                        identifier=None,
                        project_path=None,
                        canvas_pixmap=None,
                        canvas_geometry=None,
                        window_geometry=None):
        QDialog.__init__(self, parent)

        self.project_path = project_path
        self.identifier = identifier
        self.mask = []
        self.adjust_window(window_geometry)
        self.create_place_connect_classes_buttons()
        self.create_canvas(canvas_pixmap, canvas_geometry)
        self.create_group_for_objects_on_image()
        #print("deep pixmap = ",id(self.project_path), id(project_path)) 
        self.create_control_btns()

    def create_place_connect_classes_buttons(self):
        with h5py.File(self.project_path, 'r') as hdf:
            self.classes_list = hdf.attrs[classifier.HDF_FILE_ATTR_CLASSES]
            print("classes in project = ", self.classes_list)
            i = 1 
            for el in self.classes_list:
                button = QPushButton(el)
                self.layout.addWidget(button, i, 0)
                i += 1


    def create_group_for_objects_on_image(self):
        with h5py.File(self.project_path, 'r+') as hdf:
            parent_group = hdf[classifier.HDF_GROUP_OBJECT_LAYERS_NAME]
            print(parent_group)

    def create_control_btns(self):
        
        print_mask_btn = QPushButton("Напечатать маску")
        print_mask_btn.clicked.connect(self.print_mask)

        clear_mask_btn = QPushButton("Очистить маску")
        clear_mask_btn.clicked.connect(self.clear_mask)

        save_mask_btn = QPushButton("Сохранить маску в файл")
        save_mask_btn.clicked.connect(self.save_mask)

        self.layout.addWidget(save_mask_btn, 0, 2)
        self.layout.addWidget(print_mask_btn, 0, 1)
        self.layout.addWidget(clear_mask_btn, 0, 0)


    #def convert_mask_to_numpy(self):


    def save_mask(self):
        with h5py.File(self.project_path, 'r+') as hdf:
            group_features = hdf[classifier.HDF_GROUP_FEATURES_NAME]
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
            srcs_tuple = group_srcs[str(self.identifier)]
            self.feature_shape = srcs_tuple[()].shape

    
            self.feature_base = np.random.rand(self.feature_shape[0], self.feature_shape[1], self.feature_shape[2])
            
            print(self.feature_base)
            cv2.imshow("base_mask",self.feature_base)

            #print(srcs_tuple[()])
            #cv2.imshow("sd", srcs_tuple[()])
            
            #print(dataset_shape)
            #mask_as_dataset = group_features[str(self.identifier)]
            #print(mask_as_dataset)

    def print_mask(self):
        print(self.canvas.mask)
    
    def clear_mask(self): 
        #painter = QPainter(self.canvas.pixmap)
        #painter.eraseRect(self.canvas.rect())
        #self.canvas.painter.eraseRect(self.canvas.rect())
        self.canvas.mask.clear()

    def adjust_window(self, geometry):
        self.setWindowTitle("Разметка изображения")
        #self.setGeometry(geometry)  #SETGEOMETRY портит координаты
        #self.layout = QHBoxLayout()
        self.layout = QGridLayout()
        #self.image_layout = QHBoxLayout()
        self.setLayout(self.layout)
        #self.layout.addLayout(self.image_layout, 2, 1) # правильно растянуть область изображения

        #print(item)
    
    def create_canvas(self, canvas_pixmap, canvas_geometry):
        self.canvas = Canvas(pixmap=canvas_pixmap)
        #self.canvas.setPixmap(canvas_pixmap)
        #self.canvas.setGeometry(canvas_geometry)
        #self.image_layout.addWidget(self.canvas)
        self.layout.addWidget(self.canvas, 1,1)
    