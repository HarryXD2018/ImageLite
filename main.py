import cv2
import numpy as np
import sys
import os
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget

from frame_design.camera_ui import Camera_Window
from frame_design.main_ui import Ui_MainWindow


class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        self.setupUi(self)
        self.img = np.ndarray(())
        self.img_name = 'img'
        self.img_path = '.'
        self.img_type = 'png'
        self.win_cam = None
        self.cap = None
        self.actionLoad_image.triggered.connect(self.load_image)
        self.actionSave_image.triggered.connect(self.save_image)
        self.actionCamera_2.triggered.connect(self.camera)

    def load_image(self):
        filepath, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './', '*.png *.jpg *.bmp')
        self.img_name, self.img_type = filepath.split('/')[-1].split('.')
        self.img_path = "/".join(filepath.split('/')[:-1])
        if self.img_name is '':
            return
        self.img = cv2.imread(filepath, -1)
        if self.img.size == 1:
            return
        self.refresh()

    def save_image(self):
        file_name, tmp = QFileDialog.getSaveFileName(
            self, 'Save Image', '{}/{}_ImageLite'.format(self.img_path, self.img_name), '*.png *.jpg *.bmp',
            '*.{}'.format(self.img_type))
        if file_name is '':
            return
        if self.img.size == 1:
            return
        img_output = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(file_name, img_output)

    def refresh(self):
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.qImg = QImage(self.img.data, self.img.shape[1], self.img.shape[0],
                           self.img.shape[1]*3, QImage.Format_RGB888)

        self.label.setPixmap(QPixmap.fromImage(self.qImg))
        self.label.adjustSize()

    def camera(self):
        self.win_cam = Camera_Window()
        self.win_cam.button_cap.clicked.connect(self.load_cap_image)
        self.win_cam.show()

    def load_cap_image(self):
        self.img = self.win_cam.image
        self.refresh()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())

