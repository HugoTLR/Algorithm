#3rd Party
import cv2 as cv
import numpy as np
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
#System
from glob import glob
import sys
import threading
import time
#Local
from Classes.eca import ECA
from cste import *
from ImageBuilder import *
from utils import display_image
from Widgets.ImageWidget import ImageWidget 


class Tab_ECA(QWidget):
  def __init__(self):
    super(Tab_ECA,self).__init__()
    #Load UI From ui file
    loadUi(f'{UIS_FOLDER}/tab_eca.ui',self) #Load Ui From QT

    #Insert image widget
    self.image_widget = ImageWidget()
    self.verticalLayout_2.insertWidget(0,self.image_widget)

    self.eca = None


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

    self.eca = ECA(ECA_WIDTH,ECA_HEIGHT,rule_id,is_random)

    self.image = np.zeros((self.eca.n_steps,self.eca.w,3),dtype=np.uint8)
    self.stop_event = threading.Event()
    self.c_thread = threading.Thread(target=self.anim_listener,args=(self.stop_event,))

    self.c_thread.start()

  def update_visual(self,step):
    img = ImageBuilder.build(b_type='eca',data=self.eca.states,step=step, im=self.image )
    self.image_widget.setImage(display_image(img))
