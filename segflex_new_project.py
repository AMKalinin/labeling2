from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy)

import segflex_classes_choose
from PyQt5.QtCore import pyqtSignal
import segflex_main


class new_project_dialog(QDialog): #qformlayout???
    signal1 = pyqtSignal()
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        #print(segflex_main.ggg)
        self.adjust_window()
        self.create_place_buttons()

    def create_place_buttons(self):
        btn_cancel = QPushButton("Отмена")
        btn_ok = QPushButton("ОК")
        label_name = QLabel("Название проекта:")
        label_path = QLabel("Путь хранения:")
        text_area_name = QLineEdit()
        text_area_path = QLineEdit()

        btn_cancel.clicked.connect(self.on_cancel)
        btn_ok.clicked.connect(self.on_seg_class_choose)

        layout_buttons = QHBoxLayout()
        layout_name = QHBoxLayout()
        layout_path = QHBoxLayout()

        layout_buttons.addWidget(btn_cancel)
        layout_buttons.addWidget(btn_ok)
        layout_name.addWidget(label_name)
        layout_name.addWidget(text_area_name)
        layout_path.addWidget(label_path)
        layout_path.addWidget(text_area_path)

        self.layout.addLayout(layout_name)
        self.layout.addLayout(layout_path)
        self.layout.addLayout(layout_buttons)

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



