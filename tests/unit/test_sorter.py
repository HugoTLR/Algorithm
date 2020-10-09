import unittest

from random import choice

from Classes import sorter

class TestSorter(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    if cls is not TestSorter and cls.setUp is not TestSorter.setUp:
      orig_setUp = cls.setUp
      def setUpOverride(self, *args, **kwargs):
        TestSorter.setUp(self)
        return orig_setUp(self, *args, **kwargs)
      cls.setUp = setUpOverride

  def setUp(self):
    self.data = [0,9,8,6,3,5,4,2,1,7]
    self.data_size = len(self.data)

  def test_swap(self):
    i = choice([v for v in range(self.data_size)])
    j = choice([v for v in range(self.data_size) if v != i])
    self.assertTrue(self.data_size > 0)
    self.assertTrue(i >= 0 and i < self.data_size )
    self.assertTrue(j >= 0 and j < self.data_size )
    self.assertTrue(j != i)
    result = sorter.Sorter().swap(self.data,i,j)
    self.assertEqual(result, sorter.Sorter().swap(self.data,i,j) )

class TestInsertion(TestSorter):
  def setUp(self):
    self.sorter = sorter.Insertion()
    self.sorter.data = self.data
    self.sorter.data_size = self.data_size

  def test_insertion_build_status(self):
    """
    Test that we are correctly building insertion sort status
    """
    idx = 3
    result = self.sorter.build_status(idx)
    self.assertEqual(result, [1,1,1,1,2,0,0,0,0,0])

  def test_insertion_sort(self):
    """
    Test that we are correctly sorting data
    """
    self.sorter.sort(self.data)
    result = self.sorter.steps[-1]
    self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])


class TestSelection(TestSorter):
  def setUp(self):
    self.sorter = sorter.Selection()
    self.sorter.data = self.data
    self.sorter.data_size = self.data_size

  def test_selection_build_status(self):
    """
    Test that we are correctly building selection sort status
    """
    idx = 3
    idx2 = 5
    result = self.sorter.build_status(idx,idx2)
    self.assertEqual(result, [1,1,1,2,0,3,0,0,0,0])

  def test_selection_sort(self):
    """
    Test that we are correctly sorting data
    """
    self.sorter.sort(self.data)
    result = self.sorter.steps[-1]
    self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])


class TestQuicksort(TestSorter):
  def setUp(self):
    self.sorter = sorter.Quicksort()
    self.sorter.data = self.data
    self.sorter.data_size = self.data_size

  def test_quicksort_build_status(self):
    """
    Test that we are correctly building quicksort status
    """
    low, high, i = 3, 8, 5
    result = self.sorter.build_status(i, low, high)
    self.assertEqual(result, [1,1,1,4,0,2,0,0,3,0])

  def test_quicksort_sort(self):
    """
    Test that we are correctly sorting data
    """
    self.sorter.sort(self.data)
    result = self.sorter.steps[-1]
    self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])


class TestBubblesort(TestSorter):
  def setUp(self):
    self.sorter = sorter.Bubblesort()
    self.sorter.data = self.data
    self.sorter.data_size = self.data_size

  def test_bubblesort_build_status(self):
    """
    Test that we are correctly building bubblesort status
    """
    idx = 2
    n = self.data_size - 1 
    result = self.sorter.build_status(idx - 1, idx, n)
    self.assertEqual(result, [0,2,2,0,0,0,0,0,0,1])

  def test_bubblesort_sort(self):
    """
    Test that we are correctly sorting data
    """
    self.sorter.sort(self.data)
    result = self.sorter.steps[-1]
    self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])



class TestBubblesortOptimized(TestSorter):
  def setUp(self):
    self.sorter = sorter.Bubblesort_Optimized()
    self.sorter.data = self.data
    self.sorter.data_size = self.data_size

  def test_bubblesort_optimized_build_status(self):
    """
    Test that we are correctly building bubblesort status
    """
    idx = 2
    n = self.data_size - 1 
    result = self.sorter.build_status(idx - 1, idx, n)
    self.assertEqual(result, [0,2,2,0,0,0,0,0,0,1])

  def test_bubblesort_optimized_sort(self):
    """
    Test that we are correctly sorting data
    """
    self.sorter.sort(self.data)
    result = self.sorter.steps[-1]
    self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])


class TestBubblesortOptimized2(TestSorter):
  def setUp(self):
    self.sorter = sorter.Bubblesort_Optimized_2()
    self.sorter.data = self.data
    self.sorter.data_size = self.data_size

  def test_bubblesort_optimized_2_build_status(self):
    """
    Test that we are correctly building bubblesort status
    """
    idx = 2
    n = self.data_size - 1 
    result = self.sorter.build_status(idx - 1, idx, n)
    self.assertEqual(result, [0,2,2,0,0,0,0,0,0,1])

  def test_bubblesort_optimized_2_sort(self):
    """
    Test that we are correctly sorting data
    """
    self.sorter.sort(self.data)
    result = self.sorter.steps[-1]
    self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])


class TestCombsort(TestSorter):
  def setUp(self):
    self.sorter = sorter.Combsort()
    self.sorter.data = self.data
    self.sorter.data_size = self.data_size

  def test_combsort_build_status(self):
    """
    Test that we are correctly building bubblesort status
    """
    gap = 3
    idx = 5
    result = self.sorter.build_status(gap,idx,gap+idx)
    self.assertEqual(result, [0,0,0,0,0,4,2,2,3,0])

  def test_combsort_sort(self):
    """
    Test that we are correctly sorting data
    """
    self.sorter.sort(self.data)
    result = self.sorter.steps[-1]
    self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])


class TestGnomesort(TestSorter):
  def setUp(self):
    self.sorter = sorter.Gnomesort()
    self.sorter.data = self.data
    self.sorter.data_size = self.data_size

  def test_gnomesort_build_status(self):
    """
    Test that we are correctly building bubblesort status
    """
    idx = 5
    result = self.sorter.build_status(idx)
    self.assertEqual(result, [1,1,1,1,1,2,0,0,0,0])

  def test_gnomesort_sort(self):
    """
    Test that we are correctly sorting data
    """
    self.sorter.sort(self.data)
    result = self.sorter.steps[-1]
    self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])

if __name__ == "__main__":
  unittest.main()