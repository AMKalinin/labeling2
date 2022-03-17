from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox)
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import segflex_seg_window as seg_window
import segflex_classifier as classifier
import h5py


class task_widget(QGroupBox):
    def __init__(self, path, identifier, mode, signal):
        super().__init__()
        self.project_path = path
        self.identifier = identifier
        self.mode = mode
        self.signal = signal
        self.unit_ui()

    def unit_ui(self):
        self.create_layouts()
        self.fill_layouts()
        self.place_layouts()
        self.adjust_window()

    def create_layouts(self):
        self.layout = QHBoxLayout()
        self.layout_preview = QVBoxLayout()
        self.layout_info = QVBoxLayout()
        self.layout_actions =QVBoxLayout()

    def fill_layouts(self):
        self.fill_preview()
        self.fill_info()
        self.fill_actions()

    def place_layouts(self):
        self.layout.addLayout(self.layout_preview)
        self.layout.addLayout(self.layout_info)
        self.layout.addLayout(self.layout_actions)
        self.layout_preview.addWidget(self.preview)
        self.layout_info.addWidget(self.info_number)
        self.layout_info.addWidget(self.info_created_by)
        self.layout_info.addWidget(self.info_last_update)
        if self.mode == classifier.TASK_WIDGET_MODE_0:
            self.layout_actions.addWidget(self.btn_edit)
            self.layout_actions.addWidget(self.btn_tocheck)
        if self.mode == classifier.TASK_WIDGET_MODE_1:
            self.layout_actions.addWidget(self.btn_redo)
            self.layout_actions.addWidget(self.btn_done)


    def adjust_window(self):
        self.setMaximumHeight(120)
        self.setLayout(self.layout)
    
    def fill_preview(self):
        self.preview = QLabel(self)
        pixmap = self.create_previw()
        self.preview.setPixmap(pixmap)

    def fill_info(self):
        self.info_number = QLabel("#" )#+ name)
        self.info_created_by = QLabel("Created by Hashly on November 1st 2021")
        self.info_last_update = QLabel("Last updated 15 days ago")

    def fill_actions(self):
        if self.mode == classifier.TASK_WIDGET_MODE_0:
            self.btn_tocheck = QPushButton("Отправить модератору")
            self.btn_tocheck.clicked.connect(self.on_tocheck)
            self.btn_edit = QPushButton("Разметить")
            self.btn_edit.clicked.connect(self.on_edit)
        if self.mode == classifier.TASK_WIDGET_MODE_1:
            self.btn_redo = QPushButton("Вернуть на доработку")
            self.btn_redo.clicked.connect(self.on_redo)
            self.btn_done = QPushButton("Готово")
            self.btn_done.clicked.connect(self.on_edit)

    def create_previw(self): 
        with h5py.File(self.project_path, 'r') as hdf:
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]                
            dataset = group_srcs[str(self.identifier)]
            image_as_numpy = dataset[()]
            height, width, channel = image_as_numpy.shape
            bytesPerLine = 3 * width
            image_as_qimage = QImage(image_as_numpy, width, height, bytesPerLine, QImage.Format_RGB888)
            image_correct_rgb = image_as_qimage.rgbSwapped()
            image_as_pixmap = QPixmap(image_correct_rgb)
            image_resized = image_as_pixmap.scaled(100, 100)

            return image_resized

    def on_redo(self):
        with h5py.File(self.project_path, 'r+') as hdf:
            group = hdf[classifier.HDF_GROUP_SRCS_NAME]                
            task = group[str(self.identifier)]
            task.attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_1
        self.signal.emit(self.project_path)

    def on_done(self):
        with h5py.File(self.project_path, 'r+') as hdf:
            group = hdf[classifier.HDF_GROUP_SRCS_NAME]                
            task = group[str(self.identifier)]
            task.attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_3
        self.signal.emit(self.project_path)

    def on_tocheck(self):
        with h5py.File(self.project_path, 'r+') as hdf:
            group = hdf[classifier.HDF_GROUP_SRCS_NAME]                
            task = group[str(self.identifier)]
            task.attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_2
        self.signal.emit(self.project_path)

    def on_edit(self):
        pass
        self.seg_window = seg_window.seg_window(self, self.project_path)
        self.seg_window.exec_()


    def emit_delete_signal(self):
        #self.Signal_OneParameter.emit("date_str")
        with h5py.File(self.project_path, 'r+') as hdf:
            group = hdf[classifier.HDF_GROUP_SRCS_NAME]                
            task = group[str(self.identifier)]
            task.attrs[classifier.HDF_TASK_STATUS] = classifier.HDF_TASK_STATUS_2
        self.deleteLater()
        pass




