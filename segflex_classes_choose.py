import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QDialog,
    QComboBox, QApplication, QListView, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog)
from PyQt5.QtCore import pyqtSignal, QObject

import segflex_classifier as classifier
import time
import os
import h5py
import cv2

class classes_choose(QDialog):
    signal1 = pyqtSignal()
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        classifier.current_project.classes.clear()

        self.adjust_window()
        self.create_place_combo_boxes()
        self.create_place_choose_buttons()
        self.create_place_choose_image_buttons()
        self.create_place_control_buttons()

    def on_btn_ok(self, event):
        classifier.time_start = time.localtime()
        classifier.time_last_change = time.localtime()
        self.create_new_project_file()
        self.signal1.emit()
        #print(classifier.current_project.classes)
        self.deleteLater()

    def create_new_project_file(self):
        folder_name = "/__projects" #дублирование 
        projects_dir = os.getcwd()
        projects_dir += folder_name
        project_name = projects_dir + '/' + classifier.current_project.name + classifier.HDF_POSTFIX  #classifier.current_project.name
        with h5py.File(project_name, 'w-') as hdf:
            hdf.attrs[classifier.HDF_FILE_ATTR_NAME] = classifier.current_project.name
            hdf.attrs[classifier.HDF_FILE_ATTR_TIME_C] = time.localtime()
            hdf.attrs[classifier.HDF_FILE_ATTR_TIME_U] = time.localtime()
            hdf.attrs[classifier.HDF_FILE_ATTR_DESCRIPTION] = classifier.current_project.description
            hdf.attrs[classifier.HDF_FILE_ATTR_CLASSES] = classifier.current_project.classes
            hdf.create_group(classifier.HDF_GROUP_SRCS_NAME)
            hdf.create_group(classifier.HDF_GROUP_FEATURES_NAME)
            image_group = hdf.require_group(classifier.HDF_GROUP_SRCS_NAME)
            identifier = 0
            for image_path in self.selected_images_list:
                print(image_path)
                image_as_numpy = cv2.imread(image_path)
                image_group.create_dataset(str(identifier), data=image_as_numpy)
                #dataset = image_group.require_dataset(str(identifier)) добавление атрибутов в датасет???
                identifier += 1

            #file_dialog = QFileDialog.getOpenFileName()[0]
            #print(file_dialog)
    
    def adjust_window(self):
        self.setWindowTitle("Выбор классов проекта")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
    
    def create_place_choose_image_buttons(self):
        self.selected_images = QLabel("Выбранные изображения: ")
        self.selected_images_list = []

        btn_add = QPushButton("Добавить изображение")
        btn_add.clicked.connect(self.add_images)

        selected_images_layout = QVBoxLayout()
        selected_images_layout.addWidget(self.selected_images)
        selected_images_layout.addWidget(btn_add)

        self.layout.addLayout(selected_images_layout)

    def add_images(self):
        file_dialog = QFileDialog.getOpenFileName()[0]
        if file_dialog not in self.selected_images_list:
            self.selected_images_list.append(file_dialog)
        images = " ".join(self.selected_images_list)
        self.selected_images.setText("Выбранные изображения: " + images)
        #print(self.selected_images_list)


    
    def create_place_choose_buttons(self):
        self.select_label = QLabel("Выбрано: ")
        btn_add = QPushButton("Добавить")
        btn_remove = QPushButton("Удалить")

        choose_layout = QVBoxLayout()
        choose_layout.addWidget(self.select_label)
        choose_layout.addWidget(btn_add)
        choose_layout.addWidget(btn_remove)

        btn_add.clicked.connect(self.on_btn_add)
        btn_remove.clicked.connect(self.on_btn_remove)

        self.layout.addLayout(choose_layout)        

    def create_place_control_buttons(self):
        btn_ok = QPushButton("Ок")
        btn_cancel = QPushButton("Отмена")

        control_layout = QHBoxLayout()
        control_layout.addWidget(btn_cancel)
        control_layout.addWidget(btn_ok)

        btn_ok.clicked.connect(self.on_btn_ok)

        self.layout.addLayout(control_layout)

    def create_place_combo_boxes(self):
        self.box_base = QComboBox(self)
        self.box_secondary = QComboBox(self)
        self.box_thirdly = QComboBox(self)

        combo_layout = QVBoxLayout()
        combo_layout.addWidget(self.box_base)
        combo_layout.addWidget(self.box_secondary)
        combo_layout.addWidget(self.box_thirdly)

        self.box_base.activated.connect(self.choose_secondary)
        self.box_secondary.activated.connect(self.choose_thirdly)

        self.box_base.addItems(classifier.code_base)

        self.layout.addLayout(combo_layout)

    def choose_secondary(self):
        self.box_secondary.clear()
        self.box_thirdly.clear()

        self.base_index = self.box_base.currentIndex()
        if self.base_index == 0:
            self.box_secondary.addItems(classifier.code_100)
        elif self.base_index == 1:
            self.box_secondary.addItems(classifier.code_200)
        elif self.base_index == 2:
            self.box_secondary.addItems(classifier.code_300)
        elif self.base_index == 3:
            self.box_secondary.addItems(classifier.code_400)

    def choose_thirdly(self):
        self.box_thirdly.clear()

        secondary_index = self.box_secondary.currentIndex()

        if self.base_index == 2 and secondary_index == 2:
            self.box_thirdly.addItems(classifier.code_320)
        elif self.base_index == 3 and secondary_index == 0:
            self.box_thirdly.addItems(classifier.code_490)
        elif self.base_index == 3 and secondary_index == 1:
            self.box_thirdly.addItems(classifier.code_410)
        elif self.base_index == 3 and secondary_index == 2:
            self.box_thirdly.addItems(classifier.code_420)
        elif self.base_index == 3 and secondary_index == 4:
            self.box_thirdly.addItems(classifier.code_440)
        elif self.base_index == 3 and secondary_index == 5:
            self.box_thirdly.addItems(classifier.code_450)
        elif self.base_index == 3 and secondary_index == 6:
            self.box_thirdly.addItems(classifier.code_460)

    def on_btn_add(self):
        text = self.box_thirdly.currentText()
        if text not in classifier.current_project.classes:
            classifier.current_project.classes.append(text)
        self.display_classes_list()

    def on_btn_remove(self):
        text = self.box_thirdly.currentText()
        if text in classifier.current_project.classes:
            classifier.current_project.classes.remove(text)
        self.display_classes_list()

    def display_classes_list(self):
        classifier.current_project.classes.sort()
        classes = " ".join(classifier.current_project.classes)
        self.select_label.setText("Выбрано: " + classes)
