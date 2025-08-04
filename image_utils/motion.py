import numpy as np
import cv2

def simulate_motion_distortion(image, direction="horizontal", intensity=15):
    """
    Simulate motion distortion effect to create directional streaking or smearing.
    
    This function creates a directional motion distortion by applying a specialized
    blur kernel along a specific axis. Unlike standard motion blur, this effect can
    create more pronounced streaking patterns that simulate rapid movement or
    digital distortion artifacts. The effect is particularly useful for creating
    glitch aesthetics, simulating fast movement, or adding artistic distortion.
    
    Args:
        image: Input image as numpy array (any format supported by OpenCV)
        direction: Direction of motion distortion
                  - "horizontal": Streaking effect from left to right
                  - "vertical": Streaking effect from top to bottom
                  - "diagonal": Streaking effect along the diagonal
        intensity: Intensity of the motion effect (pixel length)
                  Higher values create more pronounced streaking
                  Typical values: 5 (subtle), 15 (moderate), 30 (strong)
        
    Returns:
        Image with simulated motion distortion as float32 array
        (Not converted to uint8 to allow for further processing)
    
    Note:
        The function creates specialized kernels based on the selected direction
        The effect is applied uniformly across the entire image
    """
    # Make a copy to avoid modifying the original and ensure float32 for processing
    result = image.copy().astype(np.float32)
    
    # Create motion blur kernel based on direction
    if direction == "horizontal":
        kernel = np.zeros((1, intensity))
        kernel[0, :] = 1.0 / intensity
    elif direction == "vertical":
        kernel = np.zeros((intensity, 1))
        kernel[:, 0] = 1.0 / intensity
    else:  # diagonal
        kernel = np.eye(intensity) / intensity
    
    # Apply the filter
    result = cv2.filter2D(result, -1, kernel)
    
    return result

def simulate_zoom_motion(image, intensity=5):
    """
    Simulate zoom motion blur effect to create radial blurring from the center.
    
    This function creates a radial blur effect that simulates camera zoom during
    exposure or rapid movement toward/away from the subject. It works by blending
    multiple scaled versions of the image with different weights, creating a
    progressive blur that radiates from the center of the image. This effect is
    useful for simulating fast zoom operations, creating a sense of speed or
    movement, or adding dramatic focus to the center of an image.
    
    Args:
        image: Input image as numpy array (any format supported by OpenCV)
        intensity: Intensity of the zoom effect (number of blend steps)
                  Higher values create more pronounced zoom trails
                  Typical values: 3 (subtle), 5 (moderate), 10 (strong)
        
    Returns:
        Image with simulated zoom motion as float32 array
        (Not converted to uint8 to allow for further processing)
    
    Note:
        The effect is centered on the middle of the image
        The function preserves the original image dimensions
        Higher intensity values require more processing time
    """
    # Make a copy to avoid modifying the original and ensure float32 for processing
    result = image.copy().astype(np.float32)
    
    # Get image dimensions
    h, w = image.shape[:2]
    center_x, center_y = w // 2, h // 2
    
    # Create a series of scaled images and blend them
    for i in range(1, intensity + 1):
        # Calculate scale factor
        scale = 1 + (i / (intensity * 10))
        
        # Calculate new dimensions
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        # Resize the image - ensure we're using float32 for the original image
        image_float = image.copy().astype(np.float32)
        scaled = cv2.resize(image_float, (new_w, new_h))
        
        # Calculate crop coordinates to get back to original size
        start_x = (new_w - w) // 2
        start_y = (new_h - h) // 2
        
        # Crop the image
        cropped = scaled[start_y:start_y+h, start_x:start_x+w]
        
        # Add to result with decreasing weight
        alpha = 1.0 / (i + 1)
        result = cv2.addWeighted(result, 1 - alpha, cropped, alpha, 0)
    
    return result