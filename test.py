import sys
from Widgets.app import App
from Widgets.ImageWidget import ImageWidget
from PyQt5.QtCore import QTimer, QPoint, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel
from PyQt5.QtWidgets import QWidget, QAction, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPainter, QImage, QTextCursor

import cv2 as cv

# Main window
class MyWindow(QMainWindow):
    text_update = pyqtSignal(str)

    # Create main window
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.central = QWidget(self)
        self.textbox = QTextEdit(self.central)
        self.textbox.setMinimumSize(300, 100)

        self.vlayout = QVBoxLayout()        # Window layout
        self.displays = QHBoxLayout()
        self.disp = ImageWidget(self)    
        self.displays.addWidget(self.disp)
        self.vlayout.addLayout(self.displays)
        self.label = QLabel(self)
        self.vlayout.addWidget(self.label)
        self.vlayout.addWidget(self.textbox)
        self.central.setLayout(self.vlayout)
        self.setCentralWidget(self.central)

        self.mainMenu = self.menuBar()      # Menu bar
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(exitAction)

        im = cv.imread('C:\\Users\\Shir0w\\Desktop\\Figure_1.png')

        scale = 2
        disp_size = im.shape[1]//scale, im.shape[0]//scale
        disp_bpl = disp_size[0] * 3
        if scale > 1:
            im = cv.resize(im, disp_size, 
                             interpolation=cv.INTER_CUBIC)
        qim = QImage(im.data, disp_size[0], disp_size[1],QImage.Format_RGB888)
        self.disp.setImage(qim)


if __name__ == '__main__':
  app = QApplication(sys.argv)
  win = MyWindow()
  win.show()
  # win.start()
  sys.exit(app.exec_())

#EOF