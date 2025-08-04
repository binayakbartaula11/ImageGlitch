"""Multi-Page ImageGlitch & AI Background Removal Application

A comprehensive image processing suite with two main components:
1. AI-powered background removal with multiple model options
2. Real-time image manipulation with various glitch effects

The application uses Streamlit for the UI, OpenCV and PIL for image processing,
and rembg for AI background removal capabilities.

Features:
- Multiple specialized AI models for background removal
- Real-time preview of image effects
- Various export options (PNG, JPEG) with transparency support
- Session state management for persistent user experience
"""

import streamlit as st
import os
import gc
import numpy as np
import cv2
from PIL import Image
import io
import time
import requests
import re
from urllib.parse import urlparse
from typing import Tuple, Dict, Any

# Import custom image effect utilities from modular packages
from image_utils.noise import add_gaussian_noise, add_salt_pepper_noise  # Noise generation effects
from image_utils.blur import apply_gaussian_blur, apply_motion_blur, apply_box_blur  # Blur effects
from image_utils.shaky import simulate_shaky, simulate_directional_shake  # Camera shake simulation
from image_utils.motion import simulate_motion_distortion, simulate_zoom_motion  # Motion effects

# Background removal imports with enhanced error handling and debugging
# This allows the app to run even if rembg is not installed, with detailed feedback
REMBG_AVAILABLE = False
REMBG_ERROR_MESSAGE = None
rembg_remove = None
new_session = None

# Initialize rembg with session state to prevent repeated logging
if 'rembg_initialized' not in st.session_state:
    st.session_state.rembg_initialized = True
    
    try:
        # First, test basic rembg import
        import rembg
        print(f"✅ rembg imported successfully - version: {getattr(rembg, '__version__', 'unknown')}")
        
        # Test specific function imports
        from rembg import remove as rembg_remove, new_session
        print("✅ rembg functions imported successfully")
        
        # Test if we can create a basic session (this is where many deployments fail)
        try:
            test_session = new_session('u2net')
            print("✅ rembg model session test successful")
            REMBG_AVAILABLE = True
            print("🎉 rembg is fully available and ready")
        except Exception as session_error:
            print(f"❌ rembg model session failed: {session_error}")
            REMBG_ERROR_MESSAGE = f"Model loading failed: {str(session_error)}"
            # Keep functions available but flag the model issue
            REMBG_AVAILABLE = False
            
    except ImportError as import_error:
        print(f"❌ rembg import failed: {import_error}")
        # Check for specific dependency issues
        error_str = str(import_error).lower()
        if 'numba' in error_str or 'llvmlite' in error_str:
            REMBG_ERROR_MESSAGE = f"Python version incompatibility: {str(import_error)} (try Python 3.9)"
        else:
            REMBG_ERROR_MESSAGE = f"Import failed: {str(import_error)}"
        REMBG_AVAILABLE = False
        rembg_remove = None
        new_session = None
    except Exception as general_error:
        print(f"❌ rembg general error: {general_error}")
        REMBG_ERROR_MESSAGE = f"General error: {str(general_error)}"
        REMBG_AVAILABLE = False
        rembg_remove = None
        new_session = None
    
    # Store the final status in session state
    if not REMBG_AVAILABLE and REMBG_ERROR_MESSAGE:
        print(f"❌ rembg is not available: {REMBG_ERROR_MESSAGE}")
else:
    # If already initialized, just import silently
    try:
        import rembg
        from rembg import remove as rembg_remove, new_session
        REMBG_AVAILABLE = True
        REMBG_ERROR_MESSAGE = None
    except:
        REMBG_AVAILABLE = False
        REMBG_ERROR_MESSAGE = "rembg not available"
        rembg_remove = None
        new_session = None


os.environ["U2NET_HOME"] = "/tmp/u2net_models"

class BackgroundRemovalManager:
    """Manages background removal functionality with proper error handling and model management.
    
    This class handles the loading and management of AI models for background removal,
    provides a consistent interface for background removal operations, and ensures
    proper error handling and resource management.
    
    Key responsibilities:
    - Lazy-loading of AI models to minimize memory usage
        - Session management for efficient model reuse
        - Supports pre-bundled model files
    - Consistent error handling and user feedback
    - Support for multiple output formats (transparent, white bg, custom color)
    """
    
    # Available AI models with detailed descriptions for UI display and selection
    MODELS = {
        "u2net": {
            "name": "U2-Net (General)",
            "description": "🎯 Best for general photos with people, objects",
            "suitable_for": "General purpose, portraits, objects",
            "size": "~176MB"
        },
        "u2net_human_seg": {
            "name": "U2-Net Human",
            "description": "👤 Optimized for human segmentation",
            "suitable_for": "Human portraits, people photos",
            "size": "~176MB"
        },
        "u2net_cloth_seg": {
            "name": "U2-Net Cloth",
            "description": "👕 Specialized for clothing items",
            "suitable_for": "Fashion, clothing, apparel",
            "size": "~176MB"
        },
        "isnet-general-use": {
            "name": "IS-Net General",
            "description": "🌟 High accuracy for various subjects",
            "suitable_for": "High-quality general purpose",
            "size": "~173MB"
        },
        "silueta": {
            "name": "Silueta",
            "description": "⚡ Fast processing, good quality",
            "suitable_for": "Quick processing, good for most images",
            "size": "~43MB"
        }
    }
    
    def __init__(self):
        self.sessions = {}
        self.model_loaded = {}
    
    def get_session(self, model_name: str):
        """Get or create a session for the specified model.
        
        This method implements lazy loading of AI models - only loading them when
        needed and caching them for future use. This approach saves memory and
        reduces startup time.
        
        Args:
            model_name: The name of the model to load (must be one of the keys in MODELS)
            
        Returns:
            A session object for the specified model
            
        Raises:
            ImportError: If rembg library is not available
            RuntimeError: If model loading fails for any reason
        """
        if not REMBG_AVAILABLE:
            raise ImportError("rembg library is not available")
        
        # Check if model is already loaded - if not, load it
        # Unload any previously loaded models to save memory
        for loaded_model in list(self.sessions.keys()):
            if loaded_model != model_name:
                del self.sessions[loaded_model]

        try:
            # Create a new session for this model
            model_path = f"models/{model_name}.onnx"  # Adjust the path if you have pre-bundled models
            if os.path.exists(model_path):
                self.sessions[model_name] = new_session(model_name=model_name, path=model_path)
            else:
                self.sessions[model_name] = new_session(model_name)
            self.model_loaded[model_name] = True
        except Exception as e:
            # Provide detailed error information for troubleshooting
            raise RuntimeError(f"Failed to load model '{model_name}': {str(e)}")
        
        return self.sessions[model_name]
    
    def remove_background(self, image: np.ndarray, model_name: str = "u2net", 
                         return_rgba: bool = True, bg_color: str = None) -> np.ndarray:
        """
        Remove background from image using the specified AI model.
        
        This method handles the complete background removal process including:
        - Input validation and preprocessing
        - Model selection and application
        - Output format handling (transparent, white, or custom background)
        - Error handling and reporting
        
        Args:
            image: Input image as numpy array (RGB or RGBA format)
            model_name: Model to use for background removal (must be one of the keys in MODELS)
            return_rgba: If True, returns RGBA image with transparency; if False, returns RGB 
                        with either white or custom background
            bg_color: Optional hex color string for custom background (e.g., "#FF0000" for red)
                     Only used when return_rgba is False
        
        Returns:
            Processed image as numpy array (RGBA if return_rgba=True, RGB otherwise)
            
        Raises:
            ImportError: If rembg library is not installed
            RuntimeError: If background removal process fails
        """
        if not REMBG_AVAILABLE:
            raise ImportError("rembg library is not installed - please install with 'pip install rembg'")
        
        try:
            # Step 1: Preprocess input image - ensure correct format for processing
            if image.dtype != np.uint8:
                # Convert from float to uint8 if needed (e.g., if image came from another processing step)
                image = (image * 255).astype(np.uint8)
            
            # Convert numpy array to PIL Image (required by rembg)
            input_pil = Image.fromarray(image)
            
            # Step 2: Get or create model session (lazy loading)
            session = self.get_session(model_name)
            
            # Step 3: Apply background removal using the selected model
            output_pil = rembg_remove(input_pil, session=session)
            
            # Step 4: Convert result back to numpy array for further processing
            output_array = np.array(output_pil)
            
            # Step 5: Handle output format based on user preferences
            if return_rgba:
                # Option A: Return transparent background (RGBA)
                if output_array.shape[2] == 3:  # If model returned RGB instead of RGBA
                    # Add fully opaque alpha channel
                    alpha = np.ones((output_array.shape[0], output_array.shape[1], 1), dtype=output_array.dtype) * 255
                    output_array = np.concatenate([output_array, alpha], axis=2)
            elif bg_color:  # Custom background color
                # Option B: Return RGB with custom background color
                if output_array.shape[2] == 4:  # If we have alpha channel
                    # Convert hex color string to RGB tuple
                    bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
                    
                    # Alpha blending formula: result = foreground*alpha + background*(1-alpha)
                    alpha = output_array[:, :, 3:4] / 255.0  # Normalize alpha to 0-1 range
                    rgb = output_array[:, :, :3]  # Get RGB channels
                    custom_bg = np.ones_like(rgb) * np.array(bg_rgb)  # Create background color array
                    output_array = (rgb * alpha + custom_bg * (1 - alpha)).astype(np.uint8)  # Blend
            else:
                # Option C: Return RGB with white background (default fallback)
                if output_array.shape[2] == 4:  # If we have alpha channel
                    # Alpha blending with white background
                    alpha = output_array[:, :, 3:4] / 255.0
                    rgb = output_array[:, :, :3]
                    white_bg = np.ones_like(rgb) * 255  # White background (all 255s)
                    output_array = (rgb * alpha + white_bg * (1 - alpha)).astype(np.uint8)
                
            return output_array
            
        except Exception as e:
            # Provide detailed error information for troubleshooting
            raise RuntimeError(f"Background removal failed: {str(e)}")
    
    def is_model_loaded(self, model_name: str) -> bool:
        """Check if a model is already loaded."""
        return self.model_loaded.get(model_name, False)
    
    def get_model_info(self, model_name: str) -> dict:
        """Get information about a specific model."""
        return self.MODELS.get(model_name, {})


