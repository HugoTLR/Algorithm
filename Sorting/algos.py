from copy import deepcopy as dc

class Sorter:
  #0 For unchecked
  #2 for actual checked
  # 1 for done with
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

  def build_status(self):
    raise NotImplementedError("Must override build_status")

  def sort(self):
    raise NotImplementedError("Must override sort")

class Insertion(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    return super().__str__()

  def build_status(self,i,l):
    ll = []
    for j in range(l):
      if j <= i :
        ll.append(1)
      elif j > i + 1:
        ll.append(0)
      else:
        ll.append(2)
    return ll

  def sort(self,l):
    self.init_step = dc(l)
    self.init_status = self.build_status(-1,len(l))
    self.steps = [dc(l)]
    self.steps_status = [self.build_status(0,len(l))]

    i,len_l = 1,len(l)
    while i < len_l:

      x, j = l[i], i-1
      while j >= 0 and l[j] > x:
        l[j+1] = l[j]
        j -= 1
      l[j+1]= x
      self.steps_status.append(self.build_status(i,len_l))
      self.steps.append(dc(l))
      i += 1

    self.final_step = self.steps[-1]
    self.steps = self.steps[:-1]
    self.final_status = self.steps_status[-1]
    self.steps_status = self.steps_status[:-1]

class Selection(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    return super().__str__()

  def build_status(self,i,jmin,l):
    ll = []
    for j in range(l):
      if j == jmin:
        ll.append(2)
      else:
        if j <= i :
          ll.append(1)
        else:
          ll.append(0)
    return ll

  def sort(self,l):
    self.init_step = dc(l)
    self.init_status = self.build_status(0,0,len(l))
    self.steps = []
    self.steps_status = []
    len_l = len(l)
    for i in range(len_l-1):
      jmin = i
      for j in range(i+1,len_l,1):
        if (l[j] < l[jmin]):
          jmin = j

      status = self.build_status(i,jmin,len_l)
      self.steps_status.append(status)
      self.steps_status[-1][i] = 2
      self.steps.append(dc(l))
      if jmin != i:
        l = self.swap(l,i,jmin)

    self.final_step = dc(l)
    self.final_status = [1 for _ in range(len_l)]


class Quicksort(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    super().__str__()

  def build_status(self,i,l):
    ll = []
    for j in range(l):
      if j == i:
        ll.append(2)
      elif j < i:
        ll.append(1)
      else:
        ll.append(0)
    return ll

  def sort(self,data):
    lo = 0
    hi = len(data) -1
    len_d = len(data)
    self.init_step = dc(data)
    self.init_status = self.build_status(hi,len_d)
    self.steps = []
    self.steps_status =[]
    self.run_sort(data,lo,hi)

    self.final_step = dc(data)
    self.final_status = self.build_status(hi+1,len_d)
   

  def partition(self,data,lo,hi):
    pivot = data[hi]
    i = lo


    for j in range(lo,hi,1):
      if data[j] < pivot:
        self.swap(data,i,j)
        i += 1
    self.swap(data,i,hi)
    return i

  #Bcs of recursivity we need to initialize init step outside the function
  def run_sort(self,data,lo,hi):
     if lo < hi:
      p = self.partition(data,lo,hi)
      self.steps.append(dc(data))
      self.steps_status.append(self.build_status(p,len(data)))
      
      self.run_sort(data,lo,p-1)
      self.run_sort(data,p+1,hi)
"""
l = [1,8,7,9,6,5,4,3,2,44]
s = Quicksort()
s.sort(l,0,len(l)-1)

print(s.init_step)
print(s.final_step)
print()
for step in s.steps:
  print(step)
"""