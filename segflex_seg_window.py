from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QPoint#, QVector
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                            QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                            QPlainTextEdit, QLineEdit, QMenu,
                            QScrollArea, QToolButton, QSizePolicy, QComboBox, QToolBar, 
                            QStatusBar)

from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor, QFont, QBrush, QPen, QPolygon

import os
import h5py
import numpy as np
import cv2
import segflex_classifier as classifier
import segflex_draw_window as draw
import re
from ast import literal_eval as make_tuple
import time


class myLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.base_pixmap = QPixmap()
        self.overlayed_pixmap = QPixmap()
        self.toggle_show_hide_mask = False
        self.polygon = QPolygon()

    def update_base(self, pixmap):
        self.base_pixmap = pixmap
        self.overlayed_pixmap = pixmap
        self.update()

    def mousePressEvent(self, event):
        print(event.button())
        self.update()

    def overlay_mask(self, polygon):
        print("overlay called")
        self.toggle_show_hide_mask = True
        self.polygon = polygon
        self.repaint()

    def restore_srcs(self):
        print("restore called")
        self.toggle_show_hide_mask = False
        self.repaint()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap()
        if self.toggle_show_hide_mask:
            pixmap = self.overlayed_pixmap
        else:
            pixmap = self.base_pixmap
        if self.toggle_show_hide_mask:
            painter2 = QPainter(pixmap)
            painter2.drawPolygon(self.polygon)
            self.overlayed_pixmap = pixmap
            self.toggle_toggle()
        painter.drawPixmap(0, 0, pixmap)

    def toggle_toggle(self):
        if self.toggle_show_hide_mask:
            self.toggle_show_hide_mask = False
        else:
            self.toggle_show_hide_mask = True


