import math
import random
import cv2 as cv
from time import time


class Quadratic:
  def __init__(self):
    pass

  





class Range:
  HALF = lambda x: int(x/2)
  QUARTER = lambda x: int(x/4)

  def __init__(self,cx,cy):
    self.cx = cx
    self.cy = cy

  def __eq__(self,other):
    if type(other) != type(self):
      raise TypeError
    return self.cx == other.cx and self.cy == other.cy
  def __str__(self):
    return (self.cx,self.cy)

  def contains(self):
    raise NotImplementedError
  def intersects(self,other):
    raise NotImplementedError
  def move(self):
    raise NotImplementedError
  
class Pt(Range):
  def __init__(self,cx,cy,radius):
    self.cx = cx
    self.cy = cy
    self.radius = radius #Just for collision test for performance
    self.depth = None
    self.highlited = False
    #Here we can add class object later on to use this generic quadtree

  def __eq__(self,other):
    return Range.__eq__(self,other) and self.radius == other.radius

  def contains(self,p):
    return math.sqrt((p.cx-self.cx)**2+(p.cy-self.cy)**2) <= (self.radius+p.radius)

  def intersects(self,other):
    raise NotImplementedError

  def move(self):
    self.cx += random.choice([-1,1])
    self.cy += random.choice([-1,1])
    self.cx = int(self.cx)
    self.cy = int(self.cy)
    self.highlited = False #Reset the collision boolean

  def __str__(self):
    return f"({self.cx},{self.cy})"
class Quad(Range):
  def __init__(self,cx,cy,w,h):
    Range.__init__(self,cx,cy)
    self.w = w
    self.h = h

  def __str__(self):
    return f"{(self.cx,self.cy,self.w,self.h)}"
  def contains(self,p):
    return (p.cx >= self.cx-Range.HALF(self.w) and p.cx < self.cx + Range.HALF(self.w)) and \
        (p.cy >= self.cy-Range.HALF(self.h) and p.cy < self.cy + Range.HALF(self.h))
  def intersects(self,other):
    if type(other) == Quad:
      return not (self.cx + Range.HALF(self.w) < other.cx - Range.HALF(other.w) or other.cx + Range.HALF(other.w) < self.cx -  Range.HALF(self.w) or \
          self.cy + Range.HALF(self.h) < other.cy - Range.HALF(other.h) or other.cy + Range.HALF(other.h) < self.cy - Range.HALF(self.h))
    elif type(other) == Pt:
      return not (self.cx + Range.HALF(self.w) < other.cx - other.radius or other.cx + other.radius < self.cx - Range.HALF(self.w) or \
          self.cy + Range.HALF(self.h) < other.cy - other.radius or other.cy + other.radius < self.cy - Range.HALF(self.h))

  def move(self):
    raise NotImplementedError







class QuadTree:
  def __init__(self,roi):
    self.roi = Quad(roi[0],roi[1],roi[2],roi[3])
    self.child = {}
    self.points = []

    self.divided = False

  def __str__(self):
    res = f"{self.roi} divided:{self.divided} points : {[p.__str__() for p in self.points]}\n"
    if self.divided:
      for v in self.child.values():
        res = res + v.__str__()
    return res




  def divide(self):
    self.child["NE"] = QuadTree( (self.roi.cx + Range.QUARTER(self.roi.w),self.roi.cy - Range.QUARTER(self.roi.h),Range.HALF(self.roi.w),Range.HALF(self.roi.h)  ) ) 
    self.child["SE"] = QuadTree( (self.roi.cx + Range.QUARTER(self.roi.w),self.roi.cy + Range.QUARTER(self.roi.h),Range.HALF(self.roi.w),Range.HALF(self.roi.h)  ) ) 
    self.child["SW"] = QuadTree( (self.roi.cx - Range.QUARTER(self.roi.w),self.roi.cy + Range.QUARTER(self.roi.h),Range.HALF(self.roi.w),Range.HALF(self.roi.h)  ) ) 
    self.child["NW"] = QuadTree( (self.roi.cx - Range.QUARTER(self.roi.w),self.roi.cy - Range.QUARTER(self.roi.h),Range.HALF(self.roi.w),Range.HALF(self.roi.h)  ) ) 
    self.divided = True

  def push_to_child(self,p,d=1):
    for v in self.child.values():
      if v.roi.contains(p):
        v.insert(p,d)
        break

  def insert(self,p,d=0):
    if not self.roi.contains(p):
      return
    else:
      if len(self.points) < POINT_LIMIT:
        p.depth = d
        self.points.append(p)
      else:
        if not self.divided:
          self.divide()
        self.push_to_child(p,d+1)



  

  def query(self,ran,found=[]):
    if not self.roi.intersects(ran):
      return

    for p in self.points:
      if ran.contains(p):
        found.append(p)

    for v in self.child.values():
      v.query(ran,found)

    return found

