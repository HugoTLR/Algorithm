import cv2 as cv
import numpy as np

WHITE = (255,255,255)
GRAY = (125,125,125)
BLUE = (0,0,255)

class ImageBuilder:
  def __init__(self,w,h):
    self.w = w
    self.h = h
    pass

  def build_image(self):
    self.im = np.zeros((self.h,self.w,3),dtype=np.uint8)
    for i,d in enumerate(self.data):
      tl,br = (i*self.skipper+1,int(self.h-d*self.h)),(i*self.skipper+self.skipper-1,self.h)

      color = GRAY
      if self.data_status[i] == 1:
        color = WHITE
      elif self.data_status[i] == 2:
        color = BLUE
      cv.rectangle(self.im,tl,br,color,-1)


  def set_data(self,data,data_status):
    self.data = self.norm(data)
    self.data_status = data_status
    self.skipper = self.w // len(self.data)

  def norm(self,l):
    return [(float(i))/(max(l)) for i in l]