class PreviewManager:
    """
    Manages different preview quality modes and image optimization for efficient UI rendering.
    
    This class provides utilities for resizing and optimizing images based on different
    quality-performance tradeoffs. It helps balance between processing speed and visual quality
    by defining standard preview modes with specific size and quality parameters.
    
    The preview system is critical for maintaining responsive UI performance while still
    providing meaningful visual feedback to users during image processing operations.
    
    Key features:
    - Predefined quality modes (Fast, Balanced, High Quality) with optimized parameters
    - Intelligent resizing that preserves aspect ratio
    - Performance optimization through size reduction for real-time previews
    - Quality-aware processing that adapts to user preference and device capabilities
    
    This class works in conjunction with the caching system to further optimize
    performance by avoiding redundant processing of identical parameter sets.
    """
    
    # Dictionary defining the available preview quality modes with their parameters
    # Each mode balances between performance and quality for different use cases
    PREVIEW_MODES = {
        # Fast mode: Prioritizes UI responsiveness over image quality
        "Fast": {"max_size": 300, "quality": 75, "description": "⚡ Fast preview (300px max)"},
        # Balanced mode: Default option with good compromise between quality and speed
        "Balanced": {"max_size": 500, "quality": 85, "description": "⚖️ Balanced quality (500px max)"},
        # High Quality mode: Prioritizes visual quality for detailed inspection
        "High Quality": {"max_size": 800, "quality": 95, "description": "🎯 High quality (800px max)"}
    }
    
    @staticmethod
    def resize_for_preview(image: np.ndarray, mode: str) -> np.ndarray:
        """
        Resize image based on preview mode while maintaining aspect ratio.
        
        This method intelligently resizes images to fit within the dimensions specified by
        the selected preview mode. It preserves aspect ratio to avoid distortion and uses
        high-quality resampling for better visual results.
        
        Args:
            image: Input image as numpy array
            mode: Preview mode name (must be one of the keys in PREVIEW_MODES)
                  If invalid mode is provided, falls back to "Balanced"
        
        Returns:
            Resized image as numpy array (original image if already smaller than max_size)
        """
        # Fall back to balanced mode if an invalid mode is specified
        if mode not in PreviewManager.PREVIEW_MODES:
            mode = "Balanced"
        
        # Get maximum dimension size from the selected mode
        max_size = PreviewManager.PREVIEW_MODES[mode]["max_size"]
        h, w = image.shape[:2]
        
        # Skip resizing if image is already smaller than the target size
        if max(h, w) <= max_size:
            return image
        
        # Calculate new dimensions while preserving aspect ratio
        if h > w:  # Portrait orientation
            new_h = max_size
            new_w = int(w * (max_size / h))
        else:      # Landscape or square orientation
            new_w = max_size
            new_h = int(h * (max_size / w))
        
        # Use high-quality Lanczos resampling for better visual quality
        pil_image = Image.fromarray(image)
        resized = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)
        return np.array(resized)


def load_image(uploaded_file):
    """Load and convert uploaded file to numpy array."""
    image = Image.open(uploaded_file)
    image_array = np.array(image)
    return image_array


def load_image_from_url(url):
    """Load an image from a URL."""
    try:
        if not urlparse(url).scheme:
            raise ValueError("Missing scheme in URL. Perhaps you meant to add 'https://'")

        response = requests.get(url)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch image from URL: {e}")
    except Exception as e:
        raise ValueError(f"Failed to process image from URL: {e}")


def is_valid_url(url):
    """Check if the URL is valid and an image with strong validation."""
    if not url or len(url.strip()) == 0:
        return False
    
    try:
        # Parse the URL to check its components
        parsed = urlparse(url)
        
        # Check for valid scheme
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # Check for netloc (hostname) - this catches URLs like "https://"
        if not parsed.netloc or len(parsed.netloc.strip()) == 0:
            return False
        
        # Check for valid domain structure (must have at least one dot)
        if '.' not in parsed.netloc:
            return False
        
        # Check for valid image extensions in the path
        if not parsed.path or not parsed.path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')):
            return False
        
        # Additional regex validation for URL structure
        regex = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?))'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(regex.match(url))
        
    except Exception:
        return False


