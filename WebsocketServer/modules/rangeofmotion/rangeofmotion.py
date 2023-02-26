def circular_to_square(theta, magnitude):
    return 1, 0

def SquareToCircular():
    pass



def map_circular_magnitude_to_circumstribed_square(circular_magnitude, outer_magnitude_upper_range):
    """
    Maps a smaller magnitude from a circle to a larger one on the square circumscribed to that circle.
    
    Args:
        inner_magnitude: magnitude of a joystick in the range 0 to 1.
        outer_magnitude_upper_range: the upper range of the out magnitude.
        
    Returns:
        the mappings 
    """
    
    if circular_magnitude > 1:
        raise ValueError(f'circular magnitude must be <= 1.  Actual value was { circular_magnitude }')
    
    if circular_magnitude < 0:
        raise ValueError(f'circular magnitude must be > 0.  Actual value was { circular_magnitude }')
    
    return (circular_magnitude * outer_magnitude_upper_range)