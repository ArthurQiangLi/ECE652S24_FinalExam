# test_lcm.py

import ece_652_final
from  ece_652_final import lcm
import unittest
from math import isclose
from unittest.mock import mock_open, patch

class TestLCM(unittest.TestCase):
    def test_lcm(self):
        self.assertTrue(isclose(lcm(4, 5), 20, rel_tol=1e-5))
        self.assertTrue(isclose(lcm(0, 1), 0, rel_tol=1e-5))
        self.assertTrue(isclose(lcm(6, 8), 24, rel_tol=1e-5))
        self.assertTrue(isclose(lcm(21, 6), 42, rel_tol=1e-5))
        self.assertTrue(isclose(lcm(12, 15), 60, rel_tol=1e-5))
        self.assertTrue(isclose(lcm(100, 25), 100, rel_tol=1e-5))
        self.assertTrue(isclose(lcm(9, 28), 252, rel_tol=1e-5))
        self.assertTrue(isclose(lcm(62.5, 125), 125, rel_tol=1e-5))
        self.assertTrue(isclose(lcm(1.25, 10), 10, rel_tol=1e-5))


class TestECE(unittest.TestCase):
    def test_read_file_to_list__function(self):
        mock_data = "2,14,25\n4,16,17\n8,21,25\n5,20,30\n7,14,25\n"
        expected_output = [[2, 14, 25], [4, 16, 17], [8, 21, 25], [5, 20, 30], [7, 14, 25]]

        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = ece_652_final.read_file_to_list('workload2.txt')
            self.assertEqual(result, expected_output)

    def test_read_file_to_list__function_execution_integer(self):
        mock_data = "2,14,25\n4,16,17\n8,21,25\n5,20,30\n7,14,25\n"
        expected_output = [[2, 14, 25], [4, 16, 17], [8, 21, 25], [5, 20, 30], [7, 14, 25]]

        # Use patch to replace 'open' with a mock object
        with patch('builtins.open', mock_open(read_data=mock_data)):
            # Call the function to read from the "file"
            ece_652_final.read_file_to_list('workload1.txt')
            # Check if the global tasks list matches the expected output
            self.assertEqual(ece_652_final.tasks, expected_output)

    def test_read_file_to_list__function_execution_float(self):
        mock_data = "2.12,14,25\n4,16,17\n8,21.333,25\n5,20,30\n7,14,25.5\n"
        expected_output = [[2.12, 14, 25], [4, 16, 17], [8, 21.333, 25], [5, 20, 30], [7, 14, 25.5]]

        # Use patch to replace 'open' with a mock object
        with patch('builtins.open', mock_open(read_data=mock_data)):
            # Call the function to read from the "file"
            ece_652_final.read_file_to_list('workload1.txt')
            # Check if the global tasks list matches the expected output
            self.assertEqual(ece_652_final.tasks, expected_output)


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
