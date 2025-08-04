# 🎨 ImageGlitch - AI-Powered Image Manipulation Suite

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![OpenCV](https://img.shields.io/badge/opencv-4.12+-green.svg)](https://opencv.org)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

> A comprehensive image processing suite combining AI-powered background removal with real-time glitch effects and artistic image manipulation.

## 🌟 Features

### ✂️ AI Background Removal
- **5 Specialized AI Models** - Choose the perfect model for your image type
- **Professional Output Options** - Transparent PNG, custom backgrounds, or white backgrounds
- **Multiple Model Support** - U2-Net, IS-Net, and Silueta models for different use cases
- **High-Quality Processing** - Preserve image details with advanced AI algorithms
- **Dual Input Support** - Upload files or paste image URLs directly (.jpg, .png, .webp, etc.)
- **Dynamic Model Loading** - Lazy loading with automatic memory management
- **Pre-bundled Model Support** - Optional local model storage for offline deployment

### 🎨 Real-Time Image Glitch Effects
- **Live Preview System** - See effects instantly as you adjust parameters
- **Multiple Effect Categories** - Noise, blur, shake, and motion effects
- **Extreme Mode** - Unlock high-intensity parameters for dramatic results
- **Smart Performance** - Intelligent caching and quality modes for smooth operation
- **Session State Optimization** - Persistent user experience with memory-efficient storage

### 🚀 Performance Optimizations
- **Memory Management** - Dynamic model loading prevents memory overflow
- **Intelligent Caching** - Preview cache system with hash-based optimization
- **Deployment Stability** - Enhanced error handling and logging for cloud environments
- **Session State Management** - Suppressed redundant logging and efficient state persistence
- **Garbage Collection** - Automatic cleanup of unused models and resources

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/binayakbartaula11/ImageGlitch.git
cd ImageGlitch
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **For AI Background Removal (optional but recommended):**
```bash
pip install rembg
```

4. **For GPU acceleration (optional):**
```bash
pip install rembg[gpu]
```

### Launch the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Deployment Options

#### Local Development
For local development with auto-reload:
```bash
streamlit run app.py --server.runOnSave true
```

#### Cloud Deployment (Streamlit Cloud/Heroku)
The application is optimized for cloud deployment with:
- **Automatic dependency management** - All required packages in requirements.txt
- **System library support** - packages.txt for system dependencies
- **Memory optimization** - Dynamic model loading prevents memory overflow
- **Error recovery** - Comprehensive logging for deployment diagnostics
- **Python 3.9 compatibility** - Specified in runtime.txt for maximum compatibility

#### Docker Deployment
For containerized deployment:
```dockerfile
# Use Python 3.9 for optimal compatibility
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . /app
WORKDIR /app

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 📚 Documentation

Comprehensive documentation is available to help you get the most out of ImageGlitch:

- **[📖 User Guide](docs/user-guide.md)** - Complete usage instructions and tutorials
- **[👨‍💻 Developer Guide](docs/developer-guide.md)** - Development setup and contribution guidelines
- **[🔧 API Reference](docs/api-reference.md)** - Technical API documentation
- **[⚙️ Configuration Guide](docs/configuration.md)** - Settings and customization options
- **[❓ FAQ & Troubleshooting](docs/faq.md)** - Common issues and solutions
- **[📝 Technical Whitepaper](WHITEPAPER.md)** - In-depth technical analysis and implementation details

For a complete overview of all available documentation, visit the **[docs directory](docs/)**.

## 📖 Quick Usage Guide

### AI Background Removal

1. **Load Your Image** - Two convenient input methods:
   - **📁 Upload File** - Drag-and-drop or browse (PNG, JPG, JPEG, BMP, TIFF)
   - **🌐 Paste URL** - Load images directly from web links (e.g., `https://example.com/image.jpg`)
2. **Select AI Model** - Choose from 5 specialized models based on your image type:
   - **U2-Net General** - Best for general photos with people and objects
   - **U2-Net Human** - Optimized for human portraits
   - **U2-Net Cloth** - Specialized for clothing and fashion items
   - **IS-Net General** - High accuracy for various subjects
   - **Silueta** - Fast processing with good quality
3. **Choose Output Format**:
   - 🔳 **Transparent** - RGBA with transparent background
   - ⬜ **White Background** - Clean white background
   - 🎨 **Custom Color** - Any color background of your choice
4. **Process and Download** - Multiple format options available

### ImageGlitch Effects

1. **Load Your Image** - Same dual input methods:
   - **📁 Upload File** - Drag-and-drop or browse for local files
   - **🌐 Paste URL** - Direct loading from image URLs
2. **Configure Real-Time Preview**:
   - **Auto Preview** - See effects instantly
   - **Quality Modes** - Fast, Balanced, or High Quality
   - **Extreme Mode** - Unlock maximum intensity parameters
3. **Apply Effects**:
   - **🔊 Noise Effects** - Gaussian and Salt & Pepper noise
   - **🌫️ Blur Effects** - Gaussian, Motion, and Box blur
   - **📳 Shake Effects** - Camera shake and directional movement
   - **🏃 Motion Effects** - Motion distortion and zoom blur
4. **Process Full Quality** - Generate high-resolution output
5. **Download Results** - PNG, JPEG, and original image options

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[OpenCV](https://opencv.org/)** - Computer vision and image processing
- **[PIL/Pillow](https://pillow.readthedocs.io/)** - Python Imaging Library
- **[NumPy](https://numpy.org/)** - Numerical computing
- **[rembg](https://github.com/danielgatis/rembg)** - AI background removal
- **[SciPy](https://scipy.org/)** - Scientific computing

## 📁 Project Structure

```
ImageGlitch/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── WHITEPAPER.md          # Technical whitepaper and implementation details
├── image_utils/           # Image processing utilities
│   ├── __init__.py        # Package initialization
│   ├── blur.py            # Blur effects (Gaussian, Motion, Box)
│   ├── noise.py           # Noise effects (Gaussian, Salt & Pepper)
│   ├── shaky.py           # Camera shake effects
│   └── motion.py          # Motion distortion effects
├── docs/                  # Comprehensive documentation
│   ├── README.md          # Documentation overview and navigation
│   ├── overview.md        # Project introduction and features
│   ├── getting-started.md # Installation and quick setup
│   ├── user-guide.md      # Complete usage instructions
│   ├── configuration.md   # Settings and customization
│   ├── developer-guide.md # Development and contribution guide
│   ├── api-reference.md   # Technical API documentation
│   ├── faq.md             # FAQ and troubleshooting
│   ├── deployment.md      # Guide for deploying the project in different environments
│   └── optimization.md    # Document detailing optimizations and performance tuning
│   └── changelog.md       # Version history and updates
├── screenshots/                                            # All visual assets and demo images
│   ├── background_removal_selected_bgcolor.png             # Background removed with selected color
│   ├── background_removal_selected_whitebackground.png     # Background removed with white
│   ├── mercedes-300-SL-imageglitch.png                     # ImageGlitch output (Mercedes 300SL)
├── .streamlit/           # Streamlit configuration files and deployment settings
│   ├── config.toml       # Streamlit config file
├── packages.txt          # List of required packages for the project (customized)
├── runtime.txt           # Environment and runtime specifications for deployment
└── README.md             # Main project overview
```

## 🔧 System Requirements

### Minimum Requirements
- **Python** 3.7 or higher
- **RAM** 4GB (8GB recommended for large images)
- **Storage** 1GB free space (for AI models)
- **Internet** Required for initial model downloads

### Recommended Specifications
- **Python** 3.9+
- **RAM** 8GB or more
- **GPU** NVIDIA GPU with CUDA support (optional, for acceleration)
- **Storage** 2GB free space

## 🎯 AI Model Information

| Model | Size | Best For | Description |
|-------|------|----------|-------------|
| **U2-Net General** | ~176MB | General purpose, portraits, objects | 🎯 Best overall performance for most images |
| **U2-Net Human** | ~176MB | Human portraits, people photos | 👤 Optimized for human segmentation |
| **U2-Net Cloth** | ~176MB | Fashion, clothing, apparel | 👕 Specialized for clothing items |
| **IS-Net General** | ~173MB | High-quality general purpose | 🌟 High accuracy for various subjects |
| **Silueta** | ~43MB | Quick processing | ⚡ Fast processing, good for most images |

## 🎨 Effect Categories

### Noise Effects
- **Gaussian Noise** - Adds natural-looking sensor noise for authentic glitch effects
- **Salt & Pepper Noise** - Creates random white and black pixels for digital corruption simulation

### Blur Effects
- **Gaussian Blur** - Smooth, natural blur for depth and focus effects
- **Motion Blur** - Directional blur simulating camera or subject movement
- **Box Blur** - Uniform averaging blur for pixelated effects

### Shake Effects
- **Camera Shake** - Random movement simulation for handheld camera feel
- **Directional Shake** - Controlled movement in specific directions

### Motion Effects
- **Motion Distortion** - Directional streaking for speed and movement simulation
- **Zoom Motion** - Radial blur from center point for dramatic zoom effects

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to your branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings for new functions
- Test your changes with various image types
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤖 Acknowledgments
This project would not have reached peak glitchiness without Claude, Warp, and Trae. Their involvement was... experimental at best, chaotic at worst — but hey, we made it! Without them, this would have just been a "mildly pixelated inconvenience" generator. Thanks (I guess?).

## 🌟 Technical Acknowledgments

- **[rembg](https://github.com/danielgatis/rembg)** - Excellent AI background removal library
- **[Streamlit](https://streamlit.io/)** - Amazing framework for rapid web app development
- **[OpenCV](https://opencv.org/)** - Comprehensive computer vision library
- **U2-Net, IS-Net, Silueta models** - Powerful AI models for background segmentation

## 🚀 Deployment and Performance

### Cloud Deployment Configuration
ImageGlitch includes optimized configuration files for seamless deployment:

- **runtime.txt**: Specifies Python 3.9.18 for maximum compatibility
- **packages.txt**: System dependencies for OpenCV and image processing
- **.streamlit/config.toml**: Streamlit-specific deployment settings
- **requirements.txt**: Pinned Python package versions

### Performance Optimization Features
- **Dynamic Model Loading**: Only one AI model loaded at a time to prevent memory overflow
- **Intelligent Caching**: Hash-based preview system reduces redundant processing
- **Session State Management**: Optimized for Streamlit to prevent memory bloat
- **Automatic Garbage Collection**: Explicit cleanup of unused models and resources

### Performance Tips
- Use **Fast preview mode** for real-time adjustments
- Enable **Auto Preview** for immediate feedback
- Process **full quality** only when satisfied with preview
- Use **GPU acceleration** if available (install `rembg[gpu]`)
- Monitor system memory usage during processing

## 🐛 Troubleshooting

### Installation Issues

**"rembg library not installed"**
```bash
pip install rembg
```

**System library missing (Linux/WSL)**
```bash
sudo apt-get install libgl1-mesa-glx libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1
```

### Performance Issues

**Out of memory errors**
- Reduce image size before processing
- Use Fast preview mode
- Close other applications to free RAM
- Only one AI model loads at a time (memory optimization)

**Slow processing**
- Update to latest versions of dependencies
- Use GPU acceleration if available
- Reduce preview quality for faster feedback
- Use Silueta model for fastest processing

### Deployment Issues

**Cloud deployment failures**
- Ensure Python 3.9.18 specified in runtime.txt
- Verify all system packages listed in packages.txt
- Check .streamlit/config.toml for proper settings
- Review deployment logs for specific error messages

## 📚 Additional Resources

- **[📝 Technical Whitepaper](WHITEPAPER.md)** - Deep dive into implementation details and algorithms
- **[📖 Complete Documentation](docs/)** - User guides, API reference, and developer resources
- **[🚀 Getting Started Guide](docs/getting-started.md)** - Quick setup and first steps
- **[🌍 Deployment Guide](docs/deployment.md)** - Cloud, Docker, and platform deployment instructions
- **[⚡ Optimization Guide](docs/optimization.md)** - Performance tuning and memory management

## 📧 Contact & Support

- **Repository**: [github.com/binayakbartaula11/ImageGlitch](https://github.com/binayakbartaula11/ImageGlitch)
- **Issues**: [Report bugs or request features](https://github.com/binayakbartaula11/ImageGlitch/issues)
- **Discussions**: [Ask questions and share ideas](https://github.com/binayakbartaula11/ImageGlitch/discussions)

---

