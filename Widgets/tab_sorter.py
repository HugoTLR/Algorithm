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

      self.sld_steps.setMinimum(0)

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
      self.update_visual()

    def slt_sort_run(self):
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
      self.total_steps = len(self.sorter.steps)-1
      self.sld_steps.setMaximum(self.total_steps)

      self.current_step = 0
      self.sld_steps.setValue(0)
      self.update_visual()

    def update_visual(self):
      if self.current_step == 0:
        text = "Initial Step"
      elif self.current_step == self.total_steps:
        text = "Final Step"
      else:
        text = f"Step {self.current_step} / {self.total_steps}" 
      img = self.build_image()
      self.lbl_visu.setPixmap(img)
      self.lbl_step.setText(text)

    def build_image(self):
      image = self.im_builder.build_image_list(self.sorter.steps[self.current_step],self.sorter.steps_status[self.current_step])
      q_pix = QPixmap.fromImage(QImage(image.data,image.shape[1],image.shape[0],QImage.Format_RGB888))
      return q_pix