def image_to_bytes(image_array, format='PNG'):
    """Convert numpy array to bytes for download."""
    # Ensure the image is in the correct format for PIL
    if image_array.dtype != np.uint8:
        image_array = np.clip(image_array, 0, 255).astype(np.uint8)
    
    # Handle different image formats and ensure RGB for JPEG
    if len(image_array.shape) == 2:  # Grayscale image
        image_pil = Image.fromarray(image_array, mode='L')
    elif image_array.shape[2] == 4 and format.upper() == 'JPEG':  # RGBA image for JPEG
        # JPEG doesn't support alpha channel, convert to RGB
        image_pil = Image.fromarray(image_array).convert('RGB')
    else:  # RGB or RGBA image
        image_pil = Image.fromarray(image_array)
    
    # Save to buffer with high quality for JPEG
    buf = io.BytesIO()
    if format.upper() == 'JPEG':
        image_pil.save(buf, format=format, quality=95)
    else:
        image_pil.save(buf, format=format)
    
    return buf.getvalue()


def apply_imageglitch_effects(image: np.ndarray, effects: Dict[str, Any]) -> np.ndarray:
    """
    Apply multiple image manipulation effects based on user-selected parameters.
    
    This function serves as the central processing pipeline for the ImageGlitch tool,
    applying various effects in a specific order to create complex image manipulations.
    It handles multiple effect categories including noise, blur, shake, and motion effects,
    each with their own parameters controlled through the effects dictionary.
    
    The processing pipeline maintains image data as float32 throughout to prevent
    clipping and data loss between effect applications, ensuring high-quality results
    even with multiple stacked effects.
    
    Args:
        image: Input image as numpy array (uint8 or float32)
        effects: Dictionary containing effect parameters with the following structure:
                {effect_name: {"enabled": bool, param1: value1, param2: value2, ...}}
                Where effect_name can be: gaussian_noise, salt_pepper_noise, gaussian_blur,
                motion_blur, box_blur, camera_shake, directional_shake, motion_distortion,
                or zoom_motion
    
    Returns:
        Processed image as float32 numpy array with all enabled effects applied
    
    Note:
        Effects are applied in a specific order: noise → blur → shake → motion
        This order produces the most natural-looking results when combining effects
    """
    # Make a deep copy to avoid modifying the original
    # Ensure we're working with a float array for processing to avoid clipping during operations
    result = image.copy().astype(np.float32)
    
    # Apply noise effects
    if effects.get('gaussian_noise', {}).get('enabled', False):
        noise_params = effects['gaussian_noise']
        result = add_gaussian_noise(result, var=noise_params['variance'])
        # Ensure we maintain float32 for further processing
        result = result.astype(np.float32)
    
    if effects.get('salt_pepper_noise', {}).get('enabled', False):
        noise_params = effects['salt_pepper_noise']
        result = add_salt_pepper_noise(result, amount=noise_params['amount'])
        # Ensure we maintain float32 for further processing
        result = result.astype(np.float32)
    
    # Apply blur effects
    if effects.get('gaussian_blur', {}).get('enabled', False):
        blur_params = effects['gaussian_blur']
        result = apply_gaussian_blur(result, kernel_size=blur_params['kernel_size'])
        # Ensure we maintain float32 for further processing
        result = result.astype(np.float32)
    
    if effects.get('motion_blur', {}).get('enabled', False):
        blur_params = effects['motion_blur']
        result = apply_motion_blur(result, degree=blur_params['degree'], angle=blur_params['angle'])
        # Ensure we maintain float32 for further processing
        result = result.astype(np.float32)
    
    if effects.get('box_blur', {}).get('enabled', False):
        blur_params = effects['box_blur']
        result = apply_box_blur(result, kernel_size=blur_params['kernel_size'])
        # Ensure we maintain float32 for further processing
        result = result.astype(np.float32)
    
    # Apply shake effects
    if effects.get('camera_shake', {}).get('enabled', False):
        shake_params = effects['camera_shake']
        result = simulate_shaky(result, intensity=shake_params['intensity'])
        # Ensure we maintain float32 for further processing
        result = result.astype(np.float32)
    
    if effects.get('directional_shake', {}).get('enabled', False):
        shake_params = effects['directional_shake']
        result = simulate_directional_shake(result, direction=shake_params['direction'], intensity=shake_params['intensity'])
        # Ensure we maintain float32 for further processing
        result = result.astype(np.float32)
    
    # Apply motion effects
    if effects.get('motion_distortion', {}).get('enabled', False):
        motion_params = effects['motion_distortion']
        result = simulate_motion_distortion(result, direction=motion_params['direction'], intensity=motion_params['intensity'])
        # Ensure we maintain float32 for further processing
        result = result.astype(np.float32)
    
    if effects.get('zoom_motion', {}).get('enabled', False):
        motion_params = effects['zoom_motion']
        result = simulate_zoom_motion(result, intensity=motion_params['intensity'])
        # Ensure we maintain float32 for further processing
        result = result.astype(np.float32)
    
    # Ensure the result is in the correct format for display and export
    # Clip values to valid range and convert to uint8
    result = np.clip(result, 0, 255).astype(np.uint8)
    
    return result


def hash_effects(effects: Dict[str, Any]) -> str:
    """
    Create a unique hash string from the effects dictionary for caching purposes.
    
    This function generates a consistent, unique identifier for a specific combination
    of image effects and their parameters. The hash is used as a key in the preview cache
    system to avoid redundant processing of identical effect combinations.
    
    The function works by:
    1. Converting the effects dictionary to a sorted string representation
    2. Generating an MD5 hash of this string
    3. Returning the hexadecimal digest as a unique identifier
    
    Args:
        effects: Dictionary containing effect parameters with structure:
                {effect_name: {"enabled": bool, param1: value1, param2: value2, ...}}
    
    Returns:
        A 32-character hexadecimal string uniquely identifying the effects combination
    
    Note:
        This function is critical for the caching system that improves UI responsiveness
        by avoiding redundant processing of identical effect combinations.
    """
    import hashlib
    effect_str = str(sorted(effects.items()))
    return hashlib.md5(effect_str.encode()).hexdigest()


def initialize_session_state():
    """
    Initialize Streamlit session state variables for persistent storage across reruns.
    
    This function sets up two critical session state variables:
    - bg_manager: Stores the BackgroundRemovalManager instance for AI model management
    - preview_cache: Dictionary to store processed image previews to avoid redundant processing
    
    The function checks if these variables already exist before initializing them to
    prevent resetting values on Streamlit reruns.
    """
    if 'bg_manager' not in st.session_state:
        st.session_state.bg_manager = BackgroundRemovalManager() if REMBG_AVAILABLE else None
    if 'preview_cache' not in st.session_state:
        st.session_state.preview_cache = {}


