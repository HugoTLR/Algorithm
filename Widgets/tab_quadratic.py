import sys
from envvar import UIS_FOLDER,DATA_FOLDER
from glob import glob
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import QWidget
import threading
from image import ImageBuilder
import random
from Classes.quadratic import *


class Tab_Quadratic(QWidget):
    def __init__(self):
      super(Tab_Quadratic,self).__init__()
      #Load UI From ui file
      loadUi(f'{UIS_FOLDER}/tab_quadratic.ui',self) #Load Ui From QT

      self.im_builder = ImageBuilder()
      self.quadra = Quadratic()
      self.c_thread = None
      self.show()

    def anim_listener(self,stop_event):
      state = True
      while state and not stop_event.isSet():
        #Check Collision
        self.quadra.qtree = self.quadra.check_collision(self.quadra.qtree)
        #Draw
        self.update_visual()
        #Update
        self.quadra.qtree = self.quadra.update_qtree(self.quadra.qtree)
      sys.exit()

    def slt_start(self):

      # print(dir(self.c_thread))
      points = [Pt(random.randint(0,Quadratic.WIN_W),random.randint(0,Quadratic.WIN_H),random.randint(2,2)) for _ in range(Quadratic.NB_POINTS)]

      self.quadra.update_points(points)
      self.quadra.create_qtree()
      self.stop_event = threading.Event()
      self.c_thread = threading.Thread(target=self.anim_listener,args=(self.stop_event,))


      self.c_thread.start()

    def slt_stop(self):
      self.stop_event.set()
      self.c_thread.join()


      self.update_visual()
      

    def update_visual(self):
      img = self.build_image()
      self.lbl_visu.setPixmap(img)

    def build_image(self):
      image = self.im_builder.build_image_qtree(self.quadra.qtree)
      q_pix = QPixmap.fromImage(QImage(image.data,image.shape[1],image.shape[0],QImage.Format_RGB888))
      return q_pix

