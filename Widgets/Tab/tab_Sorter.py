#3rd party
#System
#Local
from Classes.sorter import *
from Widgets.Tab.tab import Tab

class Tab_Sorter(Tab):
    """
    Class managing the Sorter Tab in our application
    """

    def __init__(self):
      # Instantiate Widget and UI
      super(Tab_Sorter,self).__init__('Sorter')
      self.className = Sorter

      # Populate ListView with:
        # Avaiable sorting algorithm
        # Avaiable unsorted list
      self.populate()


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
      
      if data == None:
        return

      if item == "Insertion":
        self.object = Insertion()
      elif item == "Selection":
        self.object = Selection()
      elif item == "Quicksort":
        self.object = Quicksort()
      elif item == "Bubblesort":
        self.object = Bubblesort()
      elif item == "Bubblesort_Optimized":
        self.object = Bubblesort_Optimized()
      elif item == "Bubblesort_Optimized_2":
        self.object = Bubblesort_Optimized_2()
      elif item == "Combsort":
        self.object = Combsort()
      elif item == "Gnomesort":
        self.object = Gnomesort()

      self.object.sort(dc(data))

      self.total_steps = len(self.object.steps) - 1
      self.sld_steps.setMaximum(self.total_steps)

      self.current_step = 0
      self.sld_steps.setValue(0)
      self.update_visual()
