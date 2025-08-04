# 📖 User Guide

This comprehensive guide will walk you through every feature of ImageGlitch, from basic background removal to advanced creative effects.

## 🎯 Interface Overview

### Main Navigation

ImageGlitch features a clean, three-page interface:

1. **🏠 Home** - Overview and navigation hub
2. **✂️ AI Background Removal** - Professional background removal tools
3. **🎨 ImageGlitch Tool** - Real-time creative effects

### Sidebar Controls

The sidebar contains all interactive controls:
- File upload area
- Tool-specific settings
- Parameter sliders
- Action buttons
- System status indicators

## ✂️ AI Background Removal

### Step 1: Load Your Image

1. **Choose Input Method** in the sidebar:
   - **📁 Upload File** for local files
   - **🌐 Paste URL** for direct web links (e.g., `https://example.com/image.jpg`)
2. **Supported Formats**: PNG, JPG, JPEG, BMP, TIFF, WEBP
3. **Feedback and Validation**:
   - **Success indicator** for valid URLs
   - **Error messages** for unsupported formats or invalid links

#### 🌐 Using URL Input

**Where to Find:**
- Located in the sidebar under "Image Input"
- Select "URL" option from the radio buttons
- Text input field appears for pasting URLs

**Accepted URL Formats:**
- Direct image links ending with: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.webp`
- Must start with `http://` or `https://`
- Examples:
  - `https://example.com/photo.jpg`
  - `https://site.org/images/portrait.png`
  - `https://cdn.service.com/assets/image.webp`

**Error Handling and Feedback:**
- **✅ Valid URL**: Green checkmark with "Valid image URL detected"
- **❌ Invalid URL**: Red error message with specific issue
- **🔄 Loading**: Spinner shown while fetching image from URL
- **⚠️ Failed Load**: Clear error message if image cannot be loaded

**Benefits of URL Loading:**
- **No Download Required**: Process images directly from the web
- **Quick Access**: Test with online image galleries or stock photos
- **Collaboration**: Share image URLs with team members for processing
- **Demo and Tutorial**: Easy access to example images for demonstrations
- **Batch Workflow**: Integrate with web-based asset management systems

### Step 2: Choose AI Model

Select the optimal model for your image type:

| Model | Best For | When to Use |
|-------|----------|-------------|
| **U2-Net General** | General photos | Default choice for most images |
| **U2-Net Human** | People, portraits | Photos with human subjects |
| **U2-Net Cloth** | Fashion, clothing | Product photography, apparel |
| **IS-Net General** | High precision | When quality is more important than speed |
| **Silueta** | Quick processing | Fast results, good quality |

**Model Information Display:**
- ✅ **Loaded models** show green checkmark
- 📥 **Unloaded models** show download indicator
- 📦 **Model size** and description provided

### Step 3: Configure Output Settings

Choose your background preference:

#### 🔳 Transparent Background
- Creates RGBA PNG with alpha channel
- Perfect for overlaying on other images
- Professional composition workflows

#### ⬜ White Background  
- Clean, standard white background
- Good for general use cases
- Smaller file sizes

#### 🎨 Custom Color Background
- Choose any color with color picker
- Real-time preview of selected color
- Brand-consistent backgrounds

### Step 4: Set Preview Quality

Balance speed vs. quality:
- **Fast (300px)** - Quick adjustments
- **Balanced (500px)** - Default, good compromise  
- **High Quality (800px)** - Final review

### Step 5: Process Image

1. **Click "🎯 Remove Background"**
2. **Processing indicator** shows progress
3. **Result appears** in right column
4. **Success message** confirms completion

### Step 6: Download Results

Three download options available:
- **📥 Download PNG** - Processed image
- **📥 Download JPEG** - RGB version (if applicable)
- **📥 Download Original** - Backup of original

## 🎨 ImageGlitch Effects

### Step 1: Upload and Configure

1. **Upload image** using sidebar controls
2. **Enable Auto Preview** for real-time updates
3. **Choose Preview Quality** based on your hardware
4. **Toggle Extreme Mode** for advanced parameters

### Step 2: Apply Noise Effects

#### 🔊 Gaussian Noise
Simulates camera sensor noise and film grain:
- **Variance**: Controls noise intensity
- **Normal range**: 0.0 - 0.1
- **Extreme range**: 0.0 - 5.0

#### 🔊 Salt & Pepper Noise  
Creates digital corruption effects:
- **Amount**: Percentage of pixels affected
- **Normal range**: 0.0 - 0.1
- **Extreme range**: 0.0 - 1.0

### Step 3: Add Blur Effects

#### 🌫️ Gaussian Blur
Natural, smooth blur for depth effects:
- **Kernel Size**: Blur intensity (odd numbers only)
- **Normal range**: 3 - 15
- **Extreme range**: 3 - 101

