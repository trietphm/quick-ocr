#!/bin/bash

# Transparent OCR Application - Installation Script for Fedora
# This script installs all required dependencies for the OCR application

echo "Installing Transparent OCR Application dependencies..."

# Update system
echo "Updating system packages..."
#sudo dnf update -y

# Install Tesseract OCR and language packs
echo "Installing Tesseract OCR..."
sudo dnf install -y tesseract tesseract-langpack-eng tesseract-langpack-chi-sim

# Install screenshot tools for Wayland compatibility
echo "Installing screenshot tools..."
sudo dnf install -y gnome-screenshot grim

# Install Python and development packages
echo "Installing Python development packages..."
sudo dnf install -y python3-pip python3-devel

# Install Qt5 dependencies
echo "Installing Qt5 dependencies..."
sudo dnf install -y python3-qt5 python3-qt5-devel qt5-qtwayland

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --user -r requirements.txt

# Make the main script executable
chmod +x main.py

echo ""
echo "Installation complete!"
echo ""
echo "To run the application:"
echo "  python3 main.py"
echo ""
echo "Controls:"
echo "  - Click and drag to move window"
echo "  - Orange button: Toggle language (EN/CN)"
echo "  - Blue button: Capture OCR (or Ctrl+Enter)"
echo "  - Escape: Exit application"
echo ""
echo "Make sure to position the transparent window over text you want to capture!"
