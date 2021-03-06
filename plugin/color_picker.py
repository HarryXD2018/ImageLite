# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QGuiApplication, QColor, QCursor
from PyQt5.QtWidgets import QWidget, QApplication

from frame_design.color_picker_ui import Ui_ColorCatcher



class ColorPicker(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ColorCatcher()
        self.ui.setupUi(self)
        self.setObjectName('color')
        self.ui.lineEditMark.setText("Press space to mark!")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.catch)
        self.timer.start(100)
        self.nowColor = None
        self.setCursor(Qt.CrossCursor)
        self.show()


    def catch(self):
        x = QCursor.pos().x()
        y = QCursor.pos().y()
        pixmap = QGuiApplication.primaryScreen().grabWindow(QApplication.desktop().winId(), x, y, 1, 1)
        if not pixmap.isNull():
            image = pixmap.toImage()
            if not image.isNull():
                if image.valid(0, 0):
                    color = QColor(image.pixel(0, 0))
                    r, g, b, _ = color.getRgb()
                    self.nowColor = color
                    self.ui.lineEditMove.setText('(%d, %d, %d) %s' % (r, g, b, color.name().upper()))
                    self.ui.lineEditMove.setStyleSheet('QLineEdit{border:2px solid %s;}' % (color.name()))
                    self.ui.lineEditMove.setStyleSheet('QLineEdit{background: %s;}' % (color.name()))
                    # self.ui.lineEditMove.setColor(color)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.ui.lineEditMark.setText(self.ui.lineEditMove.text())
            self.ui.lineEditMark.setStyleSheet('QLineEdit{border:2px solid %s;}' % (self.nowColor.name()))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = ColorPicker()
    # mainWindow.setWindowIcon(QIcon('./shuoGG_re.ico'))
    mainWindow.show()
    sys.exit(app.exec_())
