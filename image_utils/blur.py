import numpy as np
import cv2

def apply_gaussian_blur(image, kernel_size=5):
    """
    Apply Gaussian blur to an image for smooth, natural-looking blur effects.
    
    This function applies a Gaussian filter to the image, which creates a smooth blur
    by weighting pixels according to a Gaussian distribution (bell curve). This type of
    blur is ideal for simulating out-of-focus effects, reducing noise, or creating a
    soft focus effect. The blur is applied equally in all directions.
    
    Args:
        image: Input image as numpy array (any format supported by OpenCV)
        kernel_size: Size of the Gaussian kernel (must be odd)
                    Larger values create more pronounced blur effects
                    Typical values: 3 (subtle), 5 (moderate), 9 (strong), 15 (very strong)
        
    Returns:
        Blurred image as float32 array
        (Not converted to uint8 to allow for further processing)
    
    Note:
        If an even kernel size is provided, it will be incremented by 1 to ensure oddness
        The function preserves the original image dimensions and channels
    """
    # Ensure we're working with float32 for processing
    image_float = image.copy().astype(np.float32)
    
    # Ensure kernel size is odd
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(image_float, (kernel_size, kernel_size), 0)
    
    return blurred

def apply_motion_blur(image, degree=12, angle=45):
    """
    Apply directional motion blur to simulate camera or subject movement.
    
    This function creates a directional blur effect that simulates relative motion
    between the camera and subject. It works by applying a custom kernel that blurs
    pixels along a specific angle, creating a streak effect. This is useful for
    simulating fast-moving objects, camera shake in a specific direction, or
    intentional creative motion effects.
    
    Args:
        image: Input image as numpy array (any format supported by OpenCV)
        degree: Length of the motion blur in pixels
                Higher values create longer motion streaks
                Typical values: 5 (subtle), 12 (moderate), 20 (strong)
        angle: Angle of motion in degrees (0-360)
               0/180: horizontal motion
               90/270: vertical motion
               Other values: diagonal motion
        
    Returns:
        Motion blurred image as float32 array
        (Not converted to uint8 to allow for further processing)
    
    Note:
        The function uses Bresenham's line algorithm to create the motion kernel
        The kernel size is automatically adjusted to be odd if necessary
    """
    # Ensure we're working with float32 for processing
    image_float = image.copy().astype(np.float32)
    
    # Convert angle to radians
    angle_rad = np.deg2rad(angle)
    
    # Create the motion blur kernel
    kernel_size = degree
    if kernel_size % 2 == 0:
        kernel_size += 1  # Ensure odd size
    
    kernel = np.zeros((kernel_size, kernel_size))
    
    # Calculate center point
    center = kernel_size // 2
    
    # Create a line using Bresenham's algorithm
    x_offset = int(center * np.cos(angle_rad))
    y_offset = int(center * np.sin(angle_rad))
    
    # Draw the line on the kernel
    cv2.line(kernel, 
             (center - x_offset, center - y_offset), 
             (center + x_offset, center + y_offset), 
             1, thickness=1)
    
    # Normalize the kernel
    kernel = kernel / np.sum(kernel) if np.sum(kernel) > 0 else kernel
    
    # Apply the filter
    motion_blur = cv2.filter2D(image_float, -1, kernel)
    
    return motion_blur

def apply_box_blur(image, kernel_size=5):
    """
    Apply box blur (averaging filter) to an image for uniform blurring effects.
    
    This function applies a simple averaging filter where each pixel is replaced with
    the average value of its neighborhood. Unlike Gaussian blur which weights pixels
    based on distance, box blur weights all pixels equally within the kernel area.
    This creates a more uniform, sometimes pixelated blur effect that can be useful
    for simulating older cameras, reducing detail, or creating certain artistic effects.
    
    Args:
        image: Input image as numpy array (any format supported by OpenCV)
        kernel_size: Size of the box kernel (must be odd)
                    Larger values create more pronounced blur effects
                    Typical values: 3 (subtle), 5 (moderate), 9 (strong)
        
    Returns:
        Blurred image as float32 array
        (Not converted to uint8 to allow for further processing)
    
    Note:
        If an even kernel size is provided, it will be incremented by 1 to ensure oddness
        The function preserves the original image dimensions and channels
        Box blur is computationally more efficient than Gaussian blur but less natural-looking
    """
    # Ensure we're working with float32 for processing
    image_float = image.copy().astype(np.float32)
    
    # Ensure kernel size is odd
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    # Create a box kernel
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
    
    # Apply the filter
    box_blur = cv2.filter2D(image_float, -1, kernel)
    
    return box_blur