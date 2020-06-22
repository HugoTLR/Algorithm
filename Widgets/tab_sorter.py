import sys
from envvar import UIS_FOLDER,DATA_FOLDER
from glob import glob
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import QWidget

from Classes.sorter import *
from image import ImageBuilder


class Tab_Sorter(QWidget):
    def __init__(self):
      super(Tab_Sorter,self).__init__()
      #Load UI From ui file
      loadUi(f'{UIS_FOLDER}/tab_sorter.ui',self) #Load Ui From QT

      self.im_builder = ImageBuilder()
      self.sorter = None

      self.populate_algo_list()
      self.populate_data_list()

      self.sld_steps.setMinimum(-1)

      self.show()

    def get_implemented_algorithm(self):
      return [cls.__name__ for cls in Sorter.__subclasses__()]

    def populate_algo_list(self):
      for algorithm in self.get_implemented_algorithm():
        self.lst_func.addItem(algorithm)

    def populate_data_list(self):
      for file in glob(f"{DATA_FOLDER}/Sorter/*.txt"):
        f_name = file.split('\\')[-1]
        self.lst_data.addItem(f_name)

    def get_data_from_file(self):
      try:
        f_name = self.lst_data.currentItem().text()
      except AttributeError:
        return None
      txt = open(f"{DATA_FOLDER}/Sorter/{f_name}",'r').read()
      return [int(i) for i in txt.split(',')]

    def slt_sld_step(self,val):
      self.current_step = val
      init,final = False,False
      if self.current_step == -1: init = True
      elif self.current_step == self.total_steps: final = True
      self.build_visuals(init=init,final=final)

    def slt_sort_run(self):
      self.current_step = -1
      item = self.lst_func.currentItem().text()
      data = self.get_data_from_file()
      print(f"Sorting {len(data)} items")
      if data == None:
        return

      if item == "Insertion":
        self.sorter = Insertion()
      elif item == "Selection":
        self.sorter = Selection()
      elif item == "Quicksort":
        self.sorter = Quicksort()
      elif item == "Bubblesort":
        self.sorter = Bubblesort()
      elif item == "Bubblesort_Optimized":
        self.sorter = Bubblesort_Optimized()
      elif item == "Bubblesort_Optimized_2":
        self.sorter = Bubblesort_Optimized_2()
      elif item == "Combsort":
        self.sorter = Combsort()
      elif item == "Gnomesort":
        self.sorter = Gnomesort()


      self.sorter.sort(dc(data))
      self.total_steps = len(self.sorter.steps)
      self.sld_steps.setMaximum(self.total_steps)

      self.sld_steps.setValue(-1)
      self.build_visuals(init=True)


    def build_visuals(self,init=False,final=False):
      #print(f"{self.current_step=} {self.total_steps=}")
      text = f"Step {self.current_step+1} / {self.total_steps}"
      if init:
        data,status = self.sorter.init_step,self.sorter.init_status
        text = "Initial State"
      elif final:
        data,status = self.sorter.final_step,self.sorter.final_status
        text = "Final State"
      else:
        data,status = self.sorter.steps[self.current_step],self.sorter.steps_status[self.current_step]
      self.im_builder.set_data_list(data,status)
      self.im_builder.build_image_list()

      q_im = QImage(self.im_builder.im.data,self.im_builder.MAX_W,self.im_builder.MAX_H,QImage.Format_RGB888)

      q_pix = QPixmap.fromImage(q_im)

      self.lbl_visu.setPixmap(q_pix)
      self.lbl_step.setText(text)
