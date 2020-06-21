from PyQt5 import QtWidgets

import sys
from ui import Ui
from app import App
#Main file
#Run our app
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  window = App()

  # window = Ui()
  sys.exit(app.exec_())