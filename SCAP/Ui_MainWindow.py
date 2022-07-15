# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 768)
        self.actionFile = QAction(MainWindow)
        self.actionFile.setObjectName(u"actionFile")
        self.actionFolder = QAction(MainWindow)
        self.actionFolder.setObjectName(u"actionFolder")
        self.actionAutomatic_Counting = QAction(MainWindow)
        self.actionAutomatic_Counting.setObjectName(u"actionAutomatic_Counting")
        self.actionAssisted_Counting = QAction(MainWindow)
        self.actionAssisted_Counting.setObjectName(u"actionAssisted_Counting")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Automatic = QPushButton(self.centralwidget)
        self.Automatic.setObjectName(u"Automatic")
        self.Automatic.setGeometry(QRect(20, 700, 75, 24))
        self.Assisted = QPushButton(self.centralwidget)
        self.Assisted.setObjectName(u"Assisted")
        self.Assisted.setGeometry(QRect(120, 700, 75, 24))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(490, 320, 49, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuProcessing = QMenu(self.menubar)
        self.menuProcessing.setObjectName(u"menuProcessing")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuProcessing.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionFile)
        self.menuFile.addAction(self.actionFolder)
        self.menuHelp.addAction(self.actionAbout)
        self.menuProcessing.addAction(self.actionAutomatic_Counting)
        self.menuProcessing.addAction(self.actionAssisted_Counting)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionFile.setText(QCoreApplication.translate("MainWindow", u"Read New File", None))
        self.actionFolder.setText(QCoreApplication.translate("MainWindow", u"Read New Folder", None))
        self.actionAutomatic_Counting.setText(QCoreApplication.translate("MainWindow", u"Automatic Counting", None))
        self.actionAssisted_Counting.setText(QCoreApplication.translate("MainWindow", u"Assisted Counting", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.Automatic.setText(QCoreApplication.translate("MainWindow", u"Automatic", None))
        self.Assisted.setText(QCoreApplication.translate("MainWindow", u"Assisted", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Imagem Original", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuProcessing.setTitle(QCoreApplication.translate("MainWindow", u"Processing", None))
    # retranslateUi

