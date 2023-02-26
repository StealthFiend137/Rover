import sys
sys.path.append('../modules/rangeofmotion/')

import unittest
import math

import rangeofmotion

class tCircularToSquareTests(unittest.TestCase):

    def test_extremeties_return_full_x_or_y(self):
        test_cases = [
            (0, 1, 0),
            #((math.pi / 4), 0, 1),
            #((math.pi) / 2, -1, 0),
            #((-math.pi) / 4, 0, -1)
        ]
        
        for theta, expected_x, expected_y in test_cases:
            with self.subTest(theta = theta, expected_x = expected_x, expected_y = expected_y):
                
                magnitude = 1
                actual_x, actual_y = rangeofmotion.circular_to_square(theta, magnitude)
                self.assertEqual(expected_x, actual_x)
                self.assertEqual(expected_y, actual_y)
    
    def diagonals_return_extreme_x_andy(self):
        self.assertEqual(1, 2)