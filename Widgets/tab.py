#3rd Party
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
#System
from glob import glob
#Local
from cste import UIS_FOLDER,DATA_FOLDER
from ImageBuilder import *
from utils import display_image
from Widgets.ImageWidget import ImageWidget

class Tab(QWidget):
  def __init__(self,name):
    super(Tab,self).__init__()
    loadUi(f'{UIS_FOLDER}/tab_{name}.ui',self)

    self.name = name
    self.object = None #Object that'll handle subclasses
    self.insert_image_widget()

  def insert_image_widget(self):
    self.image_widget = ImageWidget()
    self.verticalLayout_2.insertWidget(0,self.image_widget)

  def clear_visual(self):
    self.image_widget.clear()

  def update_visual(self,step=None):
    text = None

    if self.name == 'ECA':
      img = ImageBuilder.build(b_type=self.name, data = self.object.states, step = step, im=self.image)
    elif self.name == 'Other':
      img = self.object.update()
    elif self.name == 'Pathfinder':
      text = self.format_text()
      img = ImageBuilder.build(b_type=self.name, data=self.object.steps[self.current_step] )
    elif self.name == 'Quadratic':
      img = ImageBuilder.build(b_type=self.name, data=self.object.qtree, im=None, quads=self.object.show_quad,resize=True )
    elif self.name == 'Sorter':
      text = self.format_text()
      img = ImageBuilder.build(b_type=self.name, data = self.object.steps[self.current_step], status = self.object.steps_status[self.current_step])

    #Update step label
    if text is not None:
      self.lbl_step.setText(text)
    self.image_widget.setImage(display_image(img))

  def format_text(self):
    if self.current_step == 0:
      text = "Initial Step"
    elif self.current_step == self.total_steps:
      text = "Final Step"
    else:
      text = f"Step {self.current_step} / {self.total_steps}" 
    return text

  def get_implemented_algorithm(self):
    return [cls.__name__ for cls in self.className.__subclasses__()]

  def get_avaiable_data(self):
    return glob(f"{DATA_FOLDER}/{self.name}/*.txt")

  def populate(self):
    self.populate_algo_list()
    self.populate_data_list()

  def populate_algo_list(self):
    for algorithm in self.get_implemented_algorithm():
      self.lst_func.addItem(algorithm)

  def populate_data_list(self):
    for file in self.get_avaiable_data():
      f_name = file.split('\\')[-1]
      self.lst_data.addItem(f_name)

  def get_data_from_file(self):
    try:
      f_name = self.lst_data.currentItem().text()
    except AttributeError:
      return None
    
    txt = open(f"{DATA_FOLDER}/{self.name}/{f_name}",'r').read()


    if self.name == 'Pathfinder':
      return [[col for col in row] for row in txt.split('\n')]
    else:
      return [int(i) for i in txt.split(',')]
