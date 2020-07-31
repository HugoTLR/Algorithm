import numpy as np
import cv2 as cv
from bokeh.palettes import inferno
import time
from math import sqrt
from numba import njit,cuda, types, typed
import numba

#PYTHON 3.6 x64

def hex_to_bgr(hex_str):
  hex_str = hex_str[1:]
  assert len(hex_str) == 6, "Invalid hex"
  rgb = tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
  return rgb

def build_palette(size):
  p = {}
  palette = inferno(size)
  for j in range(size):

    p[j] = hex_to_bgr(palette[j])
  return p


def rescale(val,o_start,o_end,start,end):
  return (val-o_start)*(end-start) / (o_end-o_start)+start



def mandelbrot(W,H,ITER):
  b_x = -2.5
  e_x = 1
  b_y = -1
  e_y = 1
  result = np.zeros((H,W),dtype=np.uint8)
  for j,row in enumerate(result):
    for i,val in enumerate(row):
      x0 = rescale(i,0,W,b_x,e_x)
      y0 = rescale(j,0,H,b_y,e_y)
      x = .0
      y = .0
      x2 = 0
      y2 = 0
      iteration = 0
      while x2 + y2 <= 4 and iteration < ITER:
        y = 2*x*y+y0
        x = x2 - y2 + x0
        x2 = x*x
        y2 = y*y
        iteration += 1
      result[j][i] = iteration
  return result

# function optimized to run on gpu  
@njit
def mandelbrot_complex(W,H,ITER):
  b_x = -2.5
  e_x = 1
  b_y = -1
  e_y = 1
  i_x = (e_x - b_x)
  i_y = (e_y-b_y)

  result = np.zeros((H,W),dtype=np.uint8)
  for j in range(H):
    for i in range(W):
      c = complex(b_x + (i/W) * i_x, b_y + (j/H)*i_y)

      z = 0
      iteration = 0
      while abs(z) <= 2 and iteration < ITER:
        z *= z
        z += c
        iteration += 1
      result[j][i] = iteration
  return result
if __name__ == "__main__":

  W,H = 800,600
  ITER = 256


  palette = build_palette(ITER)
  start = time.time()
  result = mandelbrot(W,H,ITER-1)
  print(f"Mandelbrot in {time.time()-start:.3f} secs")

  im = np.zeros((H,W,3),dtype=np.uint8)
  for j,row in enumerate(result):
    for i,val in enumerate(row):
      im[j][i] = palette[val]
  im = cv.cvtColor(im,cv.COLOR_BGR2RGB)

  start = time.time()
  res = mandelbrot_complex(W,H,ITER-1)
  print(f"GPU Mandelbrot in {time.time()-start:.3f} secs")
  
  im2 = np.zeros((H,W,3),dtype=np.uint8)
  for j,row in enumerate(res):
    for i,val in enumerate(row):
      im2[j][i] = palette[val]
  im2 = cv.cvtColor(im2,cv.COLOR_BGR2RGB)

  # for r in res:
  #   print(' '.join([str(rr) for rr in r]))


  cv.imshow("Im",np.hstack([im,im2]))
  cv.waitKey()
  cv.destroyAllWindows()