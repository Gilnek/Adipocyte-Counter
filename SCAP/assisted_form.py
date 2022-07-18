# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'assisted.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform, QPen, QShortcut)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QSizePolicy, QSlider, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1200, 900)
        self.Processed_image = QLabel(Dialog)
        self.Processed_image.setObjectName(u"Processed_image")
        self.Processed_image.setGeometry(QRect(90, 30, 1020, 768))
        self.Processed_image.setCursor(QCursor(Qt.CrossCursor))
        self.FFDist = QSlider(Dialog)
        self.FFDist.setObjectName(u"FFDist")
        self.FFDist.setGeometry(QRect(10, 870, 160, 22))
        self.FFDist.setOrientation(Qt.Horizontal)
        self.Save = QPushButton(Dialog)
        self.Save.setObjectName(u"Save")
        self.Save.setGeometry(QRect(970, 870, 75, 24))
        self.Cancel = QPushButton(Dialog)
        self.Cancel.setObjectName(u"Cancel")
        self.Cancel.setGeometry(QRect(1100, 870, 75, 24))
        self.Reset = QPushButton(Dialog)
        self.Reset.setObjectName(u"Reset")
        self.Reset.setGeometry(QRect(210, 870, 75, 24))
        self.label_texto_em_cima_da_parada = QLabel(Dialog)
        self.label_texto_em_cima_da_parada.setObjectName(u"label_texto_em_cima_da_parada")
        self.label_texto_em_cima_da_parada.setGeometry(QRect(40, 850, 71, 16))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

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
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.Processed_image.setText(QCoreApplication.translate("Dialog", u"PreProcessed_Image_Assisted", None))
        self.Save.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.Cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.Reset.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.label_texto_em_cima_da_parada.setText(QCoreApplication.translate("Dialog", u"Threshold", None))
    # retranslateUi

