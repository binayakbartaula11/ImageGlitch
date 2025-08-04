# ⚙️ Configuration

## Overview

ImageGlitch uses intelligent defaults and runtime configuration to provide optimal performance across different hardware setups. This guide covers all available configuration options and customization possibilities.

## 🔧 Application Settings

### Preview Quality Modes

Configure real-time preview performance based on your hardware:

```python
PREVIEW_MODES = {
    "Fast": {
        "max_size": 300,
        "quality": 75,
        "description": "⚡ Fast preview (300px max)"
    },
    "Balanced": {
        "max_size": 500, 
        "quality": 85,
        "description": "⚖️ Balanced quality (500px max)"
    },
    "High Quality": {
        "max_size": 800,
        "quality": 95,
        "description": "🎯 High quality (800px max)"
    }
}
```

**Customization**: Edit these values in `app.py` under the `PreviewManager` class to adjust:
- `max_size`: Maximum image dimension for preview
- `quality`: JPEG compression quality (1-100)
- `description`: UI display text

### AI Model Configuration

Available AI models and their settings:

```python
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
    # ... additional models
}
```

**Model Priority**: Models are loaded in the order specified. To change default model, modify the `model_options` list order.

## 🎨 Effect Parameters

### Default Parameter Ranges

#### Normal Mode Parameters
```python
# Noise Effects
GAUSSIAN_NOISE_RANGE = (0.0, 0.1)
SALT_PEPPER_RANGE = (0.0, 0.1)

# Blur Effects  
GAUSSIAN_BLUR_RANGE = (3, 15)  # odd numbers only
MOTION_BLUR_DEGREE_RANGE = (1, 30)
BOX_BLUR_RANGE = (3, 15)  # odd numbers only

# Shake Effects
CAMERA_SHAKE_RANGE = (1, 10)
DIRECTIONAL_SHAKE_RANGE = (1, 10)

# Motion Effects
MOTION_DISTORTION_RANGE = (1, 20)
ZOOM_MOTION_RANGE = (1, 10)
```

#### Extreme Mode Parameters  
```python
# Noise Effects (Extreme)
GAUSSIAN_NOISE_EXTREME = (0.0, 5.0)
SALT_PEPPER_EXTREME = (0.0, 1.0)

# Blur Effects (Extreme)
GAUSSIAN_BLUR_EXTREME = (3, 101)
MOTION_BLUR_EXTREME = (1, 100)
BOX_BLUR_EXTREME = (3, 101)

# Shake Effects (Extreme)
CAMERA_SHAKE_EXTREME = (1, 50)
DIRECTIONAL_SHAKE_EXTREME = (1, 50)

# Motion Effects (Extreme)
MOTION_DISTORTION_EXTREME = (1, 100)
ZOOM_MOTION_EXTREME = (1, 50)
```

**Customization**: Modify these ranges in the `show_imageglitch_page()` function to adjust slider bounds.

## 💾 Session State Configuration

### Cache Settings

```python
# Preview cache configuration
CACHE_MAX_SIZE = 100  # Maximum cached previews
CACHE_CLEANUP_THRESHOLD = 150  # Trigger cleanup at this size

# Model cache settings
MODEL_TIMEOUT = 3600  # Model session timeout (seconds)
AUTO_CLEANUP = True   # Automatic memory cleanup
```

### Performance Thresholds

```python
# Processing time thresholds (milliseconds)
FAST_PREVIEW_THRESHOLD = 100
WARNING_THRESHOLD = 500
TIMEOUT_THRESHOLD = 5000

# Memory usage limits
MAX_PREVIEW_MEMORY = 200  # MB
MAX_MODEL_MEMORY = 2048   # MB
```

## 🌐 Environment Variables

Set these environment variables to customize behavior:

### Model Download Configuration
```bash
# Custom model cache directory
export REMBG_HOME="/path/to/model/cache"

# Disable GPU acceleration
export CUDA_VISIBLE_DEVICES=""

# Custom download timeout
export MODEL_DOWNLOAD_TIMEOUT=300
```

### Performance Tuning
```bash
# Number of processing threads
export OPENCV_NUM_THREADS=4

# Memory optimization
export OMP_NUM_THREADS=2
export NUMBA_NUM_THREADS=2
```

### Development Settings
```bash
# Enable debug mode
export IMAGEGLITCH_DEBUG=true

# Custom log level
export LOG_LEVEL=INFO

# Disable caching for development
export DISABLE_CACHE=true
```

## 📁 File Format Configuration

### Supported Input Formats
```python
SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg', 'bmp', 'tiff']
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit
```

### Output Quality Settings
```python
# JPEG output quality
JPEG_QUALITY = 95

# PNG compression level (0-9)
PNG_COMPRESSION = 6

# Default output format
DEFAULT_OUTPUT_FORMAT = 'PNG'
```

## 🎯 UI Customization

### Theme Configuration

Create a custom theme by modifying Streamlit configuration:

```toml
# .streamlit/config.toml
[theme]
primaryColor = "#4F8BF9"
backgroundColor = "#FFFFFF" 
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Page Layout Settings
```python
# Page configuration
PAGE_CONFIG = {
    "page_title": "ImageGlitch & AI Background Removal",
    "page_icon": "🎨",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}