#### 🌫️ Motion Blur
Directional blur simulating movement:
- **Degree**: Length of motion streak
- **Angle**: Direction of movement (0-360°)
- **Normal degree range**: 1 - 30
- **Extreme degree range**: 1 - 100

#### 🌫️ Box Blur
Uniform, pixelated blur effect:
- **Kernel Size**: Averaging area (odd numbers)
- **Normal range**: 3 - 15  
- **Extreme range**: 3 - 101

### Step 4: Simulate Shake Effects

#### 📳 Camera Shake
Random camera movement simulation:
- **Intensity**: Maximum pixel displacement
- **Normal range**: 1 - 10
- **Extreme range**: 1 - 50

#### 📳 Directional Shake
Controlled shake in specific directions:
- **Direction**: Horizontal, Vertical, or Both
- **Intensity**: Movement strength
- **Normal range**: 1 - 10
- **Extreme range**: 1 - 50

### Step 5: Add Motion Effects

#### 🏃 Motion Distortion
Creates directional streaking:
- **Direction**: Horizontal, Vertical, or Diagonal
- **Intensity**: Streak length
- **Normal range**: 1 - 20
- **Extreme range**: 1 - 100

#### 🏃 Zoom Motion Blur
Radial blur from center point:
- **Intensity**: Number of zoom layers
- **Normal range**: 1 - 10
- **Extreme range**: 1 - 50

### Step 6: Preview and Process

#### Real-Time Preview
- **Auto Preview**: Instant updates as you adjust
- **Manual Refresh**: Click to update preview
- **Performance Stats**: Processing time display
- **Active Effects**: List of enabled effects

#### Full Quality Processing
1. **Adjust parameters** using preview
2. **Click "🎯 Process Full Quality"**
3. **Wait for processing** (1-3 seconds typically)
4. **Review final result**

### Step 7: Download Results

Multiple format options:
- **📥 Download PNG** - High quality, lossless
- **📥 Download JPEG** - Smaller file size
- **📥 Download Original** - Unmodified backup

## 💡 Tips and Best Practices

### For Background Removal

1. **Choose the right model**:
   - Use U2-Net Human for portraits
   - Use U2-Net Cloth for fashion photography
   - Use Silueta for quick results

2. **Image quality matters**:
   - Higher resolution images give better results
   - Good lighting and contrast improve accuracy
   - Avoid extremely busy backgrounds when possible

3. **Output format selection**:
   - Use transparent PNG for professional workflows
   - Use custom colors for brand consistency
   - Use white background for general applications

### For Creative Effects

1. **Start subtle, build up**:
   - Begin with low parameter values
   - Gradually increase intensity
   - Combine multiple effects for complexity

2. **Use preview effectively**:
   - Enable Auto Preview for immediate feedback
   - Use Fast mode while experimenting
   - Switch to High Quality for final review

3. **Effect combination tips**:
   - Noise → Blur → Shake → Motion (processing order)
   - Motion blur works well with directional shake
   - Combine different noise types for texture

4. **Performance optimization**:
   - Use Balanced preview mode as default
   - Close other applications for large images
   - Process full quality only when satisfied

### Hardware Optimization

#### For CPU-Only Systems
- Use Fast or Balanced preview modes
- Process smaller images when possible
- Close unnecessary applications
- Consider using Silueta model for speed

#### For GPU-Accelerated Systems
- Install `rembg[gpu]` for AI acceleration
- Use High Quality preview mode
- Process multiple images efficiently
- Take advantage of parallel processing

## 🔄 Workflow Integration

### Design Workflows
1. Remove background with ImageGlitch
2. Import transparent PNG into design software
3. Apply additional effects and compositing
4. Export final design

### Photography Workflows  
1. Batch process product photos
2. Create consistent background styles
3. Apply creative effects for artistic shots
4. Maintain original files for re-processing

### Content Creation Workflows
1. Remove backgrounds from photos
2. Add creative glitch effects
3. Export multiple formats for different platforms
4. Archive processed versions

## 🎨 Creative Ideas

### Portrait Photography
- Remove background, add colored backdrop
- Apply subtle camera shake for handheld feel
- Use motion blur for dynamic portraits

### Product Photography
- Clean transparent backgrounds
- Add motion effects for dynamic product shots
- Create glitch aesthetic for tech products

### Social Media Content
- Combine background removal with creative effects
- Use extreme mode for dramatic viral content
- Create consistent brand backgrounds

### Digital Art
- Use as preprocessing for digital paintings
- Create glitch art with multiple effects
- Experiment with noise textures

---

*Next: [Configuration →](configuration.md)*
