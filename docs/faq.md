# ❓ FAQ & Troubleshooting

## 🤔 Frequently Asked Questions

### General Questions

#### Q: What is ImageGlitch?
**A:** ImageGlitch is an open-source image processing suite that combines AI-powered background removal with real-time creative effects. It offers 5 specialized AI models for background segmentation and multiple categories of visual effects.

#### Q: Is ImageGlitch free to use?
**A:** Yes! ImageGlitch is completely free and open-source. There are no subscription fees, usage limits, or hidden costs.

#### Q: Do I need an internet connection to use ImageGlitch?
**A:** You need an internet connection only for the initial download of AI models (first-time setup). After that, all processing happens locally on your machine.

#### Q: Is my data safe? Are images uploaded to the cloud?
**A:** Absolutely safe! All image processing happens locally on your computer. No images are uploaded to any servers or cloud services.

### Installation & Setup

#### Q: What are the system requirements?
**A:** 
- **Minimum**: Python 3.7+, 4GB RAM, 1GB storage
- **Recommended**: Python 3.9+, 8GB+ RAM, NVIDIA GPU with CUDA support, 2GB+ storage

#### Q: How do I install ImageGlitch?
**A:** 
```bash
git clone https://github.com/binayakbartaula11/ImageGlitch.git
cd ImageGlitch
pip install -r requirements.txt
streamlit run app.py
```

#### Q: Can I run ImageGlitch without GPU?
**A:** Yes! ImageGlitch works on CPU-only systems. GPU acceleration is optional and only speeds up AI background removal.

### AI Background Removal

#### Q: Which AI model should I choose?
**A:**
- **U2-Net General**: Best for most images (default choice)
- **U2-Net Human**: Use for portraits and people photos
- **U2-Net Cloth**: Best for fashion and clothing items
- **IS-Net General**: Highest quality, slower processing
- **Silueta**: Fastest processing, good quality

#### Q: Why are models downloading automatically?
**A:** AI models are downloaded on first use to save storage space and bandwidth. This is a one-time process per model.

#### Q: Can I use custom AI models?
**A:** Currently, ImageGlitch supports the built-in models from the rembg library. Custom model support is planned for future releases.

#### Q: How accurate is the background removal?
**A:** Accuracy depends on image quality, lighting, and contrast. The specialized models (Human, Cloth) typically perform better for their specific use cases.

### Creative Effects

#### Q: What's the difference between Normal and Extreme Mode?
**A:**
- **Normal Mode**: Safe parameter ranges suitable for most users
- **Extreme Mode**: Extended ranges for dramatic effects and professional use

#### Q: Can I combine multiple effects?
**A:** Yes! You can enable multiple effects simultaneously. They're applied in a specific order: Noise → Blur → Shake → Motion.

#### Q: Why do effects process in real-time for preview but not full quality?
**A:** Real-time previews use smaller, optimized images. Full quality processing uses your original image resolution and may take longer.

#### Q: Can I save effect presets?
**A:** Effect presets aren't currently saved between sessions, but this feature is planned for future releases.

### Performance & Quality

#### Q: The application is running slowly. How can I improve performance?
**A:**
- Use "Fast" preview mode
- Close other applications to free RAM
- Use smaller images for testing
- Enable GPU acceleration if available
- Use the Silueta model for faster background removal

#### Q: Why does preview quality differ from final output?
**A:** Previews are optimized for speed using smaller image sizes and compression. Final processing uses your full-resolution image.

#### Q: How much RAM does ImageGlitch use?
**A:** RAM usage varies by image size and active effects:
- Base application: ~200MB
- AI models: 1.4GB - 2.3GB each (when loaded)
- Image processing: Depends on image size

### File Formats & Output

#### Q: What image formats are supported?
**A:** 
- **Input**: PNG, JPG, JPEG, BMP, TIFF
- **Output**: PNG (with transparency), JPEG

#### Q: Why can't I download JPEG with transparent background?
**A:** JPEG format doesn't support transparency. Use PNG for transparent backgrounds.

#### Q: What's the maximum file size I can upload?
**A:** The default limit is 50MB. You can modify this in the configuration if needed.

#### Q: Can I batch process multiple images?
**A:** Batch processing isn't currently available in the UI but can be implemented programmatically using the API functions.

## 🔧 Troubleshooting

### Installation Issues

#### "rembg library not installed"
**Problem**: AI background removal features are unavailable.

**Solution**:
```bash
pip install rembg
```

For GPU acceleration:
```bash
pip install rembg[gpu]
```

#### "ModuleNotFoundError: No module named 'streamlit'"
**Problem**: Required dependencies not installed.

**Solution**:
```bash
pip install -r requirements.txt
```

#### Permission errors during installation
**Problem**: Insufficient permissions to install packages.

**Solution**:
- Use virtual environment: `python -m venv venv`
- Install with user flag: `pip install --user -r requirements.txt`
- Run as administrator (Windows) or use `sudo` (Linux/Mac)

