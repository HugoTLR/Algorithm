import cv2 as cv
import numpy as np
from Classes.quadratic import Quadratic,QuadTree,Pt

class ImageBuilder:
  COLORS = {"WHITE":(255,255,255),\
              "GRAY":(75,75,75),\
              "BLUE":(0,0,255),\
              "GREEN":(0,255,0),\
              "RED": (255,0,0),\
              "BLACK": (0,0,0),\
              "ORANGE":(255,125,0),\
              "PURPLE":(200,0,255),\
              "PINK":(255,0,200)}

  MAX_W = 960
  MAX_H = 720

  PATTERN_SIZE = 13

  def __init__(self):
    pass

  def build_image_list(self,data,status):
    h,w,data = self.format_list(data)
    im = np.zeros((h,w,3),dtype=np.uint8)
    for i,d in enumerate(data):

      color = ImageBuilder.COLORS["GRAY"]
      if status[i] == 1:
        color = ImageBuilder.COLORS["WHITE"]
      elif status[i] == 2:
        color = ImageBuilder.COLORS["BLUE"]
      elif status[i] == 3:
        color = ImageBuilder.COLORS["GREEN"]
      cv.line(im,(i,int(h-d*h)),(i,h),color=color)
    im = cv.resize(im,(ImageBuilder.MAX_W,ImageBuilder.MAX_H),interpolation=cv.INTER_AREA )
    return im

  def format_list(self,data):
    data = self.norm(data)
    w = len(data)
    h = int(w/4*3)
    return h,w,data
  def set_data_list(self,data,data_status):
    self.data = self.norm(data)
    self.data_status = data_status
    len_d = len(self.data)
    self.w = len_d
    self.h = int(self.w/4*3)

  def norm(self,l):
    return [(float(i))/(max(l)) for i in l]

  def build_image_arr(self,data):
    h,w = self.get_shape(data)
    im = np.zeros((h*ImageBuilder.PATTERN_SIZE,w*ImageBuilder.PATTERN_SIZE,3),dtype=np.uint8)
    for j,row in enumerate(data):
      for i,col in enumerate(row):
        pattern = self.build_pattern(col)
        im[j*ImageBuilder.PATTERN_SIZE:j*ImageBuilder.PATTERN_SIZE+ImageBuilder.PATTERN_SIZE,i*ImageBuilder.PATTERN_SIZE:i*ImageBuilder.PATTERN_SIZE+ImageBuilder.PATTERN_SIZE] = pattern
    im = cv.resize(im,(700,700),interpolation=cv.INTER_AREA)
    return im

  def build_image_qtree(self,obj,im=None,quads=False):
    if im is None:
      im = np.zeros((Quadratic.WIN_H,Quadratic.WIN_W,3),dtype=np.uint8)
    if obj is not None:
      if type(obj) == QuadTree:
        for p in obj.points:
          self.build_image_qtree(p,im)
        if quads:
          tl = obj.roi.cx-int(obj.roi.w/2),obj.roi.cy-int(obj.roi.h/2)
          br = obj.roi.cx+int(obj.roi.w/2),obj.roi.cy+int(obj.roi.h/2)
          cv.rectangle(im,tl,br,ImageBuilder.COLORS["GREEN"],1)

        for q in obj.child.values():
          self.build_image_qtree(q,im,quads)
      elif type(obj) == Pt:
        color = ImageBuilder.COLORS["WHITE"]
        if obj.highlited:
          color = ImageBuilder.COLORS["RED"]
        cv.circle(im,(int(obj.cx),int(obj.cy)),(obj.radius),color,-1)
    return im

  def build_pattern(self,value):
    pattern = np.zeros((ImageBuilder.PATTERN_SIZE,ImageBuilder.PATTERN_SIZE,3),dtype=np.uint8)
    color = self.get_color(value)
    cv.rectangle(pattern,(1,1),(ImageBuilder.PATTERN_SIZE-2,ImageBuilder.PATTERN_SIZE-2),color,-1)
    return pattern

  def get_shape(self,data):
    return len(data), len(data[0])


  def get_color(self,value):
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
    elif value == 'O':
      color = ImageBuilder.COLORS["PINK"]

    return color

