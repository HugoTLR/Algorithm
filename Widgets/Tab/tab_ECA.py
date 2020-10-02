#3rd Party
import cv2 as cv
import numpy as np
#System
from glob import glob
import sys
import threading
import time
#Local
from Classes.eca import ECA
from cste import ECA_WIDTH, ECA_HEIGHT
from Widgets.Tab.tab import Tab


class Tab_ECA(Tab):
  def __init__(self):
    super(Tab_ECA,self).__init__('ECA')



  def anim_listener(self,stop_event):
    for k in range(self.object.n_steps):
      self.object.step(k)
      self.update_visual(k)
      time.sleep(.01)

    self.stop_event.set()

    sys.exit()

  def slt_start(self):
    self.current_step = 0

    rule_id = int(self.txt_rule.toPlainText())
    is_random = self.cb_random.isChecked()

    self.object = ECA(ECA_WIDTH,ECA_HEIGHT,rule_id,is_random)

    self.image = np.zeros((self.object.n_steps,self.object.w,3),dtype=np.uint8)
    self.stop_event = threading.Event()
    self.c_thread = threading.Thread(target=self.anim_listener,args=(self.stop_event,))

    self.c_thread.start()

