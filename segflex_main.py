from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy)

import segflex_new_project

class main_window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, flags=QtCore.Qt.Window)
        
        self.adjust_main_window()
        self.create_place_widgets_main_window()

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

    def create_table(self): #QTabBar - более общий
        table = QTabWidget()

        tab1 = QWidget()
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

        self.main_layout = QGridLayout()
        main_frame.setLayout(self.main_layout)

