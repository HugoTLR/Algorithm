#3rd Party
from PyQt5.QtWidgets import QApplication
#System
import sys
#Local
from Widgets.app import App

#Main file
#Run our app
if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = App()
  sys.exit(app.exec_())