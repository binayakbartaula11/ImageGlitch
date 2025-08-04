# 🚀 Deployment Guide

## Overview

ImageGlitch is designed for easy deployment across various environments, from local development to cloud platforms. This guide covers deployment strategies, optimization techniques, and troubleshooting for different scenarios.

## 🏠 Local Development

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/binayakbartaula11/ImageGlitch.git
cd ImageGlitch

# Install dependencies
pip install -r requirements.txt

# Launch application
streamlit run app.py
```

### Development Mode

For active development with auto-reload:

```bash
streamlit run app.py --server.runOnSave true
```

### Environment Configuration

Create a `.env` file for local configuration:

```env
# Model storage path (optional)
U2NET_HOME=/path/to/models

# Debug mode
DEBUG=true

# GPU acceleration (if available)
CUDA_VISIBLE_DEVICES=0
```

## ☁️ Cloud Deployment

### Streamlit Cloud

ImageGlitch is optimized for Streamlit Cloud deployment with the following files:

**requirements.txt**:
```
streamlit==1.47.1
rembg==2.0.67
numpy==2.2.6
pillow==11.3.0
opencv-python-headless==4.12.0.88
scikit-image==0.25.2
tqdm==4.67.1
numba==0.61.2
llvmlite==0.44.0
onnxruntime==1.20.1
requests==2.31.0
urllib3==2.0.7
```

**packages.txt**:
```
libgl1-mesa-glx
libgl1
libglib2.0-0
libsm6
libxext6
libxrender-dev
libgomp1
```

**runtime.txt**:
```
python-3.9.18
```

### Deployment Optimizations

1. **Memory Management**: Dynamic model loading prevents memory overflow
2. **System Dependencies**: All required libraries specified in packages.txt
3. **Python Compatibility**: Python 3.9 for optimal package compatibility
4. **Error Recovery**: Comprehensive logging for deployment diagnostics

### Deployment Checklist

- [ ] All dependencies listed in requirements.txt
- [ ] System packages specified in packages.txt
- [ ] Python version set in runtime.txt
- [ ] No hardcoded file paths
- [ ] Error handling for missing dependencies
- [ ] Memory optimization enabled
- [ ] Logging configured for production

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
# Use Python 3.9 for optimal compatibility
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directory for model storage
RUN mkdir -p /tmp/u2net_models

# Set environment variables
ENV U2NET_HOME=/tmp/u2net_models
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  imageglitch:
    build: .
    ports:
      - "8501:8501"
    environment:
      - U2NET_HOME=/tmp/u2net_models
      - STREAMLIT_SERVER_HEADLESS=true
    volumes:
      - model_cache:/tmp/u2net_models
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  model_cache:
```

### Building and Running

```bash
# Build the image
docker build -t imageglitch .

# Run the container
docker run -p 8501:8501 imageglitch

# Or use docker-compose
docker-compose up -d
```

## 🌐 Heroku Deployment

### Setup Files

**Procfile**:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt**:
```
python-3.9.18
```

**Aptfile**:
```
libgl1-mesa-glx
libglib2.0-0
libsm6
libxext6
libxrender-dev
libgomp1
```

### Deployment Commands

```bash
# Create Heroku app
heroku create your-app-name

# Add buildpacks
heroku buildpacks:add --index 1 heroku-community/apt
heroku buildpacks:add --index 2 heroku/python

# Set environment variables
heroku config:set U2NET_HOME=/tmp/u2net_models

# Deploy
git push heroku main
```

## 🔧 Environment-Specific Configurations

### Memory-Constrained Environments

For environments with limited memory (< 4GB):

```python
# In app.py - add memory optimization
import gc

# Force garbage collection after model operations
def cleanup_memory():
    gc.collect()
    if hasattr(gc, 'set_threshold'):
        gc.set_threshold(700, 10, 10)  # More aggressive GC
```

### GPU-Enabled Environments

For environments with GPU support:

```bash
# Install GPU-accelerated packages
pip install rembg[gpu]
pip install onnxruntime-gpu

# Set CUDA environment
export CUDA_VISIBLE_DEVICES=0
```

### Offline Deployment

For environments without internet access:

1. **Pre-bundle Models**: Download models locally and include in deployment
2. **Model Directory Structure**:
   ```
   models/
   ├── u2net.onnx
   ├── u2net_human_seg.onnx
   ├── u2net_cloth_seg.onnx
   ├── isnet-general-use.onnx
   └── silueta.onnx
   ```

3. **Configuration**:
   ```python
   # Set local model path
   os.environ["U2NET_HOME"] = "./models"
   ```

## 📊 Performance Tuning

### Memory Optimization

```python
# Configuration for different deployment tiers
DEPLOYMENT_CONFIGS = {
    'basic': {
        'max_preview_size': 300,
        'cache_size': 10,
        'models_to_load': ['silueta']  # Smallest model only
    },
    'standard': {
        'max_preview_size': 500,
        'cache_size': 20,
        'models_to_load': ['silueta', 'u2net']
    },
    'premium': {
        'max_preview_size': 800,
        'cache_size': 50,
        'models_to_load': 'all'
    }
}
```

