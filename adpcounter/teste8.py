#!/usr/bin/env python3
import sys
#from PyQt5.QtCore import Qt, QPoint, pyqtSlot
#from PyQt5.QtWidgets import QMainWindow, QApplication, QShortcut
#import PySide6
#from PyQt5.QtGui import QPixmap, QPainter, QPen, QKeySequence
from PySide6.QtCore import Qt, QPoint, Slot
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QPainter, QPixmap, QPen, QKeySequence, QShortcut

from PySide6 import QtCore

class Menu(QMainWindow):

    image: QPixmap
    OG_shape: tuple[int,int]

    def __init__(self):
        super().__init__()

        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"),self)
        self.save_shortcut.activated.connect(self.save)

        self.drawing = False
        self.lastPoint = QPoint()
        self.image = QPixmap("limpoclose.jpg")
        self.OG_shape = (
            self.image.width(),
            self.image.height()
        )
        self.image = self.image.scaled(1020,768,QtCore.Qt.IgnoreAspectRatio)
        self.setGeometry(100, 100, 500, 300)
        #self.resize(self.image.width(), self.image.height())
        self.setFixedSize(self.image.width(), self.image.height())
        self.show()
       

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.position()
        if event.button() == Qt.RightButton:
            self.drawing = True
            self.lastPoint = event.position()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
            painter.drawLine(self.lastPoint, event.position())
            # https://stackoverflow.com/questions/67496362/qmouseevent-object-has-no-attribute-pos
            self.lastPoint = event.position()
            self.update()

        if event.buttons() == Qt.RightButton and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.white, 5, Qt.SolidLine))
            painter.drawLine(self.lastPoint, event.position())
            # https://stackoverflow.com/questions/67496362/qmouseevent-object-has-no-attribute-pos
            self.lastPoint = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False
        if event.button == Qt.RightButton:
            self.drawing = False    

    @Slot()
    def save(self):
        self.image.scaled(*self.OG_shape).save("temp.png","png")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec())

