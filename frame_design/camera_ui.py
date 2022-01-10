#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QBrush, QPixmap
import os
import time


class Camera_Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Camera_Window, self).__init__(parent)
        # self.setBac
        # self.face_recong = face.Recognition()
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.set_ui()
        self.slot_init()
        self.__flag_work = 0
        self.x = 0
        self.count = 0
        self.cam_on = False

    def set_ui(self):
        self.textBrowser = QtWidgets.QLabel("Camera")
        self.textBrowser.setAlignment(Qt.AlignCenter)

        self.mm_layout = QVBoxLayout()
        self.l_down_widget = QtWidgets.QWidget()
        self.__layout_main = QtWidgets.QHBoxLayout()
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()
        self.button_open_camera = QtWidgets.QPushButton(u'Camera On')
        self.button_cap = QtWidgets.QPushButton(u'Capture')
        self.button_open_camera.setMinimumHeight(50)
        self.button_cap.setMinimumHeight(50)

        # move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。
        self.move(500, 500)

        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(100, 100)

        self.label_show_camera.setFixedSize(641, 481)
        # self.label_show_camera.setFixedSize(1300, 481)
        self.label_show_camera.setAutoFillBackground(False)

        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_cap)
        self.__layout_fun_button.addWidget(self.label_move)
        # 添加一个右侧的组件
        self.right_widget = QWidget()
        self.right_widget_layout = QHBoxLayout()
        self.cap_label = QLabel()
        self.cap_label.setFixedSize(641, 481)
        # self.label_show_camera.setFixedSize(1300, 481)
        self.cap_label.setAutoFillBackground(False)
        self.right_widget_layout.addWidget(self.label_show_camera)
        self.right_widget_layout.addWidget(self.cap_label)
        self.right_widget.setLayout(self.right_widget_layout)

        self.__layout_main.addWidget(self.right_widget)
        self.__layout_main.addLayout(self.__layout_fun_button)
        self.l_down_widget.setLayout(self.__layout_main)
        self.mm_layout.addWidget(self.textBrowser)
        self.mm_layout.addWidget(self.l_down_widget)
        self.setLayout(self.mm_layout)
        self.label_move.raise_()
        self.setWindowTitle(u'Camera')

    def slot_init(self):
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_cap.clicked.connect(self.capx)

    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM,  cv2.CAP_DSHOW)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            # if msg==QtGui.QMessageBox.Cancel:
            #                     pass
            else:
                self.timer_camera.start(30)
                self.button_open_camera.setText(u'Close Camera')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.button_open_camera.setText(u'Open Camera')

    def show_camera(self):
        self.cam_on = True
        flag, self.image = self.cap.read()
        self.image = cv2.flip(self.image, 1)
        show = cv2.resize(self.image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        self.showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(self.showImage))

    def capx(self):
        if self.cam_on:
            print(os.path.abspath('.'))
            FName = r".\tmp\cap{}".format(time.strftime('%H%M%S', time.localtime()))
            self.cap_label.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
            self.showImage.save(FName + ".jpg", "JPG", 100)

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        if self.timer_camera.isActive():
            self.timer_camera.stop()
        event.accept()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = Camera_Window()
    # ex.setStyleSheet("#MainWindow{border-image:url(DD.png)}")
    ex.show()
    sys.exit(App.exec_())
