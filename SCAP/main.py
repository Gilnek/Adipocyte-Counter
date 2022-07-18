# This Python file uses the following encoding: utf-8
import sys
from typing import Any

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
from PySide6.QtCore import Slot, QSize, QEventLoop, QPoint, Qt
from PySide6.QtGui import QAction, QPixmap, QKeySequence, QShortcut, QPainter, QPen


import PySide6.QtCore as QtCore
from cv2 import threshold

from Ui_MainWindow import Ui_MainWindow
from final_form import Ui_Dialog as Ui_final_form
from assisted_form import Ui_Dialog as Ui_assisted_form
from drawing_form import DrawingDialog
#from panel_form import Ui_Form as Ui_panel_form
import processing_definitions


#class PanelForm(QWidget):
#    def __init__(self):
#        super(PanelForm, self).__init__()
##        self.ui = Ui_panel_form()
#       self.ui.setupUi(self)

class FinalForm(QWidget):
    def __init__(self):
        super(FinalForm, self).__init__()
        self.ui = Ui_final_form()
        self.ui.setupUi(self)
        self.ui.Save.triggered.connect()
        self.ui.Cancel.triggered.connect()
        self.ui.Num_Adp_wr.setText() #vai passar o valor dos adipócitos
        self.img_shape = (1020,768)
        self.pix = QPixmap() #passa o pixmap da imagem final
        self.pix.fill()
        self.ui.label.setPixmap(self.pix)

