from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox)

import segflex_new_project
import segflex_project_as_object as project

class AnyObjects(QObject):
    # создаем свой сигнал
    own_signal = pyqtSignal()


class main_window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, flags=QtCore.Qt.Window)
        
        self.adjust_main_window()
        self.set_params()
        self.create_place_widgets_main_window()

    def set_params(self):
        self.ao = AnyObjects()
        # обработчик сигнала, связанного с объектом
        self.ao.own_signal.connect(self.on_clicked)
        # параметры главного окна

    def on_clicked(self):
        print('Тут сообщение')

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
        
        a1 = project.project_as_object(self)
        a2 = project.project_as_object(self)
        a3 = project.project_as_object(self)
        a4 = project.project_as_object(self)
        a5 = project.project_as_object(self)



        self.scrollarea = QScrollArea(self)
        #self.scrollarea.setFixedWidth(250)
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget(self.scrollarea)
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)

        self.layout_SArea.addWidget(a1)
        self.layout_SArea.addWidget(a2)
        self.layout_SArea.addWidget(a3)
        self.layout_SArea.addWidget(a4)
        self.layout_SArea.addWidget(a5)
        widget.setMinimumSize(600, 400)
        #widget.adjustSize()

        tab2 = QWidget()
        tab3 = QWidget()

        table.addTab(self.scrollarea, "Проект")
        table.addTab(tab2, "Редактирование")
        table.addTab(tab3, "Просмотр")

        #self.main_layout.addWidget(self.scrollarea, 1, 0, 3, 1)
        self.main_layout.addWidget(table, 1, 0, 3, 1)

    def create_table1(self): #QTabBar - более общий
        table = QTabWidget()


        #tab1 = QWidget()
        tab1 = QGroupBox()

        layout1 = QVBoxLayout()


        a1 = project.project_as_object(self)
        a2 = project.project_as_object(self)
        a3 = project.project_as_object(self)
        a4 = project.project_as_object(self)
        a5 = project.project_as_object(self)
        a6 = project.project_as_object(self)
        
        #tab1.setLayout(layout1)

        #b1 = QPushButton("asd")
        #b2 = QLabel("sd")
        #layout1.addWidget(b1)
        #layout1.addWidget(b2)

        #layout1.addWidget(a1)
        #layout1.addWidget(a2)
        #layout1.addWidget(a3)
        #layout1.addWidget(a4)
        #layout1.addWidget(a5)
        #layout1.addWidget(a6)


        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setWidget(tab1)
        layout_small = QVBoxLayout(tab1)

        layout_small.addWidget(a1)
        layout_small.addWidget(a2)
        layout_small.addWidget(a3)
        layout_small.addWidget(a4)
        layout_small.addWidget(a5)
        layout_small.addWidget(a6)

        tab2 = QWidget()
        tab3 = QWidget()

        table.addTab(tab1, "Проект")
        table.addTab(tab2, "Редактирование")
        table.addTab(tab3, "Просмотр")

        table.setMinimumWidth(600)
        table.adjustSize()
        self.main_layout.addWidget(table, 1, 0, 3, 1)

    def create_description(self, file_description=""): #рамка? фон? форматирование описания?
        description = QLabel(file_description)
        self.main_layout.addWidget(description, 2, 1)

    def on_create_new_project_clicked(self):
        dialog = segflex_new_project.new_project_dialog(self)
        dialog.exec_()

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

