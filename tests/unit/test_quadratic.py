import unittest

from random import randint,choice
from Classes import quadratic as quad

class TestRange(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    if cls is not TestRange and cls.setUp is not TestRange.setUp:
      orig_setUp = cls.setUp
      def setUpOverride(self, *args, **kwargs):
        TestRange.setUp(self)
        return orig_setUp(self, *args, **kwargs)
      cls.setUp = setUpOverride

  def setUp(self):

    self.h = randint(0,800)
    self.w = randint(0,1000)
    self.cx, self.cy = randint(0,self.w), randint(0,self.h)

  def test_init(self):
    self.assertTrue(self.cx >= 0)
    self.assertTrue(self.cy >= 0)

  def test_eq(self):
    ret = quad.Range(self.cx,self.cy).__eq__(quad.Range(self.cx,self.cy))
    self.assertTrue(ret)

class TestPt(TestRange):
  def setUp(self):
    self.radius = randint(1,10)
    self.pt = quad.Pt(self.cx,self.cy,self.radius)

  def test_init(self):
    self.assertTrue(self.radius > 0)

  def test_eq(self):
    ret = self.pt.__eq__(quad.Pt(self.cx,self.cy,self.radius))
    self.assertTrue(ret)

  def test_contains(self):
    pt = quad.Pt(randint(self.cx-self.radius,self.cx+self.radius),\
                  randint(self.cy-self.radius,self.cy+self.radius),\
                  randint(1,10))

    ret = self.pt.contains(pt)
    self.assertTrue(ret)

  def test_move(self):
    self.pt.move()
    self.assertTrue(type(self.pt.cx) == int)
    self.assertTrue(type(self.pt.cy) == int)
    self.assertFalse(self.pt.highlited)

class TestQuad(TestRange):
  def setUp(self):
    self.quad = quad.Quad(self.cx,self.cy,self.w,self.h)

  def test_init(self):
    self.assertTrue(self.w > 0)
    self.assertTrue(self.h > 0)

  def test_contains(self):
    pt = quad.Pt(randint(self.cx-quad.Range.HALF(self.w),self.cx+quad.Range.HALF(self.w)),\
                randint(self.cy-quad.Range.HALF(self.h),self.cy+quad.Range.HALF(self.h)),randint(1,10))
    
    ret = self.quad.contains(pt)
    self.assertTrue(ret)

  def test_intersects(self):
    pt = quad.Pt(randint(self.cx-quad.Range.HALF(self.w),self.cx+quad.Range.HALF(self.w)),\
                randint(self.cy-quad.Range.HALF(self.h),self.cy+quad.Range.HALF(self.h)),\
                randint(1,10))
    # print(str(self.quad),str(pt))
    ret = self.quad.intersects(pt)
    self.assertTrue(ret)

    qd = quad.Quad(randint(self.cx - quad.Range.HALF(self.w), self.cx + quad.Range.HALF(self.w) ),\
                    randint(self.cy - quad.Range.HALF(self.h), self.cy + quad.Range.HALF(self.h) ),\
                    self.w,\
                    self.h)
    ret = self.quad.intersects(qd)
    self.assertTrue(ret)

if __name__ == "__main__":
  unittest.main()