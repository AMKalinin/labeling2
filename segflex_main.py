from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox,
                            QFileDialog, QSplitter)

import segflex_new_project
import segflex_project_as_widget as project
import segflex_task_as_widget as task_base
import os
import json
import segflex_classifier as classifier
import h5py
import time


class main_window(QMainWindow):
    signal_reparse = pyqtSignal(str)
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, flags=QtCore.Qt.Window)
        self.init_ui()
        
    def init_ui(self):
        self.adjust_main_window()
        self.check_create_projects_folder()
        self.init_layouts()
        self.init_widgets()
        self.set_layouts()
        self.place_widgets()
        self.connect_ui()
        self.parse_projects_folder()

    def adjust_main_window(self):
        self.main_frame = QFrame()
        self.setCentralWidget(self.main_frame)
        self.setWindowTitle("Segmentation app. 0.9")
        self.resize(1000, 400)

    def check_create_projects_folder(self):
        if not os.path.exists(classifier.PROJECTS_FOLDER_FULL_NAME):
            os.mkdir(classifier.PROJECTS_FOLDER_FULL_NAME)

    def init_layouts(self):
        self.main_layout = QGridLayout()
        self.tab_projects_layout = QVBoxLayout()
        self.tab_tasks_left_layout = QVBoxLayout()
        self.tab_tasks_right_layout = QVBoxLayout()
        self.btn_group_open_layout = QVBoxLayout()

    def init_widgets(self):
        self.init_table()
        self.init_btns()

    def set_layouts(self):
        self.main_frame.setLayout(self.main_layout)
        self.tab_projects_group.setLayout(self.tab_projects_layout)
        self.tab_tasks_left_group.setLayout(self.tab_tasks_left_layout)
        self.tab_tasks_right_group.setLayout(self.tab_tasks_right_layout)
        self.btns_group_open.setLayout(self.btn_group_open_layout)

    def place_widgets(self):
        self.tab.addTab(self.tab_projects_area, "??????????????")
        self.tab.addTab(self.tab_split, "????????????")
        self.main_layout.addWidget(self.tab, 0, 0, 4, 1)
        self.main_layout.addWidget(self.btns_group_open, 0, 1)

    def connect_ui(self):
        self.signal_reparse.connect(self.parse_tasks)
        self.btn_project_new.clicked.connect(self.on_create_new_project_clicked)
        

    def init_table(self):
        self.tab = QTabWidget()
        self.tab_projects_area = QScrollArea(self)
        self.tab_tasks_left_area = QScrollArea(self)
        self.tab_tasks_right_area = QScrollArea(self)

        self.tab_projects_area.setWidgetResizable(True)
        self.tab_tasks_left_area.setWidgetResizable(True)
        self.tab_tasks_right_area.setWidgetResizable(True)

        self.tab_split = QSplitter()
        self.tab_split.addWidget(self.tab_tasks_left_area)
        self.tab_split.addWidget(self.tab_tasks_right_area)

        self.tab_projects_group = QGroupBox(self.tab_projects_area)
        self.tab_tasks_left_group = QGroupBox(self.tab_tasks_left_area)
        self.tab_tasks_right_group = QGroupBox(self.tab_tasks_right_area)

        self.tab_projects_group.setTitle("??????????????")
        self.tab_tasks_left_group.setTitle("????????????????")
        self.tab_tasks_right_group.setTitle("???????????????? ?? ????????????????????????????")

        self.tab_projects_area.setWidget(self.tab_projects_group)
        self.tab_tasks_left_area.setWidget(self.tab_tasks_left_group)
        self.tab_tasks_right_area.setWidget(self.tab_tasks_right_group)

    def init_btns(self):
        self.btns_group_open = QGroupBox()

        self.btn_project_new = QPushButton("?????????????? ?????????? ???????? ??????????????")
        self.btn_project_add = QPushButton("???????????????? ???????????? ???? ...")
        self.btn_project_based = QPushButton("?????????????? ???????????? ???? ???????????? ??????????????????????????")

        self.btn_group_open_layout.addWidget(self.btn_project_new)
        self.btn_group_open_layout.addWidget(self.btn_project_add)
        self.btn_group_open_layout.addWidget(self.btn_project_based)
    
    def parse_projects_folder(self):
        self.clear_table_layout(layout=self.tab_projects_layout)
        projects_list = os.listdir(classifier.PROJECTS_FOLDER_FULL_NAME)
        for project_short_name in projects_list:
            if project_short_name.find(classifier.HDF_POSTFIX) != -1:
                project_full_name = classifier.PROJECTS_FOLDER_FULL_NAME + '/' + project_short_name
                with h5py.File(project_full_name, 'r') as hdf:
                    project_name = hdf.attrs[classifier.HDF_FILE_NAME]
                    project_classes = hdf.attrs[classifier.HDF_FILE_CLASSES]
                    project_widget = project.project_as_widget(name=project_name, classes=project_classes, path=project_full_name, signal= self.signal_reparse)
                    self.tab_projects_layout.addWidget(project_widget)
    """
    def create_description(self, file_description=""): #??????????? ??????? ???????????????????????????? ?????????????????
        description = QLabel(file_description)
        self.main_layout.addWidget(description, 2, 1)
    """
    def on_create_new_project_clicked(self):
        self.dialog = segflex_new_project.new_project_dialog(self)
        self.dialog.signal1.connect(self.parse_projects_folder)
        self.dialog.exec_()

    def parse_tasks(self, project_path):
        self.clear_table_layout(layout=self.tab_tasks_left_layout)
        self.clear_table_layout(layout=self.tab_tasks_right_layout)
        with h5py.File(project_path, 'r') as hdf: #ATTRS???
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
            number_of_images = len(group_srcs.keys())
            for number in range(number_of_images):
                status = group_srcs[str(number)].attrs[classifier.HDF_TASK_STATUS]
                if status == classifier.HDF_TASK_STATUS_0 or status == classifier.HDF_TASK_STATUS_1:
                    task_widget = task_base.task_widget(path=project_path, identifier=number, mode=classifier.TASK_WIDGET_MODE_0, signal=self.signal_reparse)
                    self.tab_tasks_left_layout.addWidget(task_widget)
                if status == classifier.HDF_TASK_STATUS_2 or status == classifier.HDF_TASK_STATUS_3:
                    task_widget = task_base.task_widget(path=project_path, identifier=number, mode=classifier.TASK_WIDGET_MODE_1, signal=self.signal_reparse)
                    self.tab_tasks_right_layout.addWidget(task_widget)
            


    def clear_table_layout(self, layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)

    def check_create_projects_folder(self):
        if not os.path.exists(classifier.PROJECTS_FOLDER_FULL_NAME):
            os.mkdir(classifier.PROJECTS_FOLDER_FULL_NAME)

    