class seg_window(QDialog):
    def __init__(self, parent=None, path=None):
        QDialog.__init__(self, parent)
        self.project_path = path
        self.identifier = 0
        self.current_image_position = 1
       
        self.adjust_window()
        self.open_images_dir()
        self.open_image(self.identifier)
        self.create_navigation_bar()
        self.create_instruments_bar()
        self.create_control_btns()
        self.draw_pencil_instruments()
        print("shallow pixmap = ",id(self.display.pixmap()), id(self.display))
        
    def create_control_btns(self):
        edit_btn = QPushButton("Сегментировать")
        edit_btn.clicked.connect(self.on_edit)

        self.show_existing_mask_button = QPushButton("Показать маску")
        self.show_existing_mask_button.setCheckable(True)
        self.show_existing_mask_button.setChecked(False)
        self.show_existing_mask_button.toggled["bool"].connect(self.on_show_existing_mask_button)

        self.layout.addWidget(edit_btn, 1, 2)
        self.layout.addWidget(self.show_existing_mask_button, 2, 2)
    
    def on_show_existing_mask_button(self, status):
        if status == True:
            self.show_existing_mask_button.setChecked(True)
            self.overlay_existing_mask()
        else:
            self.show_existing_mask_button.setChecked(False)
            self.hide_existing_mask()

    def overlay_existing_mask(self):
        self.parse_current_image_attrs()
        print("objects parsed")

    def hide_existing_mask(self):
        self.display.restore_srcs()
        print("maska skrita")
    
    def get_qvector_from_attr(self):
        pass

    def parse_current_image_attrs(self):
        with h5py.File(self.project_path, 'r+') as hdf:
            group_srcs = hdf[classifier.HDF_GROUP_SRCS_NAME]
            image_srcs = group_srcs[str(self.identifier)]
            current_object_index = int(image_srcs.attrs[classifier.HDF_IMAGE_ATTR_INDEX])

            for index in range(1, current_object_index + 1):
                    polygon = QPolygon()
                    tmp_str1 = image_srcs.attrs[str(index)]
                    tmp_str2 = re.sub(r' ', '', tmp_str1)
                    tmp_list = re.findall(r'\([0-9]+,[0-9]+\)', tmp_str2)
                    tuple_list = []
                    for pair in tmp_list:
                        tuple_list.append(make_tuple(pair))
                    for int_pair in tuple_list:
                        polygon.append(QPoint(int_pair[0], int_pair[1]))

                    self.display.overlay_mask(polygon)
                    print("index = ", index, "curoi = ", current_object_index)

    



    def on_edit(self):
        self.drawing_dialog = draw.drawing_dialog(  canvas_pixmap=self.display.base_pixmap,
                                                    canvas_geometry = self.display.geometry(),
                                                    window_geometry=self.geometry(),
                                                    project_path = self.project_path,
                                                    identifier = self.identifier
                                                    )
        self.drawing_dialog.exec_()
    
    def create_instruments_bar(self):
        instruments_bar = QToolBar()

        dots_instruments_btn = QToolButton()
        dots_instruments_icon = QIcon()
        dots_instruments_icon.addPixmap(QPixmap(classifier.ICON_SEG_TBTN_DOTS_INSTRUMENT_FULL))
        dots_instruments_btn.setIcon(dots_instruments_icon)

        instruments_bar.addWidget(dots_instruments_btn)

        #dots_instruments_btn.clicked.connect(self.draw_dots_instruments)

        self.layout.addWidget(instruments_bar, 1, 0)

    def draw_pencil_instruments(self):
        self.canvas = QPixmap(self.display.pixmap())
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black
        self.lastPoint = QPoint()


    def create_navigation_bar(self):
        navigation_bar = QToolBar()

        previous_btn = QToolButton()
        previous_icon = QIcon()
        previous_icon.addPixmap(QPixmap(classifier.ICON_SEG_TBTN_PREVIOUS_FULL))
        previous_btn.setIcon(previous_icon)

        to_first_btn = QToolButton()
        to_first_icon = QIcon()
        to_first_icon.addPixmap(QPixmap(classifier.ICON_SEG_TBTN_TOFIRST_FULL))
        to_first_btn.setIcon(to_first_icon)

        to_last_btn = QToolButton()
        to_last_icon = QIcon()
        to_last_icon.addPixmap(QPixmap(classifier.ICON_SEG_TBTN_TOLAST_FULL))
        to_last_btn.setIcon(to_last_icon)

        next_btn = QToolButton()
        next_icon = QIcon()
        next_icon.addPixmap(QPixmap(classifier.ICON_SEG_TBTN_NEXT_FULL))
        next_btn.setIcon(next_icon)

        """
        dots_instruments_btn = QToolButton()
        dots_instruments_icon = QIcon()
        dots_instruments_icon.addPixmap(QPixmap(classifier.ICON_SEG_TBTN_DOTS_INSTRUMENT_FULL))
        dots_instruments_btn.setIcon(dots_instruments_icon)

        navigation_bar.addWidget(dots_instruments_btn)
        """
        self.image_position_postfix = ' / ' + str(self.image_position_max) 
        self.image_position_widget = QLabel(str(self.current_image_position) + self.image_position_postfix) 

        navigation_bar.addWidget(to_first_btn)
        navigation_bar.addWidget(previous_btn)
        navigation_bar.addWidget(next_btn)
        navigation_bar.addWidget(to_last_btn)
        navigation_bar.addWidget(self.image_position_widget)

        to_first_btn.clicked.connect(self.on_to_first)
        previous_btn.clicked.connect(self.on_previous)
        next_btn.clicked.connect(self.on_next)
        to_last_btn.clicked.connect(self.on_to_last)

        self.layout.addWidget(navigation_bar, 0, 0, 1, 2)#, Qt.AlignTop)# | Qt.AlignHCenter) #области  

        
    def on_to_first(self):
        if self.identifier != 0:
            self.identifier = 0
            self.current_image_position = 1
            self.open_image(self.identifier)
            self.update_image_position_widget()

    def on_to_last(self):
        if self.identifier != self.identifier_max:
            self.identifier = self.identifier_max
            self.current_image_position = self.image_position_max
            self.open_image(self.identifier)
            self.update_image_position_widget()

    def on_previous(self):
        if self.identifier > 0:
            self.identifier -= 1
            self.current_image_position -= 1
            self.open_image(self.identifier)
            self.update_image_position_widget()

    def on_next(self):
        if self.identifier < self.identifier_max:
            self.identifier += 1
            self.current_image_position += 1
            self.open_image(self.identifier)
            self.update_image_position_widget()
    
    def update_image_position_widget(self):
        self.image_position_widget.setText(str(self.current_image_position) + self.image_position_postfix)

    """
    def open_file(self):
        self.hdf = h5py.File(self.project_path, 'w')
        self.identifier_max = self.hdf.keys()
        print(self.identifier_max)

    #def closeEvent(self, event):
    #    self.hdf.close()
    """

    def open_image(self, identifier):  #каждый раз открываю проблема закрыть корректно файл, если один раз
        self.clear_window_layout(self.image_layout)
        self.display = myLabel()
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
            #self.display.setPixmap(image_as_pixmap)
            self.display.update_base(image_as_pixmap)
            self.image_layout.addWidget(self.display)


    def open_images_dir(self):
        self.images_dir = os.getcwd()
        
        self.images_dir += "/__images"
        print(self.images_dir)
        if not os.path.exists(self.images_dir):
            print("no __images directory")
            os.mkdir(self.images_dir)
        self.images_list = os.listdir(self.images_dir)
        print(self.images_list)

    def adjust_window(self):
        self.setWindowTitle("Выбор изображения")
        self.setFixedSize(800,800)
        #self.layout = QHBoxLayout()
        self.layout = QGridLayout()
        self.image_layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addLayout(self.image_layout, 2, 1) # правильно растянуть область изображения
        
    def initPre(self):
        """
        Initialize stuff that are shared by actions, menus, widgets etc.
        """
        self.layout.addWidget(QToolBar('Document', objectName='document_toolbar'))
        self.layout.addWidget(QToolBar('Editor', objectName='editor_toolbar'))
        self.layout.addWidget(QToolBar('View', objectName='view_toolbar'))
        self.layout.addWidget(QToolBar('Graphol', objectName='graphol_toolbar')) 
    
    def clear_window_layout(self, layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().setParent(None)