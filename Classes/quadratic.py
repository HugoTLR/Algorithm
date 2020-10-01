#3rd Party
import cv2 as cv
#System
import math
import random
from time import time
#Local


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
  def __init__(self,roi,pt_limit):
    self.limit = pt_limit
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
    self.child["NE"] = QuadTree( (self.roi.cx + Range.QUARTER(self.roi.w),self.roi.cy - Range.QUARTER(self.roi.h),Range.HALF(self.roi.w),Range.HALF(self.roi.h)  ) ,self.limit) 
    self.child["SE"] = QuadTree( (self.roi.cx + Range.QUARTER(self.roi.w),self.roi.cy + Range.QUARTER(self.roi.h),Range.HALF(self.roi.w),Range.HALF(self.roi.h)  ) ,self.limit) 
    self.child["SW"] = QuadTree( (self.roi.cx - Range.QUARTER(self.roi.w),self.roi.cy + Range.QUARTER(self.roi.h),Range.HALF(self.roi.w),Range.HALF(self.roi.h)  ) ,self.limit) 
    self.child["NW"] = QuadTree( (self.roi.cx - Range.QUARTER(self.roi.w),self.roi.cy - Range.QUARTER(self.roi.h),Range.HALF(self.roi.w),Range.HALF(self.roi.h)  ) ,self.limit) 
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
      if len(self.points) < self.limit:
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


class Quadratic:
  SEARCH_H = 50
  WIN_W = 600
  WIN_H = 400
  RADIUS = 2

  def __init__(self,nb_points = 500,pt_limit = 20):
    self.nb_points = nb_points
    self.pt_limit = pt_limit
    self.show_quad = False
    self.collision_loop = False

  def update_points(self,points):
    self.points = points

  def create_qtree(self):
    assert len(self.points) > 0, "At least one point needed in order to build the tree"
    self.qtree = QuadTree(( int(Quadratic.WIN_W/2),int(Quadratic.WIN_H/2),Quadratic.WIN_W,Quadratic.WIN_H),self.pt_limit)
    for p in self.points:
      self.qtree.insert(p)

  def update_qtree(self,qtree):
    #start = time()

    if qtree is not None:
      for points in qtree.points:
        points.move()
      if qtree.divided:
        for v in qtree.child.values():
          self.update_qtree(v)
    return qtree
  def check_collision(self,obj):
    for p in obj.points:
      collided_pts = self.qtree.query(p,[])
      if collided_pts:
        if len(collided_pts) > 1: #We have more than our point
          p.highlited = True
          for c in collided_pts:
            c.highlited = True
    for q in obj.child.values():
      self.check_collision(q)
    return obj

  def normal_collision_check(self):
    for j,p in enumerate(self.points):
      for i,pt in enumerate(self.points):
        if p.__eq__(pt):
          continue
        if p.contains(pt):
          self.points[j].highlited = True
          self.points[i].highlited = True
