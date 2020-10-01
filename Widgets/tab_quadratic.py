#3rd Party
import numpy as np
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
#System
from glob import glob
import random
import time 
import threading
import sys
#Local
from Classes.quadratic import *
from envvar import UIS_FOLDER,DATA_FOLDER
from ImageBuilder import *
from utils import display_image
from Widgets.ImageWidget import ImageWidget 

class Tab_Quadratic(QWidget):
    def __init__(self):
      super(Tab_Quadratic,self).__init__()
      #Load UI From ui file
      loadUi(f'{UIS_FOLDER}/tab_quadratic.ui',self) #Load Ui From QT

      self.CPT = 0
      # self.im_builder = ImageBuilder()

      #Insert image widget
      self.image_widget = ImageWidget()
      self.verticalLayout_2.insertWidget(0,self.image_widget)

      self.quadra = None
      self.c_thread = None
      self.lbl_fps.setText(f"Average FPS : ")

    def anim_listener(self,stop_event):
      state = True
      while state and not stop_event.isSet():
        start = time.time()
        #Check if we need to recompute the quad structure on each loop
        #Since our particles are moving
        if self.quadra.show_quad:
          self.quadra.create_qtree()

        #Check Collision
        if self.quadra.collision_loop:
          self.quadra.normal_collision_check()
        else:
          self.quadra.qtree = self.quadra.check_collision(self.quadra.qtree)
        #Draw
        self.update_visual()
        #Update
        self.quadra.qtree = self.quadra.update_qtree(self.quadra.qtree)
        end = time.time()

        self.lbl_fps.setText(f"Average FPS : {1/(end-start):.5f}")
        time.sleep(.01) # Avoid crashing if too few points
      sys.exit()

    def slt_start(self):

      # print(dir(self.c_thread))
      nb_points = int(self.txt_points.toPlainText())
      pt_limit = int(self.txt_limit.toPlainText())
      points = [Pt(random.randint(0,Quadratic.WIN_W),random.randint(0,Quadratic.WIN_H),3) for _ in range(nb_points)]
      self.quadra = Quadratic(nb_points,pt_limit)
      self.quadra.update_points(points)
      self.quadra.create_qtree()
      self.stop_event = threading.Event()
      self.c_thread = threading.Thread(target=self.anim_listener,args=(self.stop_event,))


      self.c_thread.start()

    def slt_stop(self):
      self.stop_event.set()
      self.c_thread.join()


      self.clear_visual()
    
    def slt_quads_changed(self,value):
      self.quadra.show_quad = False
      if value != 0:
        self.quadra.show_quad = True

    def slt_collision_changed(self,value):
      self.quadra.collision_loop = False
      if value != 0:
        self.quadra.collision_loop = True

    def clear_visual(self):
      self.image_widget.clear()

    def update_visual(self):
      img = ImageBuilder.build(b_type='qtree', data=self.quadra.qtree, im=None, quads=self.quadra.show_quad,resize=True )
      self.image_widget.setImage(display_image(img))