```

### Custom CSS Styling
```css
/* Custom styles in main app */
.nav-button {
    background-color: #4F8BF9;
    border-radius: 8px;
    padding: 15px 25px;
    transition: all 0.3s ease;
}

.nav-button:hover {
    background-color: #3A66B7;
    transform: translateY(-2px);
}
```

## 🔒 Security Configuration

### File Upload Security
```python
# Allowed file extensions
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff'}

# Maximum file size (bytes)
MAX_UPLOAD_SIZE = 50 * 1024 * 1024

# Enable file type validation
VALIDATE_FILE_TYPE = True

# Scan uploads for malicious content
ENABLE_SECURITY_SCAN = False
```

### Privacy Settings
```python
# Disable telemetry
DISABLE_TELEMETRY = True

# Local processing only
CLOUD_PROCESSING = False

# Automatic file cleanup
AUTO_DELETE_UPLOADS = True
CLEANUP_INTERVAL = 3600  # seconds
```

## 📊 Performance Configuration

### Memory Management
```python
# Garbage collection settings
GC_THRESHOLD = (700, 10, 10)
AUTO_GC_ENABLED = True

# Memory limits per process
MAX_MEMORY_USAGE = 4096  # MB
MEMORY_WARNING_THRESHOLD = 3072  # MB
```

### Processing Optimization
```python
# Image processing settings
USE_MULTITHREADING = True
MAX_WORKER_THREADS = 4

# AI model optimization
ENABLE_MODEL_QUANTIZATION = False
USE_GPU_ACCELERATION = True
MIXED_PRECISION = False
```

## 🔄 Backup and Recovery

### Automatic Backups
```python
# Enable automatic backups
AUTO_BACKUP = True
BACKUP_INTERVAL = 3600  # seconds
MAX_BACKUPS = 10

# Backup location
BACKUP_DIRECTORY = "./backups/"
```

### Recovery Settings
```python
# Crash recovery
ENABLE_CRASH_RECOVERY = True
RECOVERY_FILE = ".imageglitch_recovery"

# Session restoration
RESTORE_SESSION = True
SESSION_TIMEOUT = 7200  # seconds
```

## 🛠️ Custom Configuration File

Create a `config.yaml` file for persistent settings:

```yaml
# config.yaml
application:
  name: "ImageGlitch"
  version: "1.0.0"
  debug: false

preview:
  default_quality: "Balanced"
  cache_size: 100
  auto_preview: true

models:
  default_model: "u2net"
  auto_download: true
  cache_directory: "./models/"

effects:
  extreme_mode_default: false
  processing_threads: 4

output:
  default_format: "PNG"
  quality: 95
  preserve_originals: true

performance:
  memory_limit: 4096
  gc_threshold: 0.8
  timeout: 30
```

### Loading Custom Configuration
```python
import yaml

def load_config():
    try:
        with open('config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return get_default_config()

config = load_config()
```

## 🔧 Advanced Customization

### Adding Custom Effects

1. **Create effect module**:
```python
# image_utils/custom_effect.py
def apply_custom_effect(image, parameter1=1.0, parameter2=True):
    """Your custom effect implementation"""
    result = image.copy().astype(np.float32)
    # Custom processing here
    return result
```

2. **Register effect**:
```python
# Add to effects dictionary
custom_effects = {
    'custom_effect': {
        'enabled': False,
        'parameter1': 1.0,
        'parameter2': True
    }
}
```

3. **Add UI controls**:
```python
# Add slider controls in sidebar
custom_enabled = st.sidebar.checkbox("Custom Effect")
if custom_enabled:
    param1 = st.sidebar.slider("Parameter 1", 0.0, 2.0, 1.0)
    param2 = st.sidebar.checkbox("Parameter 2", True)
```

### Custom AI Models

To add support for additional AI models:

1. **Add model definition**:
```python
CUSTOM_MODELS = {
    "custom_model": {
        "name": "Custom Model",
        "description": "Custom segmentation model",
        "suitable_for": "Specific use case",
        "size": "~XXXmb"
    }
}
```

2. **Implement model loading**:
```python
def load_custom_model(model_path):
    # Custom model loading logic
    return model_session
```

## 🔍 Debugging Configuration

### Debug Mode Settings
```python
# Enable comprehensive logging
DEBUG_MODE = True
LOG_LEVEL = "DEBUG"
LOG_FILE = "imageglitch_debug.log"

# Performance profiling
ENABLE_PROFILING = True
PROFILE_OUTPUT = "performance_profile.json"

# Memory tracking
TRACK_MEMORY = True
MEMORY_LOG = "memory_usage.log"
```

### Diagnostic Tools
```python
# System information logging
LOG_SYSTEM_INFO = True
LOG_MODEL_INFO = True
LOG_PERFORMANCE_METRICS = True

# Error reporting
DETAILED_ERROR_MESSAGES = True
STACK_TRACE_IN_UI = False  # Security consideration
```

---

*Next: [Developer Guide →](developer-guide.md)*
