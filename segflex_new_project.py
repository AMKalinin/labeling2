from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy)

import segflex_classes_choose
from PyQt5.QtCore import pyqtSignal
import segflex_main
import segflex_classifier as classifier
import os


class new_project_dialog(QDialog): #qformlayout???
    signal1 = pyqtSignal()
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        #print(segflex_main.ggg)
        self.adjust_window()
        self.create_place_buttons()

    def create_place_buttons(self):
        btn_cancel = QPushButton("Отмена")
        self.btn_ok = QPushButton("ОК")
        label_name = QLabel("Название проекта:")
        #label_path = QLabel("Путь хранения:")
        label_description = QLabel("Описание проекта:")
        self.text_area_name = QLineEdit()
        self.text_area_description = QLineEdit()
        #text_area_path = QLineEdit()

        self.text_area_name.editingFinished.connect(self.set_project_name)
        self.text_area_description.editingFinished.connect(self.set_project_description)

        btn_cancel.clicked.connect(self.on_cancel)
        self.btn_ok.clicked.connect(self.on_seg_class_choose)

        layout_buttons = QHBoxLayout()
        layout_name = QHBoxLayout()
        layout_path = QHBoxLayout()
        layout_description = QHBoxLayout()

        layout_buttons.addWidget(btn_cancel)
        layout_buttons.addWidget(self.btn_ok)
        layout_name.addWidget(label_name)
        layout_name.addWidget(self.text_area_name)

        layout_description.addWidget(label_description)
        layout_description.addWidget(self.text_area_description)
        
        #layout_path.addWidget(label_path)
        #layout_path.addWidget(text_area_path)

        self.layout.addLayout(layout_name)
        self.layout.addLayout(layout_description)
        #self.layout.addLayout(layout_path)
        self.layout.addLayout(layout_buttons)

    def check_project_name(self):
        folder_name = "/__projects" #дублируется в мейне
        projects_dir = os.getcwd()
        projects_dir += folder_name
        projects_list = os.listdir(projects_dir)
        if self.text_area_name.text() + '.hdf5' in projects_list:
            self.btn_ok.setDisabled(True)
        else:
            self.btn_ok.setEnabled(True)
            

    def set_project_name(self):
        self.check_project_name()
        classifier.current_project.name = self.text_area_name.text()
        print(classifier.current_project.name)
    
    def set_project_description(self):
        classifier.current_project.description = self.text_area_description.text()
        print(classifier.current_project.description)


    def adjust_window(self):
        self.setWindowTitle("Создание нового проекта")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def on_seg_class_choose(self):
        dialog = segflex_classes_choose.classes_choose(self)
        dialog.signal1.connect(self.gosignal)
        dialog.exec_()

    def gosignal(self):
        self.signal1.emit()
        self.deleteLater()

    def on_cancel(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.close()



