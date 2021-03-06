#3rd Party
import cv2 as cv
from numpy import zeros, uint8
#System
import random
#Local
from Classes.quadratic import Quadratic,QuadTree,Pt
from cste import *

class ImageBuilder:
  @staticmethod
  def build(b_type,**kwargs):
    if b_type == 'Sorter':
      return ListBuilder.build(**kwargs)
    elif b_type == 'Pathfinder':
      return ArrBuilder.build(**kwargs)
    elif b_type == 'ECA':
      return EcaBuilder.build(**kwargs)
    elif b_type == 'Quadratic':
      return QTreeBuilder.build(**kwargs)
    else:
      raise NotImplementedError('Type not implemented') 

  @staticmethod
  def norm(data):
    return [(float(i))/(max(data)) for i in data]
  
class ListBuilder(ImageBuilder):

  @staticmethod
  def build(**kwargs):
    data = kwargs['data']
    try:
      status = kwargs['status']
      h,w,data = ListBuilder.prepare_data(data)

      image = zeros((h,w,3),dtype=uint8)

      for i, (d,s) in enumerate(zip(data,status)):
        color = COLORS[STATUS[s]]
        cv.line(image,(i,int(h-d*h)),(i,h),color=color)
      image = cv.resize(image,(WIDTH,HEIGHT),interpolation=cv.INTER_AREA)
      return image
    except KeyError:
      pass

  @staticmethod
  def prepare_data(data):
    data = ImageBuilder.norm(data)
    w = len(data)
    h = int(w/4*3) #4:3 image format
    return h, w, data
    


class ArrBuilder(ImageBuilder):
  @staticmethod
  def build(**kwargs):
    #BOTH DIC OF KEY: idx  VALUE: value / status
    data = kwargs['data']
    h, w = len(data), len(data[0])
    image = zeros((h*PATTERN_SIZE,w*PATTERN_SIZE,3),dtype=uint8)
   
    for j,row in enumerate(data):
      for i,col in enumerate(row):
        pattern = PATTERNS[SYM_TO_STAT[col]]
        image[j*PATTERN_SIZE:j*PATTERN_SIZE+PATTERN_SIZE, i*PATTERN_SIZE:i*PATTERN_SIZE+PATTERN_SIZE] = pattern
    image = cv.resize(image,(WIDTH,HEIGHT),interpolation=cv.INTER_AREA)
    return image

class EcaBuilder(ImageBuilder):
  @staticmethod
  def build(**kwargs):
    states = kwargs['data']
    image = kwargs['im']
    step = kwargs['step']
    state = states[step]
    for i,val in enumerate(state):
      image[step][i] = (val*255,val*255,val*255)
    return image

class QTreeBuilder(ImageBuilder):
  @staticmethod
  def build(**kwargs):
    obj = kwargs['data']
    image = kwargs['im']
    quads = kwargs['quads']
    resize = kwargs['resize']

    if image is None:
      image = zeros((Quadratic.WIN_H,Quadratic.WIN_W,3),dtype=uint8)

    if obj is not None:
      if type(obj) == QuadTree:
        for p in obj.points:
          QTreeBuilder.build(data=p,im=image,quads= False,resize=False)
        if quads:
          tl = obj.roi.cx-int(obj.roi.w/2),obj.roi.cy-int(obj.roi.h/2)
          br = obj.roi.cx+int(obj.roi.w/2),obj.roi.cy+int(obj.roi.h/2)
          cv.rectangle(image,tl,br,COLORS["GREEN"],1)

        for q in obj.child.values():
          QTreeBuilder.build(data=q,im=image,quads=quads,resize=False)
      elif type(obj) == Pt:
        color = COLORS["WHITE"]
        if obj.highlited:
          color = COLORS["RED"]

        cv.circle(image,(int(obj.cx),int(obj.cy)),(obj.radius),color,-1)
    if resize:
      image = cv.resize(image,(WIDTH,HEIGHT),interpolation=cv.INTER_AREA)
    return image


if __name__ == "__main__":

  # print(PATTERNS)

  d = [17,86,78,48,75,66,27,35,37,44,70,26,13,97,34,99,62,47,7,95,18,60,55,2,53,56,82,71,21,28,20,68,54,51,72,92,16,79,36,4,23,73,14,57,43,15,22,5,19,77,76,67,89,32,46,74,45,85,30,39,91,41,40,10,24,98,93,33,69,1,49,58,65,83,100,84,88,25,6,63,38,9,12,80,29,42,96,87,50,94,61,52,59,11,31,8,90,81,64,3]
  status = [random.choice([0,1,2,3]) for _ in range(len(d))]
  # d = []
  # status = []
  ib = ImageBuilder()
  im = ImageBuilder.build('sorter',data=d,status=status)
  cv.imshow('im',im)
  cv.waitKey(0)
  cv.destroyAllWindows()