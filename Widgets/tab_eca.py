import sys
from envvar import UIS_FOLDER,DATA_FOLDER
from glob import glob
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import QWidget
from Classes.eca import ECA
from image import ImageBuilder
import threading
import time
import cv2 as cv
import numpy as np

class Tab_ECA(QWidget):
  def __init__(self):
    super(Tab_ECA,self).__init__()
    #Load UI From ui file
    loadUi(f'{UIS_FOLDER}/tab_eca.ui',self) #Load Ui From QT

    self.im_builder = ImageBuilder()
    self.eca = None



    # self.show()

  def anim_listener(self,stop_event):
    for k in range(self.eca.n_steps):
      self.eca.step(k)
      self.update_visual(k)
      time.sleep(.01)

    self.stop_event.set()

    sys.exit()

  def slt_start(self):
    self.current_step = 0

    rule_id = int(self.txt_rule.toPlainText())
    is_random = self.cb_random.isChecked()

    self.eca = ECA(901,450,rule_id,is_random)

    self.image = np.zeros((self.eca.n_steps,self.eca.w,3),dtype=np.uint8)
    self.stop_event = threading.Event()
    self.c_thread = threading.Thread(target=self.anim_listener,args=(self.stop_event,))


    self.c_thread.start()



  def update_visual(self,step):
    img = self.build_image(step)
    self.lbl_visu.setPixmap(img)

  def build_image(self,step):
    self.image = self.im_builder.build_image_eca(self.image,self.eca.states,step)
    q_pix = QPixmap.fromImage(QImage(self.image.data,self.image.shape[1],self.image.shape[0],self.image.shape[1]*3,QImage.Format_RGB888))
    return q_pix
