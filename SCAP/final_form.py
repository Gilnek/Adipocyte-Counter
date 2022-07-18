# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'final.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1200, 900)
        self.Imagem_Final = QLabel(Dialog)
        self.Imagem_Final.setObjectName(u"Imagem_Final")
        self.Imagem_Final.setGeometry(QRect(90, 30, 1020, 768))
        self.Save = QPushButton(Dialog)
        self.Save.setObjectName(u"Save")
        self.Save.setGeometry(QRect(950, 860, 75, 24))
        self.Cancel = QPushButton(Dialog)
        self.Cancel.setObjectName(u"Cancel")
        self.Cancel.setGeometry(QRect(1100, 860, 75, 24))
        self.Num_Adp_wr = QLineEdit(Dialog)
        self.Num_Adp_wr.setObjectName(u"Num_Adp_wr")
        self.Num_Adp_wr.setGeometry(QRect(150, 860, 113, 22))
        self.Num_Adp = QLabel(Dialog)
        self.Num_Adp.setObjectName(u"Num_Adp")
        self.Num_Adp.setGeometry(QRect(20, 860, 121, 16))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.Imagem_Final.setText(QCoreApplication.translate("Dialog", u"Final", None))
        self.Save.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.Cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.Num_Adp.setText(QCoreApplication.translate("Dialog", u"Number of Adipocytes", None))
    # retranslateUi

