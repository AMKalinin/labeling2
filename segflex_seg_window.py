from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar, 
                            QStatusBar)

from PyQt5.QtGui import QImage, QPixmap, QIcon

import os
import h5py
import numpy as np
import cv2
import segflex_classifier as classifier

class seg_window(QDialog):
    def __init__(self, parent=None, path=None):
        QDialog.__init__(self, parent)
        self.path = path
        self.identifier = 0
        self.current_image_position = 1
       
        self.adjust_window()
        self.open_images_dir()
        self.open_image(self.identifier)
        self.create_navigation_bar()
        #self.create_image_area()
        #self.initPre()
    
    def create_navigation_bar(self):
        navigation_bar = QToolBar()

        previous_btn = QToolButton()
        previous_icon = QIcon()
        previous_icon.addPixmap(QPixmap(classifier.ICON_SEG_TBTN_PREVIOUS_FULL), QIcon.Normal, QIcon.Off)
        previous_btn.setIcon(previous_icon)

        next_btn = QToolButton()
        next_icon = QIcon()
        next_icon.addPixmap(QPixmap(classifier.ICON_SEG_TBTN_NEXT_FULL), QIcon.Normal, QIcon.Off)
        next_btn.setIcon(next_icon)

        self.image_position_postfix = ' / ' + str(self.image_position_max) 
        self.image_position_widget = QLabel(str(self.current_image_position) + self.image_position_postfix) 
        #next_btn.setText("Next")


        #toolButton.setCheckable(True)
        #toolButton.setAutoExclusive(True)
        #toolButton.setCheckable(True)
        #toolButton.setAutoExclusive(True)

        navigation_bar.addWidget(previous_btn)
        navigation_bar.addWidget(next_btn)
        navigation_bar.addWidget(self.image_position_widget)

        previous_btn.clicked.connect(self.on_previous)
        next_btn.clicked.connect(self.on_next)

        self.layout.addWidget(navigation_bar, 0, 0, Qt.AlignTop | Qt.AlignHCenter) #области  
        

    def on_previous(self):
        if self.identifier > 0:
            self.identifier -= 1
            self.current_image_position -= 1
            self.open_image(self.identifier)
            self.image_position_widget.setText(str(self.current_image_position) + self.image_position_postfix)


    def on_next(self):
        if self.identifier < self.identifier_max:
            self.identifier += 1
            self.current_image_position += 1
            self.open_image(self.identifier)
            self.image_position_widget.setText(str(self.current_image_position) + self.image_position_postfix)

    """
    def open_file(self):
        self.hdf = h5py.File(self.path, 'w')
        self.identifier_max = self.hdf.keys()
        print(self.identifier_max)

    #def closeEvent(self, event):
    #    self.hdf.close()
    """

    def open_image(self, identifier):  #каждый раз открываю проблема закрыть корректно файл, если один раз
        self.clear_window_layout(self.image_layout)
        self.display = QLabel()
        self.display.setMaximumSize(600, 600)
        with h5py.File(self.path, 'r') as hdf:
            self.identifier_max = len(list(hdf[classifier.HDF_GROUP_SRCS_NAME].keys())) - 1 #starting with 0
            self.image_position_max = self.identifier_max + 1 #starting with 1
            print(list(hdf[classifier.HDF_GROUP_SRCS_NAME].keys()))
            print(self.identifier_max)
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
            dataset = group_srcs[str(identifier)]
            image_as_numpy = dataset[()]
            height, width, channel = image_as_numpy.shape
            bytesPerLine = 3 * width
            image_as_qimage = QImage(image_as_numpy, width, height, bytesPerLine, QImage.Format_RGB888)
            image_correct_rgb = image_as_qimage.rgbSwapped()
            image_as_pixmap = QPixmap(image_correct_rgb)
            self.display.setPixmap(image_as_pixmap)
            self.image_layout.addWidget(self.display)

    """
            
    def create_image_area2(self):
        self.image_index = 0
        self.display = QLabel()
        self.display.setMaximumSize(100,100)
        #pixmap = QtGui.QPixmap(self.images_list[self.image_index])
        self.image_adr = self.images_dir + "/" + self.images_list[self.image_index]
                    #"C:\_python_pr\8.3_version_2_data_labeling\__images\image — копия (2).jpg"
                    #"/__images/" + self.images_list[self.image_index]
        print(self.image_adr)
        self.pixmap = QtGui.QPixmap(self.image_adr)

        self.display.setPixmap(self.pixmap)
        #image = QImage(self.images_list[self.image_index])
        #self.display.setPixmap(QPixmap.fromImage(image))
        #f = open(self.images_list[self.image_imdex])
        self.layout.addWidget(self.display)
    """


    def open_images_dir(self):
        self.images_dir = os.getcwd()
        
        self.images_dir += "/__images"
        print(self.images_dir)
        if not os.path.exists(self.images_dir):
            print("no __images directory")
            os.mkdir(self.images_dir)
        self.images_list = os.listdir(self.images_dir)
        print(self.images_list)

    def adjust_window(self):
        self.setWindowTitle("Разметка проекта")
        self.setMinimumSize(800,800)
        #self.layout = QHBoxLayout()
        self.layout = QGridLayout()
        self.image_layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addLayout(self.image_layout, 1, 1, 1, 1) # правильно растянуть область изображения
        
    def initPre(self):
        """
        Initialize stuff that are shared by actions, menus, widgets etc.
        """
        self.layout.addWidget(QToolBar('Document', objectName='document_toolbar'))
        self.layout.addWidget(QToolBar('Editor', objectName='editor_toolbar'))
        self.layout.addWidget(QToolBar('View', objectName='view_toolbar'))
        self.layout.addWidget(QToolBar('Graphol', objectName='graphol_toolbar')) 
    
    def clear_window_layout(self, layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)