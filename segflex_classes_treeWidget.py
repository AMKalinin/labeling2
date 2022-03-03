from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

import segflex_classifier as classifier


class allTree(QTreeWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.setDropAction(Qt.CopyAction)
        event.accept()

    def dropEvent(self, event):
        if event.source() == self:
            return
        widget = event.source().currentItem()
        if widget is None:
            return
        if widget.parent() is None:
            ind = event.source().indexOfTopLevelItem(widget)
            text = widget.child(0).text(1) + '_' + widget.child(0).text(0)
        else:
            ind = event.source().indexOfTopLevelItem(widget.parent())
            text = widget.text(1) + '_' + widget.text(0)
        if text in classifier.current_project.classes:
            classifier.current_project.classes.remove(text)
            event.source().takeTopLevelItem(ind)
        event.accept()


class selectedTree(allTree):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dropEvent(self, event):
        widget = event.source().currentItem()
        text = widget.text(1) + '_' + widget.text(0)

        def get_parent(item):
            if item.parent() is None:
                return QTreeWidgetItem([item.text(0), item.text(1)])
            return get_parent(item.parent())

        if event.source().indexOfTopLevelItem(widget) >= 0:
            return

        if text not in classifier.current_project.classes:
            classifier.current_project.classes.append(text)

            par = get_parent(widget)
            par.addChild(QTreeWidgetItem([widget.text(0), widget.text(1)]))
            self.addTopLevelItem(par)
            self.expandItem(par)
            self.setCurrentItem(par)
            event.accept()
