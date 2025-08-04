# 🔧 API Reference

This document provides a comprehensive reference for the ImageGlitch API, including all classes, functions, and modules available for developers.

## 📚 Core Modules

### `app.py` - Main Application

#### Classes

##### `BackgroundRemovalManager`

Manages AI models for background removal operations.

```python
class BackgroundRemovalManager:
    """Manages background removal functionality with proper error handling and model management."""
    
    def __init__(self):
        """Initialize the background removal manager."""
        
    def get_session(self, model_name: str):
        """Get or create a session for the specified model.
        
        Args:
            model_name (str): The name of the model to load
            
        Returns:
            Session object for the specified model
            
        Raises:
            ImportError: If rembg library is not available
            RuntimeError: If model loading fails
        """
        
    def remove_background(self, image: np.ndarray, model_name: str = "u2net", 
                         return_rgba: bool = True, bg_color: str = None) -> np.ndarray:
        """Remove background from image using the specified AI model.
        
        Args:
            image (np.ndarray): Input image as numpy array
            model_name (str): Model to use for background removal
            return_rgba (bool): If True, returns RGBA image with transparency
            bg_color (str): Optional hex color string for custom background
            
        Returns:
            np.ndarray: Processed image as numpy array
            
        Raises:
            ImportError: If rembg library is not installed
            RuntimeError: If background removal process fails
        """
        
    def is_model_loaded(self, model_name: str) -> bool:
        """Check if a model is already loaded.
        
        Args:
            model_name (str): Name of the model to check
            
        Returns:
            bool: True if model is loaded, False otherwise
        """
        
    def get_model_info(self, model_name: str) -> dict:
        """Get information about a specific model.
        
        Args:
            model_name (str): Name of the model
            
        Returns:
            dict: Model information including name, description, size
        """
```

**Available Models:**
- `u2net`: General purpose model (~176MB)
- `u2net_human_seg`: Human portrait optimization (~176MB)
- `u2net_cloth_seg`: Clothing and fashion specialized (~176MB)
- `isnet-general-use`: High accuracy general purpose (~173MB)
- `silueta`: Fast processing model (~43MB)

##### `PreviewManager`

Manages preview quality modes for performance optimization.

```python
class PreviewManager:
    """Manages different preview quality modes and image optimization."""
    
    PREVIEW_MODES = {
        "Fast": {"max_size": 300, "quality": 75},
        "Balanced": {"max_size": 500, "quality": 85},
        "High Quality": {"max_size": 800, "quality": 95}
    }
    
    @staticmethod
    def resize_for_preview(image: np.ndarray, mode: str) -> np.ndarray:
        """Resize image based on preview mode while maintaining aspect ratio.
        
        Args:
            image (np.ndarray): Input image as numpy array
            mode (str): Preview mode name
            
        Returns:
            np.ndarray: Resized image as numpy array
        """
```

#### Functions

##### Image Processing Functions

```python
def load_image(uploaded_file):
    """Load and convert uploaded image to numpy array.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        np.ndarray: Image as numpy array
    """

def image_to_bytes(image_array, format='PNG'):
    """Convert numpy array to bytes for download.
    
    Args:
        image_array (np.ndarray): Image as numpy array
        format (str): Output format ('PNG' or 'JPEG')
        
    Returns:
        bytes: Image data as bytes
    """

def apply_imageglitch_effects(image: np.ndarray, effects: Dict[str, Any]) -> np.ndarray:
    """Apply multiple image manipulation effects based on user-selected parameters.
    
    Args:
        image (np.ndarray): Input image as numpy array
        effects (Dict[str, Any]): Dictionary containing effect parameters
        
    Returns:
        np.ndarray: Processed image with all enabled effects applied
    """

def hash_effects(effects: Dict[str, Any]) -> str:
    """Create a unique hash string from the effects dictionary for caching.
    
    Args:
        effects (Dict[str, Any]): Dictionary containing effect parameters
        
    Returns:
        str: 32-character hexadecimal hash string
    """
```

##### Session Management

```python
def initialize_session_state():
    """Initialize Streamlit session state variables for persistent storage."""

def show_bg_removal_page():
    """Render the AI Background Removal page with all UI components."""

def show_imageglitch_page():
    """Render the ImageGlitch page with real-time image manipulation features."""

def show_home_page():
    """Render the application home page with feature overview."""

def main():
    """Main application entry point that sets up the Streamlit interface."""
```

## 🎨 Image Effects Modules

### `image_utils/blur.py`

#### Functions

```python
def apply_gaussian_blur(image, kernel_size=5):
    """Apply Gaussian blur to an image for smooth, natural-looking blur effects.
    
    Args:
        image (np.ndarray): Input image as numpy array
        kernel_size (int): Size of the Gaussian kernel (must be odd)
        
    Returns:
        np.ndarray: Blurred image as float32 array
    """

def apply_motion_blur(image, degree=12, angle=45):
    """Apply directional motion blur to simulate camera or subject movement.
    
    Args:
        image (np.ndarray): Input image as numpy array
        degree (int): Length of the motion blur in pixels
        angle (int): Angle of motion in degrees (0-360)
        
    Returns:
        np.ndarray: Motion blurred image as float32 array
    """

def apply_box_blur(image, kernel_size=5):
    """Apply box blur (averaging filter) to an image for uniform blurring effects.
    
    Args:
        image (np.ndarray): Input image as numpy array
        kernel_size (int): Size of the box kernel (must be odd)
        
    Returns:
        np.ndarray: Blurred image as float32 array
    """
```

### `image_utils/noise.py`

#### Functions

