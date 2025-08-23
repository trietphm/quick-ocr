# System Tray OCR Application

A Linux system tray application that can capture screenshots and perform OCR (Optical Character Recognition) using Tesseract. Designed specifically for Fedora and Wayland compatibility.

## Features

- **System Tray Integration**: Runs quietly in the system tray
- **OCR Capture**: Screenshot area selection with automatic text recognition
- **Language Support**: English and Chinese Simplified OCR
- **Command Line Support**: Direct OCR capture via command line
- **Clipboard Integration**: Automatically copies detected text to clipboard
- **Wayland Compatible**: Works on modern Linux desktop environments

## Requirements

### System Dependencies

Install the required system packages on Fedora:

```bash
# Install Tesseract OCR and language packs
sudo dnf install tesseract tesseract-langpack-eng tesseract-langpack-chi-sim

# Install screenshot tools for Wayland
sudo dnf install gnome-screenshot grim slurp

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

#### System Tray Mode (Default)
```bash
python3 main.py
```

The application will run in the system tray. Right-click the tray icon to access options.

#### Command Line OCR
```bash
python3 main.py ocr
```

This will immediately trigger the area selection for OCR capture and exit after completion.

#### Using the run script
```bash
./run.sh          # System tray mode
./run.sh ocr      # Direct OCR capture
```

### System Tray Controls

- **Right-click tray icon** to open context menu
- **📷 Capture OCR**: Start area selection for OCR
- **🌐 Language**: Switch between English and Chinese
- **❌ Quit**: Exit the application

### How It Works

1. **System Tray Mode**: Click "Capture OCR" from the tray menu
2. **Command Line Mode**: Run `python3 main.py ocr`
3. The application will:
   - Show an area selection cursor
   - Let you drag to select the text area
   - Capture a screenshot of the selected area
   - Process the image with Tesseract OCR
   - Copy the detected text to your clipboard
   - Show a notification with the result

## Features Details

### System Tray Integration
- Runs quietly in the background
- Minimal resource usage when idle
- Easy access via right-click menu
- Clean, unobtrusive operation

### OCR Functionality
- Uses [Tesseract OCR Engine](https://github.com/tesseract-ocr/tesseract)
- Supports English (`eng`) and Chinese Simplified (`chi_sim`)
- Interactive area selection for precise capture
- Automatic text recognition and clipboard integration
- Works with various image qualities

### Command Line Interface
- `python3 main.py` - Start system tray mode
- `python3 main.py ocr` - Direct OCR capture
- `python3 main.py --help` - Show usage information

## Troubleshooting

### Common Issues

1. **"Tesseract not found" error**:
   ```bash
   sudo dnf install tesseract tesseract-langpack-eng tesseract-langpack-chi-sim
   ```

2. **Screenshot not working**:
   - Install required tools: `sudo dnf install gnome-screenshot grim slurp`
   - The app tries `gnome-screenshot` first, then falls back to `grim` with `slurp`

3. **PyQt5 import error**:
   ```bash
   sudo dnf install python3-qt5
   pip install PyQt5
   ```

4. **System tray not visible**:
   - Ensure your desktop environment supports system tray
   - Some minimal desktop environments may not show system tray icons
   - Try using the command line mode: `python3 main.py ocr`

### Wayland Specific Notes

This application is designed to work with Wayland. If you encounter issues:

- Make sure you have a Wayland-compatible screenshot tool installed
- The application tries `gnome-screenshot` first, then falls back to `grim` with `slurp`
- Some desktop environments may require additional permissions for screenshot capture
- For area selection, `slurp` is required when using `grim`

## Development

### Project Structure
```
ocr/
├── main.py           # Main application file
├── requirements.txt  # Python dependencies
├── run.sh           # Convenience script
└── README.md        # This file
```

### Key Classes
- `OCRTrayIcon`: System tray application with OCR functionality
- Command line argument parsing for direct OCR execution

## License

This project uses the Tesseract OCR engine, which is licensed under the Apache License 2.0.

## Contributing

Feel free to submit issues and enhancement requests!
