import sys
from envvar import UIS_FOLDER,DATA_FOLDER
from glob import glob
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import QWidget

from Classes.sorter import *
from Classes.pathfinder import *
from image import ImageBuilder


class Tab_Pathfinder(QWidget):
    def __init__(self):
      super(Tab_Pathfinder,self).__init__()
      #Load UI From ui file
      loadUi(f'{UIS_FOLDER}/tab_pathfinder.ui',self) #Load Ui From QT

      self.im_builder = ImageBuilder()
      self.pathfinder = None

      self.populate_algo_list()
      self.populate_data_list()
      self.sld_steps.setMinimum(-1)

      self.show()

    def get_implemented_algorithm(self):
      return [cls.__name__ for cls in Pathfinder.__subclasses__()]

    def populate_algo_list(self):
      for algorithm in self.get_implemented_algorithm():
        self.lst_func.addItem(algorithm)

    def populate_data_list(self):
      for file in glob(f"{DATA_FOLDER}/Pathfinder/*.txt"):
        f_name = file.split('\\')[-1]
        self.lst_data.addItem(f_name)

    def get_data_from_file(self):
      try:
        f_name = self.lst_data.currentItem().text()
      except AttributeError:
        return None
      txt = open(f"{DATA_FOLDER}/Pathfinder/{f_name}",'r').read()
      return [[col for col in row] for row in txt.split('\n')]

    def slt_sld_steps(self,val):
      self.current_step = val
      init,final = False,False
      if self.current_step == -1: init = True
      elif self.current_step == self.total_steps: final = True
      self.build_visuals(init=init,final=final)

    def slt_btn_run(self):
      self.current_step = -1
      item = self.lst_func.currentItem().text()
      data = self.get_data_from_file()
      if data == None:
        return

        ##FILL
      if item == "Dijkstra":
        self.pathfinder = Dijkstra()

      self.pathfinder.solve(data)
      self.total_steps = len(self.pathfinder.steps)
      self.sld_steps.setMaximum(self.total_steps)
      self.sld_steps.setValue(-1)
      self.build_visuals(init=True)


    def build_visuals(self,init=False,final=False):
      print(f"{self.current_step=} {self.total_steps=}")
      text = f"Step {self.current_step+1} / {self.total_steps}"
      if init:
        data = self.pathfinder.init_step
        text = "Initial State"
      elif final:
        data = self.pathfinder.final_step
        text = "Final State"
      else:
        data = self.pathfinder.steps[self.current_step]
      self.im_builder.set_data_arr(data)
      self.im_builder.build_image_arr()

      q_im = QImage(self.im_builder.im.data,500,500,QImage.Format_RGB888)

      q_pix = QPixmap.fromImage(q_im)

      self.lbl_visu.setPixmap(q_pix)
      self.lbl_step.setText(text)
