# Quick OCR

A Linux system tray application for OCR (Optical Character Recognition) with screenshot capture using Tesseract.

## Features

- System tray integration with right-click menu
- Area selection screenshot capture  
- Multi-language OCR: English, Chinese, or both
- Command line support for automation
- Auto-copy results to clipboard
- Wayland/X11 compatible

## Installation

### Quick Install
```bash
sudo ./install.sh
```

### Manual Install  
```bash
# Install dependencies (Fedora)
sudo dnf install tesseract tesseract-langpack-eng tesseract-langpack-chi_sim python3-qt5 gnome-screenshot grim slurp

# Install Python packages
pip install PyQt5 pytesseract Pillow pyperclip
```

## Usage

```bash
# System tray mode
python3 main.py
quick-ocr                        # After install

# Direct OCR  
python3 main.py ocr --lang eng+chi_sim
quick-ocr ocr --lang eng+chi_sim # After install
```

## Uninstall
```bash
sudo ./uninstall.sh
```

## Keyboard Shortcut Setup

After installation, set up a keyboard shortcut in GNOME Settings:
- **Command**: `/usr/local/bin/quick-ocr ocr`
- **Key**: `Ctrl+Shift+O` (or your preference)

## Language Options
- `eng` - English only
- `chi_sim` - Chinese Simplified only  
- `eng+chi_sim` - Both languages

## Troubleshooting

**Tesseract not found**: `sudo dnf install tesseract tesseract-langpack-eng`

**Screenshot fails**: `sudo dnf install gnome-screenshot grim slurp`  

**PyQt5 error**: `sudo dnf install python3-qt5`

**No system tray**: Use command line mode `quick-ocr ocr`
