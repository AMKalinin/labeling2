from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox,
                            QFileDialog)

import segflex_new_project
import segflex_project_as_widget as project
import segflex_task_as_widget as task
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
                    project_widget = project.project_as_widget(name=project_name, classes=project_classes, path=project_full_name)
                    project_widget.signal_parse_tasks.connect(self.parse_tasks)
                    self.layout_SArea.addWidget(project_widget)


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
        self.scrollarea2 = QScrollArea(self)
        self.scrollarea2.setWidgetResizable(True)
        widget2 = QWidget(self.scrollarea2)
        self.scrollarea2.setWidget(widget2)
        self.layout_tasks_box = QVBoxLayout(widget2)
        #self.parse_tasks()

        tab2 = QWidget()
        tab3 = QWidget()

        self.table.addTab(self.scrollarea, "Проекты")
        self.table.addTab(self.scrollarea2, "Задачи")
        self.table.addTab(tab3, "Просмотр")

        #self.main_layout.addWidget(self.scrollarea, 1, 0, 3, 1)
        self.main_layout.addWidget(self.table, 1, 0, 3, 1)

    def create_description(self, file_description=""): #рамка? фон? форматирование описания?
        description = QLabel(file_description)
        self.main_layout.addWidget(description, 2, 1)

    def on_create_new_project_clicked(self):
        self.dialog = segflex_new_project.new_project_dialog(self)
        #self.dialog.signal1.connect(self.create_new_project_file())
        self.dialog.signal1.connect(self.parse_projects_folder)
        self.dialog.exec_()

    def parse_tasks(self, project_path):
        self.clear_table_layout(layout=self.layout_tasks_box)
        with h5py.File(project_path, 'r') as hdf: #ATTRS???
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
            number_of_images = len(group_srcs.keys())
            for number in range(number_of_images):
                task_widget = task.task_as_widget(classes=[], path=project_path, identifier=number)
                self.layout_tasks_box.addWidget(task_widget)
            self.table.setCurrentWidget(self.scrollarea2)
            print(number_of_images, " __ ", project_path)


    """
    def open_image(self, identifier): 
        self.clear_window_layout(self.image_layout)
        self.display = seg_label.Label()
        self.display.setFixedSize(600,600)
        with h5py.File(self.project_path, 'r') as hdf:
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
            self.display.update_base(image_as_pixmap)
            self.image_layout.addWidget(self.display)
    """
    """
    def parse_projects_folder(self):
        self.clear_table_layout(layout=self.layout_SArea)
        self.check_create_projects_folder()
        projects_list = os.listdir(classifier.PROJECTS_FOLDER_FULL_NAME)
        for project_short_name in projects_list:
            if project_short_name.find(classifier.HDF_POSTFIX) != -1:
                project_full_name = classifier.PROJECTS_FOLDER_FULL_NAME + '/' + project_short_name
                with h5py.File(project_full_name, 'r') as hdf: #ATTRS???
                    to_project_name = hdf.attrs[classifier.HDF_FILE_NAME]
                    to_project_classes = hdf.attrs[classifier.HDF_FILE_ATTR_CLASSES]
                    project_widget = project.project_as_widget(name=to_project_name, classes=to_project_classes, path=project_full_name)
                    self.layout_SArea.addWidget(project_widget)
    """

    def create_place_widgets_main_window(self):
        self.create_button_group()
        #self.create_button_group_2()
        self.create_button_group_3()
        self.create_table()
        #self.create_description("Here must be project description")


    def adjust_main_window(self):
        main_frame = QFrame()
        self.setCentralWidget(main_frame)
        self.setWindowTitle("Segmentation app. 0.8")
        self.resize(1000, 400)

        self.main_layout = QGridLayout()
        main_frame.setLayout(self.main_layout)


    def clear_table_layout(self, layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)

    def check_create_projects_folder(self):
        if not os.path.exists(classifier.PROJECTS_FOLDER_FULL_NAME):
            os.mkdir(classifier.PROJECTS_FOLDER_FULL_NAME)

    
