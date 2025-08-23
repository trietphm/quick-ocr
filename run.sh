#!/bin/bash
# Run Quick OCR Application
# Usage: 
#   ./run.sh                    # Run in system tray mode
#   ./run.sh ocr                # Direct OCR capture (English)
#   ./run.sh ocr eng            # Direct OCR capture with English
#   ./run.sh ocr chi_sim        # Direct OCR capture with Chinese
#   ./run.sh ocr eng+chi_sim    # Direct OCR capture with both languages

if [ "$1" = "ocr" ]; then
    if [ -n "$2" ]; then
        # Language specified
        python3 main.py ocr --lang "$2"
    else
        # Default language
        python3 main.py ocr
    fi
else
    python3 main.py
fi
