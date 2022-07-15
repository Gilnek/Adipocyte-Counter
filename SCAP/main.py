# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFileSelector, Slot
from PySide6.QtGui import QAction

from Ui_MainWindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionFile.triggered.connect(self.run_action_file)
        self.ui.actionFolder.triggered.connect(self.run_action_folder)
    
    def run_action_file(self):
        print("run_action_file")
        self.ui.Assisted.setEnabled(True)
    
    def run_action_folder(self):
        print("run_action_folder")
        self.ui.Assisted.setDisabled(True)
    
    def qualquer(self):
        print("euaqui")
        self.ui.actionFile.setText("bamboo")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    #window = loadUI("mainwindow.ui")
    window.show()
    sys.exit(app.exec())
