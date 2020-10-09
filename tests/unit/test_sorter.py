import unittest

from Classes import sorter

class BaseTestCases:

  class TestSorter(unittest.TestCase):

    def setUp(self):
      self.data = [0,9,8,6,3,5,4,2,1,7]
      self.data_size = len(self.data)

    def test_swap(self):
      i, j = 1, 8
      self.assertTrue(self.data_size > 0)
      self.assertTrue( (i >= 0 and i < self.data_size) )
      self.assertTrue( (j >= 0 and j < self.data_size and j != i ))

    # def test_build_status(self):
    #   raise NotImplementedError('Use child function')


class TestInsertion(BaseTestCases.TestSorter):
  def setUp(self):
    super(TestInsertion, self).setUp()
    self.sorter = sorter.Insertion()

  def test_insertion_swap(self):
    super(TestInsertion, self).test_swap()

  def test_insertion_build_status(self):
    """
    Test that we are correctly building insertion sort status
    """
    idx = 3
    result = self.sorter.build_status(idx,self.data_size)
    self.assertEqual(result, [1,1,1,1,2,0,0,0,0,0])


class TestSelection(BaseTestCases.TestSorter):
  def setUp(self):
    super(TestSelection, self).setUp()
    self.sorter = sorter.Selection()

  def test_selection_swap(self):
    super(TestSelection, self).test_swap()

  def test_selection_build_status(self):
    """
    Test that we are correctly building selection sort status
    """
    idx = 3
    idx2 = 5
    result = self.sorter.build_status(idx,idx2,self.data_size)
    self.assertEqual(result, [1,1,1,1,0,2,0,0,0,0])


class TestQuicksort(BaseTestCases.TestSorter):
  def setUp(self):
    super(TestQuicksort, self).setUp()
    self.sorter = sorter.Quicksort()

  def test_quicksort_swap(self):
    super(TestQuicksort, self).test_swap()

  def test_quicksort_build_status(self):
    """
    Test that we are correctly building quicksort status
    """
    result = self.sorter.build_status(self.data_size, self.data_size - 1)
    self.assertEqual(result, [0,0,0,0,0,0,0,0,0,2])

    i = 5
    low = 4
    high = 6
    result = self.sorter.build_status(self.data_size, i, low, high)
    self.assertEqual(result, [1,1,1,1,3,2,3,0,0,0])

class TestBubblesort(BaseTestCases.TestSorter):
  def setUp(self):
    super(TestBubblesort, self).setUp()
    self.sorter = sorter.Bubblesort()

  def test_bubblesort_swap(self):
    super(TestBubblesort, self).test_swap()

  def test_bubblesort_build_status(self):
    """
    Test that we are correctly building bubblesort status
    """
    result = self.sorter.build_status(self.data_size)
    self.assertEqual(result, [0,0,0,0,0,0,0,0,0,0])
    
    idx = 2
    n = self.data_size - 1 
    result = self.sorter.build_status(self.data_size,idx - 1, idx, n)
    self.assertEqual(result, [0,2,2,0,0,0,0,0,0,1])




class TestBubblesortOptimized(BaseTestCases.TestSorter):
  def setUp(self):
    super(TestBubblesortOptimized, self).setUp()

  def test_swap(self):
    super(TestBubblesortOptimized, self).test_swap()

class TestBubblesortOptimized2(BaseTestCases.TestSorter):
  def setUp(self):
    super(TestBubblesortOptimized2, self).setUp()

  def test_swap(self):
    super(TestBubblesortOptimized2, self).test_swap()

class TestGnomesort(BaseTestCases.TestSorter):
  def setUp(self):
    super(TestGnomesort, self).setUp()

  def test_swap(self):
    super(TestGnomesort, self).test_swap()



# class TestInsertion(unittest.TestCase):

#   def test_sort(self):
#     """
#     Test that we are correctly sorting data
#     """
#     data = [0,9,8,6,3,5,4,2,1,7]
#     self.sorter.sort(data)
#     result = self.sorter.steps[-1]
#     self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])


# class TestSelection(unittest.TestCase):

#   def test_sort(self):
#     """
#     Test that we are correctly sorting data
#     """
#     data = [0,9,8,6,3,5,4,2,1,7]
#     self.sorter.sort(data)
#     result = self.sorter.final_step
#     self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])


# class TestQuicksort(unittest.TestCase):
#   def setUp(self):
#     self.sorter = sorter.Quicksort()

#   def test_build_status(self):
#     """
#     Test that we are correctly building quicksort status
#     """
#     data = [1,0,8,4,6,7,5,3,6,9]
#     data_size = len(data)
#     result = self.sorter.build_status(data_size, data_size - 1)
#     self.assertEqual(result, [0,0,0,0,0,0,0,0,0,2])

#     i = 5
#     low = 4
#     high = 6
#     result = self.sorter.build_status(data_size, i, low, high)
#     self.assertEqual(result, [1,1,1,1,3,2,3,0,0,0])

#   def test_sort(self):
#     """
#     Test that we are correctly sorting data
#     """
#     data = [0,9,8,6,3,5,4,2,1,7]
#     self.sorter.sort(data)
#     result = self.sorter.final_step
#     self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])

#   def test_partition(self):
#     """
#     Test that we are correctly partitining data
#     """
#     data = [0,9,8,6,3,5,4,2,1,7]
#     low, high = 2, 5
#     result = self.sorter.partition(data, low, high)
#     self.assertEqual(result, 3)



if __name__ == "__main__":
  unittest.main()