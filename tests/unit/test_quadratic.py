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
    pt = quad.Pt(randint(self.cx-self.radius,self.cx+self.radius-1),\
                  randint(self.cy-self.radius,self.cy+self.radius-1),\
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
    """
    Test that quad contain point
    """
    pt = quad.Pt(randint(self.cx-quad.Range.HALF(self.w),self.cx-1+quad.Range.HALF(self.w)),\
                randint(self.cy-quad.Range.HALF(self.h),self.cy-1+quad.Range.HALF(self.h)),\
                randint(1,10))
    
    ret = self.quad.contains(pt)
    self.assertTrue(ret)

  def test_intersects(self):
    """
    Test that quad intersects with point
    """
    pt = quad.Pt(randint(self.cx-quad.Range.HALF(self.w),self.cx+quad.Range.HALF(self.w)),\
                randint(self.cy-quad.Range.HALF(self.h),self.cy+quad.Range.HALF(self.h)),\
                randint(1,10))
    ret = self.quad.intersects(pt)
    self.assertTrue(ret)
    """

    Test that quad intersects with quad

    """
    qd = quad.Quad(randint(self.cx - quad.Range.HALF(self.w), self.cx + quad.Range.HALF(self.w) ),\
                    randint(self.cy - quad.Range.HALF(self.h), self.cy + quad.Range.HALF(self.h) ),\
                    self.w,\
                    self.h)
    ret = self.quad.intersects(qd)
    self.assertTrue(ret)

class TestQuadTree(unittest.TestCase):
  def setUp(self):
    self.h = randint(0,800)
    self.w = randint(0,1000)
    self.cx, self.cy = randint(0,self.w), randint(0,self.h)
    self.pt_limit = randint(1,50)
    self.qtree = quad.QuadTree((self.cx,self.cy,self.w,self.h),self.pt_limit)
    self.pt =  quad.Pt(randint(self.cx-quad.Range.HALF(self.w),self.cx+quad.Range.HALF(self.w)),\
            randint(self.cy-quad.Range.HALF(self.h),self.cy+quad.Range.HALF(self.h)),\
            randint(1,10))
  def test_divide(self):
    self.qtree.divide()
    self.assertTrue(self.qtree.divided)
    self.assertIsInstance(self.qtree.child['NE'], quad.QuadTree)
    self.assertIsInstance(self.qtree.child['NW'], quad.QuadTree)
    self.assertIsInstance(self.qtree.child['SE'], quad.QuadTree)
    self.assertIsInstance(self.qtree.child['SW'], quad.QuadTree)

  def test_push_to_child(self):
    self.test_divide()

    n_pts_ne = len(self.qtree.child['NE'].points)
    n_pts_nw = len(self.qtree.child['NW'].points)
    n_pts_se = len(self.qtree.child['SE'].points)
    n_pts_sw = len(self.qtree.child['SW'].points)
    self.qtree.push_to_child(self.pt)
    self.assertTrue(len(self.qtree.child['NE'].points) in [n_pts_ne,n_pts_ne+1])
    self.assertTrue(len(self.qtree.child['NW'].points) in [n_pts_nw,n_pts_nw+1])
    self.assertTrue(len(self.qtree.child['SE'].points) in [n_pts_se,n_pts_se+1])
    self.assertTrue(len(self.qtree.child['SW'].points) in [n_pts_sw,n_pts_sw+1])


  def test_insert(self):
    n_pts = len(self.qtree.points)
    self.qtree.insert(self.pt)
    self.assertEqual(len(self.qtree.points), n_pts + 1)

  def test_query(self):
    self.test_insert()
    result = self.qtree.query(self.pt)
    self.assertIn(self.pt, result)


class TestQuadratic(unittest.TestCase):
  def setUp(self):
    self.quadratic = quad.Quadratic(randint(1,500),randint(1,20))

  def test_update_points(self):
    pts = [quad.Pt(randint(0,100),randint(0,100),randint(0,10)) for _ in range(self.quadratic.nb_points)]
    self.quadratic.update_points(pts)
    self.assertEqual(pts,self.quadratic.points)

  def test_create_qtree(self):
    self.test_update_points()
    self.quadratic.create_qtree()
    self.assertIsInstance(self.quadratic.qtree, quad.QuadTree)

  def test_update_qtree(self):
    """
    Should be an integration test ?
    """
    pass

  def test_check_collision(self):
    """
    Should be an integration test ?
    """
    pass

  def test_normal_collision_check(self):
    """
    Should be an integration test ?
    """
    pass

if __name__ == "__main__":
  unittest.main()