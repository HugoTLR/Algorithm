import sys
from envvar import UIS_FOLDER,DATA_FOLDER
from glob import glob
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import QWidget

from Classes.sorter import *
from image import ImageBuilder

from Widgets.ImageWidget import ImageWidget 
from ImageBuilder import *

class Tab_Sorter(QWidget):
    """
    Class managing the Sorter Tab in our application
    """

    def __init__(self):
      # Instantiate Widget and UI
      super(Tab_Sorter,self).__init__()
      loadUi(f'{UIS_FOLDER}/tab_sorter.ui',self)
      # Instantiate Image wrapper and Algo Sorter
      self.im_builder = ImageBuilder()
      self.sorter = None

      self.image_widget = ImageWidget()
      self.verticalLayout_2.insertWidget(0,self.image_widget)

      # Populate ListView with:
        # Avaiable sorting algorithm
        # Avaiable unsorted list
      self.populate()

      # self.show()

    def get_implemented_algorithm(self):
      return [cls.__name__ for cls in Sorter.__subclasses__()]


    def populate(self):
      self.populate_algo_list()
      self.populate_data_list()


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
      """
      Update our visual on slider changes
      """
      self.current_step = val
      self.update_visual()

    def slt_sort_run(self):
      """
      Run algorithm using selected item in ListViews
      """
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
      img = ImageBuilder.build(b_type='sorter', data = self.sorter.steps[self.current_step], status = self.sorter.steps_status[self.current_step])
      self.display_image(img)
      self.lbl_step.setText(text)


    def build_image(self):
      image = self.im_builder.build_image_list(self.sorter.steps[self.current_step],self.sorter.steps_status[self.current_step])
      q_pix = QPixmap.fromImage(QImage(image.data,image.shape[1],image.shape[0],QImage.Format_RGB888))
      return q_pix

    def display_image(self,image):
      scale = 1
      disp_size = image.shape[1]//scale, image.shape[0]//scale
      disp_bpl = disp_size[0] * 3
      if scale > 1:
          image = cv.resize(image, disp_size, 
                           interpolation=cv.INTER_CUBIC)
      qim = QImage(image.data, disp_size[0], disp_size[1],QImage.Format_RGB888)
      self.image_widget.setImage(qim)