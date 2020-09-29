import cv2 as cv
import numpy as np

from random import choice,random, uniform

from math import ceil

def draw_corners(img,grid):
  for j, row in enumerate(grid):
    for i, col in enumerate(row):
      cv.circle(img,(i*RESO,j*RESO),3,int(col*255),-1)
  return img

def draw_lines(img,grid):
  for j, row in enumerate(grid[:-1]):
    for i, col in enumerate(row[:-1]):
      a = grid[j][i]
      b = grid[j][i + 1]
      c = grid[j + 1][i + 1]
      d = grid[j + 1][i]

      st = state(round(a),round(b),round(c),round(d))
      # img = cv.putText(img, str(st), (int(i*RESO + RESO/3),int(j*RESO + RESO/2)), cv.FONT_HERSHEY_SIMPLEX , 0.3, 0, 1, cv.LINE_AA) 
      img = draw_line(st,img,j,i)
  return img

def draw_line(state, img, j, i):
  a = ( int( i * RESO + RESO / 2 ), j * RESO )
  b = ( ( i + 1 ) * RESO          , int( j * RESO + RESO / 2 ) )
  c = ( int( i * RESO + RESO / 2 ), ( j + 1 ) * RESO           )
  d = ( i * RESO                  , int( j * RESO + RESO / 2 ) )

  if state in [1, 10, 14]:
    cv.line(img,a,d,255,1)
  if state in [2, 5, 13]:
    cv.line(img,a,b,255,1)
  if state in [3, 12]:
    cv.line(img,b,d,255,1)
  if state in [4, 10, 11]:
    cv.line(img,b,c,255,1)
  if state in [5, 7, 8]:
    cv.line(img,c,d,255,1)
  if state in [6, 9]:
    cv.line(img,a,c,255,1)

  return img

      
def state(a,b,c,d):
  return 1 * a + 2 * b + 4 * c + 8 * d

def rescale(val,o_start,o_end,start,end):
  return (val-o_start)*(end-start) / (o_end-o_start)+start

def scale(grid):
  return [[rescale(grid[j][i],-1,1,0,1) for i in range(len(grid[0]))] for j in range(len(grid))]


if __name__ == "__main__":
  WIDTH = 600
  HEIGHT = 400

  RESO = 15

  from pynoise import perlin
  perlin_gen = perlin.Perlin(frequency=10)

  cpt = 0.0
  while True:
    img = np.full((HEIGHT,WIDTH),127,dtype=np.uint8)
    grid = np.array([[(perlin_gen.value(j/HEIGHT,i/WIDTH,cpt)) for i in range(0,WIDTH+RESO,RESO)] for j in range(0,HEIGHT+RESO,RESO)])
    grid = scale(grid)

    img = draw_corners(img,grid)
    img = draw_lines(img,grid)


    cv.imshow('im',img)
    key = cv.waitKey(1)
    if key == ord('q') & 0xFF:
      break
    cpt += .01
    if cpt >= 10:
      cpt = 0
  cv.destroyAllWindows()


