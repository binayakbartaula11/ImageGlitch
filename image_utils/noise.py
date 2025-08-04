import numpy as np
import cv2

def add_gaussian_noise(image, var=0.01):
    """
    Add Gaussian noise to an image to simulate sensor noise or grain effects.
    
    This function applies random Gaussian noise to each pixel in the image, creating
    a natural-looking noise pattern similar to what occurs in low-light photography
    or high-ISO settings. The noise is normally distributed with zero mean and
    controlled variance.
    
    Args:
        image: Input image as numpy array (any format supported by OpenCV)
        var: Variance of the Gaussian noise (0.0-1.0)
             Higher values create more pronounced noise
             Typical values: 0.01 (subtle), 0.05 (moderate), 0.1 (strong)
        
    Returns:
        Image with added Gaussian noise as float32 array
        (Not converted to uint8 to allow for further processing)
    
    Note:
        The function preserves the original image dimensions and channels
    """
    # Make a copy to avoid modifying the original
    # Ensure we're working with float32 for processing
    result = image.copy().astype(np.float32)
    
    # Generate Gaussian noise
    mean = 0
    sigma = var ** 0.5
    
    # Generate noise for each channel if colored image
    if len(image.shape) == 3:
        h, w, c = image.shape
        noise = np.random.normal(mean, sigma, (h, w, c)) * 255
    else:
        h, w = image.shape
        noise = np.random.normal(mean, sigma, (h, w)) * 255
    
    # Add noise to the image
    noisy_image = result + noise
    
    # Return the image without converting to uint8 yet
    # This allows for further processing in the pipeline
    return noisy_image

def add_salt_pepper_noise(image, amount=0.01):
    """
    Add salt and pepper noise to an image to simulate impulse noise or digital artifacts.
    
    This function randomly sets pixels to either white (salt) or black (pepper), creating
    a distinctive speckled pattern. Unlike Gaussian noise which affects all pixels to varying
    degrees, salt and pepper noise only affects a specific percentage of pixels but does so
    dramatically. This type of noise is common in digital transmission errors or dead pixels.
    
    Args:
        image: Input image as numpy array (any format supported by OpenCV)
        amount: Proportion of the image to be affected by noise (0.0-1.0)
                Higher values create more pronounced noise
                Typical values: 0.01 (subtle), 0.05 (moderate), 0.1 (strong)
                The noise is evenly split between salt (white) and pepper (black)
        
    Returns:
        Image with added salt and pepper noise as float32 array
        (Not converted to uint8 to allow for further processing)
    
    Note:
        The function preserves the original image dimensions and channels
    """
    # Make a copy to avoid modifying the original
    # Ensure we're working with float32 for processing
    result = image.copy().astype(np.float32)
    
    # Salt (white) mode
    num_salt = np.ceil(amount * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape[:2]]
    if len(image.shape) == 3:  # Color image
        result[coords[0], coords[1], :] = 255.0
    else:  # Grayscale image
        result[coords[0], coords[1]] = 255.0
    
    # Pepper (black) mode
    num_pepper = np.ceil(amount * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape[:2]]
    if len(image.shape) == 3:  # Color image
        result[coords[0], coords[1], :] = 0.0
    else:  # Grayscale image
        result[coords[0], coords[1]] = 0.0
    
    # Return the image without converting to uint8 yet
    # This allows for further processing in the pipeline
    return result