import sys
from envvar import UIS_FOLDER,DATA_FOLDER
from glob import glob
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import QWidget

from Classes.sorter import *
from Classes.pathfinder import *
from image import ImageBuilder

from Widgets.ImageWidget import ImageWidget 

import cv2 as cv
class Tab_Pathfinder(QWidget):
    def __init__(self):
      super(Tab_Pathfinder,self).__init__()
      #Load UI From ui file
      loadUi(f'{UIS_FOLDER}/tab_pathfinder.ui',self) #Load Ui From QT


      self.image_widget = ImageWidget()
      self.verticalLayout_3.addWidget(self.image_widget)


      self.im_builder = ImageBuilder()
      self.pathfinder = None

      self.populate_algo_list()
      self.populate_data_list()
      self.sld_steps.setMinimum(0)



    def display_image(self,image):
      scale = 1
      disp_size = image.shape[1]//scale, image.shape[0]//scale
      disp_bpl = disp_size[0] * 3
      if scale > 1:
          image = cv.resize(image, disp_size, 
                           interpolation=cv.INTER_CUBIC)
      qim = QImage(image.data, disp_size[0], disp_size[1],QImage.Format_RGB888)
      self.image_widget.setImage(qim)

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
      self.update_visual()

    def slt_btn_run(self):
      self.current_step = 0
      item = self.lst_func.currentItem().text()
      data = self.get_data_from_file()
      if data == None:
        return

      ##FILL
      if item == "Dijkstra":
        self.pathfinder = Dijkstra()
      elif item == "AStar":
        self.pathfinder = AStar()

      self.pathfinder.solve(data)
      self.total_steps = len(self.pathfinder.steps)-1
      self.sld_steps.setMaximum(self.total_steps)
      self.sld_steps.setValue(self.current_step)
      self.update_visual()


    def update_visual(self):
      if self.current_step == 0:
        text = "Initial Step"
      elif self.current_step == self.total_steps:
        text = "Final Step"
      else:
        text = f"Step {self.current_step} / {self.total_steps}" 
      # img = self.build_image()
      # self.lbl_visu.setPixmap(img)

      img = self.im_builder.build_image_arr(self.pathfinder.steps[self.current_step])
      self.display_image(img)
      self.lbl_step.setText(text)

    def build_image(self):
      image = self.im_builder.build_image_arr(self.pathfinder.steps[self.current_step])
      q_pix = QPixmap.fromImage(QImage(image.data,image.shape[1],image.shape[0],QImage.Format_RGB888))

      return q_pix