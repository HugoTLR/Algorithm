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
from Classes.other import *
from cste import UIS_FOLDER,DATA_FOLDER
from ImageBuilder import *
from utils import display_image
from Widgets.ImageWidget import ImageWidget 


class Tab_Other(QWidget):
  def __init__(self):
    super(Tab_Other,self).__init__()
    #Load UI From ui file
    loadUi(f'{UIS_FOLDER}/tab_other.ui',self) #Load Ui From QT

    #Insert image widget
    self.image_widget = ImageWidget()
    self.verticalLayout_2.insertWidget(0,self.image_widget)

    self.other = None
    self.populate()

  def populate(self):
    self.populate_algo_list()

  def populate_algo_list(self):
    for algorithm in self.get_implemented_algorithm():
      self.lst_func.addItem(algorithm)

  def get_implemented_algorithm(self):
    return [cls.__name__ for cls in Other.__subclasses__()]


  def anim_listener(self,stop_event):
    state = True
    while state and not stop_event.isSet():
      start = time.time()
      #Draw
      self.update_visual()

      time.sleep(0.01) # Avoid crashing if too few points
      #Update
      end = time.time()

      self.lbl_fps.setText(f"Average FPS : {1/(end-start):.5f}")
    sys.exit()


  def slt_start(self):
    item = self.lst_func.currentItem().text()

    if item == "MarchingSquare":
        self.other = MarchingSquare()
    elif item == "Raycast_2D":
      self.other = Raycast_2D()
    self.stop_event = threading.Event()
    self.c_thread = threading.Thread(target=self.anim_listener,args=(self.stop_event,))
    self.c_thread.start()

  def slt_stop(self):
    self.stop_event.set()
    self.c_thread.join()
    self.clear_visual()

  def clear_visual(self):
    self.image_widget.clear()

  def update_visual(self):
    img = self.other.update()
    self.image_widget.setImage(display_image(img))