class DrawingForm(QWidget):
    #close_image: Any = None
    pix: QPixmap
    resized_pix: QPixmap
    drawing_dialog: DrawingDialog
    def __init__(self):
        super(DrawingForm, self).__init__()

        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"),self)
        self.save_shortcut.activated.connect(self.save)

        self.drawing_dialog = DrawingDialog()

        self.drawing = False
        self.lastPoint = QPoint()
        self.ui = Ui_assisted_form()
        self.ui.setupUi(self)
        self.drawing = False
        # self.ui.Save.clicked.connect()
        # self.ui.Cancel.clicked.connect()
        self.ui.Reset.clicked.connect(self.teste)
        # self.ui.FFDist.triggered.connect()
        self.img_shape = (1020,768)
        self.pix = QPixmap() #passa o pixmap da imagem assistida
        self.pix.fill()
        #self.ui.Processed_image.setPixmap(self.pix)
    
    def teste(self):
        print("tentando carai")
        self.drawing_dialog.show()
        # Cria um loop para segurar a execução
        loop = QEventLoop()
        # Conecta destruição do widget com saida do loop
        self.drawing_dialog.destroyed.connect(loop.quit)
        self.drawing_dialog.destroyed.connect(self.update_image_from_drawing)
        # Executa loop para segurar a execução
        loop.exec()
    def update_image_from_drawing(self):
        self.resized_pix = self.drawing_dialog.get_pixmap()
        self.ui.Processed_image.setPixmap(self.resized_pix)

    # def paintEvent(self, event):
    #     painter = QPainter(self.ui.Processed_image)
    #     painter.drawPixmap(self.rect(), self.resized_pix)

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.drawing = True
    #         self.lastPoint = event.position()
    #     if event.button() == Qt.RightButton:
    #         self.drawing = True
    #         self.lastPoint = event.position()

    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.LeftButton and self.drawing:
    #         painter = QPainter(self.resized_pix)
    #         painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
    #         painter.drawLine(self.lastPoint, event.position())
          
    #         self.lastPoint = event.position()
    #         self.update()

    #     if event.buttons() == Qt.RightButton and self.drawing:
    #         painter = QPainter(self.resized_pix)
    #         painter.setPen(QPen(Qt.white, 5, Qt.SolidLine))
    #         painter.drawLine(self.lastPoint, event.position())
          
    #         self.lastPoint = event.position()
    #         self.update()

    # def mouseReleaseEvent(self, event):
    #     if event.button == Qt.LeftButton:
    #         self.drawing = False
    #     if event.button == Qt.RightButton:
    #         self.drawing = False  

    # def set_close_image(self, image: Any) -> None:
    #     self.close_image = image

    def set_pixmap(self, image: QPixmap) -> None:
        self.pix = image
        self.resized_pix = self.pix.scaled(QSize(1020,768),QtCore.Qt.IgnoreAspectRatio)
        self.ui.Processed_image.setPixmap(self.resized_pix)

    @Slot()
    def save(self):
        self.resized_pix.save("temp.png","png")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #conectando o sinal triggered de uma QAction em uma função
        self.ui.actionFile.triggered.connect(self.run_action_file)
        self.ui.actionFolder.triggered.connect(self.run_action_folder)
        #desabilitando botões
        self.ui.Assisted.setDisabled(True)
        self.ui.Automatic.setDisabled(True)
        #conectando o sinal clicked
        self.ui.Assisted.clicked.connect(self.run_assisted)
        self.ui.Automatic.clicked.connect(self.run_automatic)
        self.ui.label.setText(u'')
        self.img_shape = (1020,768)
        self.pix = QPixmap(*self.img_shape)
        self.pix.fill()
        self.ui.label.setPixmap(self.pix)
        # sub janelas
        self.assisted_form = DrawingForm()

    def run_action_file(self):
        print("run_action_file")
        # selector = QFileDialog(
        #     parent=None,
        #     caption="Selecione a imagem desejada",
        #     directory='.',
        #     filter="*.png; *.jpg; *.jpeg; *.bpm"
        # )
        # selector.setFileMode(QFileDialog.ExistingFile)
        # selector.
        fileName, used_filter = QFileDialog.getOpenFileName(self,
            caption="Selecione uma imagem",
            dir=".",
            filter="Arquivos de Imagem (*.png *.jpg *.bmp)")
        print(f'path given: "{fileName}"')
        if fileName:
            self.pix.load(fileName)
            self.pix_scaled = self.pix.scaled(QSize(*self.img_shape), QtCore.Qt.KeepAspectRatio)
            self.ui.label.setPixmap(self.pix_scaled)
            self.ui.Assisted.setEnabled(True)
            self.ui.Automatic.setEnabled(True)
    
    def run_action_folder(self):
        print("run_action_folder")
        path = QFileDialog.getExistingDirectory(
            caption="Selecione uma pasta contendo as imagens",
            dir='.'
        )
        print(path)
        if path:
            self.ui.Automatic.setEnabled(True)

    def run_assisted(self):
        print('run_assisted')
        pix_image = self.pix
        cv_image = processing_definitions.pix2cv(pix_image)
        gray_image = processing_definitions.gray_scale_transformation(cv_image)
        contrast_stretching_image = processing_definitions.contrast_stretching(gray_image)
        blur_image = processing_definitions.blur(contrast_stretching_image)
        canny_edge_image = processing_definitions.canny_edge(blur_image)
        gauss_thresh_image = processing_definitions.gaussian_threshold(canny_edge_image)
        erode_image = processing_definitions.erode(gauss_thresh_image)
        rso_image = processing_definitions.remove_small_objects(erode_image)
        close_image = processing_definitions.closing(rso_image)
        #aqui diferente da automatica vai fazer a chamada para a tela de pintar
        self.assisted_form.set_pixmap(
            processing_definitions.cv2pix(close_image)
        )
        self.call_assisted_window()
        
        floodfill_image, processed_image = processing_definitions.flood_fill(close_image, cv_image)
        ff_dist_image, ff_bin_image= processing_definitions.dist_transform_plus_thresh()
        adipocyte_number = processing_definitions.count_it(ff_dist_image, ff_bin_image, processed_image)
        final_image = processing_definitions.cv2pix(processed_image)
        #self.clean_up()

    def run_automatic(self):
        print('run_auto')
        pix_image = self.pix
        cv_image = processing_definitions.pix2cv(pix_image)
        gray_image = processing_definitions.gray_scale_transformation(cv_image)
        contrast_stretching_image = processing_definitions.contrast_stretching(gray_image)
        blur_image = processing_definitions.blur(contrast_stretching_image)
        canny_edge_image = processing_definitions.canny_edge(blur_image)
        gauss_thresh_image = processing_definitions.gaussian_threshold(canny_edge_image)
        erode_image = processing_definitions.erode(gauss_thresh_image)
        rso_image = processing_definitions.remove_small_objects(erode_image)
        close_image = processing_definitions.closing(rso_image)
        floodfill_image, processed_image = processing_definitions.flood_fill(close_image, cv_image)
        ff_dist_image, ff_bin_image= processing_definitions.dist_transform_plus_thresh()
        adipocyte_number = processing_definitions.count_it(ff_dist_image, ff_bin_image, processed_image)
        final_image = processing_definitions.cv2pix(processed_image)
        print("adipocitos aqui: ", adipocyte_number)
        #self.clean_up()

    def clean_up(self):
        self.ui.Assisted.setDisabled(True)
        self.ui.Automatic.setDisabled(True)
        self.pix = QPixmap(*self.img_shape)
        self.pix.fill()
        self.ui.label.setPixmap(self.pix)

    def qualquer(self):
        print("euaqui")
        #self.ui.actionFile.setText("bamboo")
    
    def call_assisted_window(self):
        self.assisted_form.show()
        # Cria um loop para segurar a execução
        loop = QEventLoop()
        # Conecta destruição do widget com saida do loop
        self.assisted_form.destroyed.connect(loop.quit)
        # Executa loop para segurar a execução
        loop.exec()
    #call_assisted_window

   


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    #window = loadUI("mainwindow.ui")
    window.show()
    sys.exit(app.exec())