def build_qtree(points):
  start = time()
  qtree = QuadTree(( int(WIN_W/2),int(WIN_H/2),WIN_W,WIN_H))
  for p in points:
    qtree.insert(p)
  # print(f"QTree created in {time()-start:.03f} seconds") 
  return qtree

def draw(im,obj,rect=False):
  if type(obj) == QuadTree:
    for p in obj.points:
      draw(im,p)
    if rect:
      tl = obj.roi.cx-int(obj.roi.w/2),obj.roi.cy-int(obj.roi.h/2)
      br = obj.roi.cx+int(obj.roi.w/2),obj.roi.cy+int(obj.roi.h/2)
      cv.rectangle(im,tl,br,(0,255,0),1)

    for q in obj.child.values():
      draw(im,q,rect)
  elif type(obj) == Pt:
    color = (255,255,255)
    if obj.highlited:
      color = (0,0,255)
    cv.circle(im,(int(obj.cx),int(obj.cy)),(obj.depth+1),color,-1)


def update_qtree(qtree):
  #start = time()
  for points in qtree.points:
    points.move()
  if qtree.divided:
    for v in qtree.child.values():
      update_qtree(v)
  return qtree
def check_collision(obj):
  for p in obj.points:
    # ell = Pt(p.cx,p.cy,p.radius)
    collided_pts = qtree.query(p,[])
    if collided_pts:
      if len(collided_pts) > 1: #We have more than our point
        p.highlited = True
        for c in collided_pts:
          c.highlited = True
  for q in obj.child.values():
    check_collision(q)
  return obj

def normal_collision_check(points):
  for j,p in enumerate(points):
    for i,pt in enumerate(points):
      if p.__eq__(pt):
        continue
      if p.contains(pt):
        points[j].highlited = True
        points[i].highlited = True


if __name__ == "__main__":
  import numpy as np
  show_every = 50
  SEARCH_W = 100
  SEARCH_H = 50
  WIN_W = 600
  WIN_H = 400
  NB_POINTS = 500
  RADIUS = 2

  POINT_LIMIT = 20

  
  points = [Pt(random.randint(0,WIN_W),random.randint(0,WIN_H),random.randint(2,2)) for _ in range(NB_POINTS)]


  text_position = (10,WIN_H-20)

  q_tree_colision_method = True
  q_tree_rect = False
  qtree = build_qtree(points)
  while True:


    start = time()
    im = np.zeros((WIN_H,WIN_W,3))
    if q_tree_colision_method:
      qtree = check_collision(qtree)
    else:
      normal_collision_check(points)
    draw(im,qtree,rect=q_tree_rect)
    # points = qtree.query(qtree.roi,[])
    qtree = update_qtree(qtree)
    end = time()


    cv.putText(im,f"Average FPS: {1/(end-start):.5f}",\
                text_position,cv.FONT_HERSHEY_SIMPLEX,.5,(0, 255, 255),2)
    # print(f"Average FPS: {1/(end-start):.5f}")
    cv.imshow("im",im)
    key = cv.waitKey(1)
    if key == ord('q') & 0xFF:
      break
    elif key == ord('s') & 0xFF:
      q_tree_colision_method = not q_tree_colision_method
      print(q_tree_colision_method)
    elif key == ord('r') & 0xFF:
      q_tree_rect = not q_tree_rect

  cv.destroyAllWindows()