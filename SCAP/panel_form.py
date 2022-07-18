# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'panel.ui'
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
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QSlider,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(257, 99)
        self.FFDist = QSlider(Form)
        self.FFDist.setObjectName(u"FFDist")
        self.FFDist.setGeometry(QRect(50, 50, 160, 22))
        self.FFDist.setOrientation(Qt.Horizontal)
        self.label_threshold = QLabel(Form)
        self.label_threshold.setObjectName(u"label_threshold")
        self.label_threshold.setGeometry(QRect(70, 20, 131, 16))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_threshold.setText(QCoreApplication.translate("Form", u"Threshold Proportion", None))
    # retranslateUi

