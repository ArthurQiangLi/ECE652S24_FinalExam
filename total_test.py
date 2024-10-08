# test_lcm.py

import ece_652_final
from  ece_652_final import lcm, allocate_time_to_task, calculate_hyperperiod
import unittest
from math import isclose
from unittest.mock import mock_open, patch

class TestCalculateHyperperiod(unittest.TestCase):
    def test_integer_periods(self):
        periods = [50, 75, 100]
        expected_hyperperiod = 300
        result = calculate_hyperperiod(periods)
        self.assertAlmostEqual(result, expected_hyperperiod, places=5)    
    
    def test_integer_periods(self):
        periods = [14,16,21,20,14]
        expected_hyperperiod = 1680
        result = calculate_hyperperiod(periods)
        self.assertAlmostEqual(result, expected_hyperperiod, places=5)

    def test_integer_periods(self):
        periods = [14,16,21,20,14, 20, 20]
        expected_hyperperiod = 1680
        result = calculate_hyperperiod(periods)
        self.assertAlmostEqual(result, expected_hyperperiod, places=5)        
    
    def test_mixed_periods(self):
        periods = [50, 62.5, 125]
        expected_hyperperiod = 250
        result = calculate_hyperperiod(periods)
        self.assertAlmostEqual(result, expected_hyperperiod, places=5)

    def test_float_periods(self):
        periods = [50.0, 75.0, 100.0]
        expected_hyperperiod = 300.0
        result = calculate_hyperperiod(periods)
        self.assertAlmostEqual(result, expected_hyperperiod, places=5)

    def test_small_float_periods(self):
        periods = [0.1, 0.25, 0.5]
        expected_hyperperiod = 0.5
        result = calculate_hyperperiod(periods)
        self.assertAlmostEqual(result, expected_hyperperiod, places=5)


# class TestReadFile(unittest.TestCase):
#     def test_read_file_to_list__function(self):
#         mock_data = "2,14,25\n4,16,17\n8,21,25\n5,20,30\n7,14,25\n"
#         expected_output = [[2, 14, 25], [4, 16, 17], [8, 21, 25], [5, 20, 30], [7, 14, 25]]

#         with patch('builtins.open', mock_open(read_data=mock_data)):
#             result = ece_652_final.read_file_to_list('workload2.txt')
#             self.assertEqual(result, expected_output)

#     def test_read_file_to_list__function_execution_integer(self):
#         mock_data = "2,14,25\n4,16,17\n8,21,25\n5,20,30\n7,14,25\n"
#         expected_output = [[2, 14, 25], [4, 16, 17], [8, 21, 25], [5, 20, 30], [7, 14, 25]]

#         # Use patch to replace 'open' with a mock object
#         with patch('builtins.open', mock_open(read_data=mock_data)):
#             # Call the function to read from the "file"
#             ece_652_final.read_file_to_list('workload1.txt')
#             # Check if the global tasks list matches the expected output
#             self.assertEqual(ece_652_final.tasks, expected_output)

#     def test_read_file_to_list__function_execution_float(self):
#         mock_data = "2.12,14,25\n4,16,17\n8,21.333,25\n5,20,30\n7,14,25.5\n"
#         expected_output = [[2.12, 14, 25], [4, 16, 17], [8, 21.333, 25], [5, 20, 30], [7, 14, 25.5]]

#         # Use patch to replace 'open' with a mock object
#         with patch('builtins.open', mock_open(read_data=mock_data)):
#             # Call the function to read from the "file"
#             ece_652_final.read_file_to_list('workload1.txt')
#             # Check if the global tasks list matches the expected output
#             self.assertEqual(ece_652_final.tasks, expected_output)

class TestAllocateTimeToTask(unittest.TestCase):
    def test_example1(self):
        T_available = [[1, 3], [4, 6], [7, 9], [10, 12]]
        T_required = [0, 5]
        execution_time = 2.0

        expected_T_available = [[4, 6], [7, 9], [10, 12]]
        expected_T_allocated = [[1, 3.0]]
        expected_IsOK = True

        T_available, T_allocated, IsOK = allocate_time_to_task(T_available, T_required, execution_time)
        self.assertEqual(T_available, expected_T_available)
        self.assertEqual(T_allocated, expected_T_allocated)
        self.assertEqual(IsOK, expected_IsOK)

    def test_example2(self):
        T_available = [ [4, 6], [7, 9], [10, 12]]
        T_required = [4, 9]
        execution_time = 2.0

        expected_T_available = [[7, 9], [10, 12]]
        expected_T_allocated = [[4, 6.0]]
        expected_IsOK = True

        T_available, T_allocated, IsOK = allocate_time_to_task(T_available, T_required, execution_time)
        self.assertEqual(T_available, expected_T_available)
        self.assertEqual(T_allocated, expected_T_allocated)
        self.assertEqual(IsOK, expected_IsOK)

    def test_example3(self):
        T_available = [[7, 9], [10, 12]]
        T_required = [8, 12]
        execution_time = 2.0

        expected_T_available = [[7, 8], [11, 12]]
        expected_T_allocated = [[8, 9], [10, 11]]
        expected_IsOK = True

        T_available, T_allocated, IsOK = allocate_time_to_task(T_available, T_required, execution_time)
        self.assertEqual(T_available, expected_T_available)
        self.assertEqual(T_allocated, expected_T_allocated)
        self.assertEqual(IsOK, expected_IsOK)

    def test_example4(self):
        T_available = [[0, 12]]
        T_required = [0, 3]
        execution_time = 1

        expected_T_available = [[1, 12]]
        expected_T_allocated = [[0, 1]]
        expected_IsOK = True

        T_available, T_allocated, IsOK = allocate_time_to_task(T_available, T_required, execution_time)
        self.assertEqual(T_available, expected_T_available)
        self.assertEqual(T_allocated, expected_T_allocated)
        self.assertEqual(IsOK, expected_IsOK)

    def test_example5(self):
        T_available = [[1, 12]]
        T_required = [3, 6]
        execution_time = 1

        expected_T_available = [[1,3],[4, 12]]
        expected_T_allocated = [[3, 4]]
        expected_IsOK = True

        T_available, T_allocated, IsOK = allocate_time_to_task(T_available, T_required, execution_time)
        self.assertEqual(T_available, expected_T_available)
        self.assertEqual(T_allocated, expected_T_allocated)
        self.assertEqual(IsOK, expected_IsOK)

    def test_example6(self):
        T_available = [[1,3],[4, 12]]
        T_required = [6, 9]
        execution_time = 1

        expected_T_available = [[1,3],[4,6],[7, 12]]
        expected_T_allocated = [[6, 7]]
        expected_IsOK = True

        T_available, T_allocated, IsOK = allocate_time_to_task(T_available, T_required, execution_time)
        self.assertEqual(T_available, expected_T_available)
        self.assertEqual(T_allocated, expected_T_allocated)
        self.assertEqual(IsOK, expected_IsOK)

    def test_example6(self):
        T_available = [[1,3],[4,6],[7, 12]]
        T_required = [9, 12]
        execution_time = 1

        expected_T_available = [[1,3],[4,6],[7,9], [10, 12]]
        expected_T_allocated = [[9, 10]]
        expected_IsOK = True

        T_available, T_allocated, IsOK = allocate_time_to_task(T_available, T_required, execution_time)
        self.assertEqual(T_available, expected_T_available)
        self.assertEqual(T_allocated, expected_T_allocated)
        self.assertEqual(IsOK, expected_IsOK)

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
