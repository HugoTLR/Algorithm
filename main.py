import sys
from app import App
from PyQt5.QtWidgets import QApplication

#Main file
#Run our app
if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = App()
  sys.exit(app.exec_())