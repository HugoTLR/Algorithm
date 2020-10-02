#3rd party
from cv2 import circle, COLOR_GRAY2BGR, cvtColor, INTER_AREA, line, resize
import cv2 as cv
from opensimplex import OpenSimplex
from numpy import array, full, uint8
#System
from math import ceil, cos, sin, radians, sqrt
from random import choice, random, uniform, randint
import sys
#Local
from cste import *

class Other:
  def __init__(self):
    pass

  def rescale(self,val,o_start,o_end,start,end):
    return (val-o_start)*(end-start) / (o_end-o_start)+start

  def scale(self,grid):
    return array([[self.rescale(grid[j][i],-1,1,0,1) for i in range(len(grid[0]))] for j in range(len(grid))])



class MarchingSquare(Other):
  def __init__(self):
    super(MarchingSquare,self).__init__()
    self.ops = OpenSimplex()
    self.z = 0

  def update(self):
    img = full((M_HEIGHT,M_WIDTH),127,uint8)
    grid = array([[(self.ops.noise3d(i/FEATURE_SIZE,j/FEATURE_SIZE,self.z)) for i in range(N_WIDTH + 1)] for j in range(N_HEIGHT + 1)])
    grid = self.scale(grid)

    img = self.draw_corners(img,grid)
    img = self.draw_lines(img,grid)

    self.z += Z_INC
    img = cvtColor(img,COLOR_GRAY2BGR)
    img = resize(img,(WIDTH,HEIGHT),interpolation=INTER_AREA)
    return img

  def state(self,a,b,c,d):
    return 1 * a + 2 * b + 4 * c + 8 * d

  def draw_corners(self,img,grid):
    for j, row in enumerate(grid):
      for i, col in enumerate(row):
        circle(img,(i*RESO,j*RESO),3,int(col*255),-1)
    return img

  def draw_lines(self,img,grid):
    for j, row in enumerate(grid[:-1]):
      for i, col in enumerate(row[:-1]):
        a = grid[j][i]
        b = grid[j][i + 1]
        c = grid[j + 1][i + 1]
        d = grid[j + 1][i]

        st = self.state(round(a),round(b),round(c),round(d))
        img = self.draw_line(st,img,j,i)
    return img

  def draw_line(self,state, img, j, i):
    a = ( int( i * RESO + RESO / 2 ), j * RESO )
    b = ( ( i + 1 ) * RESO          , int( j * RESO + RESO / 2 ) )
    c = ( int( i * RESO + RESO / 2 ), ( j + 1 ) * RESO           )
    d = ( i * RESO                  , int( j * RESO + RESO / 2 ) )

    if state in [1, 10, 14]:
      line(img,a,d,255,1)
    if state in [2, 5, 13]:
      line(img,a,b,255,1)
    if state in [3, 12]:
      line(img,b,d,255,1)
    if state in [4, 10, 11]:
      line(img,b,c,255,1)
    if state in [5, 7, 8]:
      line(img,c,d,255,1)
    if state in [6, 9]:
      line(img,a,c,255,1)

    return img


class Raycast_2D(Other):
  def __init__(self):
    super(Raycast_2D,self).__init__()
    self.ops = OpenSimplex()
    self.xoff = 0
    self.yoff = 10

    self.boundaries = self.generate_boundaries()
    self.particle = Particle(int(WIDTH/2),int(HEIGHT/2))
    self.initialise_image()

  def generate_boundaries(self,nb_bound = 6):
    boundaries = self.generate_borders()
    boundaries.extend(self.generate_bounds(nb_bound))
    return boundaries

  def generate_borders(self):
    top = Boundary((0,0),(WIDTH,0))
    right = Boundary((WIDTH,0),(WIDTH,HEIGHT))
    bot = Boundary((0,HEIGHT),(WIDTH,HEIGHT))
    left = Boundary((0,0),(0,HEIGHT))
    return [top,right,bot,left]

  def generate_bounds(self,nb):
    boundaries = []
    for _ in range(nb):
      boundaries.append( Boundary( ( randint(0,WIDTH), randint(0,HEIGHT) ), ( randint(0,WIDTH), randint(0,HEIGHT) ) ) )
    return boundaries

  def initialise_image(self):
    self.image = full((HEIGHT,WIDTH),50,dtype=uint8)
    for boundary in self.boundaries:
      self.image = boundary.draw(self.image)

  def draw(self):
    self.image = self.particle.draw(self.image,self.boundaries)

  def update(self):
    self.initialise_image()
    noise_X = self.ops.noise2d(self.xoff,self.xoff)
    noise_X = self.rescale(noise_X,-1,1,0,1) * WIDTH
    noise_Y = self.ops.noise2d(self.yoff,self.yoff)
    noise_Y = self.rescale(noise_Y,-1,1,0,1) * HEIGHT
    self.particle.update(int(noise_X),int(noise_Y))

    self.draw()

    self.xoff += .01
    self.yoff += .01

    return cvtColor(self.image,COLOR_GRAY2BGR)


class Boundary:
  def __init__(self,a,b):
    self.a = a
    self.b = b

  def draw(self,img):
    line(img,self.a,self.b,0,3)
    return img

class Particle:
  def __init__(self,x,y,nb_rays=360):
    self.x = x
    self.y = y
    self.rays = self.build_rays(nb_rays)

  def update(self,x,y):
    self.x = x
    self.y = y

  def build_rays(self,nb_rays):
    deg_per_rays = int(360/nb_rays)
    rays = [Ray(self,radians(i)) for i in range(0,360,deg_per_rays)]
    return rays

  def dist(self,p2):
    return sqrt( (p2[0]-self.x)**2 + (p2[1] - self.y)**2 )

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
    circle(img,(self.x,self.y),5,255,-1)
    return img


class Ray:
  def __init__(self,parent,angle):
    self.parent = parent
    self.direction = self.dir_from_angle(angle)

  def dir_from_angle(self,angle):
    return (cos(angle),sin(angle))

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
      return None

    t = ( (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4) ) / denominator
    u = -( (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3) ) / denominator
    if t >= 0 and t <= 1 and u >= 0:
      x = x1 + t * (x2 - x1)
      y = y1 + t * (y2 - y1)
      return (int(x),int(y))
    else:
      return None

  def draw(self,img,pt):
    line(img,(self.parent.x,self.parent.y),pt,200,1)
    return img

