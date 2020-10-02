#3rd Party
import numpy as np
#System
from glob import glob
import random
import threading
import sys
#Local
from Classes.quadratic import *
from Widgets.tab import Tab

class Tab_Quadratic(Tab):
    def __init__(self):
      super(Tab_Quadratic,self).__init__('Quadratic')
      self.className = Quadratic

      self.object = None
      self.c_thread = None
      self.lbl_fps.setText(f"Average FPS : ")
      

    def anim_listener(self,stop_event):
      import time 
      state = True
      while state and not stop_event.isSet():
        start = time.time()

        #Check if we need to recompute the quad structure on each loop
        #Since our particles are moving
        if self.object.show_quad:
          self.object.create_qtree()

        #Check Collision
        if self.object.collision_loop:
          self.object.normal_collision_check()
        else:
          self.object.qtree = self.object.check_collision(self.object.qtree)
        #Draw
        self.update_visual()
        #Update
        self.object.qtree = self.object.update_qtree(self.object.qtree)

        end = time.time()

        self.lbl_fps.setText(f"Average FPS : {1/(end-start):.5f}")
        time.sleep(.01) # Avoid crashing if too few points
      sys.exit()

    def slt_start(self):

      # print(dir(self.c_thread))
      nb_points = int(self.txt_points.toPlainText())
      pt_limit = int(self.txt_limit.toPlainText())
      points = [Pt(random.randint(0,Quadratic.WIN_W),random.randint(0,Quadratic.WIN_H),3) for _ in range(nb_points)]
      self.object = Quadratic(nb_points,pt_limit)
      self.object.update_points(points)
      self.object.create_qtree()
      self.stop_event = threading.Event()
      self.c_thread = threading.Thread(target=self.anim_listener,args=(self.stop_event,))


      self.c_thread.start()

    def slt_stop(self):
      self.stop_event.set()
      self.c_thread.join()
      self.clear_visual()
    
    def slt_quads_changed(self,value):
      self.object.show_quad = False
      if value != 0:
        self.object.show_quad = True

    def slt_collision_changed(self,value):
      self.object.collision_loop = False
      if value != 0:
        self.object.collision_loop = True
