import sys
import unittest
import math

sys.path.append('../modules/rangeofmotion/')
import rangeofmotion

class CircularToSquareTests(unittest.TestCase):
    
    def test_maping_of_numbers(self):
        test_cases = [
            (1, 0.5, 0.5),
            (2, 0.75, 1.5),
            (2, 0.5, 1),
        ]
        
        for high_bound, input, expected_result in test_cases:
            with self.subTest(high_bound = high_bound, input = input, expected_output = expected_result):
                actual_result = rangeofmotion.map_magnitude(input, high_bound)
                self.assertEqual(expected_result, actual_result)
    
    def test_out_of_range_input_throws(self):
        test_cases = [
            -0.1,
            1.1,
        ]
        for value in test_cases:
            with self.subTest(value = value):
                self.assertRaises(ValueError, rangeofmotion.map_magnitude, value, 1)

    def test_get_square_magnitude(self):
        test_cases = [
            (0, 1, 1), # north
            (math.pi / 2, 1, 1), # east
            (math.pi, 1, 1), # south
            (-math.pi, 1, 1), # also south
            (-math.pi / 2, 1, 1),  # west
            ((math.pi) / 4, 1, 1.414), # north east
            ((math.pi) / 8, 1, 1.082), # north north east
        ]
        
        for theta, input_magnitude, expected_magnitude in test_cases:
            with self.subTest(theta = theta, input_magnitude = input_magnitude, expected_magnitude = expected_magnitude):
                adjusted_magnitude = rangeofmotion.get_square_magnitude(theta)
                self.assertAlmostEqual(expected_magnitude, adjusted_magnitude, places=3)

    def test_get_joystick_position(self):
        test_cases = [
            (0, 1, 0, 1), # north
            (math.pi / 2, 1, 1, 0), # east
            (math.pi, 1, 0, -1), # south
            (-math.pi, 1, 0, -1), # also south
            (-math.pi / 2, 1, -1, 0),  # west
            (math.pi / 4, 1.414, 1, 1), # north east
            (math.pi / 8, 1.082, 0.414, 1), # north north east
        ]
        for theta, magnitude, expected_x, expected_y in test_cases:
            with self.subTest(theta = theta, magnitude = magnitude, expected_x = expected_x, expected_y = expected_y):
                actual_x, actual_y = rangeofmotion.get_joystick_position(theta, magnitude);
                self.assertAlmostEqual(expected_x, actual_x, places=3)
                self.assertAlmostEqual(expected_y, actual_y, places=3)
                
    def test_tank_stearing(self):
        test_cases = [
            (0, 1, 1, 1), # north
            (1, 0, 1, -1), # east
            (0, -1, -1, -1), # south
            (-1, 0, -1, 1), # west
        ]
        
        for x, y, expected_left, expected_right in test_cases:
            with self.subTest(x = x, y = y, expected_left = expected_left, expected_right = expected_right):
                actual_left, actual_right = rangeofmotion.joystick_position_to_tank(x, y)
                self.assertAlmostEqual(expected_left, actual_left, places=3)
                self.assertAlmostEqual(expected_right, actual_right, places=3)