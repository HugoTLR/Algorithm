import cv2 as cv
import numpy as np

class ImageBuilder:
  WHITE = (255,255,255)
  GRAY = (125,125,125)
  BLUE = (0,0,255)
  GREEN = (0,255,0)

  MIN_W = 640
  MIN_H = 480

  MAX_W = 1024
  MAX_H = 768
  def __init__(self):
    pass

  def build_image(self):
    self.im = np.zeros((self.h,self.w,3),dtype=np.uint8)
    for i,d in enumerate(self.data):
      tl,br = (i,int(self.h-d*self.h)),(i+1,self.h)
      color = ImageBuilder.GRAY
      if self.data_status[i] == 1:
        color = ImageBuilder.WHITE
      elif self.data_status[i] == 2:
        color = ImageBuilder.BLUE
      elif self.data_status[i] == 3:
        color = ImageBuilder.GREEN
      cv.rectangle(self.im,tl,br,color,-1)
    self.im = cv.resize(self.im,(ImageBuilder.MAX_W,ImageBuilder.MAX_H),interpolation=cv.INTER_AREA)


  def set_data(self,data,data_status):
    self.data = self.norm(data)
    self.data_status = data_status
    len_d = len(self.data)
    self.w = len_d
    self.h = int(self.w/4*3)

  def norm(self,l):
    return [(float(i))/(max(l)) for i in l]


