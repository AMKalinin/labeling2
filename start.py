from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu)
import sys


class NewProjectSegClassChoose(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle("Выбор классов разметки")

        layout_big = QVBoxLayout()
        layout_buttons = QHBoxLayout()
        layout_frames = QHBoxLayout()

        btn_cancel = QPushButton("Отмена")
        btn_ok = QPushButton("ОК")

        frame_left = QWidget()
        frame_right = QWidget()

        layout_frames.addWidget(frame_left)
        layout_frames.addWidget(frame_right)
        layout_buttons.addWidget(btn_cancel)
        layout_buttons.addWidget(btn_ok)
        layout_big.addLayout(layout_frames)
        layout_big.addLayout(layout_buttons)

        self.setLayout(layout_big)


class NewProjectDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle("Создание нового проекта")

        btn_cancel = QPushButton("Отмена")
        btn_ok = QPushButton("ОК")

        label_name = QLabel("Название проекта:")
        label_path = QLabel("Путь хранения:")

        text_area_name = QLineEdit()
        text_area_path = QLineEdit()

        layout_buttons = QHBoxLayout()
        layout_big = QVBoxLayout()
        layout_name = QHBoxLayout()
        layout_path = QHBoxLayout()

        layout_buttons.addWidget(btn_cancel)
        layout_buttons.addWidget(btn_ok)
        layout_name.addWidget(label_name)
        layout_name.addWidget(text_area_name)
        layout_path.addWidget(label_path)
        layout_path.addWidget(text_area_path)
        layout_big.addLayout(layout_name)
        layout_big.addLayout(layout_path)
        layout_big.addLayout(layout_buttons)

        btn_ok.clicked.connect(self.on_seg_class_choose)

        self.setLayout(layout_big)

    def on_seg_class_choose(self):
        dialog = NewProjectSegClassChoose(self)
        dialog.exec_()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, flags=QtCore.Qt.Window)
        self.setWindowTitle("Segmentation app. 0.3")

        #задаем главный виджет главного окна
        mainFrame = QFrame()

        self.setCentralWidget(mainFrame)

        #инициализируем виджеты
        self.createButtonGroup()
        self.createButtonGroup2()
        self.createTable()
        self.createDescription("Here must be project description")
        self.createButtonGroup3()

        mainLayout = QGridLayout()

        #помещаем виджеты на 0 столбец
        #растягиваем таблицу на 3 слота вниз       
        mainLayout.addWidget(self.Table, 1, 0, 3, 1)


        #помещаем виджеты на 1 столбец
        mainLayout.addWidget(self.ButtonGroup3, 0, 1)
        mainLayout.addWidget(self.ButtonGroup, 1, 1)
        mainLayout.addWidget(self.Description, 2, 1)
        mainLayout.addWidget(self.ButtonGroup2, 3, 1)

        mainFrame.setLayout(mainLayout)

    def createButtonGroup(self):
        self.ButtonGroup = QGroupBox()

        btn1 = QPushButton("Создать новый проект")
        btn2 = QPushButton("Открыть проект")
        btn3 = QPushButton("Создать проект на основе существующего") #- функционал должен перейти в создать новый

        layout = QVBoxLayout()
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)

        btn1.clicked.connect(self.on_create_new_project_clicked)

        self.ButtonGroup.setLayout(layout)

    def createButtonGroup2(self):
        self.ButtonGroup2 = QGroupBox()

        btn1 = QPushButton("Параметры проекта")
        btn2 = QPushButton("Добавить изображение")
        btn3 = QPushButton("Удалить изображение")

        layout = QVBoxLayout()
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)

        self.ButtonGroup2.setLayout(layout)

    def createButtonGroup3(self):
        self.ButtonGroup3 = QGroupBox()

        btn1 = QPushButton("Волков Илья. Редактор")
        layout = QHBoxLayout()
        layout.addWidget(btn1)

        self.ButtonGroup3.setLayout(layout)


    def createTable(self): #QTabBar - более общий
        self.Table = QTabWidget()

        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        self.Table.addTab(tab1, "Проект")
        self.Table.addTab(tab2, "Редактирование")
        self.Table.addTab(tab3, "Просмотр")

        self.Table.setMinimumWidth(600)
        self.Table.adjustSize()

    def createDescription(self, file_description=""): #рамка? фон? форматирование описания?
        self.frameDescription = QFrame()
        self.Description = QLabel(self.frameDescription)
        self.Description.setText(file_description)
        
    def on_create_new_project_clicked(self):
        dialog = NewProjectDialog(self)
        dialog.exec_()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())