### Resource Monitoring

Add monitoring for production deployments:

```python
import psutil
import logging

def log_system_stats():
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent()
    
    logging.info(f"Memory usage: {memory.percent}%")
    logging.info(f"CPU usage: {cpu}%")
    
    if memory.percent > 85:
        logging.warning("High memory usage detected")
```

## 🔍 Troubleshooting Deployment Issues

### Common Issues and Solutions

#### 1. Memory Errors (Out of Memory)

**Symptoms**:
- Application crashes during model loading
- Deployment fails with memory-related errors

**Solutions**:
```python
# Enable memory optimization
os.environ["OPENCV_OPENCL_DEVICE"] = "disabled"  # Disable OpenCL
os.environ["NUMBA_DISABLE_JIT"] = "1"  # Disable Numba JIT compilation

# Use headless OpenCV
# In requirements.txt: opencv-python-headless instead of opencv-python
```

#### 2. Import Errors (Missing Dependencies)

**Symptoms**:
- `ImportError: libGL.so.1: cannot open shared object file`
- `ModuleNotFoundError: No module named 'onnxruntime'`

**Solutions**:
```bash
# For libGL errors - add to packages.txt or install system packages
libgl1-mesa-glx
libglib2.0-0

# For onnxruntime - ensure it's in requirements.txt
onnxruntime==1.20.1
```

#### 3. Model Loading Failures

**Symptoms**:
- Models fail to download or load
- Network timeouts during model initialization

**Solutions**:
```python
# Add retry logic for model loading
def load_model_with_retry(model_name, max_retries=3):
    for attempt in range(max_retries):
        try:
            return new_session(model_name)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt)  # Exponential backoff
```

#### 4. Performance Issues

**Symptoms**:
- Slow preview generation
- High memory usage
- Frequent timeouts

**Solutions**:
```python
# Optimize for deployment environment
if os.environ.get('STREAMLIT_SERVER_HEADLESS'):
    # Production optimizations
    PREVIEW_MODE = "Fast"  # Force fast preview
    MAX_CACHE_SIZE = 10    # Limit cache size
    GC_FREQUENCY = 5       # More frequent garbage collection
```

### Debug Mode

Enable debug mode for deployment troubleshooting:

```python
# Add debug logging
if os.environ.get('DEBUG', 'false').lower() == 'true':
    logging.basicConfig(level=logging.DEBUG)
    st.write("Debug mode enabled")
    
    # Show system information
    st.write(f"Python version: {sys.version}")
    st.write(f"Available memory: {psutil.virtual_memory().available / 1024 / 1024:.1f} MB")
    st.write(f"CPU count: {psutil.cpu_count()}")
```

## 📈 Deployment Monitoring

### Health Checks

Implement health checks for monitoring:

```python
def health_check():
    """Check system health for monitoring"""
    checks = {
        'memory_ok': psutil.virtual_memory().percent < 90,
        'imports_ok': True,
        'models_accessible': os.path.exists(os.environ.get('U2NET_HOME', '/tmp')),
    }
    
    try:
        import rembg
        checks['rembg_available'] = True
    except ImportError:
        checks['rembg_available'] = False
        checks['imports_ok'] = False
    
    return all(checks.values()), checks
```

### Metrics Collection

For production monitoring:

```python
# Add metrics endpoint
@st.cache_data
def get_app_metrics():
    return {
        'uptime': time.time() - start_time,
        'processed_images': st.session_state.get('processed_count', 0),
        'cache_hit_rate': calculate_cache_hit_rate(),
        'memory_usage': psutil.virtual_memory().percent,
        'models_loaded': len(st.session_state.bg_manager.sessions)
    }
```

## 🔐 Security Considerations

### Input Validation

```python
def validate_image_input(uploaded_file):
    """Validate uploaded image files"""
    if not uploaded_file:
        return False, "No file uploaded"
    
    # Check file size (limit to 10MB)
    if uploaded_file.size > 10 * 1024 * 1024:
        return False, "File too large (max 10MB)"
    
    # Check file type
    allowed_types = ['image/jpeg', 'image/png', 'image/bmp', 'image/tiff']
    if uploaded_file.type not in allowed_types:
        return False, "Invalid file type"
    
    return True, "Valid file"
```

### Environment Variables

Secure configuration management:

```python
# Use environment variables for sensitive config
MODEL_STORAGE_PATH = os.environ.get('U2NET_HOME', '/tmp/u2net_models')
DEBUG_MODE = os.environ.get('DEBUG', 'false').lower() == 'true'
MAX_UPLOAD_SIZE = int(os.environ.get('MAX_UPLOAD_SIZE_MB', '10'))
```

---

*For more deployment examples and advanced configurations, see the [GitHub repository](https://github.com/binayakbartaula11/ImageGlitch).*
