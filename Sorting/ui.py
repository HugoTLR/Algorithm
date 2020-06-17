from PyQt5 import uic, QtWidgets, QtGui
import sys
from algos import *
from image import ImageBuilder
class Ui(QtWidgets.QMainWindow):
  def __init__(self):
    super(Ui,self).__init__()
    #Load UI From ui file
    uic.loadUi('../layout.ui',self) #Load Ui From QT

    self.sorter = None
    self.im_builder = ImageBuilder(640,480)

    # -1 is the key for initial state
    self.sld_steps.setMinimum(-1)


    self.show()


  def slt_sld_step(self):
    print(f"Allo ? {self.sld_steps.value()}")
    self.current_step = self.sld_steps.value()
    init,final = False,False

    if self.current_step == -1: init = True
    elif self.current_step == self.total_steps: final = True
    self.build_visuals(init=init,final=final)



  def slt_sort_run(self):
    l = [2,8,7,3,4,9,5,6,1]
    item = self.lst_func.currentItem().text()

    if item == "insertion":
      self.sorter = Insertion()
    elif item == "selection":
      self.sorter = Selection()

    self.sorter.sort(dc(l))
    self.current_step = 0
    self.total_steps = len(self.sorter.steps)
    self.sld_steps.setMaximum(self.total_steps)
    self.build_visuals()

  def build_visuals(self,init=False,final=False):
    print(f"{self.current_step=} {self.total_steps=}")
    text = f"Step {self.current_step+1} / {self.total_steps}"
    if init:
      data,status = self.sorter.init_step,self.sorter.init_status
      text = "Initial State"
    elif final:
      data,status = self.sorter.final_step,self.sorter.final_status
      text = "Final State"
    else:
      data,status = self.sorter.steps[self.current_step],self.sorter.steps_status[self.current_step]
    self.im_builder.set_data(data,status)
    self.im_builder.build_image()
    # self.lbl_visu.setText(self.sorter.__str__())
    self.lbl_visu.setPixmap(QtGui.QPixmap(QtGui.QImage(self.im_builder.im.data,self.im_builder.w,self.im_builder.h,QtGui.QImage.Format_RGB888)))
    self.lbl_step.setText(text)

