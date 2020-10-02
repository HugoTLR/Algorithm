#3rd party
#System
from glob import glob
import sys
#Local
from Classes.pathfinder import *
from Widgets.Tab.tab import Tab

import cv2 as cv

class Tab_Pathfinder(Tab):
    def __init__(self):
      super(Tab_Pathfinder,self).__init__('Pathfinder')
      self.className = Pathfinder

      #List avaiable algo and data
      self.populate()

      #Set stepts slider to 0
      self.sld_steps.setMinimum(0)

    def slt_sld_steps(self,val):
      self.current_step = val
      self.update_visual()

    def slt_btn_run(self):
      self.current_step = 0
      item = self.lst_func.currentItem().text()
      data = self.get_data_from_file()
      if data == None:
        return

      ##FILL
      if item == "Dijkstra":
        self.object = Dijkstra()
      elif item == "AStar":
        self.object = AStar()

      self.object.solve(data)
      self.total_steps = len(self.object.steps)-1
      self.sld_steps.setMaximum(self.total_steps)
      self.sld_steps.setValue(self.current_step)
      self.update_visual()

