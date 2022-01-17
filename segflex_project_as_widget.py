from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox)
import sys
"""
class project_as_object(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
"""

class project_as_widget(QGroupBox):
    def __init__(self, parent=None):
        QGroupBox.__init__(self, parent)

        layout = QHBoxLayout()
        layout_preview = QVBoxLayout()
        layout_info = QVBoxLayout()
        layout_status = QVBoxLayout()
        layout_jobs = QVBoxLayout()
        layout_actions =QVBoxLayout()

        layout.addLayout(layout_preview)
        layout.addLayout(layout_info)
        layout.addLayout(layout_status)
        layout.addLayout(layout_jobs)
        layout.addLayout(layout_actions)


        image = QLabel(self)
        pixmap = QtGui.QPixmap("image.jpg")
        image.setPixmap(pixmap)
        image.setFixedSize(100, 100)

        info_number = QLabel("#141999: Тест")
        info_created_by = QLabel("Created by Hashly on November 1st 2021")
        info_last_update = QLabel("Last updated 15 days ago")

        status = QLabel("Pending")

        jobs = QLabel("0 of 1 jobs")

        btn_open = QPushButton("Open")
        actions_bar = QComboBox()
        actions_bar.addItems(["do smth1", "do smth2"])


        layout_preview.addWidget(image)
        layout_info.addWidget(info_number)
        layout_info.addWidget(info_created_by)
        layout_info.addWidget(info_last_update)
        layout_status.addWidget(status)
        layout_jobs.addWidget(jobs)
        layout_actions.addWidget(btn_open)
        layout_actions.addWidget(actions_bar)



        self.setLayout(layout)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = project_as_object()
    w.show()
    sys.exit(app.exec_())

