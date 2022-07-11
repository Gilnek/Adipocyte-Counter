#!/usr/bin/env python3
import sys
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QShortcut
from PyQt5.QtGui import QPixmap, QPainter, QPen, QKeySequence

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
        self.image = self.image.scaled(1020,768,0)
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
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    @pyqtSlot()
    def save(self):
        self.image.scaled(*self.OG_shape).save("temp.png","png")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec_())