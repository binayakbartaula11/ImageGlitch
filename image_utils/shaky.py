import numpy as np
import cv2

def simulate_shaky(image, intensity=10):
    """
    Simulate a shaky camera effect by applying random transformations in both directions.
    
    This function creates a realistic camera shake effect by randomly displacing the image
    in both horizontal and vertical directions. The displacement is controlled by the
    intensity parameter, which determines the maximum possible pixel shift.
    
    Args:
        image: Input image as numpy array (any format supported by OpenCV)
        intensity: Intensity of the shake effect (pixel displacement range)
                  Higher values create more pronounced shake effects
        
    Returns:
        Image with random shake effect applied (same type as input)
    
    Note:
        Uses border replication to avoid black edges in the resulting image
    """
    # Ensure we're working with float32 for processing
    image_float = image.copy().astype(np.float32)
    
    # Get image dimensions
    h, w = image_float.shape[:2]
    
    # Create random translation matrix
    dx = np.random.randint(-intensity, intensity + 1)
    dy = np.random.randint(-intensity, intensity + 1)
    
    # Create transformation matrix
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    
    # Apply affine transformation
    result = cv2.warpAffine(image_float, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
    
    return result

def simulate_directional_shake(image, direction='horizontal', intensity=10):
    """
    Simulate a directional camera shake effect with controlled movement direction.
    
    This function creates a realistic camera shake effect by displacing the image
    in a specified direction. Unlike the random shake effect, this function allows
    precise control over the direction of movement, making it suitable for simulating
    specific types of camera movement or vibration.
    
    Args:
        image: Input image as numpy array (any format supported by OpenCV)
        direction: Direction of the shake ('horizontal', 'vertical', or 'both')
                  - 'horizontal': Shake only along the x-axis
                  - 'vertical': Shake only along the y-axis
                  - 'both': Shake in both directions (similar to simulate_shaky)
        intensity: Intensity of the shake effect (pixel displacement range)
                  Higher values create more pronounced shake effects
        
    Returns:
        Image with directional shake effect applied (same type as input)
    
    Note:
        Uses border replication to avoid black edges in the resulting image
    """
    # Ensure we're working with float32 for processing
    image_float = image.copy().astype(np.float32)
    
    # Get image dimensions
    h, w = image_float.shape[:2]
    
    # Create random translation based on direction
    if direction == 'horizontal':
        dx = np.random.randint(-intensity, intensity + 1)
        dy = 0
    elif direction == 'vertical':
        dx = 0
        dy = np.random.randint(-intensity, intensity + 1)
    else:  # both
        dx = np.random.randint(-intensity, intensity + 1)
        dy = np.random.randint(-intensity, intensity + 1)
    
    # Create transformation matrix
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    
    # Apply affine transformation
    result = cv2.warpAffine(image_float, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
    
    return result