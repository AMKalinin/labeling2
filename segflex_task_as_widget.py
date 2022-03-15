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


class task_as_widget(QGroupBox):
    #Signal_OneParameter = pyqtSignal(str)

    def __init__(self,
    classes,
    path,
    identifier,
    parent=None,
    ide=0):
        #QGroupBox.__init__(self, name, classes, parent, ide)
        super().__init__()
        self.project_path = path
        self.identifier = identifier

        layout = QHBoxLayout()
        layout_preview = QVBoxLayout()
        layout_info = QVBoxLayout()
        layout_status = QVBoxLayout()
        layout_jobs = QVBoxLayout()
        layout_actions =QVBoxLayout()

        layout.addLayout(layout_preview)
        layout.addLayout(layout_info)
        layout.addLayout(layout_status)
        layout.addLayout(layout_jobs)
        layout.addLayout(layout_actions)


        image = QLabel(self)
        pixmap = self.create_previw()
        image.setPixmap(pixmap)
        #image.setFixedSize(100, 100)

        info_number = QLabel("#" + str(ide) )#+ name)
        info_created_by = QLabel("Created by Hashly on November 1st 2021")
        info_last_update = QLabel("Last updated 15 days ago")

        status = QLabel(" ".join(str(classes)))

        jobs = QLabel("0 of 1 jobs")

        self.btn_open = QPushButton("Open")

        self.btn_delete = QPushButton("Отправить модератору")
        self.btn_delete.clicked.connect(self.emit_delete_signal)
        self.btn_edit = QPushButton("Разметить")
        self.btn_edit.clicked.connect(self.on_edit)
        actions_bar = QComboBox()
        actions_bar.addItems(["do smth1", "do smth2"])

        btn_id_in_layout = QPushButton("print id")
        #btn_id_in_layout.clicked.connect()


        layout_preview.addWidget(image)
        #layout_info.addWidget(info_number)
        #layout_info.addWidget(info_created_by)
        #layout_info.addWidget(info_last_update)
        #layout_status.addWidget(status)
        #layout_jobs.addWidget(jobs)

        #layout_actions.addWidget(self.btn_open)
        layout_actions.addWidget(self.btn_edit)
        layout_actions.addWidget(self.btn_delete)
        

        #layout_actions.addWidget(actions_bar)


        self.setMaximumHeight(120)
        self.setLayout(layout)

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


    def emit_delete_signal(self):
        #self.Signal_OneParameter.emit("date_str")
        self.deleteLater()
        pass

    def on_edit(self):
        pass
        self.seg_window = seg_window.seg_window(self, self.project_path)
        self.seg_window.exec_()

