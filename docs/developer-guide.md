# 👨‍💻 Developer Guide

Welcome to the Developer Guide. This document is intended for developers interested in contributing to or extending the functionality of ImageGlitch. Here, you'll find a comprehensive overview of the codebase, key components, and development best practices.

## 🔍 Codebase Structure

```plaintext
ImageGlitch/
├── app.py                 # Main Streamlit application
├── requirements.txt          # Python dependencies
├── WHITEPAPER.md            # Technical whitepaper and implementation details
├── image_utils/             # Image processing utilities
│   ├── __init__.py          # Package initialization
│   ├── blur.py              # Blur effects (Gaussian, Motion, Box)
│   ├── noise.py             # Noise effects (Gaussian, Salt & Pepper)
│   ├── shaky.py             # Camera shake effects
│   └── motion.py            # Motion distortion effects
├── docs/                    # Comprehensive documentation
│   ├── README.md            # Documentation overview and navigation
│   ├── overview.md          # Project introduction and features
│   ├── getting-started.md   # Installation and quick setup
│   ├── user-guide.md        # Complete usage instructions
│   ├── configuration.md     # Settings and customization
│   ├── developer-guide.md   # Development and contribution guide
│   ├── api-reference.md     # Technical API documentation
│   ├── faq.md               # FAQ and troubleshooting
│   └── changelog.md         # Version history and updates
└── README.md                # Main project README
```

## 🗂️ Key Components

### Application File (app.py)
This is the main entry point for the ImageGlitch application. It sets up the Streamlit interface and manages the overall flow:
- **BackgroundRemovalManager**: Controls AI models for background removal.
- **Effect Pipeline**: Handles real-time effects processing.
- **Session State**: Manages user session data and caching.

### Image Utils Package (image_utils/)
Contains the core image processing modules:
- **blur.py**: Implements Gaussian, Motion, and Box blur effects.
- **noise.py**: Adds Gaussian and Salt & Pepper noise effects.
- **shaky.py**: Simulates camera shake effects.
- **motion.py**: Handles motion distortion and zoom effects.

## 🛠️ Extending ImageGlitch

### Adding New Glitch Effects
1. **Create a new module** in `image_utils/` for your effect.
2. **Define your effect function** following existing file patterns.
3. **Register the new effect** in `app.py` under the appropriate effect category.
4. **Update UI controls** in the Streamlit sidebar if needed.

### Adding New AI Models
1. **Define the new model** inside the `BackgroundRemovalManager` class.
2. **Implement loading logic** for the new model.
3. **Update model selection** in UI to include your new model.

## 🏗️ Environment Setup

### Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/binayakbartaula11/ImageGlitch.git
   cd ImageGlitch
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application for development**:
   ```bash
   streamlit run app.py
   ```

### Testing and Debugging

1. **Enable debug mode** by setting environment variable `IMAGEGLITCH_DEBUG=true`.
2. **Use logging** to check for errors or debugging information.
3. **Unit tests** can be added using Python's unittest framework.
4. **Profiles** can be created to benchmark and optimize performance.

## 📥 Contributing

### Contribution Workflow

1. **Fork the repository** on GitHub.
2. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit your changes**:
   ```bash
   git commit -m "Add your feature"
   ```
4. **Push to your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a pull request** and describe your changes.

### Coding Standards

- **PEP 8 Compliance**: Ensure code adheres to PEP 8 style guide.
- **Docstrings**: Document all modules, classes, and functions.
- **Tests**: Add or update tests for any changes.

## 🔧 Troubleshooting Development

### Common Issues

- **Dependencies not installing**: Ensure your Python environment is correctly set up.
- **Streamlit UI not loading**: Check logs for error messages, ensure `venv` is activated.
- **Model issues**: Confirm model paths and validity within `rembg` dependency.

## 👥 Community and Support

### Community Contributions

We welcome community contributions, feedback, and feature requests:
- **GitHub Issues**: For bug reports and feature requests.
- **Discussions**: Share ideas and solutions with other users.
- **Pull Requests**: Contribute code by following the contribution workflow.

---

*Next: [API Reference →](api-reference.md)*
