# Transparent OCR Application

A Linux application with a transparent window that can capture screenshots and perform OCR (Optical Character Recognition) using Tesseract. Designed specifically for Fedora and Wayland compatibility.

## Features

- **Transparent Window**: See-through window that can be resized and moved
- **OCR Capture**: Screenshot capture with automatic text recognition
- **Language Support**: English and Chinese Simplified OCR
- **Keyboard Shortcut**: Ctrl+Enter for quick OCR capture
- **Clipboard Integration**: Automatically copies detected text to clipboard
- **Wayland Compatible**: Works on modern Linux desktop environments

## Requirements

### System Dependencies

Install the required system packages on Fedora:

```bash
# Install Tesseract OCR and language packs
sudo dnf install tesseract tesseract-langpack-eng tesseract-langpack-chi-sim

# Install screenshot tools for Wayland
sudo dnf install gnome-screenshot grim

# Install Python development packages
sudo dnf install python3-pip python3-devel

# Install Qt5 dependencies
sudo dnf install python3-qt5 python3-qt5-devel
```

### Python Dependencies

Install Python dependencies using pip:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install PyQt5 pytesseract Pillow pyperclip
```

## Installation

1. Clone or download this repository
2. Install system dependencies (see above)
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python3 main.py
```

### Controls

- **Move Window**: Click and drag anywhere on the window border
- **Resize Window**: Drag the window edges (standard window resizing)
- **Language Toggle**: Click the orange "EN/CN" button to switch between English and Chinese
- **OCR Capture**: 
  - Click the blue camera button (📷)
  - Or press **Ctrl+Enter**
- **Close Application**: Press **Escape**

### How It Works

1. Position the transparent window over the text you want to capture
2. Click the OCR button or press Ctrl+Enter
3. The application will:
   - Temporarily hide the window
   - Capture a screenshot of the area
   - Process the image with Tesseract OCR
   - Copy the detected text to your clipboard
   - Show the window again

## Features Details

### Window Properties
- Fully transparent background
- Stays on top of other windows
- Frameless design for minimal interference
- Resizable and movable

### OCR Functionality
- Uses [Tesseract OCR Engine](https://github.com/tesseract-ocr/tesseract)
- Supports English (`eng`) and Chinese Simplified (`chi_sim`)
- Automatic text recognition and clipboard integration
- Works with various image qualities

### UI Elements
- **Blue Camera Button**: Triggers OCR capture
- **Orange Language Button**: Toggles between EN (English) and CN (Chinese)
- Both buttons are positioned at the top-right of the window

## Troubleshooting

### Common Issues

1. **"Tesseract not found" error**:
   ```bash
   sudo dnf install tesseract tesseract-langpack-eng tesseract-langpack-chi-sim
   ```

2. **Screenshot not working**:
   - Install `gnome-screenshot`: `sudo dnf install gnome-screenshot`
   - Or install `grim` for Wayland: `sudo dnf install grim`

3. **PyQt5 import error**:
   ```bash
   sudo dnf install python3-qt5
   pip install PyQt5
   ```

4. **Window not transparent**:
   - Ensure you're running on a compositor-enabled desktop environment
   - Try running with `QT_QPA_PLATFORM=wayland python3 main.py`

### Wayland Specific Notes

This application is designed to work with Wayland. If you encounter issues:

- Make sure you have a Wayland-compatible screenshot tool installed
- The application tries `gnome-screenshot` first, then falls back to `grim`
- Some desktop environments may require additional permissions for screenshot capture

## Development

### Project Structure
```
ocr/
├── main.py           # Main application file
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

### Key Classes
- `TransparentOCRWindow`: Main application window
- `FloatingButton`: OCR capture button
- `LanguageButton`: Language selection button

## License

This project uses the Tesseract OCR engine, which is licensed under the Apache License 2.0.

## Contributing

Feel free to submit issues and enhancement requests!
