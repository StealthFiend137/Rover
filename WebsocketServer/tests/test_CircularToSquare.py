import sys
import unittest
import math

sys.path.append('../modules/rangeofmotion/')
import rangeofmotion

class tCircularToSquareTests(unittest.TestCase):
    
    def test_maping_of_numbers(self):
        test_cases = [
            (1, 0.5, 0.5),
            (2, 0.75, 1.5),
            (2, 0.5, 1),
        ]
        
        for high_bound, input, expected_result in test_cases:
            with self.subTest(high_bound = high_bound, input = input, expected_output = expected_result):
                actual_result = rangeofmotion.map_circular_magnitude_to_circumstribed_square(input, high_bound)
                self.assertEqual(expected_result, actual_result)
    
    def test_out_of_range_input_throws(self):
        test_cases = [
            -0.1,
            1.1,
        ]
        for value in test_cases:
            with self.subTest(value = value):
                self.assertRaises(Exception, rangeofmotion.map_circular_magnitude_to_circumstribed_square, value, 1)
            
    

    def xtest_extremeties_return_full_x_or_y(self):
        test_cases = [
            (0, 1, 0),
            #((math.pi / 4), 0, 1),
            ((math.pi) / 2, -1, 0),
            #((-math.pi) / 4, 0, -1)
        ]
        
        for theta, expected_x, expected_y in test_cases:
            with self.subTest(theta = theta, expected_x = expected_x, expected_y = expected_y):
                
                magnitude = 1
                actual_x, actual_y = rangeofmotion.circular_to_square(theta, magnitude)
                self.assertEqual(expected_x, actual_x)
                self.assertEqual(expected_y, actual_y)
    
    def dxiagonals_return_extreme_x_andy(self):
        self.assertEqual(1, 2)