def show_bg_removal_page():
    """
    Render the AI Background Removal page with all its UI components and functionality.
    
    This function creates the complete UI for the background removal tool, including:
    - Title and description
    - Error handling for missing dependencies
    - File upload interface
    - Model selection and configuration options
    - Background color customization
    - Preview quality settings
    - Processing button and progress indicators
    - Result display with download options
    
    The function also manages the processing workflow and error handling.
    """
    st.title("✂️ AI Background Removal")
    st.markdown("Remove backgrounds from your images using advanced AI models.")
    
    # Check rembg availability with detailed error information
    if not REMBG_AVAILABLE:
        st.error("❌ **rembg library not available**")
        
        # Show specific error details if available
        if REMBG_ERROR_MESSAGE:
            st.error(f"**Error Details:** {REMBG_ERROR_MESSAGE}")
        
        # Add a diagnostic button
        if st.button("🔍 Run rembg Diagnostics"):
            st.code("""
            # Run this in your terminal to debug rembg installation:
            python debug_rembg.py
            """)
        
        st.markdown("""
        **Installation Required:**
        ```bash
        pip install rembg
        ```
        **For GPU acceleration (optional):**
        ```bash
        pip install rembg[gpu]
        ```
        
        **Troubleshooting Steps:**
        1. **Force reinstall:** `pip uninstall rembg && pip install rembg`
        2. **Check system dependencies:** Make sure packages.txt includes all required libraries
        3. **Clear Streamlit cache:** Force redeploy your app
        4. **Run diagnostics:** Use the debug script provided in your repository
        
        **Common Issues:**
        - Missing system libraries (libgl1-mesa-glx, libglib2.0-0, etc.)
        - Incomplete model downloads
        - Version conflicts with other packages
        """)
        return
    
    # Sidebar controls
    st.sidebar.header("🎛️ Background Removal Settings")
    
    # Image input options
    st.sidebar.subheader("📸 Image Input")
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["Upload File", "URL"],
        help="Select how you want to provide the image"
    )
    
    uploaded_file = None
    image_url = None
    
    if input_method == "Upload File":
        # File uploader
        uploaded_file = st.sidebar.file_uploader(
            "Upload Image",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            help="Upload an image to remove its background"
        )
    else:
        # URL input
        image_url = st.sidebar.text_input(
            "Image URL (must be jpg, png, etc.)",
            placeholder="https://example.com/image.jpg",
            help="Paste a direct link to an image (jpg, png, etc.)"
        )
        
        if image_url:
            # Only validate if the user has actually typed something meaningful
            if len(image_url.strip()) > 0:
                if not is_valid_url(image_url):
                    st.sidebar.error("❌ Invalid URL! Must start with http:// or https:// and end with an image extension like jpg, png, webp.")
                    image_url = None
                else:
                    st.sidebar.success("✅ Valid image URL detected")
            else:
                # Reset to None if it's just whitespace
                image_url = None
    
    # Determine if we have an image source - only if there's actual content
    has_image = uploaded_file is not None or (image_url is not None and len(image_url.strip()) > 0)
    
    if has_image:
        # Show image source details
        if uploaded_file is not None:
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / 1024:.1f} KB"
            }
            st.sidebar.write("**File Details:**")
            for key, value in file_details.items():
                st.sidebar.write(f"- {key}: {value}")
        elif image_url is not None:
            parsed_url = urlparse(image_url)
            filename = parsed_url.path.split('/')[-1] or "image"
            st.sidebar.write("**URL Details:**")
            st.sidebar.write(f"- Filename: {filename}")
            st.sidebar.write(f"- Source: {parsed_url.netloc}")
        
        st.sidebar.markdown("---")
        
        # Model selection
        st.sidebar.subheader("🤖 AI Model Selection")
        model_options = list(BackgroundRemovalManager.MODELS.keys())
        model_labels = [f"{BackgroundRemovalManager.MODELS[m]['name']}" for m in model_options]
        
        selected_model_idx = st.sidebar.selectbox(
            "Choose AI Model",
            range(len(model_options)),
            format_func=lambda x: model_labels[x],
            index=0,
            help="Select the AI model for background removal"
        )
        selected_model = model_options[selected_model_idx]
        
        # Show model info
        model_info = BackgroundRemovalManager.MODELS[selected_model]
        st.sidebar.success(f"**{model_info['name']}**")
        st.sidebar.caption(f"📝 {model_info['description']}")
        st.sidebar.caption(f"💡 Best for: {model_info['suitable_for']}")
        st.sidebar.caption(f"📦 Size: {model_info['size']}")
        
        # Model loading status
        if st.session_state.bg_manager and st.session_state.bg_manager.is_model_loaded(selected_model):
            st.sidebar.success(f"✅ Model loaded and ready")
        else:
            st.sidebar.info(f"📥 Model will download on first use")
        
        st.sidebar.markdown("---")
        
        # Output format
        st.sidebar.subheader("🎨 Output Settings")
        output_format = st.sidebar.radio(
            "Background Type",
            ["transparent", "white", "custom"],
            format_func=lambda x: {
                "transparent": "🔳 Transparent (RGBA)",
                "white": "⬜ White Background",
                "custom": "🎨 Custom Color"
            }[x],
            help="Choose the background for the output image"
        )
        
        # Custom background color
        if output_format == "custom":
            # Use previously selected color if available
            default_color = st.session_state.bg_color if hasattr(st.session_state, 'bg_color') else "#000000"
            bg_color = st.sidebar.color_picker("Background Color", default_color)
            
            # Show a preview of the selected color
            st.sidebar.markdown(f"""
            <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <p style="color: {'white' if sum(int(bg_color[i:i+2], 16) for i in (1, 3, 5)) < 382 else 'black'}; text-align: center; margin: 0;">
                    Selected Background Color
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            bg_color = None
        
        # Preview quality
        preview_mode = st.sidebar.selectbox(
            "Preview Quality",
            ["Fast", "Balanced", "High Quality"],
            index=1,
            help="Choose preview quality vs speed"
        )
        
        st.sidebar.markdown("---")
        
        # Process button
        process_bg = st.sidebar.button("🎯 Remove Background", type="primary")
        
        # Load and display original image - only if we have valid input
        try:
            if uploaded_file is not None:
                original_image = load_image(uploaded_file)
            elif image_url is not None and len(image_url.strip()) > 0:
                with st.spinner("Loading image from URL..."):
                    pil_image = load_image_from_url(image_url)
                    original_image = np.array(pil_image)
            else:
                # This shouldn't happen due to has_image check, but just in case
                st.error("❌ No valid image source provided")
                return
        except Exception as e:
            st.error(f"❌ Failed to load image: {str(e)}")
            return
        
        # Create layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Original Image")
            st.image(original_image, use_container_width=True)
        
        with col2:
            st.subheader("✂️ Background Removed")
            
            if process_bg:
                try:
                    with st.spinner(f"Processing with {model_info['name']}..."):
                        # Process the image
                        processed_image = st.session_state.bg_manager.remove_background(
                            original_image,
                            model_name=selected_model,
                            return_rgba=(output_format == "transparent"),
                            bg_color=bg_color if output_format == "custom" else None
                        )
                        
                        # Handle custom background
                        if output_format == "custom" and processed_image.shape[2] == 4:
                            # Convert hex color to RGB
                            bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
                            
                            # Store the background color for later use
                            st.session_state.bg_color = bg_color
                            st.session_state.bg_rgb = bg_rgb
                            
                            # Blend with custom background
                            alpha = processed_image[:, :, 3:4] / 255.0
                            rgb = processed_image[:, :, :3]
                            custom_bg = np.ones_like(rgb) * np.array(bg_rgb)
                            processed_image = (rgb * alpha + custom_bg * (1 - alpha)).astype(np.uint8)
                        
                        # Store in session state
                        st.session_state.bg_processed_image = processed_image
                        st.session_state.bg_original_image = original_image
                        st.session_state.bg_output_format = output_format
                        st.session_state.bg_model_used = model_info['name']
                        
                        # Display processed image
                        st.image(processed_image, use_container_width=True)
                        
                        # Processing success message
                        st.success(f"✅ Background removed successfully using {model_info['name']}")
                        
                except ImportError:
                    st.error("❌ rembg library not available")
                except Exception as e:
                    st.error(f"❌ Processing failed: {str(e)}")
                    if "model" in str(e).lower():
                        st.info("💡 Model downloading may take a few minutes on first use")
            
            elif hasattr(st.session_state, 'bg_processed_image'):
                # Show previously processed image
                display_image = st.session_state.bg_processed_image.copy()
                
                # Re-apply custom background if needed
                if hasattr(st.session_state, 'bg_output_format') and st.session_state.bg_output_format == "custom":
                    if hasattr(st.session_state, 'bg_rgb') and display_image.shape[2] == 4:
                        # Re-apply the custom background color
                        alpha = display_image[:, :, 3:4] / 255.0
                        rgb = display_image[:, :, :3]
                        custom_bg = np.ones_like(rgb) * np.array(st.session_state.bg_rgb)
                        display_image = (rgb * alpha + custom_bg * (1 - alpha)).astype(np.uint8)
                
                st.image(display_image, use_container_width=True)
                st.info(f"✅ Processed with {st.session_state.bg_model_used}")
            
            else:
                st.info("👆 Click 'Remove Background' to process the image")
        
        # Download section
        if hasattr(st.session_state, 'bg_processed_image'):
            st.markdown("---")
            st.subheader("📥 Download Options")
            
            # Prepare the download image with proper background handling
            download_image = st.session_state.bg_processed_image.copy()
            
            # Re-apply custom background if needed
            if hasattr(st.session_state, 'bg_output_format') and st.session_state.bg_output_format == "custom":
                if hasattr(st.session_state, 'bg_rgb') and download_image.shape[2] == 4:
                    # Re-apply the custom background color
                    alpha = download_image[:, :, 3:4] / 255.0
                    rgb = download_image[:, :, :3]
                    custom_bg = np.ones_like(rgb) * np.array(st.session_state.bg_rgb)
                    download_image = (rgb * alpha + custom_bg * (1 - alpha)).astype(np.uint8)
            
            col_dl1, col_dl2, col_dl3 = st.columns(3)
            
            with col_dl1:
                if st.session_state.bg_output_format == "transparent":
                    png_bytes = image_to_bytes(download_image, 'PNG')
                    st.download_button(
                        "📥 Download PNG (Transparent)",
                        data=png_bytes,
                        file_name="background_removed.png",
                        mime="image/png"
                    )
                else:
                    png_bytes = image_to_bytes(download_image, 'PNG')
                    st.download_button(
                        "📥 Download PNG",
                        data=png_bytes,
                        file_name="background_removed.png",
                        mime="image/png"
                    )
            
            with col_dl2:
                if st.session_state.bg_output_format != "transparent":
                    jpg_bytes = image_to_bytes(download_image, 'JPEG')
                    st.download_button(
                        "📥 Download JPEG",
                        data=jpg_bytes,
                        file_name="background_removed.jpg",
                        mime="image/jpeg"
                    )
                else:
                    st.caption("JPEG not available for transparent images")
            
            with col_dl3:
                # Original image download
                orig_bytes = image_to_bytes(st.session_state.bg_original_image, 'PNG')
                st.download_button(
                    "📥 Download Original",
                    data=orig_bytes,
                    file_name="original_image.png",
                    mime="image/png"
                )
    
    else:
        # Show model information when no image is uploaded
        st.info("👆 Upload an image to start background removal")
        
        st.subheader("🤖 Available AI Models")
        
        for model_key, model_info in BackgroundRemovalManager.MODELS.items():
            with st.expander(f"{model_info['name']} - {model_info['size']}"):
                st.markdown(f"**Description:** {model_info['description']}")
                st.markdown(f"**Best for:** {model_info['suitable_for']}")
                st.markdown(f"**Model size:** {model_info['size']}")


def show_imageglitch_page():
    """
    Render the ImageGlitch page with real-time image manipulation features.
    
    This function creates the complete UI for the image glitch tool, including:
    - Title and description
    - Session state initialization for caching and performance
    - File upload interface
    - Real-time preview controls and quality settings
    - Multiple effect categories with customizable parameters:
      * Noise effects (Gaussian, Salt & Pepper)
      * Blur effects (Gaussian, Motion, Box)
      * Shake effects (Camera, Directional)
      * Motion effects (Distortion, Zoom)
    - Live preview with performance statistics
    - Full-quality processing options
    - Download options for processed images
    
    The function implements a responsive UI with real-time feedback as users
    adjust effect parameters, using caching for performance optimization.
    """
    st.title("🎨 ImageGlitch: Real-Time Image Manipulation")
    st.markdown("Apply various glitch effects and see results in real-time.")
    
    # Initialize preview cache for this page
    if 'glitch_preview_cache' not in st.session_state:
        st.session_state.glitch_preview_cache = {}
    if 'glitch_last_hash' not in st.session_state:
        st.session_state.glitch_last_hash = None
    
    # Sidebar controls
    st.sidebar.header("🎛️ ImageGlitch Controls")
    
    # Image input options
    st.sidebar.subheader("📸 Image Input")
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["Upload File", "URL"],
        help="Select how you want to provide the image"
    )
    
    uploaded_file = None
    image_url = None
    
    if input_method == "Upload File":
        # File uploader
        uploaded_file = st.sidebar.file_uploader(
            "Upload Image",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            help="Upload an image to apply glitch effects"
        )
    else:
        # URL input
        image_url = st.sidebar.text_input(
            "Image URL",
            placeholder="https://example.com/image.jpg",
            help="Paste a direct link to an image (jpg, png, etc.)"
        )
        
        if image_url:
            # Only validate if the user has actually typed something meaningful
            if len(image_url.strip()) > 0:
                if not is_valid_url(image_url):
                    st.sidebar.error("❌ Please enter a valid image URL with proper extension (.jpg, .png, .bmp, .tiff)")
                    image_url = None
                else:
                    st.sidebar.success("✅ Valid image URL detected")
            else:
                # Reset to None if it's just whitespace
                image_url = None
    
    # Determine if we have an image source - only if there's actual content
    has_image = uploaded_file is not None or (image_url is not None and len(image_url.strip()) > 0)
    
    if has_image:
        # Show image source details
        if uploaded_file is not None:
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / 1024:.1f} KB"
            }
            st.sidebar.write("**File Details:**")
            for key, value in file_details.items():
                st.sidebar.write(f"- {key}: {value}")
        elif image_url is not None:
            parsed_url = urlparse(image_url)
            filename = parsed_url.path.split('/')[-1] or "image"
            st.sidebar.write("**URL Details:**")
            st.sidebar.write(f"- Filename: {filename}")
            st.sidebar.write(f"- Source: {parsed_url.netloc}")
        
        st.sidebar.markdown("---")
        
        # Preview settings
        st.sidebar.subheader("⚡ Real-Time Preview")
        auto_preview = st.sidebar.checkbox("Auto Preview", value=True, help="Show effects in real-time")
        
        preview_mode = st.sidebar.selectbox(
            "Preview Quality",
            ["Fast", "Balanced", "High Quality"],
            index=1,
            help="Balance between speed and quality"
        )
        
        if not auto_preview:
            manual_refresh = st.sidebar.button("🔄 Refresh Preview")
        else:
            manual_refresh = False
        
        st.sidebar.markdown("---")
        
        # Extreme mode
        st.sidebar.subheader("⚡ Effect Mode")
        extreme_mode = st.sidebar.toggle("Extreme Mode", value=False, 
                                        help="Enable extreme parameter ranges")
        
        if extreme_mode:
            st.sidebar.warning("🚨 **EXTREME MODE** - High intensity effects!")
        
        st.sidebar.markdown("---")
        
        # Define original_image early for safe reference
        original_image = None
        
        try:
            if uploaded_file is not None:
                original_image = load_image(uploaded_file)
            elif image_url is not None:
                # Auto-correct URL scheme if missing
                if not image_url.lower().startswith(('http://', 'https://')):
                    image_url = "https://" + image_url
                    st.sidebar.info("ℹ️ Corrected URL to include 'https://' at the beginning")
                
                with st.spinner("Loading image from URL..."):
                    pil_image = load_image_from_url(image_url)
                    original_image = np.array(pil_image)
        except ValueError as ve:
            st.error(f"❌ Failed to load image: {str(ve)}")
            return
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            return

        if original_image is None:
            # Exit early if no valid image was loaded
            return
        
        # Effects controls
        st.sidebar.subheader("🔊 Noise Effects")
        gaussian_enabled = st.sidebar.checkbox("Gaussian Noise")
        if extreme_mode:
            gaussian_variance = st.sidebar.slider("Variance (EXTREME)", 0.0, 5.0, 0.02, key='g_var')
        else:
            gaussian_variance = st.sidebar.slider("Variance", 0.0, 0.1, 0.02, key='g_var')
        
        salt_pepper_enabled = st.sidebar.checkbox("Salt & Pepper Noise")
        if extreme_mode:
            salt_pepper_amount = st.sidebar.slider("Amount (EXTREME)", 0.0, 1.0, 0.01, key='sp_amt')
        else:
            salt_pepper_amount = st.sidebar.slider("Amount", 0.0, 0.1, 0.01, key='sp_amt')
        
        st.sidebar.subheader("🌫️ Blur Effects")
        gaussian_blur_enabled = st.sidebar.checkbox("Gaussian Blur")
        if extreme_mode:
            gaussian_kernel = st.sidebar.slider("Kernel Size (EXTREME)", 3, 101, 7, step=2, key='gb_kern')
        else:
            gaussian_kernel = st.sidebar.slider("Kernel Size", 3, 15, 7, step=2, key='gb_kern')
        
        motion_blur_enabled = st.sidebar.checkbox("Motion Blur")
        if extreme_mode:
            motion_degree = st.sidebar.slider("Degree (EXTREME)", 1, 100, 20, key='mb_deg')
        else:
            motion_degree = st.sidebar.slider("Degree", 1, 30, 20, key='mb_deg')
        motion_angle = st.sidebar.slider("Angle", 0, 360, 45, key='mb_ang')
        
        box_blur_enabled = st.sidebar.checkbox("Box Blur")
        if extreme_mode:
            box_kernel = st.sidebar.slider("Box Kernel (EXTREME)", 3, 101, 5, step=2, key='bb_kern')
        else:
            box_kernel = st.sidebar.slider("Box Kernel", 3, 15, 5, step=2, key='bb_kern')
        
        st.sidebar.subheader("📳 Shake Effects")
        camera_shake_enabled = st.sidebar.checkbox("Camera Shake")
        if extreme_mode:
            camera_intensity = st.sidebar.slider("Intensity (EXTREME)", 1, 50, 5, key='cs_int')
        else:
            camera_intensity = st.sidebar.slider("Intensity", 1, 10, 5, key='cs_int')
        
        directional_shake_enabled = st.sidebar.checkbox("Directional Shake")
        if extreme_mode:
            dir_intensity = st.sidebar.slider("Direction Intensity (EXTREME)", 1, 50, 8, key='ds_int')
        else:
            dir_intensity = st.sidebar.slider("Direction Intensity", 1, 10, 8, key='ds_int')
        shake_direction = st.sidebar.selectbox("Direction", ["horizontal", "vertical", "both"], key='ds_dir')
        
        st.sidebar.subheader("🏃 Motion Effects")
        motion_distortion_enabled = st.sidebar.checkbox("Motion Distortion")
        motion_direction = st.sidebar.selectbox("Motion Direction", ["horizontal", "vertical", "diagonal"], key='md_dir')
        if extreme_mode:
            motion_intensity = st.sidebar.slider("Motion Intensity (EXTREME)", 1, 100, 15, key='md_int')
        else:
            motion_intensity = st.sidebar.slider("Motion Intensity", 1, 20, 15, key='md_int')
        
        zoom_motion_enabled = st.sidebar.checkbox("Zoom Motion Blur")
        if extreme_mode:
            zoom_intensity = st.sidebar.slider("Zoom Intensity (EXTREME)", 1, 50, 5, key='zm_int')
        else:
            zoom_intensity = st.sidebar.slider("Zoom Intensity", 1, 10, 5, key='zm_int')
        
        st.sidebar.markdown("---")
        
        # Collect effects
        effects = {
            'gaussian_noise': {'enabled': gaussian_enabled, 'variance': gaussian_variance},
            'salt_pepper_noise': {'enabled': salt_pepper_enabled, 'amount': salt_pepper_amount},
            'gaussian_blur': {'enabled': gaussian_blur_enabled, 'kernel_size': gaussian_kernel},
            'motion_blur': {'enabled': motion_blur_enabled, 'degree': motion_degree, 'angle': motion_angle},
            'box_blur': {'enabled': box_blur_enabled, 'kernel_size': box_kernel},
            'camera_shake': {'enabled': camera_shake_enabled, 'intensity': camera_intensity},
            'directional_shake': {'enabled': directional_shake_enabled, 'intensity': dir_intensity, 'direction': shake_direction},
            'motion_distortion': {'enabled': motion_distortion_enabled, 'direction': motion_direction, 'intensity': motion_intensity},
            'zoom_motion': {'enabled': zoom_motion_enabled, 'intensity': zoom_intensity}
        }
        
        # Check if any effects are enabled
        any_effect_enabled = any(effect_params.get('enabled', False) for effect_params in effects.values())
        
        # Action button
        process_full = st.sidebar.button("🎯 Process Full Quality", type="primary", disabled=not any_effect_enabled)
        
        # Real-time preview logic
        current_hash = hash_effects(effects)
        should_update = (
            (auto_preview or manual_refresh) and
            any_effect_enabled and
            (current_hash != st.session_state.glitch_last_hash or manual_refresh)
        )
        
        if should_update:
            try:
                preview_start = time.time()
                
                # Ensure original image is in the right format before preview processing
                if original_image.dtype != np.uint8:
                    preview_orig = np.clip(original_image, 0, 255).astype(np.uint8)
                else:
                    preview_orig = original_image
                
                # Resize for preview
                preview_image = PreviewManager.resize_for_preview(preview_orig, preview_mode)
                
                # Apply effects
                processed_preview = apply_imageglitch_effects(preview_image, effects)
                
                # Ensure preview is in the right format for display
                if processed_preview.dtype != np.uint8:
                    processed_preview = np.clip(processed_preview, 0, 255).astype(np.uint8)
                
                # Store in cache
                st.session_state.glitch_preview_cache[current_hash] = processed_preview.copy()
                st.session_state.glitch_last_hash = current_hash
                st.session_state.glitch_preview_time = time.time() - preview_start
                
            except Exception as e:
                st.sidebar.error(f"Preview failed: {str(e)}")
                processed_preview = None
        else:
            processed_preview = st.session_state.glitch_preview_cache.get(current_hash)
            
            # Ensure cached preview is in the right format
            if processed_preview is not None and processed_preview.dtype != np.uint8:
                processed_preview = np.clip(processed_preview, 0, 255).astype(np.uint8)
        
        # Process full quality
        if process_full and any_effect_enabled:
            with st.spinner("Processing full quality image..."):
                try:
                    # Ensure original image is in the right format before processing
                    if original_image.dtype != np.uint8:
                        original_image = np.clip(original_image, 0, 255).astype(np.uint8)
                    
                    # Apply effects to full quality image
                    full_processed = apply_imageglitch_effects(original_image, effects)
                    
                    # Ensure processed image is in the right format for storage
                    if full_processed.dtype != np.uint8:
                        full_processed = np.clip(full_processed, 0, 255).astype(np.uint8)
                    
                    # Store processed and original images in session state
                    st.session_state.glitch_processed_image = full_processed.copy()
                    st.session_state.glitch_original_image = original_image.copy()
                    st.session_state.glitch_effects_applied = [name.replace('_', ' ').title() 
                                                             for name, params in effects.items() 
                                                             if params.get('enabled', False)]
                except Exception as e:
                    st.error(f"Processing failed: {str(e)}")
        
        # Display images
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📷 Original Image")
            st.image(original_image, use_container_width=True)
        
        with col2:
            if any_effect_enabled and processed_preview is not None:
                st.subheader("🔴 Real-Time Preview")
                st.image(processed_preview, use_container_width=True)
                
                # Show preview stats
                if hasattr(st.session_state, 'glitch_preview_time'):
                    preview_ms = st.session_state.glitch_preview_time * 1000
                    st.caption(f"Preview: {preview_mode} | Time: {preview_ms:.1f}ms")
                
                # Show active effects
                active_effects = [name.replace('_', ' ').title() for name, params in effects.items() if params.get('enabled', False)]
                st.info(f"🔴 **Active effects:** {', '.join(active_effects)}")
                
            elif hasattr(st.session_state, 'glitch_processed_image'):
                st.subheader("✅ Processed Image")
                st.image(st.session_state.glitch_processed_image, use_container_width=True)
                st.success(f"✅ **Applied:** {', '.join(st.session_state.glitch_effects_applied)}")
            
            else:
                st.subheader("🎨 Glitch Effects Preview")
                if any_effect_enabled:
                    if auto_preview:
                        st.info("🔴 Real-time preview will appear here")
                    else:
                        st.info("👆 Click 'Refresh Preview' to see effects")
                else:
                    st.info("👆 Select effects to see preview")
        
        # Download section for ImageGlitch
        if hasattr(st.session_state, 'glitch_processed_image'):
            st.markdown("---")
            st.subheader("📥 Download Processed Image")
            
            col_dl1, col_dl2, col_dl3 = st.columns(3)
            
            # Ensure processed image is in the correct format before download
            processed_image = st.session_state.glitch_processed_image
            if processed_image.dtype != np.uint8:
                processed_image = np.clip(processed_image, 0, 255).astype(np.uint8)
            
            # Ensure original image is in the correct format before download
            original_image = st.session_state.glitch_original_image
            if original_image.dtype != np.uint8:
                original_image = np.clip(original_image, 0, 255).astype(np.uint8)
            
            with col_dl1:
                png_bytes = image_to_bytes(processed_image, 'PNG')
                st.download_button(
                    "📥 Download PNG",
                    data=png_bytes,
                    file_name="imageglitch_processed.png",
                    mime="image/png",
                    help="Download the processed image with all applied effects as PNG"
                )
            
            with col_dl2:
                jpg_bytes = image_to_bytes(processed_image, 'JPEG')
                st.download_button(
                    "📥 Download JPEG",
                    data=jpg_bytes,
                    file_name="imageglitch_processed.jpg",
                    mime="image/jpeg",
                    help="Download the processed image with all applied effects as JPEG"
                )
            
            with col_dl3:
                orig_bytes = image_to_bytes(original_image, 'PNG')
                st.download_button(
                    "📥 Download Original",
                    data=orig_bytes,
                    file_name="original_image.png",
                    mime="image/png",
                    help="Download the original unmodified image"
                )
    
    else:
        # Show effects information when no image is uploaded
        st.info("👆 Upload an image to start applying glitch effects")
        
        st.subheader("🎨 Available Glitch Effects")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔊 Noise Effects:**
            - **Gaussian Noise**: Random pixel variations for authentic glitch look
            - **Salt & Pepper**: Random white and black pixels for digital corruption
            
            **🌫️ Blur Effects:**
            - **Gaussian Blur**: Smooth blur for depth and focus effects
            - **Motion Blur**: Simulates camera movement during capture
            - **Box Blur**: Simple averaging blur for pixelated effects
            """)
        
        with col2:
            st.markdown("""
            **📳 Shake Effects:**
            - **Camera Shake**: Random small movements for handheld feel
            - **Directional Shake**: Movement in specific directions
            
            **🏃 Motion Effects:**
            - **Motion Distortion**: Directional blur for speed effects
            - **Zoom Motion**: Radial blur from center point
            
            **⚡ Extreme Mode:** Unlock high-intensity parameters for dramatic effects
            """)


