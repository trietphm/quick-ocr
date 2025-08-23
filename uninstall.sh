#!/bin/bash

# Quick OCR Application - Uninstaller Script
# This script removes the Quick OCR application from the system

set -e  # Exit on any error

APP_NAME="ocr-tray"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/share/icons/hicolor/48x48/apps"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root (use sudo)"
        echo "Usage: sudo ./uninstall.sh"
        exit 1
    fi
}

confirm_uninstall() {
    echo "=============================================="
    echo "      Quick OCR Application Uninstaller"
    echo "=============================================="
    echo
    print_warning "This will completely remove the Quick OCR Application from your system."
    echo
    echo "The following will be removed:"
    echo "  • Application files in $INSTALL_DIR"
    echo "  • Launcher script at $BIN_DIR/$APP_NAME"
    echo "  • Desktop entry at $DESKTOP_DIR/$APP_NAME.desktop"
    echo "  • Application icon at $ICON_DIR/$APP_NAME.svg"
    echo
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Uninstallation cancelled."
        exit 0
    fi
}

stop_running_instances() {
    print_status "Stopping any running instances of the application..."
    
    # Kill any running Python processes with our main.py
    if pgrep -f "python3.*main.py" > /dev/null; then
        pkill -f "python3.*main.py" || true
        sleep 2
        print_success "Stopped running instances"
    else
        print_status "No running instances found"
    fi
}

remove_files() {
    print_status "Removing application files..."
    
    # Remove installation directory
    if [[ -d "$INSTALL_DIR" ]]; then
        rm -rf "$INSTALL_DIR"
        print_success "Removed $INSTALL_DIR"
    else
        print_warning "Installation directory not found: $INSTALL_DIR"
    fi
    
    # Remove launcher script
    if [[ -f "$BIN_DIR/$APP_NAME" ]]; then
        rm -f "$BIN_DIR/$APP_NAME"
        print_success "Removed launcher script: $BIN_DIR/$APP_NAME"
    else
        print_warning "Launcher script not found: $BIN_DIR/$APP_NAME"
    fi
    
    # Remove desktop entry
    if [[ -f "$DESKTOP_DIR/$APP_NAME.desktop" ]]; then
        rm -f "$DESKTOP_DIR/$APP_NAME.desktop"
        print_success "Removed desktop entry: $DESKTOP_DIR/$APP_NAME.desktop"
    else
        print_warning "Desktop entry not found: $DESKTOP_DIR/$APP_NAME.desktop"
    fi
    
    # Remove icon
    if [[ -f "$ICON_DIR/$APP_NAME.svg" ]]; then
        rm -f "$ICON_DIR/$APP_NAME.svg"
        print_success "Removed application icon: $ICON_DIR/$APP_NAME.svg"
    else
        print_warning "Application icon not found: $ICON_DIR/$APP_NAME.svg"
    fi
}

update_system() {
    print_status "Updating system databases..."
    
    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
        print_status "Updated desktop database"
    fi
    
    # Update icon cache
    if command -v gtk-update-icon-cache &> /dev/null; then
        gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
        print_status "Updated icon cache"
    fi
    
    print_success "System databases updated"
}

show_cleanup_info() {
    echo
    print_success "Quick OCR Application has been successfully uninstalled!"
    echo
    print_status "Optional cleanup:"
    echo "  • Python dependencies can be removed manually if not needed by other applications:"
    echo "    pip3 uninstall PyQt5 pytesseract Pillow pyperclip"
    echo
    echo "  • System dependencies were not removed. To remove them manually (if not needed):"
    
    # Detect package manager and show appropriate commands
    if command -v dnf &> /dev/null; then
        echo "    sudo dnf remove tesseract tesseract-langpack-eng tesseract-langpack-chi_sim"
        echo "    sudo dnf remove python3-qt5 gnome-screenshot grim slurp"
    elif command -v apt &> /dev/null; then
        echo "    sudo apt remove tesseract-ocr tesseract-ocr-eng tesseract-ocr-chi-sim"
        echo "    sudo apt remove python3-pyqt5 gnome-screenshot grim slurp"
    elif command -v pacman &> /dev/null; then
        echo "    sudo pacman -R tesseract tesseract-data-eng tesseract-data-chi_sim"
        echo "    sudo pacman -R python-pyqt5 gnome-screenshot grim slurp"
    fi
    
    echo
    print_warning "Only remove system dependencies if you're sure no other applications need them."
}

main() {
    check_root
    confirm_uninstall
    
    echo
    print_status "Starting uninstallation process..."
    
    stop_running_instances
    remove_files
    update_system
    show_cleanup_info
}

main "$@"
