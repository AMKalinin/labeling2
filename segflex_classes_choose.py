"""
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
import regex as re

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
        projects_dir = classifier.PROJECTS_FOLDER_FULL_NAME
        project_name = projects_dir + '/' + classifier.current_project.name + classifier.HDF_POSTFIX  #classifier.current_project.name
        with h5py.File(project_name, 'w-') as hdf:
            hdf.attrs[classifier.HDF_FILE_NAME] = classifier.current_project.name
            hdf.attrs[classifier.HDF_FILE_TIME_C] = time.localtime()
            hdf.attrs[classifier.HDF_FILE_TIME_U] = time.localtime()
            hdf.attrs[classifier.HDF_FILE_DESCRIPTION] = classifier.current_project.description
            hdf.attrs[classifier.HDF_FILE_CLASSES] = classifier.current_project.classes
            hdf.create_group(classifier.HDF_GROUP_SRCS_NAME)
            hdf.create_group(classifier.HDF_GROUP_FEATURES_NAME)
            #hdf.create_group(classifier.HDF_GROUP_OBJECT_LAYERS_NAME)
            image_group = hdf.require_group(classifier.HDF_GROUP_SRCS_NAME)
            identifier = 0
            for image_path in self.selected_images_list:
                print(image_path)
                image_as_numpy = cv2.imread(image_path) # neef check for supporting formats
                print(image_as_numpy.shape)
                image_group.create_dataset(str(identifier), data=image_as_numpy)
                image_srcs = image_group[str(identifier)]
                image_srcs.attrs[classifier.HDF_TASK_POLYGON_COUNT] = 0
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
        file_dialog_response = QFileDialog.getOpenFileName()[0]
        match = re.search(r'\p{IsCyrillic}', file_dialog_response) 
        assert match == None, 'cv2.imread need english file name'
        if file_dialog_response not in self.selected_images_list:
            self.selected_images_list.append(file_dialog_response)
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
"""

import sys
from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem, QWidget, QLabel, QDialog,
    QComboBox, QApplication, QListView, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog)
from PyQt5.QtCore import pyqtSignal, QObject, Qt

import segflex_classifier as classifier
import time
import os
import h5py
import cv2
import regex as re
import segflex_classes_treeWidget as treeWidget

