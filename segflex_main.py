from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox,
                            QFileDialog)

import segflex_new_project
import segflex_project_as_widget as project
import os
import json
import segflex_classifier as classifier
import h5py
import time


class main_window(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, flags=QtCore.Qt.Window)

        #super(main_window, self).__init__( parent) #? toje rabotaet

        self.adjust_main_window()
        #self.check_projects_folder()
        self.create_place_widgets_main_window()

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)


    def parse_projects_folder(self):
        self.clear_layout(layout=self.layout_SArea)
        #for i in reversed(range(self.layout_SArea.count())): 
         #   self.layout_SArea.itemAt(i).widget().setParent(None)
        folder_name = "/__projects"
        projects_dir = os.getcwd()
        projects_dir += folder_name
        if not os.path.exists(projects_dir):
            os.mkdir(path_dir)
            return 
        projects_list = os.listdir(projects_dir)
        if not projects_list:
            return
        for project_name in projects_list:
            if project_name.find(classifier.HDF_POSTFIX) > 0: #and project_name.find("project") != -1:
                project_full_name = projects_dir + '/' + project_name
                with h5py.File(project_full_name, 'r') as hdf: #ATTRS???
                    to_project_name = hdf.attrs[classifier.HDF_FILE_ATTR_NAME]
                    to_project_classes = hdf.attrs[classifier.HDF_FILE_ATTR_CLASSES]
                    project_widget = project.project_as_widget(name=to_project_name, classes=to_project_classes, path=project_full_name)
                    self.layout_SArea.addWidget(project_widget)

    #def add_project_widget(self):


            """
            for key, value in d.items():
                if key == "Name project":
                    to_project_name = value
                elif key == "List classes":
                    to_project_classes = value
                elif key == "project ID":
                    to_project_id = value
            project_widget = project.project_as_widget(name=to_project_name, classes=to_project_classes)
            self.layout_SArea.addWidget(project_widget)
            f.close()
            """

    def test2_create_widget(self, srcs_classes=[]):
        self.project_widget = project.project_as_widget(name="asd", classes=classifier.current_project.classes)
        self.layout_SArea.addWidget(self.project_widget)


    def test_create_widget(self):
        self.project_widget = project.project_as_widget(name="asd", classes=[4,4,4])
        self.layout_SArea.addWidget(self.project_widget)
    """
    def create_new_project_file(self):
        folder_name = "/__projects" #дублирование 
        projects_dir = os.getcwd()
        projects_dir += folder_name
        project_name = projects_dir + '/' + "testname" + classifier.HDF_POSTFIX  #classifier.current_project.name
        with h5py.File(project_name, 'w-') as hdf:
            hdf.attrs[classifier.HDF_FILE_ATTR_NAME] = classifier.current_project.name
            hdf.attrs[classifier.HDF_FILE_ATTR_TIME_C] = time.localtime()
            hdf.attrs[classifier.HDF_FILE_ATTR_TIME_U] = time.localtime()
            hdf.attrs[classifier.HDF_FILE_ATTR_DESCRIPTION] = classifier.current_project.description
            hdf.create_group(classifier.HDF_GROUP_SRCS_NAME)
            hdf.create_group(classifier.HDF_GROUP_FEATURES_NAME)
            image_index = 0
            image_group = hdf.require_group(classifier.HDF_GROUP_SRCS_NAME)
            file_dialog = QFileDialog.getOpenFileName()[0]
            print(file_dialog)
        #pass
    """

    def create_button_group(self):
        button_group = QGroupBox()

        btn1 = QPushButton("Создать новый проект")
        btn2 = QPushButton("Открыть проект")
        btn3 = QPushButton("Создать проект на основе существующего")

        layout = QVBoxLayout()
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        button_group.setLayout(layout)
        self.main_layout.addWidget(button_group, 1, 1)

        btn1.clicked.connect(self.on_create_new_project_clicked)
        btn3.clicked.connect(self.test_create_widget)

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
        table = QTabWidget()
        
        #a1 = project.project_as_widget(name="create_table", classes=[1,2,3])
        #a2 = project.project_as_widget(name="create_table", classes=[1,2,3])
        #a3 = project.project_as_widget(self)
        #a4 = project.project_as_widget(self)
        #a5 = project.project_as_widget(self)



        self.scrollarea = QScrollArea(self)
        #self.scrollarea.setFixedWidth(250)
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget(self.scrollarea)
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)


        self.parse_projects_folder()

        #self.layout_SArea.addWidget(a1)
        #self.layout_SArea.addWidget(a2)
        #self.layout_SArea.addWidget(a3)
        #self.layout_SArea.addWidget(a4)
        #self.layout_SArea.addWidget(a5)
        #widget.setMinimumSize(600, 400)# //skukojivaet widgeti 
        #widget.adjustSize()

        tab2 = QWidget()
        tab3 = QWidget()

        table.addTab(self.scrollarea, "Проект")
        table.addTab(tab2, "Редактирование")
        table.addTab(tab3, "Просмотр")

        #self.main_layout.addWidget(self.scrollarea, 1, 0, 3, 1)
        self.main_layout.addWidget(table, 1, 0, 3, 1)

    def create_description(self, file_description=""): #рамка? фон? форматирование описания?
        description = QLabel(file_description)
        self.main_layout.addWidget(description, 2, 1)

    def reparse(self):
        self.parse_projects_folder()

    def on_create_new_project_clicked(self):
        self.dialog = segflex_new_project.new_project_dialog(self)
        #self.dialog.signal1.connect(self.create_new_project_file())
        self.dialog.signal1.connect(self.parse_projects_folder)
        self.dialog.exec_()

    def create_place_widgets_main_window(self):
        self.create_button_group()
        self.create_button_group_2()
        self.create_button_group_3()
        self.create_table()
        self.create_description("Here must be project description")


    def adjust_main_window(self):
        main_frame = QFrame()
        self.setCentralWidget(main_frame)
        self.setWindowTitle("Segmentation app. 0.3")
        self.resize(1000, 400)

        self.main_layout = QGridLayout()
        main_frame.setLayout(self.main_layout)

