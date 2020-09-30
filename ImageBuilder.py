import cv2 as cv

from numpy import zeros, uint8
import random
STATUS = {0: "GRAY",
          1: "WHITE",
          2:"BLUE",
          3:"GREEN"
}

COLORS = {"WHITE":(255,255,255),\
            "GRAY":(75,75,75),\
            "BLUE":(0,0,255),\
            "GREEN":(0,255,0),\
            "RED": (255,0,0),\
            "BLACK": (0,0,0),\
            "ORANGE":(255,125,0),\
            "PURPLE":(200,0,255),\
            "PINK":(255,0,200)}

WIDTH = 960
HEIGHT = 720

class ImageBuilder:
  @staticmethod
  def build(**kwargs):
    data = kwargs['data']
    if type(data) == list:
      return ListBuilder.build(**kwargs)
    else:
      raise NotImplementedError('Call child method plz') 

  @staticmethod
  def norm(data):
    return [(float(i))/(max(data)) for i in data]
class ListBuilder(ImageBuilder):

  @staticmethod
  def build(**kwargs):
    #BOTH DIC OF KEY: idx  VALUE: value / status
    data = kwargs['data']
    try:
      print(f"{min(data)=} {max(data)=}")
      status = kwargs['status']
      # for i, (d,s) in enumerate(zip(data,status)):
      #   print(f"{i=} : {d=} {s=}")
      h,w,data = ListBuilder.prepare_data(data)
      print(f"{h=} {w=} {min(data)=} {max(data)=}")

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
    





if __name__ == "__main__":


  d = [17,86,78,48,75,66,27,35,37,44,70,26,13,97,34,99,62,47,7,95,18,60,55,2,53,56,82,71,21,28,20,68,54,51,72,92,16,79,36,4,23,73,14,57,43,15,22,5,19,77,76,67,89,32,46,74,45,85,30,39,91,41,40,10,24,98,93,33,69,1,49,58,65,83,100,84,88,25,6,63,38,9,12,80,29,42,96,87,50,94,61,52,59,11,31,8,90,81,64,3]
  status = [random.choice([0,1,2,3]) for _ in range(len(d))]
  # d = []
  # status = []
  ib = ImageBuilder()
  im = ImageBuilder.build(data=d,status=status)
  cv.imshow('im',im)
  cv.waitKey(0)
  cv.destroyAllWindows()