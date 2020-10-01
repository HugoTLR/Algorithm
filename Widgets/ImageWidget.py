#3rd Party
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget
#System
#Local

class ImageWidget(QWidget):
  def __init__(self, parent = None):
    super(ImageWidget,self).__init__(parent)
    self.image = None

  def clear(self):
    self.image = None
    self.update()
  def setImage(self, image):
    self.image = image
    self.setMinimumSize(image.size())
    self.update()

  def paintEvent(self, event):
    qp = QPainter()
    qp.begin(self)
    if self.image:
      qp.drawImage(QPoint(0,0),self.image)
    qp.end()


