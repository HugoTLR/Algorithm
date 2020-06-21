from PyQt5 import uic, QtWidgets, QtGui, QtCore
import sys
from tab_sorting import *
# from Sorting.algos import *
# from Sorting.image import ImageBuilder
# import inspect
# from glob import glob

class App(QtWidgets.QMainWindow):
  def __init__(self):
    super(App,self).__init__()
    #Load UI From ui file
    uic.loadUi('./app.ui',self) #Load Ui From QT


    #Initialise TabWidget
    self.tab_widget = QtWidgets.QTabWidget()


    #Automate This
    #Sorting
    self.build_tabs()
    self.setCentralWidget(self.tab_widget) 

    self.setWindowState(QtCore.Qt.WindowMaximized);
    self.show()

  def build_tabs(self):
    self.tab_widget.addTab(Tab_Sorting(),"Sorting")