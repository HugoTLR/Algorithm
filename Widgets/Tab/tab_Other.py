#3rd Party
import cv2 as cv
import numpy as np
#System
import sys
import threading
import time
#Local
from Classes.other import *
from Widgets.Tab.tab import Tab


class Tab_Other(Tab):
  def __init__(self):
    super(Tab_Other,self).__init__('Other')
    self.className = Other

    self.populate()


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
        self.object = MarchingSquare()
    elif item == "Raycast_2D":
      self.object = Raycast_2D()


    self.stop_event = threading.Event()
    self.c_thread = threading.Thread(target=self.anim_listener,args=(self.stop_event,))
    self.c_thread.start()

  def slt_stop(self):
    self.stop_event.set()
    self.c_thread.join()
    self.clear_visual()

