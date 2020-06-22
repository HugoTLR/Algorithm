import cv2 as cv
import numpy as np

class ImageBuilder:
  COLORS = {"WHITE":(255,255,255),\
              "GRAY":(125,125,125),\
              "BLUE":(0,0,255),\
              "GREEN":(0,255,0),\
              "RED": (255,0,0),\
              "BLACK": (0,0,0),\
              "ORANGE":(255,125,0),\
              "PURPLE":(125,0,255)}
  WHITE = (255,255,255)
  GRAY = (125,125,125)
  BLUE = (0,0,255)
  GREEN = (0,255,0)

  MIN_W = 640
  MIN_H = 480

  MAX_W = 1024
  MAX_H = 768

  PATTERN_SIZE = 13
  def __init__(self):
    pass

  def build_image_list(self):
    self.im = np.zeros((self.h,self.w,3),dtype=np.uint8)
    for i,d in enumerate(self.data):
      tl,br = (i,int(self.h-d*self.h)),(i+1,self.h)
      color = ImageBuilder.COLORS["GRAY"]
      if self.data_status[i] == 1:
        color = ImageBuilder.COLORS["WHITE"]
      elif self.data_status[i] == 2:
        color = ImageBuilder.COLORS["BLUE"]
      elif self.data_status[i] == 3:
        color = ImageBuilder.COLORS["GREEN"]
      cv.rectangle(self.im,tl,br,color,-1)
    self.im = cv.resize(self.im,(ImageBuilder.MAX_W,ImageBuilder.MAX_H),interpolation=cv.INTER_AREA)


  def set_data_list(self,data,data_status):
    self.data = self.norm(data)
    self.data_status = data_status
    len_d = len(self.data)
    self.w = len_d
    self.h = int(self.w/4*3)

  def norm(self,l):
    return [(float(i))/(max(l)) for i in l]

  def build_image_arr(self):
    self.im = np.zeros((self.h*ImageBuilder.PATTERN_SIZE,self.w*ImageBuilder.PATTERN_SIZE,3),dtype=np.uint8)
    for j,row in enumerate(self.data):
      for i,col in enumerate(row):
        pattern = self.build_pattern(col)
        self.im[j*ImageBuilder.PATTERN_SIZE:j*ImageBuilder.PATTERN_SIZE+ImageBuilder.PATTERN_SIZE,i*ImageBuilder.PATTERN_SIZE:i*ImageBuilder.PATTERN_SIZE+ImageBuilder.PATTERN_SIZE] = pattern
    self.im = cv.resize(self.im,(500,500),interpolation=cv.INTER_AREA)

  def build_pattern(self,value):
    pattern = np.zeros((ImageBuilder.PATTERN_SIZE,ImageBuilder.PATTERN_SIZE,3),dtype=np.uint8)
    color = ImageBuilder.COLORS["GRAY"]
    if value == 'S':
      color = ImageBuilder.COLORS["RED"]
    elif value == 'T':
      color = ImageBuilder.COLORS["GREEN"]
    elif value == 'V':
      color = ImageBuilder.COLORS["WHITE"]
    elif value == '#':
      color = ImageBuilder.COLORS["BLACK"]
    elif value == 'P':
      color = ImageBuilder.COLORS["BLUE"]
    elif value == 'C':
      color = ImageBuilder.COLORS["ORANGE"]
    elif value == 'E':
      color = ImageBuilder.COLORS["PURPLE"]


    cv.rectangle(pattern,(1,1),(ImageBuilder.PATTERN_SIZE-2,ImageBuilder.PATTERN_SIZE-2),color,-1)
    return pattern

  def set_data_arr(self,data):
    self.data = data
    self.w = len(self.data[0])
    self.h = len(self.data)


