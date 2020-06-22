import sys
from envvar import UIS_FOLDER,WIDGETS_FOLDER
from glob import glob
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QTabWidget
from PyQt5.QtCore import Qt
from Widgets.tab_sorter import Tab_Sorter
from Widgets.tab_pathfinder import Tab_Pathfinder

class App(QMainWindow):

  TAB_TO_CLASS = {"Sorter":Tab_Sorter,\
                    "Pathfinder":Tab_Pathfinder}

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

    # self.setWindowState(Qt.WindowMaximized);
    self.show()

  def build_tabs(self):
    for tab in self.get_tabs_widget():
        self.tab_widget.addTab(App.TAB_TO_CLASS[tab](),tab)


  def get_tabs_widget(self):
    tabs_name = []
    for file in glob(f"{WIDGETS_FOLDER}/tab_*.py"):
      f_name = file.split('\\')[-1]
      f_name = f_name.split('.')[0].split('_')[1]
      tabs_name.append(f_name.title())
    return tabs_name