import unittest
import math

def lcm(x, y):
    """Calculate the Least Common Multiple of two numbers."""
    return abs(x * y) // math.gcd(x, y)

class TestLCM(unittest.TestCase):
    def test_lcm(self):
        # Test cases
        self.assertEqual(lcm(4, 5), 20)
        self.assertEqual(lcm(7, 3), 21)
        self.assertEqual(lcm(10, 15), 30)
        self.assertEqual(lcm(0, 5), 0)  # LCM involving zero should be zero
        self.assertEqual(lcm(5, 0), 0)  # LCM involving zero should be zero
        self.assertEqual(lcm(-4, 5), 20)  # LCM should handle negative numbers
        self.assertEqual(lcm(4, -5), 20)  # LCM should handle negative numbers
        self.assertEqual(lcm(-4, -5), 20)  # LCM should handle negative numbers
        self.assertEqual(lcm(62.5, 125), 125)  # LCM should handle negative numbers

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