### Runtime Errors

#### "Failed to load model 'model_name'"
**Problem**: AI model download or loading failed.

**Solutions**:
1. Check internet connection
2. Retry - sometimes downloads timeout
3. Clear model cache: Delete `~/.u2net/` directory
4. Check available disk space

#### "Out of memory" errors
**Problem**: Insufficient RAM for processing.

**Solutions**:
1. Close other applications
2. Use smaller images
3. Use "Fast" preview mode
4. Restart the application
5. Process one effect at a time

#### Application freezes or becomes unresponsive
**Problem**: Processing taking too long or system overload.

**Solutions**:
1. Wait for processing to complete
2. Reduce image size
3. Disable some effects
4. Restart the application
5. Check system resources

#### "Preview failed" errors
**Problem**: Error during real-time preview generation.

**Solutions**:
1. Try different preview quality mode
2. Disable auto preview temporarily
3. Check image format compatibility
4. Restart the application

### Performance Issues

#### Slow processing speed
**Solutions**:
1. **Use GPU acceleration**: Install `rembg[gpu]`
2. **Optimize preview settings**: Use "Fast" mode
3. **Close other applications**: Free up system resources
4. **Use appropriate models**: Silueta for speed, U2-Net for quality
5. **Reduce image size**: Scale down large images

#### High memory usage
**Solutions**:
1. **Monitor usage**: Check Task Manager/Activity Monitor
2. **Restart application**: Clear accumulated cache
3. **Process smaller images**: Reduce memory requirements
4. **Limit simultaneous effects**: Process one category at a time

#### Browser loading issues
**Solutions**:
1. **Clear browser cache**: Refresh the page
2. **Try different browser**: Chrome, Firefox, Edge
3. **Check port availability**: Default is 8501
4. **Restart Streamlit**: `Ctrl+C` then `streamlit run app.py`

### UI/UX Issues

#### Interface not loading properly
**Solutions**:
1. **Refresh browser**: `F5` or `Ctrl+R`
2. **Clear browser cache**: Hard refresh `Ctrl+Shift+R`
3. **Check console errors**: Press `F12` to open developer tools
4. **Try incognito mode**: Bypass cache issues

#### Sliders not responding
**Solutions**:
1. **Refresh the page**
2. **Check browser compatibility**
3. **Disable browser extensions**: They might interfere
4. **Try different browser**

#### Images not displaying
**Solutions**:
1. **Check file format**: Ensure it's supported
2. **Verify file size**: Must be under 50MB
3. **Try different image**: Test with known good image
4. **Check browser permissions**: Allow file access

### Model-Specific Issues

#### U2-Net models not working
**Problem**: Specific model fails to load or process.

**Solutions**:
1. **Clear model cache**: Delete model files and re-download
2. **Check available space**: Models are 170-200MB each
3. **Verify rembg version**: Update to latest version
4. **Try different model**: Use Silueta as fallback

#### Inconsistent results between models
**Explanation**: Different models are trained for different purposes and will produce varying results.

**Best Practices**:
- Use U2-Net Human for people
- Use U2-Net Cloth for fashion
- Use IS-Net for highest quality
- Use Silueta for speed

## 🔍 Diagnostic Information

### Getting System Information

To help with troubleshooting, gather this information:

#### Python Environment
```bash
python --version
pip list | grep -E "(streamlit|opencv|numpy|pillow|rembg)"
```

#### System Resources
- Available RAM
- Free disk space
- GPU information (if using CUDA)

#### Error Logs
Check the Streamlit console output for detailed error messages.

### Reporting Issues

When reporting bugs, please include:

1. **System information**: OS, Python version, GPU info
2. **Error messages**: Complete error text from console
3. **Steps to reproduce**: Detailed reproduction steps
4. **Expected vs actual behavior**: What should happen vs what happens
5. **Screenshots**: If UI-related issue

## 📚 Additional Resources

### Community Support
- **GitHub Issues**: [Report bugs and request features](https://github.com/binayakbartaula11/ImageGlitch/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/binayakbartaula11/ImageGlitch/discussions)

### Documentation
- **User Guide**: Detailed usage instructions
- **Developer Guide**: For contributors and developers
- **API Reference**: Technical documentation

### External Resources
- **Streamlit Documentation**: https://docs.streamlit.io/
- **OpenCV Documentation**: https://docs.opencv.org/
- **rembg Library**: https://github.com/danielgatis/rembg

## 🔄 Staying Updated

### Getting Updates
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Version Information
Check the current version in the application footer or:
```bash
git log --oneline -1
```

### Release Notes
See [Changelog](changelog.md) for version history and new features.

---

*Need more help? Check our [GitHub Discussions](https://github.com/binayakbartaula11/ImageGlitch/discussions) or [open an issue](https://github.com/binayakbartaula11/ImageGlitch/issues).*

---

*Next: [Changelog →](changelog.md)*
