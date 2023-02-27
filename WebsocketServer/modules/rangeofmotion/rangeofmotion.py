import math

def joystick_position_to_tank(x, y):
    left = x + y
    right = y - x
    
    left = max(min(left, 1), -1)
    right = max(min(right, 1), -1)
    
    return left, right

def circular_to_square(theta, magnitude):
    square_magnitude = get_square_magnitude(theta)   
    normalized_magnitude = map_magnitude(magnitude, square_magnitude)
    result = get_joystick_position(theta, normalized_magnitude)
    return result

def get_joystick_position(theta, magnitude):
    """
    Gets the x and y coordinates for a joystick based on the theta and magnitude.
    """
    x = math.sin(theta) * magnitude
    y = math.cos(theta) * magnitude

    return x, y

def get_square_magnitude(theta):
    """
    Gets the distance to the edge of square circumscribed of side 1.
    
    Args:
        theta: the angle in radians to continue from the radius of he circle to the square.
        
    Returns:
        a (float) indicating the distance to the edge of the square.
    """
    adjacent_length = 1
    if (abs(theta) < (math.pi / 4)) or (abs(theta) > (math.pi -(math.pi /4))):
        return abs(adjacent_length / math.cos(theta))
    return abs(adjacent_length / math.sin(theta))


def map_magnitude(value, new_range_maximum):
    """
    maps a value that exists in the range 0 to 1 to a number that exists in the range 0 to 
    
    Args:
        value: magnitude of a joystick in the range 0 to 1.
        new_range_maximum: the upper range of the out magnitude.
        
    Returns:
        the mappings 
    """
    
    if value > 1:
        raise ValueError(f'circular magnitude must be <= 1.  Actual value was { value }')
    
    if value < 0:
        raise ValueError(f'circular magnitude must be > 0.  Actual value was { value }')
    
    return (value * new_range_maximum)