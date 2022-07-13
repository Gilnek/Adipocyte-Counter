# This Python file uses the following encoding: utf-8
import sys
from PyQt6 import QtWidgets, uic
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFileSelector


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
    def qualquer():
        print("euaqui")

if __name__ == "__main__":
    app = QApplication([])
 #   window = MainWindow()
    window = uic.loader("mainwindow.ui")
    window.show()
    sys.exit(app.exec_())
