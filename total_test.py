# test_lcm.py

import unittest
from math import isclose
from ece_652_final import lcm

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

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
