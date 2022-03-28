from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint, QPointF, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar,
                            QStatusBar, QListWidget)

from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygonF, QPainterPath, QRegion, QPolygon

import os
import h5py
import numpy as np
import cv2
import segflex_classifier as classifier
import copy
import re




class drawing_dialog(QDialog):
    signal1 = pyqtSignal()
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.object_class = "__" + classifier.code_100[0] + "__"

        self.adjust_window()
        self.create_control_buttons()


    def parsed_classes(self):
        with h5py.File(self.parent().parent().project_path, 'r') as hdf:
            self.classes_list = hdf.attrs[classifier.HDF_FILE_CLASSES]

    def selection_chenged(self, item):
        self.edit.setText(item.text())

    def adjust_window(self):
        self.setWindowTitle("Разметка изображения")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


    def create_control_buttons(self):
        self.edit = QLineEdit()
        self.edit.setReadOnly(True)

        self.list_class = QListWidget()
        self.parsed_classes()
        self.list_class.addItems(self.classes_list)
        self.list_class.itemClicked.connect(self.selection_chenged)
        btn_ok = QPushButton("Ок")
        btn_cancel = QPushButton("Отмена")

        control_layout = QHBoxLayout()
        control_layout.addWidget(btn_ok)
        control_layout.addWidget(btn_cancel)

        btn_ok.clicked.connect(self.btn_ok)
        btn_cancel.clicked.connect(self.btn_cancel)

        self.layout.addWidget(self.edit)
        self.layout.addLayout(control_layout)
        self.layout.addWidget(self.list_class)

    def btn_cancel(self):
        self.signal1.emit()
        self.deleteLater()

    def btn_ok(self):
        self.parent().parent().object_class = '__' + self.edit.text() + '__'
        self.signal1.emit()
        self.deleteLater()
