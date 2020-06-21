import sys
from envvar import UIS_FOLDER
from Widgets.tab_sorter import Tab_Sorter
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QTabWidget
from PyQt5.QtCore import Qt
# from Sorting.algos import *
# from Sorting.image import ImageBuilder
# import inspect
# from glob import glob

class App(QMainWindow):
  def __init__(self):
    super(App,self).__init__()
    #Load UI From ui file
    loadUi(f'{UIS_FOLDER}/app.ui',self)


    #Initialise TabWidget
    self.tab_widget = QTabWidget()


    #Automate This
    #Sorting
    self.build_tabs()
    self.setCentralWidget(self.tab_widget) 

    self.setWindowState(Qt.WindowMaximized);
    self.show()

  def build_tabs(self):
    self.tab_widget.addTab(Tab_Sorter(),"Sorting")