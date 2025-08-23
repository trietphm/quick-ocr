#!/bin/bash
# Run OCR System Tray Application
# Usage: 
#   ./run.sh          # Run in system tray mode
#   ./run.sh ocr      # Direct OCR capture

if [ "$1" = "ocr" ]; then
    python3 main.py ocr
else
    python3 main.py
fi