class classes_choose(QDialog):
    signal1 = pyqtSignal()
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        classifier.current_project.classes.clear()

        self.adjust_window()
        self.create_place_tree()
        self.create_place_choose_image_buttons()
        self.create_place_control_buttons()

    def on_btn_ok(self, event):
        #classifier.time_start = time.localtime()
        #classifier.time_last_change = time.localtime()
        self.create_new_project_file()
        self.signal1.emit()
        #print(classifier.current_project.classes)
        self.deleteLater()
    
    def create_new_project_file(self): 
        projects_dir = classifier.PROJECTS_FOLDER_FULL_NAME
        project_name = projects_dir + '/' + classifier.current_project.name + classifier.HDF_POSTFIX  #classifier.current_project.name
        with h5py.File(project_name, 'w-') as hdf:
            hdf.attrs[classifier.HDF_FILE_NAME] = classifier.current_project.name
            hdf.attrs[classifier.HDF_FILE_TIME_C] = time.localtime()
            hdf.attrs[classifier.HDF_FILE_TIME_U] = time.localtime()
            hdf.attrs[classifier.HDF_FILE_DESCRIPTION] = classifier.current_project.description
            hdf.attrs[classifier.HDF_FILE_CLASSES] = classifier.current_project.classes
            hdf.attrs[classifier.HDF_FILE_TASK_COUNT] = 0
            hdf.create_group(classifier.HDF_GROUP_SRCS_NAME)
            hdf.create_group(classifier.HDF_GROUP_FEATURES_NAME)
            image_group = hdf.require_group(classifier.HDF_GROUP_SRCS_NAME)
            identifier = 0
            for image_path in self.selected_images_list:
                print(image_path)
                image_as_numpy = cv2.imread(image_path) # neef check for supporting formats
                print(image_as_numpy.shape)
                image_group.create_dataset(str(identifier), data=image_as_numpy)
                #dataset = image_group.require_dataset(str(identifier)) добавление атрибутов в датасет???
                identifier += 1
                hdf.attrs[classifier.HDF_FILE_TASK_COUNT] += 1

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
        file_dialog_response = QFileDialog.getOpenFileName()[0]
        match = re.search(r'\p{IsCyrillic}', file_dialog_response) 
        assert match == None, 'cv2.imread need english file name'
        if file_dialog_response not in self.selected_images_list:
            self.selected_images_list.append(file_dialog_response)
        images = " ".join(self.selected_images_list)
        self.selected_images.setText("Выбранные изображения: " + images)
        #print(self.selected_images_list)


    def create_place_control_buttons(self):
        btn_ok = QPushButton("Ок")
        btn_cancel = QPushButton("Отмена")

        control_layout = QHBoxLayout()
        control_layout.addWidget(btn_cancel)
        control_layout.addWidget(btn_ok)

        btn_ok.clicked.connect(self.on_btn_ok)

        self.layout.addLayout(control_layout)

    def create_place_tree(self):
        self.tree_all_class = treeWidget.allTree(self)
        self.tree_all_class.setColumnCount(2)
        self.tree_all_class.setHeaderLabels(['Name', 'Code'])
        self.filling_tree_all_class(self.tree_all_class)

        self.tree_selected_class = treeWidget.selectedTree(self)
        self.tree_selected_class.setAcceptDrops(True)
        self.tree_selected_class.setColumnCount(2)
        self.tree_selected_class.setHeaderLabels(['Name', 'Code'])

        btn_select_class = QPushButton("Добавить")
        btn_select_class.clicked.connect(self.on_btn_add)
        btn_remove_class = QPushButton("Удалить")
        btn_remove_class.clicked.connect(self.on_btn_remove)

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(btn_select_class)
        btn_layout.addWidget(btn_remove_class)

        combo_layout = QHBoxLayout()

        combo_layout.addWidget(self.tree_all_class)
        combo_layout.addLayout(btn_layout)
        combo_layout.addWidget(self.tree_selected_class)

        self.layout.addLayout(combo_layout)

    def filling_tree_all_class(self, tree):

        tmp1 = QTreeWidgetItem([classifier.code_base[0]])
        tmp2 = QTreeWidgetItem([classifier.code_base[1]])
        tmp3 = QTreeWidgetItem([classifier.code_base[2]])
        tmp4 = QTreeWidgetItem([classifier.code_base[3]])

        def add_child(tr, s):
            for child in s:
                a = QTreeWidgetItem([child[4:], child[:3]])
                tr.addChild(a)
                if child == classifier.code_300[2]:
                    add_child(a, classifier.code_320)
                if child == classifier.code_400[1]:
                    add_child(a, classifier.code_410)
                if child == classifier.code_400[2]:
                    add_child(a, classifier.code_420)
                if child == classifier.code_400[4]:
                    add_child(a, classifier.code_440)
                if child == classifier.code_400[5]:
                    add_child(a, classifier.code_450)
                if child == classifier.code_400[6]:
                    add_child(a, classifier.code_460)

        add_child(tmp1, classifier.code_100)
        add_child(tmp2, classifier.code_200)
        add_child(tmp3, classifier.code_300)
        add_child(tmp4, classifier.code_400)
        tree.addTopLevelItem(tmp1)
        tree.addTopLevelItem(tmp2)
        tree.addTopLevelItem(tmp3)
        tree.addTopLevelItem(tmp4)

    def on_btn_add(self):

        def get_parent(item):
            if item.parent() is None:
                return QTreeWidgetItem([item.text(0), item.text(1)])
            return get_parent(item.parent())

        def struct(tree, item):
            match = tree.findItems(item.text(1)[0], Qt.MatchStartsWith | Qt.MatchRecursive, 1)
            if len(match) > 0:
                match[0].parent().addChild(QTreeWidgetItem([item.text(0), item.text(1)]))
                return 1
            return 0

        it = self.tree_all_class.currentItem()
        if self.tree_all_class.indexOfTopLevelItem(it) >= 0:
            return
        text = it.text(1) + '_' + it.text(0)
        if text not in classifier.current_project.classes:
            classifier.current_project.classes.append(text)
            if struct(self.tree_selected_class, it) == 0:
                par = get_parent(it)
                par.addChild(QTreeWidgetItem([it.text(0), it.text(1)]))
                self.tree_selected_class.addTopLevelItem(par)
                self.tree_selected_class.expandItem(par)
                self.tree_selected_class.setCurrentItem(par)

    def on_btn_remove(self):
        it = self.tree_selected_class.currentItem()
        if it is None:
            return
        if it.parent() is None:
            ind = self.tree_selected_class.indexOfTopLevelItem(it)
            for i in range(it.childCount()):
                text = it.child(i).text(1) + '_' + it.child(i).text(0)
                if text in classifier.current_project.classes:
                    classifier.current_project.classes.remove(text)
            self.tree_selected_class.takeTopLevelItem(ind)
        else:
            text = it.text(1) + '_' + it.text(0)
            if text in classifier.current_project.classes:
                classifier.current_project.classes.remove(text)
                if it.parent().childCount() <= 1:
                    ind = self.tree_selected_class.indexOfTopLevelItem(it.parent())
                    self.tree_selected_class.takeTopLevelItem(ind)
                    return
                it.parent().removeChild(it)
