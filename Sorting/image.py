import cv2 as cv
import numpy as np

WHITE = (255,255,255)
GRAY = (125,125,125)
BLUE = (0,0,255)

MIN_W = 640
MIN_H = 480

MAX_W = 1280
MAX_H = 960

OFF_WIDTH = int(int(MAX_H/20))


def pgcd(a,b):
  while b != 0:
    r = a%b
    a,b = b,r
  return a

def ppcm(a,b):
  if a == 0 or b == 0:
    return 0
  return (a*b)//pgcd(a,b)
class ImageBuilder:
  def __init__(self):
    pass

  def build_image(self):
    self.im = np.zeros((self.h,self.w,3),dtype=np.uint8)
    for i,d in enumerate(self.data):
      tl,br = (self.offset + i*self.skipper,int(self.h-d*self.h)),(self.offset + i*self.skipper+self.skipper,self.h)
      color = GRAY
      if self.data_status[i] == 1:
        color = WHITE
      elif self.data_status[i] == 2:
        color = BLUE
      cv.rectangle(self.im,tl,br,color,-1)


  def set_data(self,data,data_status):
    self.data = self.norm(data)
    self.data_status = data_status
    self.get_image_property()



  def get_image_property(self):
    len_d = len(self.data)
    if len_d < MIN_W:
      self.w = MIN_W
      self.h = MIN_H
      self.skipper = self.w//len_d
      self.offset = int((self.w - self.skipper*len_d)/2)
    else:
      self.skipper = MAX_W//len_d
      self.w = self.skipper*len_d
      self.h = int((self.w/4)*3) #4/3 ratio image
      self.offset = 0
    

  def norm(self,l):
    return [(float(i))/(max(l)) for i in l]


