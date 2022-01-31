from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar)

from PyQt5.QtGui import QImage, QPixmap

import os
import h5py
import numpy as np
import cv2

class seg_window(QDialog):
    def __init__(self, parent=None, path=None):
        QDialog.__init__(self, parent)
        #self.path = path
        with h5py.File(path, "r") as hdf:
            print("Keys: %s" % hdf.keys())
            group = hdf["srcs_images"]
            for key in group.keys():
                print(key)
            dataset = group["1"][()]
            cv2.imshow("qwe", dataset)
            #print(dataset)

            """
            arr = np.ndarray((225,225,3), "uint8")
            group = hdf.require_group("srcs_images")
            dataset = group.require_dataset("1", (225, 225, 3), "uint8")
            dataset.write_direct(arr)
            print(arr)
            """

            """
            print("Keys: %s" % hdf.keys())
            a_group_key = list(hdf.keys())[1]

            # Get the data
            names = list(hdf[a_group_key])
            dataset = hdf.a_group_key.require_dataset("1")

            print(names)
            print(dataset)
            """
            """
            dataset = hdf.require_dataset("1")
            arr = np.ndarray([1,2,3])
            dataset.read_direct(arr, shape=(255,255,3), dtype=)
            """
            #cv2.imshow("tiger", data)


    
        self.adjust_window()
        self.create_bar_tool()
        #self.open_images_dir()
        self.create_image_area()
        #self.initPre()
    
    def create_bar_tool(self):
        image_bar = QToolBar()

        toolButton1 = QToolButton()
        toolButton1.setText("Previous")
        #toolButton.setCheckable(True)
        #toolButton.setAutoExclusive(True)
        image_bar.addWidget(toolButton1)
        toolButton2 = QToolButton()
        toolButton2.setText("Next")
        #toolButton.setCheckable(True)
        #toolButton.setAutoExclusive(True)
        image_bar.addWidget(toolButton2)
        toolButton1.clicked.connect(self.on_previous)
        toolButton2.clicked.connect(self.on_next)

        #layout = QVBoxLayout()
        self.layout.addWidget(image_bar)
        
        #test_btn = QPushButton("test")

        #layout.addWidget(image_bar)
        #layout.addWidget(test_btn)
        #self.addToolBar(Qt.LeftToolBarArea, image_bar)
        
        #self.layout.addWidget(image_bar)
        #self.layout.addLayout(layout)
    def on_previous(self):
        self.image_index -= 1
        self.image_adr = self.images_dir + "/" + self.images_list[self.image_index]
        self.pixmap = QtGui.QPixmap(self.image_adr)
        self.display.setPixmap(self.pixmap)

    def on_next(self):
        self.image_index += 1
        self.image_adr = self.images_dir + "/" + self.images_list[self.image_index]
        self.pixmap = QtGui.QPixmap(self.image_adr)
        self.display.setPixmap(self.pixmap)

    def create_image_area(self):
        self.image_index = 0
        self.display = QLabel()
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


    def open_images_dir(self):
        self.images_dir = os.getcwd()
        
        self.images_dir += "/__images"
        print(self.images_dir)
        if not os.path.exists(self.images_dir):
            print("no __images directory")
            os.mkdir(self.images_dir)
        self.images_list = os.listdir(self.images_dir)
        print(self.images_list)

    def display_current_image(self):
        pass

    def adjust_window(self):
        self.setWindowTitle("Разметка проекта")
        self.setMinimumSize(100,100)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        
    def initPre(self):
        """
        Initialize stuff that are shared by actions, menus, widgets etc.
        """
        self.layout.addWidget(QToolBar('Document', objectName='document_toolbar'))
        self.layout.addWidget(QToolBar('Editor', objectName='editor_toolbar'))
        self.layout.addWidget(QToolBar('View', objectName='view_toolbar'))
        self.layout.addWidget(QToolBar('Graphol', objectName='graphol_toolbar')) 