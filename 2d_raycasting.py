import cv2 as cv
import numpy as np
import math
import sys
from random import randint

CST = 10
class Ray:
  def __init__(self,parent,angle):
    self.parent = parent
    self.direction = self.dir_from_angle(angle)

  def dir_from_angle(self,angle):
    return (math.cos(angle),math.sin(angle))

  def __str__(self):
    return f"Ray {(self.parent.x,self.parent.y)}: {self.direction}"

  def cast(self,bound):
    x1 = bound.a[0]
    y1 = bound.a[1]
    x2 = bound.b[0]
    y2 = bound.b[1]
    x3 = self.parent.x
    y3 = self.parent.y
    x4 = x3 + self.direction[0]
    y4 = y3 + self.direction[1]

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
      # print(f"{denominator=} {(x1,y1)}{ (x2,y2)}")
      return None

    t = ( (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4) ) / denominator
    u = -( (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3) ) / denominator

    # print(f"{self.direction=} {denominator=}, {t=}, {u=} {(x1,y1)}{ (x2,y2)}")
    if t >= 0 and t <= 1 and u >= 0:
      x = x1 + t * (x2 - x1)
      y = y1 + t * (y2 - y1)
      return (int(x),int(y))
    else:
      return None

  def draw(self,img,pt):
    cv.line(img,(self.parent.x,self.parent.y),pt,255,1)
    return img

class Boundary:
  def __init__(self,a,b):
    self.a = a
    self.b = b

  def draw(self,img):
    cv.line(img,self.a,self.b,0,3)
    return img

class Particle:
  def __init__(self,x,y,nb_rays):
    self.x = x
    self.y = y
    self.rays = self.build_rays(nb_rays)

  def update(self,x,y):
    self.x = x
    self.y = y


  def build_rays(self,nb):
    deg_per_rays = int(360/nb)
    rays = [Ray(self,math.radians(i)) for i in range(0,360,deg_per_rays)]
    return rays

  def dist(self,p2):
    return math.sqrt( (p2[0]-self.x)**2 + (p2[1] - self.y)**2 )

  def draw(self,img,boundaries):
    for ray in self.rays:
      min_d = sys.maxsize
      min_pt = None
      for bound in boundaries:
        pt = ray.cast(bound)
        if pt is not None:
          d = self.dist(pt)
          if d < min_d:
            min_d = d
            min_pt = pt

      
      if min_pt is not None:
        img = ray.draw(img,min_pt)
    cv.circle(img,(self.x,self.y),5,127,-1)
    return img

def init(boundaries):
  img = np.full((HEIGHT,WIDTH),50,dtype=np.uint8)
  for bound in boundaries:
    img = bound.draw(img)
  return img

def draw(img,**kwargs):
  particle = kwargs['origin']
  boundaries = kwargs['boundaries']

  
  #Particle
  img = particle.draw(img,boundaries)

  return img

def generate_borders():
  top = Boundary((0,0),(WIDTH,0))
  right = Boundary((WIDTH,0),(WIDTH,HEIGHT))
  bot = Boundary((0,HEIGHT),(WIDTH,HEIGHT))
  left = Boundary((0,0),(0,HEIGHT))
  return [top,right,bot,left]
#define the events for the 
# mouse_move. 

def generate_boundaries(nb):
  boundaries = []
  for _ in range(nb):
    boundaries.append( Boundary( ( randint(0,WIDTH-1), randint(0,HEIGHT-1) ), ( randint(0,WIDTH-1), randint(0,HEIGHT-1) ) ) )
  return boundaries

def mouse_move(event, x, y, flags, param): 
  # to check if left mouse  
  # button was clicked 
  if event == cv.EVENT_MOUSEMOVE: 
    img = init(param[0])
    param[1].update(x,y)

  
    img = draw(img,origin=param[1],boundaries=param[0])
    cv.imshow('image', img) 
    # print("\n\n\n")


if __name__ == "__main__":
  WIDTH = 600
  HEIGHT = 400


  # boundaries = generate_borders()
  # boundaries.extend([Boundary((100,100),(100,200)),Boundary((900,100),(900,400)),Boundary((300,150),(100,280)),Boundary((800,40),(500,80))])
 
  boundaries = generate_boundaries(6)
  img = init(boundaries)

  particle = Particle(int(WIDTH/2),int(HEIGHT/2),50)

  img = draw(img,origin=particle,boundaries=boundaries)

  cv.imshow('image', img) 


  

  
  cv.setMouseCallback('image', mouse_move,[boundaries,particle]) 
  cv.waitKey() 
  cv.destroyAllWindows()