def show_home_page():
    """
    Render the application home page with feature overview and navigation options.
    
    This function creates the landing page UI for the application, including:
    - Main title and application description
    - Two-column layout showcasing the main features:
      * Left column: AI Background Removal tool overview
        - Available AI models with descriptions
        - Professional features list
        - Download options
      * Right column: ImageGlitch tool overview
        - Available real-time effects
        - Live preview system features
        - Export options
    - Prominent navigation buttons with custom styling
    - System requirements and technical information
    
    The home page serves as the central hub for navigating between the two
    main tools while providing users with a clear overview of capabilities.
    """
    st.title("🎨 ImageGlitch & AI Background Removal Suite")
    st.markdown("### Professional image manipulation tools powered by AI and computer vision")
    
    # Feature overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ## ✂️ AI Background Removal
        
        **Advanced AI-powered background removal using state-of-the-art models:**
        
        🤖 **5 Specialized AI Models:**
        - U2-Net General (Best overall performance)
        - U2-Net Human (Optimized for people)
        - U2-Net Cloth (Fashion and apparel)
        - IS-Net General (High accuracy)
        - Silueta (Fast processing)
        
        🎯 **Professional Features:**
        - Transparent PNG output
        - Custom background colors
        - Multiple download formats
        - Model size optimization
        
        📥 **Download Options:**
        - PNG with transparency
        - JPEG with custom background
        - Original image backup
        """)
    
    with col2:
        st.markdown("""
        ## 🎨 ImageGlitch Tool
        
        **Real-time image manipulation with instant preview:**
        
        ⚡ **Real-Time Effects:**
        - Gaussian and Salt & Pepper noise
        - Motion blur and camera shake
        - Directional distortions
        - Zoom motion effects
        
        🔴 **Live Preview System:**
        - Instant feedback as you adjust parameters
        - 3 quality modes (Fast/Balanced/High Quality)
        - Smart caching for performance
        - Extreme mode for dramatic effects
        
        📥 **Export Options:**
        - High-resolution PNG/JPEG
        - Original image preservation
        - Multiple format support
        """)
    
    # Image Input section
    st.markdown("---")
    
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.markdown("""
        ### 📁 Upload an Image File
        
        Use drag-and-drop or browse to upload an image from your device.
        """)
    
    with col_input2:
        st.markdown("""
        ### 🌐 Enter an Image URL
        
        Paste an image URL to load an image from the internet.
        """)
    
    # Navigation buttons container - centered and side by side with custom styling
    st.markdown("""
    <style>
    .nav-button-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    .nav-button {
        background-color: #4F8BF9;
        border: none;
        color: white;
        padding: 15px 25px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        font-weight: bold;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .nav-button:hover {
        background-color: #3A66B7;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    </style>
    <div class="nav-button-container">
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        if st.button("🚀 Go to AI Background Removal", use_container_width=True, key="btn_bg_removal", help="Switch to the AI Background Removal tool"):
            st.session_state.page = "Background Removal"
            st.rerun()
    
    with col_btn2:
        if st.button("🚀 Go to ImageGlitch Tool", use_container_width=True, key="btn_imageglitch", help="Switch to the ImageGlitch tool"):
            st.session_state.page = "ImageGlitch"
            st.rerun()
            
    st.markdown("""</div>""", unsafe_allow_html=True)
    
    # Technical information
    st.markdown("---")
    st.subheader("🛠️ Technical Requirements")
    
    col_tech1, col_tech2 = st.columns(2)
    
    with col_tech1:
        st.markdown("""
        **Required Dependencies:**
        ```bash
        pip install streamlit opencv-python pillow numpy
        ```
        
        **For AI Background Removal:**
        ```bash
        pip install rembg
        ```
        
        **For GPU Acceleration (Optional):**
        ```bash
        pip install rembg[gpu]
        ```
        """)
    
    with col_tech2:
        st.markdown("""
        **System Requirements:**
        - Python 3.7+
        - 4GB+ RAM recommended
        - Internet connection for model downloads
        - GPU optional but recommended for large images
        
        **Model Downloads:**
        - Models download automatically on first use
        - Cached locally for future sessions
        - Total size: ~500MB for all models
        """)
    
    # Status indicators
    st.markdown("---")
    st.subheader("📊 System Status")
    
    col_status1, col_status2, col_status3 = st.columns(3)
    
    with col_status1:
        if REMBG_AVAILABLE:
            st.success("✅ **rembg Available**")
            st.caption("AI background removal ready")
        else:
            st.error("❌ **rembg Not Installed**")
            st.caption("Background removal unavailable")
    
    with col_status2:
        st.success("✅ **ImageGlitch Ready**")
        st.caption("Real-time effects available")
    
    with col_status3:
        st.info("📊 **Session Active**")
        st.caption("Cache and models ready")


def main():
    """
    Main application entry point that sets up the Streamlit interface and handles navigation.
    
    This function serves as the core controller for the application, responsible for:
    - Configuring the Streamlit page settings (title, icon, layout)
    - Initializing session state variables for persistent storage
    - Setting up the sidebar navigation system with page selection buttons
    - Displaying the current page indicator and system status information
    - Providing contextual quick tips based on the current page
    - Routing to the appropriate page function based on user selection
    - Rendering the application footer with credits
    
    The navigation system allows users to switch between three main views:
    1. Home page: Overview and feature showcase
    2. AI Background Removal: Tool for removing image backgrounds using AI
    3. ImageGlitch: Tool for applying various image manipulation effects
    
    The function also displays system status indicators for dependencies and
    loaded AI models to help users troubleshoot any issues.
    """
    st.set_page_config(
        page_title="ImageGlitch & AI Background Removal",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Page selection
    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    
    # Navigation in sidebar
    st.sidebar.title("🎨 Navigation")
    
    # Page buttons
    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()
    
    if st.sidebar.button("✂️ AI Background Removal", use_container_width=True):
        st.session_state.page = "Background Removal"
        st.rerun()
    
    if st.sidebar.button("🎨 ImageGlitch Tool", use_container_width=True):
        st.session_state.page = "ImageGlitch"
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Current page indicator
    st.sidebar.markdown(f"**Current Page:** {st.session_state.page}")
    
    # System status in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 System Status")
    
    if REMBG_AVAILABLE:
        st.sidebar.success("✅ rembg Available")
    else:
        st.sidebar.error("❌ rembg Missing")
        st.sidebar.caption("Install: `pip install rembg`")
    
    st.sidebar.success("✅ ImageGlitch Ready")
    
    # Model status
    if REMBG_AVAILABLE and st.session_state.bg_manager:
        loaded_models = sum(1 for model in BackgroundRemovalManager.MODELS.keys() 
                          if st.session_state.bg_manager.is_model_loaded(model))
        st.sidebar.info(f"📊 {loaded_models}/5 AI Models Loaded")
    
    st.sidebar.markdown("---")
    
    # Quick tips
    st.sidebar.subheader("💡 Quick Tips")
    if st.session_state.page == "Home":
        st.sidebar.info("Choose a tool from the navigation buttons above")
    elif st.session_state.page == "Background Removal":
        st.sidebar.info("Select the best AI model for your image type")
    elif st.session_state.page == "ImageGlitch":
        st.sidebar.info("Enable Auto Preview for real-time effects")
    
    # Route to appropriate page
    if st.session_state.page == "Home":
        show_home_page()
    elif st.session_state.page == "Background Removal":
        show_bg_removal_page()
    elif st.session_state.page == "ImageGlitch":
        show_imageglitch_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🎨 ImageGlitch & AI Background Removal Suite | 
        Built with Streamlit | 
        Powered by rembg and OpenCV</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()