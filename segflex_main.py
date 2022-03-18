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
        self.adjust_main_window()
        self.create_place_widgets_main_window()
        self.signal_reparse.connect(self.parse_tasks)

        #self.init_ui()
    
    def init_ui(self):
        self.check_create_projects_folder()
        self.create_layouts()
        self.fill_layouts()
        self.place_layouts()

        adjust_window()

    def create_layouts(self):
        self.main_layout = QGridLayout()
        #self.tab_projects_layout = QVBoxLayout()
        #self.tab_tasks_left_layout = QVBoxLayout()
        #self.tab_tasks_right_layout = QVBoxLayout()

    def fill_layouts(self):
        self.init_widgets()
        pass


    def place_layouts(self):
        self.main_frame.setLayout(self.main_layout)

        #self.tab.addTab(self.tab_project_area, "Проекты")
        #self.tab.addTab(self.tab_split, "Задачи")

        self.main_layout.addWidget(self.table, 0, 0, 4, 1)
        #self.tab.addTab(tab3, "Просмотр")
        
    def init_widgets(self):
        self.init_table()
        self.parse_table_projects()
        self.init_somebtns()


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

        self.tab_projects_group.setTitle("Проекты")
        self.tab_tasks_left_group.setTitle("Разметка")
        self.tab_tasks_right_group.setTitle("Контроль и редактирование")

        self.tab_projects_area.setWidget(self.tab_projects_group)
        self.tab_tasks_left_area.setWidget(self.tab_tasks_left_group)
        self.tab_tasks_right_area.setWidget(self.tab_tasks_right_group)

        self.tab_projects_layout = QVBoxLayout()
        self.tab_tasks_left_layout = QVBoxLayout()
        self.tab_tasks_right_layout = QVBoxLayout()

        self.tab_projects_group.setLayout(self.tab_projects_layout)
        self.tab_tasks_left_group.setLayout(self.tab_tasks_left_layout)
        self.tab_tasks_right_group.setLayout(self.tab_tasks_right_layout)

        self.tab.addTab(self.tab_projects_area, "Проекты")
        self.tab.addTab(self.tab_split, "Задачи")

        self.parse_projects_folder()


        self.tab.addTab(self.tab_projects_area, "Проекты")
        self.tab.addTab(self.tab_split, "Задачи")

        self.main_layout.addWidget(self.tab, 0, 0, 4, 1)


    def adjust_main_window(self):
        self.main_frame = QFrame()
        self.setCentralWidget(self.main_frame)
        self.main_layout = QGridLayout()
        self.main_frame.setLayout(self.main_layout)
        self.setWindowTitle("Segmentation app. 0.8")
        self.resize(1000, 400)

    """
    def parse_projects_folder(self):
        self.clear_table_layout(layout=self.layout_SArea)
        self.check_create_projects_folder()
        projects_list = os.listdir(classifier.PROJECTS_FOLDER_FULL_NAME)
        for project_short_name in projects_list:
            if project_short_name.find(classifier.HDF_POSTFIX) != -1:
                project_full_name = classifier.PROJECTS_FOLDER_FULL_NAME + '/' + project_short_name
                with h5py.File(project_full_name, 'r') as hdf: #ATTRS???
                    project_name = hdf.attrs[classifier.HDF_FILE_NAME]
                    project_classes = hdf.attrs[classifier.HDF_FILE_CLASSES]
                    #project_task_count = hdf.attrs[]
                    project_widget = project.project_as_widget(name=project_name, classes=project_classes, path=project_full_name, signal= self.signal_reparse)
                    #project_widget.signal_parse_tasks.connect(self.parse_tasks)
                    #self.signal_reparse.connect(self.parse_tasks)
                    self.layout_SArea.addWidget(project_widget)

    """

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


    def test_create_widget(self):
        self.project_widget = project.project_as_widget(name="asd", classes=[4,4,4])
        self.layout_SArea.addWidget(self.project_widget)


    def create_button_group(self):
        button_group = QGroupBox()

        btn1 = QPushButton("Создать новый файл проекта")
        btn2 = QPushButton("Добавить проект из ...")
        btn3 = QPushButton("Создать проект на основе существующего")

        layout = QVBoxLayout()
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        button_group.setLayout(layout)
        self.main_layout.addWidget(button_group, 1, 1)

        btn1.clicked.connect(self.on_create_new_project_clicked)
        #btn3.clicked.connect(self.test_create_widget)

    def create_button_group_2(self):
        button_group_2 = QGroupBox()

        btn1 = QPushButton("Параметры проекта")
        btn2 = QPushButton("Добавить изображение")
        btn3 = QPushButton("Удалить изображение")

        layout = QVBoxLayout()
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        button_group_2.setLayout(layout)
        self.main_layout.addWidget(button_group_2, 3, 1)

    def create_button_group_3(self):
        button_group_3 = QGroupBox()

        btn1 = QPushButton("Волков Илья. Редактор")

        layout = QHBoxLayout()
        layout.addWidget(btn1)
        button_group_3.setLayout(layout)
        self.main_layout.addWidget(button_group_3, 0, 1)

    def create_table(self):
        self.table = QTabWidget()
        
        self.scrollarea = QScrollArea(self)
        #self.scrollarea.setFixedWidth(250)
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget(self.scrollarea)
        self.scrollarea.setWidget(widget)
        #self.layout_SArea = QVBoxLayout(widget)
        self.layout_SArea = QVBoxLayout()
        widget.setLayout(self.layout_SArea)
        #self.layout_SArea.setParent(self.scrollarea)


        self.parse_projects_folder()

        #self.layout_SArea.addWidget(a1)
        #self.layout_SArea.addWidget(a2)
        #self.layout_SArea.addWidget(a3)
        #self.layout_SArea.addWidget(a4)
        #self.layout_SArea.addWidget(a5)
        #widget.setMinimumSize(600, 400)# //skukojivaet widgeti 
        #widget.adjustSize()
        self.scrollarea2 = QScrollArea(self)
        self.scrollarea2.setWidgetResizable(True)
        #widget2 = QWidget(self.scrollarea2)
        widget2 = QGroupBox(self.scrollarea2)
        widget2.setTitle("Разметка")
        
        self.scrollarea2.setWidget(widget2)
        self.layout_tasks_box = QVBoxLayout(widget2)
        #self.parse_tasks()

        self.scrollarea3 = QScrollArea(self)
        self.scrollarea3.setWidgetResizable(True)
        #widget3 = QWidget(self.scrollarea3)
        widget3 = QGroupBox(self.scrollarea3)
        widget3.setTitle("Контроль и редактирование")
        self.scrollarea3.setWidget(widget3)
        self.layout_tasks_box2 = QVBoxLayout(widget3)

        tab2 = QWidget()
        tab3 = QWidget()

        split = QSplitter()
        split.addWidget(self.scrollarea2)
        split.addWidget(self.scrollarea3)

        self.table.addTab(self.scrollarea, "Проекты")
        self.table.addTab(split, "Задачи")
        self.table.addTab(tab3, "Просмотр")

        #self.main_layout.addWidget(self.scrollarea, 1, 0, 3, 1)
        self.main_layout.addWidget(self.table, 0, 0, 4, 1)

    def create_description(self, file_description=""): #рамка? фон? форматирование описания?
        description = QLabel(file_description)
        self.main_layout.addWidget(description, 2, 1)

    def on_create_new_project_clicked(self):
        self.dialog = segflex_new_project.new_project_dialog(self)
        #self.dialog.signal1.connect(self.create_new_project_file())
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
                #task_widget.signal_reparse.connect(self.callreparse(project_path))
            #self.table.setCurrentWidget(self.scrollarea2)
            
        print(number_of_images, " _2_ ", project_path)


    def create_place_widgets_main_window(self):
        self.create_button_group()
        #self.create_button_group_2()
        self.create_button_group_3()
        #self.create_table()
        self.init_table()
        #self.create_description("Here must be project description")


    def clear_table_layout(self, layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)

    def check_create_projects_folder(self):
        if not os.path.exists(classifier.PROJECTS_FOLDER_FULL_NAME):
            os.mkdir(classifier.PROJECTS_FOLDER_FULL_NAME)

    
