import unittest

from Classes import sorter

class TestSorter(unittest.TestCase):
  def setUp(self):
    self.sorter = sorter.Sorter()

  def test_swap(self):
    """
    Test that we are correctly swapping values
    """
    data = [0,3,2,1]
    i, j = 1, 3
    result = self.sorter.swap(data,i,j)
    self.assertEqual(result, [0,1,2,3])


class TestInsertion(unittest.TestCase):
  def setUp(self):
    self.sorter = sorter.Insertion()

  def test_build_status(self):
    """
    Test that we are correctly building insertion sort status
    """
    data = [1,8,4,6,7,5,3,6,9]
    data_size = len(data)
    idx = 3
    result = self.sorter.build_status(idx,data_size)
    self.assertEqual(result, [1,1,1,1,2,0,0,0,0])

  def test_sort(self):
    """
    Test that we are correctly sorting data
    """
    data = [0,9,8,6,3,5,4,2,1,7]
    self.sorter.sort(data)
    result = self.sorter.steps[-1]
    self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])


class TestSelection(unittest.TestCase):
  def setUp(self):
    self.sorter = sorter.Selection()  

  def test_build_status(self):
    """
    Test that we are correctly building selection sort status
    """
    data = [1,8,4,6,7,5,3,6,9]
    data_size = len(data)
    idx = 3
    idx2 = 5
    result = self.sorter.build_status(idx,idx2,data_size)
    self.assertEqual(result, [1,1,1,1,0,2,0,0,0])

  def test_sort(self):
    """
    Test that we are correctly sorting data
    """
    data = [0,9,8,6,3,5,4,2,1,7]
    self.sorter.sort(data)
    result = self.sorter.final_step
    self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])

class TestQuicksort(unittest.TestCase):
  def setUp(self):
    self.sorter = sorter.Quicksort()

  def test_build_status(self):
    """
    Test that we are correctly building quicksort status
    """
    data = [1,0,8,4,6,7,5,3,6,9]
    data_size = len(data)
    result = self.sorter.build_status(data_size, data_size - 1)
    self.assertEqual(result, [0,0,0,0,0,0,0,0,0,2])

    i = 5
    low = 4
    high = 6
    result = self.sorter.build_status(data_size, i, low, high)
    self.assertEqual(result, [1,1,1,1,3,2,3,0,0,0])

  def test_sort(self):
    """
    Test that we are correctly sorting data
    """
    data = [0,9,8,6,3,5,4,2,1,7]
    self.sorter.sort(data)
    result = self.sorter.final_step
    self.assertEqual(result, [0,1,2,3,4,5,6,7,8,9])

  def test_partition(self):
    """
    Test that we are correctly partitining data
    """
    data = [0,9,8,6,3,5,4,2,1,7]
    low, high = 2, 5
    result = self.sorter.partition(data, low, high)
    self.assertEqual(result, 3)



if __name__ == "__main__":
  unittest.main()