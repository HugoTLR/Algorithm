from copy import deepcopy as dc

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
    self.steps = [dc(l),dc(l)]
    self.steps_status = [self.build_status(-1,len(l)),self.build_status(0,len(l))]

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

    # self.final_step = self.steps[-1]
    # self.steps = self.steps[:-1]
    # self.final_status = self.steps_status[-1]
    # self.steps_status = self.steps_status[:-1]


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

  def build_status(self,l,i,lo=-1,hi=-1):
    ll = []
    m = min(i,lo,hi)
    for j in range(l):
      if j == i:
        ll.append(2)
      elif j == lo or j == hi:
        ll.append(3)
      elif j < m:
        ll.append(1)
      else:
        ll.append(0)
    return ll

  def sort(self,data):
    lo = 0
    hi = len(data) -1
    len_d = len(data)
    self.init_step = dc(data)
    self.init_status = self.build_status(len_d,hi)
    self.steps = []
    self.steps_status =[]
    self.run_sort(data,lo,hi)

    self.final_step = dc(data)
    self.final_status = self.build_status(len_d,hi+1,len_d,len_d)
   

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
      self.steps_status.append(self.build_status(len(data),p,lo,hi))
      
      self.run_sort(data,lo,p-1)
      self.run_sort(data,p+1,hi)


class Bubblesort(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    super().__str__()

  def build_status(self,l,i=-1,ii=-1,n=-1):
    ll = []
    for j in range(l):
      if j == i or j == ii:
        ll.append(2)
      elif n != -1 and j >= n:
        ll.append(1)
      else:
        ll.append(0)
    return ll

  def sort(self,data):
    len_d = len(data)

    self.init_step = dc(data)
    self.init_status = self.build_status(len_d)
    self.steps = []
    self.steps_status =[]

    swapped = True
    n = len_d
    while swapped:
      swapped = False
      for i in range(1,len_d,1):
        self.steps.append(dc(data))
        self.steps_status.append(self.build_status(len_d,i-1,i,n))

        if data[i-1] > data[i]:
          self.swap(data,i-1,i)
          swapped = True
      n -= 1

    self.final_step = dc(data)
    self.final_status = self.build_status(len_d,len_d,len_d,-2)

class Bubblesort_Optimized(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    super().__str__()

  def build_status(self,l,i=-1,ii=-1,n=-1):
    ll = []
    for j in range(l):
      if j == i or j == ii:
        ll.append(2)
      elif n != -1 and j >= n:
        ll.append(1)
      else:
        ll.append(0)
    return ll

  def sort(self,data):
    len_d = len(data)

    self.init_step = dc(data)
    self.init_status = self.build_status(len_d)
    self.steps = []
    self.steps_status =[]

    n = len_d
    swapped = True
    while swapped:
      swapped = False
      for i in range(1,n,1):
        self.steps.append(dc(data))
        self.steps_status.append(self.build_status(len_d,i-1,i,n))

        if data[i-1] > data[i]:
          self.swap(data,i-1,i)
          swapped = True
      n -= 1

    self.final_step = dc(data)
    self.final_status = self.build_status(len_d,len_d,len_d,-2)

class Bubblesort_Optimized_2(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    return super().__str__()

  def build_status(self,l,i=-1,ii=-1,n=-1):
    ll = []
    for j in range(l):
      if j == i or j == ii:
        ll.append(2)
      elif n != -1 and j >= n:
        ll.append(1)
      else:
        ll.append(0)
    return ll

  def sort(self,data):
    len_d = len(data)
    self.init_step = dc(data)
    self.init_status = self.build_status(len_d)
    self.steps = []
    self.steps_status =[]

    n = len_d
    while n >= 1:
      new_n = 0
      for i in range(1,n,1):
        self.steps.append(dc(data))
        self.steps_status.append(self.build_status(len_d,i-1,i,n))
        if data[i-1] > data[i]:
          self.swap(data,i-1,i)
          new_n = i
      n = new_n
    self.final_step = dc(data)
    self.final_status = self.build_status(len_d,len_d,len_d,-2)

class Combsort(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    return super().__str_()


  def build_status(self,l,i,gapi):
    ll = []
    for j in range(l):
      if j == i:
        ll.append(2)
      elif j == gapi:
        ll.append(3)
      elif j < i:
        ll.append(1)
      else:
        ll.append(0)
    return ll
  def sort(self,data):
    len_d = len(data)

    self.init_step = dc(data)
    self.init_status = self.build_status(len_d,-1,-1)
    self.steps = []
    self.steps_status =[]

    gap = len_d
    shrink = 1.3 #Constant factor
    is_sorted = False

    while not is_sorted:
      gap = math.floor(gap/shrink)
      if gap <= 1:
        gap = 1
        is_sorted = True

      i = 0
      while i + gap < len_d:
        self.steps.append(dc(data))
        self.steps_status.append(self.build_status(len_d,i,i+gap))
        if data[i] > data[i+gap]:
          self.swap(data,i,i+gap)
          is_sorted = False
        i += 1


    self.final_step = dc(data)
    self.final_status = self.build_status(len_d,len_d,-1)


class Gnomesort(Sorter):
  def __init__(self):
    pass
  def __str__(self):
    return super().__str__()

  def build_status(self,l,i):
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
    pos = 0
    len_d = len(data)

    self.init_step = dc(data)
    self.init_status = self.build_status(len_d,-1)
    self.steps = []
    self.steps_status =[]

    while pos < len_d:
      self.steps.append(dc(data))
      self.steps_status.append(self.build_status(len_d,pos))
      if pos == 0 or data[pos] >= data[pos-1]:
        pos += 1
      else:
        self.swap(data,pos,pos-1)
        pos -= 1


    self.final_step = dc(data)
    self.final_status = self.build_status(len_d,len_d)