```python
def add_gaussian_noise(image, var=0.01):
    """Add Gaussian noise to an image to simulate sensor noise or grain effects.
    
    Args:
        image (np.ndarray): Input image as numpy array
        var (float): Variance of the Gaussian noise (0.0-1.0)
        
    Returns:
        np.ndarray: Image with added Gaussian noise as float32 array
    """

def add_salt_pepper_noise(image, amount=0.01):
    """Add salt and pepper noise to an image to simulate impulse noise.
    
    Args:
        image (np.ndarray): Input image as numpy array
        amount (float): Proportion of the image to be affected by noise (0.0-1.0)
        
    Returns:
        np.ndarray: Image with added salt and pepper noise as float32 array
    """
```

### `image_utils/shaky.py`

#### Functions

```python
def simulate_shaky(image, intensity=10):
    """Simulate a shaky camera effect by applying random transformations.
    
    Args:
        image (np.ndarray): Input image as numpy array
        intensity (int): Intensity of the shake effect (pixel displacement range)
        
    Returns:
        np.ndarray: Image with random shake effect applied
    """

def simulate_directional_shake(image, direction='horizontal', intensity=10):
    """Simulate a directional camera shake effect with controlled movement direction.
    
    Args:
        image (np.ndarray): Input image as numpy array  
        direction (str): Direction of the shake ('horizontal', 'vertical', or 'both')
        intensity (int): Intensity of the shake effect
        
    Returns:
        np.ndarray: Image with directional shake effect applied
    """
```

### `image_utils/motion.py`

#### Functions

```python
def simulate_motion_distortion(image, direction="horizontal", intensity=15):
    """Simulate motion distortion effect to create directional streaking or smearing.
    
    Args:
        image (np.ndarray): Input image as numpy array
        direction (str): Direction of motion distortion
        intensity (int): Intensity of the motion effect (pixel length)
        
    Returns:
        np.ndarray: Image with simulated motion distortion as float32 array
    """

def simulate_zoom_motion(image, intensity=5):
    """Simulate zoom motion blur effect to create radial blurring from the center.
    
    Args:
        image (np.ndarray): Input image as numpy array
        intensity (int): Intensity of the zoom effect (number of blend steps)
        
    Returns:
        np.ndarray: Image with simulated zoom motion as float32 array
    """
```

## 📊 Data Structures

### Effect Configuration Dictionary

The effects system uses a standardized dictionary structure:

```python
effects = {
    'gaussian_noise': {
        'enabled': bool,        # Whether effect is active
        'variance': float       # Effect-specific parameter
    },
    'salt_pepper_noise': {
        'enabled': bool,
        'amount': float
    },
    'gaussian_blur': {
        'enabled': bool,
        'kernel_size': int
    },
    'motion_blur': {
        'enabled': bool,
        'degree': int,
        'angle': int
    },
    'box_blur': {
        'enabled': bool,
        'kernel_size': int
    },
    'camera_shake': {
        'enabled': bool,
        'intensity': int
    },
    'directional_shake': {
        'enabled': bool,
        'intensity': int,
        'direction': str
    },
    'motion_distortion': {
        'enabled': bool,
        'direction': str,
        'intensity': int
    },
    'zoom_motion': {
        'enabled': bool,
        'intensity': int
    }
}
```

### Model Information Dictionary

```python
model_info = {
    "name": str,           # Display name
    "description": str,    # Short description with emoji
    "suitable_for": str,   # Use case description
    "size": str           # Model file size
}
```

## 🔧 Error Handling

### Exception Types

#### `ImportError`
Raised when required dependencies are not available:
```python
try:
    from rembg import remove as rembg_remove
except ImportError:
    # Handle missing rembg library
    pass
```

#### `RuntimeError`
Raised when model operations fail:
```python
try:
    session = self.get_session(model_name)
except RuntimeError as e:
    # Handle model loading failure
    pass
```

### Error Messages

Common error messages and their meanings:

- `"rembg library is not available"` - Install rembg package
- `"Failed to load model 'model_name'"` - Model download or loading failed
- `"Background removal failed"` - Processing error during background removal
- `"Preview failed"` - Error during real-time preview generation

## 🎯 Usage Examples

### Basic Background Removal

```python
# Initialize manager
bg_manager = BackgroundRemovalManager()

# Load image
image = load_image(uploaded_file)

# Remove background
result = bg_manager.remove_background(
    image=image,
    model_name="u2net",
    return_rgba=True
)

# Convert to bytes for download
output_bytes = image_to_bytes(result, 'PNG')
```

### Apply Multiple Effects

```python
# Define effects configuration
effects = {
    'gaussian_noise': {'enabled': True, 'variance': 0.02},
    'motion_blur': {'enabled': True, 'degree': 15, 'angle': 45},
    'camera_shake': {'enabled': True, 'intensity': 5}
}

# Apply effects
processed_image = apply_imageglitch_effects(image, effects)
```

### Custom Effect Implementation

```python
def apply_custom_effect(image, parameter1=1.0):
    """Custom effect implementation following ImageGlitch patterns."""
    
    # Ensure float32 for processing
    result = image.copy().astype(np.float32)
    
    # Apply your custom processing
    # ... custom logic here ...
    
    # Return processed image
    return result
```

## 📈 Performance Considerations

### Memory Management

- All effects work with `float32` arrays to prevent precision loss
- Images are copied to avoid modifying originals
- Caching system reduces redundant processing
- Session state manages loaded models efficiently

### Processing Pipeline

Effects are applied in specific order for optimal results:
1. Noise Effects
2. Blur Effects  
3. Shake Effects
4. Motion Effects

### Optimization Tips

- Use `PreviewManager` for real-time previews
- Enable caching with `hash_effects()` function
- Batch process similar operations
- Choose appropriate preview quality modes

---

*Next: [FAQ →](faq.md)*
