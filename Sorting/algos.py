from copy import deepcopy as dc

class Sorter:
  def __init__(self):
    pass

  def __str__(self):
    r = ""
    if self.steps:
      for s in self.steps: r = r + str(s) + "\n"
    return r

  def swap(self,l,i,j):
    x = l[i]
    l[i] = l[j]
    l[j] = x
    return l

  def insertion(self,l):
    self.init_step = dc(l)
    self.init_status = self.build_insertion_status(0,len(l))

    self.steps = []
    #0 For unchecked
    #2 for actual checked
    # 1 for done with
    i = 1
    len_l = len(l)
    self.steps_status = []

    while i < len_l:
      status = self.build_insertion_status(i,len_l)
      self.steps_status.append(status)

      x = l[i]
      j = i-1
      while j >= 0 and l[j] > x:
        l[j+1] = l[j]
        j -= 1
      l[j+1]= x
      i += 1
      self.steps.append(dc(l))

    self.final_step = dc(l)
    self.final_status = self.build_insertion_status(i,len_l)
    print(len(self.steps))
    print(len(self.steps_status))

  def build_insertion_status(self,i,l):
    ll = []
    for j in range(l):
      if j < i :
        ll.append(1)
      elif j > i+1:
        ll.append(0)
      else:
        ll.append(2)
    return ll

  def selection(self,l):
    self.init_step = dc(l)
    self.init_status = self.build_selection_status(0,0,len(l))
    self.steps = []
    self.steps_status = []
    len_l = len(l)
    for i in range(len_l-1):
      jmin = i
      for j in range(i+1,len_l,1):
        if (l[j] < l[jmin]):
          jmin = j

      status = self.build_selection_status(i,jmin,len_l)
      self.steps_status.append(status)
      self.steps_status[-1][i] = 2
      self.steps.append(dc(l))
      if jmin != i:
        l = self.swap(l,i,jmin)


    self.final_step = dc(l)
    self.final_status = [1 for _ in range(len_l)]

  def build_selection_status(self,i,jmin,l):
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

  def bottom_up_merge_sort(self,l):
    self.steps = []
    n = len(l)
    # b = dc(l)
    b = []
    width = 1
    while width < n:
      print(f"{width=}")
      i = 0
      for i in range(0,n,i + 2*width):
        print(f"{l=}")
        self.bottom_up_merge(l,i,min(i+width,n),min(i+2*width,n),b)

      for i in range(n):
        l[i] = b[i]
      self.steps.append(dc(l))
      width *= 2

  def bottom_up_merge(self,l,ileft,iright,iend,b):
    i = ileft
    j = iright
    for k in range(ileft,iend):
      if (i < iright and (j >= iend or l[i] <= l[j])):
        b[k] = l[i]
        i += 1
      else:
        b[k] = l[j]
        j += 1

  def heapsort(self,l):
    self.steps = [dc(l)]

    

# l = [2,8,7,3,4,9,5,6,1]
# sorter = Sorter()
# sorter.insertion(dc(l))
# print(sorter)

# sorter.selection(dc(l))
# print(sorter)

# Not working
# sorter.bottom_up_merge_sort(dc(l))
# print(sorter)

