#3rd party
from cv2 import circle, COLOR_GRAY2BGR, cvtColor, INTER_AREA, line, resize
import cv2 as cv
from opensimplex import OpenSimplex
from numpy import array, full, uint8
#System
from math import ceil
from random import choice, random, uniform
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
    grid = array([[(self.ops.noise3d(i/FEATURE_SIZE,j/FEATURE_SIZE,self.z)) for i in range(N_WIDTH)] for j in range(N_HEIGHT)])
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


class 2D_Raycast(Other):
  def __init__(self):
    pass
