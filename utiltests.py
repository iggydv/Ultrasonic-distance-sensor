import unittest
from util import *

class utilTests(unittest.TestCase):
    def test_average_higher(self):
        self.assertEqual(calcAverage(20,100), 44)
    def test_average_lower(self):
        self.assertEqual(calcAverage(20,10), 17)
    def test_average_negative(self):
        self.assertEqual(calcAverage(20,-20), 8)
    def test_average_same(self):
        self.assertEqual(calcAverage(20,20), 20)

    def test_velocity_positive(self):
        self.assertEqual(calcVelocity(30,40,5), 0.072)
    def test_velocity_negative(self):
        self.assertEqual(calcVelocity(40,30,5), -0.072)
    def test_velocity_zero(self):
        self.assertEqual(calcVelocity(40,40,5), 0)
    def test_velocity_time_zero(self):
        self.assertEqual(calcVelocity(40,50,0), 0)
    def test_velocity_time_negative(self):
        self.assertEqual(calcVelocity(40,50,-10), 0)

if __name__ == '__main__':
    unittest.main()
