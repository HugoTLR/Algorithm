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
import time 
import numpy as np
class Tab_Quadratic(QWidget):
    def __init__(self):
      super(Tab_Quadratic,self).__init__()
      #Load UI From ui file
      loadUi(f'{UIS_FOLDER}/tab_quadratic.ui',self) #Load Ui From QT

      self.CPT = 0
      self.im_builder = ImageBuilder()
      self.quadra = None
      self.c_thread = None
      self.lbl_fps.setText(f"Average FPS : ")
      self.show()

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
      self.lbl_visu.clear()

    def update_visual(self):
      img = self.build_image()

      
      self.lbl_visu.setPixmap(img)

    def build_image(self):
      image = self.im_builder.build_image_qtree(self.quadra.qtree,quads=self.quadra.show_quad)
      self.CPT += 1
      if self.CPT%10 == 0:
        cv.imwrite(f"./Images/gif_{self.CPT}.png",cv.cvtColor(image,cv.COLOR_RGB2BGR))
      q_pix = QPixmap.fromImage(QImage(image.data,image.shape[1],image.shape[0],QImage.Format_RGB888))
      return q_pix

