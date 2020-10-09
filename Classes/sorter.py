#3rd Party
#System
from copy import deepcopy as dc
import math
#Local

class Sorter:
  def __init__(self):
    pass

  def __str__(self):
    r = ""
    if self.steps:
      for s,ss in zip(self.steps,self.steps_status): r = r + str(s) + '\t' + str(ss) + "\n"
    return r

  def swap(self,l,i,j):
    x = l[i]
    l[i] = l[j]
    l[j] = x
    return l

  def initialize(self,data):
    self.data_size = len(data)
    self.steps = [dc(data)]
    self.steps_status = [ [0]*self.data_size ]

  def finalise(self, data):
    self.steps.append(dc(data))
    self.steps_status.append([1] * self.data_size)

  def build_status(self):
    raise NotImplementedError("Must override build_status")
  def sort(self):
    raise NotImplementedError("Must override sort")


class Insertion(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    return super().__str__()

  def build_status(self,i):
    ll = []
    for j in range(self.data_size):
      if j <= i :
        ll.append(1)
      elif j > i + 1:
        ll.append(0)
      else:
        ll.append(2)
    return ll

  def sort(self,data):
    self.initialize(data)
    i = 0
    while i < self.data_size:
      x, j = data[i], i - 1

      while j >= 0 and data[j] > x:
        data[j + 1] = data[j]
        j -= 1
      data[j + 1] = x

      self.steps_status.append(self.build_status(i))
      self.steps.append(dc(data))

      i += 1

class Selection(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    return super().__str__()

  def build_status(self,i,jmin):
    ll = []
    for j in range(self.data_size):
      if j == i:
        ll.append(2)
      elif j == jmin:
        ll.append(3)
      elif j < i:
        ll.append(1)
      else:
        ll.append(0)
    return ll

  def sort(self,data):
    self.initialize(data)
    for i in range(self.data_size):
      jmin = i
      for j in range(i + 1, self.data_size, 1):
        if (data[j] < data[jmin]):
          jmin = j
      self.steps_status.append(self.build_status(i, jmin))
      self.steps.append(dc(data))
      if jmin != i:
        data = self.swap(data, i, jmin)

    self.finalise(data)

class Quicksort(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    super().__str__()

  def build_status(self,i,low=-1,hi=-1):
    ll = []
    for j in range(self.data_size):
      if j == i:
        ll.append(2)
      elif j == low:
        ll.append(4)
      elif j == hi:
        ll.append(3)
      elif j < low:
        ll.append(1)
      else:
        ll.append(0)
    return ll

  def sort(self,data):
    self.initialize(data)
    low = 0
    hi = self.data_size - 1 

    self.run_sort(data,low,hi)

    self.finalise(data)
   

  def partition(self,data,low,hi):
    pivot = data[hi]
    i = low
    for j in range(low,hi,1):
      if data[j] < pivot:
        data = self.swap(data,i,j)
        i += 1
        self.steps.append(dc(data))
        self.steps_status.append(self.build_status(i,low,hi))
    data = self.swap(data,i,hi)

    return i

  #Bcs of recursivity we need to initialize init step outside the function
  def run_sort(self,data,low,hi):
    if low < hi:
      p = self.partition(data,low,hi)
      self.run_sort(data,low,p-1)
      self.run_sort(data,p+1,hi)



class Bubblesort(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    super().__str__()

  def build_status(self,i=-1,ii=-1,n=-1):
    ll = []
    for j in range(self.data_size):
      if j == i or j == ii:
        ll.append(2)
      elif n != -1 and j >= n:
        ll.append(1)
      else:
        ll.append(0)
    return ll

  def sort(self,data):
    self.initialize(data)

    swapped = True
    n = self.data_size
    while swapped:
      swapped = False
      for i in range(1,self.data_size,1):
        self.steps.append(dc(data))
        self.steps_status.append(self.build_status(i-1,i,n))

        if data[i-1] > data[i]:
          data = self.swap(data,i-1,i)
          swapped = True
      n -= 1

    self.finalise(data)

class Bubblesort_Optimized(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    super().__str__()

  def build_status(self,i=-1,ii=-1,n=-1):
    ll = []
    for j in range(self.data_size):
      if j == i or j == ii:
        ll.append(2)
      elif n != -1 and j >= n:
        ll.append(1)
      else:
        ll.append(0)
    return ll

  def sort(self,data):
    self.initialize(data)

    n = self.data_size
    swapped = True
    while swapped:
      swapped = False
      for i in range(1,n,1):
        self.steps.append(dc(data))
        self.steps_status.append(self.build_status(i-1,i,n))
        if data[i-1] > data[i]:
          data = self.swap(data,i-1,i)
          swapped = True
      n -= 1

    self.finalise(data)

class Bubblesort_Optimized_2(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    return super().__str__()

  def build_status(self,i=-1,ii=-1,n=-1):
    ll = []
    for j in range(self.data_size):
      if j == i or j == ii:
        ll.append(2)
      elif n != -1 and j >= n:
        ll.append(1)
      else:
        ll.append(0)
    return ll

  def sort(self,data):
    self.initialize(data)
    len_d = len(data)


    n = self.data_size
    while n > 1:
      new_n = 0
      for i in range(1,n,1):
        self.steps.append(dc(data))
        self.steps_status.append(self.build_status(i-1,i,n))
        if data[i-1] > data[i]:
          data = self.swap(data,i-1,i)
          new_n = i
      n = new_n

    self.finalise(data)

class Combsort(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    return super().__str_()


  def build_status(self,gap,i,gapi):
    ll = []
    for j in range(self.data_size):
      if j > i and j < gapi:
        ll.append(2)
      elif j == gapi:
        ll.append(3)
      elif j == i:
        ll.append(4)
      # elif j < i:
      #   ll.append(1)
      else:
        ll.append(0)
    return ll
  def sort(self,data):
    self.initialize(data)

    gap = self.data_size
    shrink = 1.3 #Constant factor
    is_sorted = False

    while not is_sorted:

      gap = math.floor(gap/shrink)
      if gap <= 1:
        gap = 1
        is_sorted = True
      i = 0
      while i + gap < self.data_size:
        self.steps.append(dc(data))
        self.steps_status.append(self.build_status(gap,i,i+gap))
        if data[i] > data[i+gap]:
          data = self.swap(data,i,i+gap)
          is_sorted = False
        i += 1

    self.finalise(data)



class Gnomesort(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    return super().__str__()

  def build_status(self,i):
    ll = []
    for j in range(self.data_size):
      if j == i:
        ll.append(2)
      elif j < i:
        ll.append(1)
      else:
        ll.append(0)
    return ll
  def sort(self,data):
    self.initialize(data)
    pos = 0

    while pos < self.data_size:
      self.steps.append(dc(data))
      self.steps_status.append(self.build_status(pos))
      if pos == 0:
        pos += 1
      if data[pos] >= data[pos-1]:
        pos += 1
      else:
        data = self.swap(data,pos,pos-1)
        pos -= 1


    self.finalise(data)