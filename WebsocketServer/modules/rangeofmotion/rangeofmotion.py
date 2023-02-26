def circular_to_square(theta, magnitude):
    return 1, 0

def SquareToCircular():
    pass


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