#!/bin/bash

# Quick OCR Application - Installation Script
# This script installs the Quick OCR application system-wide

set -e  # Exit on any error

APP_NAME="quick-ocr"
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
        echo "Usage: sudo ./install.sh"
        exit 1
    fi
}

install_system_dependencies() {
    print_status "Installing system dependencies..."
    
    # Detect package manager
    if command -v dnf &> /dev/null; then
        PKG_MANAGER="dnf"
    elif command -v apt &> /dev/null; then
        PKG_MANAGER="apt"
    elif command -v pacman &> /dev/null; then
        PKG_MANAGER="pacman"
    else
        print_error "Unsupported package manager. Please install dependencies manually:"
        echo "- tesseract and language packs"
        echo "- python3-qt5"
        echo "- gnome-screenshot or grim/slurp"
        exit 1
    fi
    
    case $PKG_MANAGER in
        "dnf")
            dnf install -y tesseract tesseract-langpack-eng tesseract-langpack-chi_sim \
                          python3-qt5 python3-pip gnome-screenshot grim slurp \
                          python3-devel || true
            ;;
        "apt")
            apt update
            apt install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-chi-sim \
                          python3-pyqt5 python3-pip gnome-screenshot grim slurp \
                          python3-dev || true
            ;;
        "pacman")
            pacman -Sy --noconfirm tesseract tesseract-data-eng tesseract-data-chi_sim \
                                  python-pyqt5 python-pip gnome-screenshot grim slurp || true
            ;;
    esac
    
    print_success "System dependencies installed"
}

install_python_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Install using pip
    pip3 install PyQt5 pytesseract Pillow pyperclip
    
    print_success "Python dependencies installed"
}

create_directories() {
    print_status "Creating installation directories..."
    
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$ICON_DIR"
    
    print_success "Directories created"
}

copy_application_files() {
    print_status "Copying application files..."
    
    # Copy main application
    cp main.py "$INSTALL_DIR/"
    cp requirements.txt "$INSTALL_DIR/"
    cp README.md "$INSTALL_DIR/"
    
    # Make main.py executable
    chmod +x "$INSTALL_DIR/main.py"
    
    print_success "Application files copied"
}

create_launcher_script() {
    print_status "Creating launcher script..."
    
    cat > "$BIN_DIR/$APP_NAME" << EOF
#!/bin/bash
# Quick OCR Application Launcher
cd "$INSTALL_DIR"
python3 main.py "\$@"
EOF
    
    chmod +x "$BIN_DIR/$APP_NAME"
    
    print_success "Launcher script created at $BIN_DIR/$APP_NAME"
}

create_icon() {
    print_status "Creating application icon..."
    
    # Create a simple SVG icon
    cat > "$ICON_DIR/$APP_NAME.svg" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
  <circle cx="24" cy="24" r="20" fill="#4682B4" stroke="#FFFFFF" stroke-width="2"/>
  <text x="24" y="30" font-family="Arial, sans-serif" font-size="20" font-weight="bold" 
        text-anchor="middle" fill="white">O</text>
  <rect x="10" y="10" width="28" height="2" fill="white" opacity="0.8"/>
  <rect x="10" y="14" width="20" height="2" fill="white" opacity="0.6"/>
  <rect x="10" y="18" width="24" height="2" fill="white" opacity="0.4"/>
</svg>
EOF
    
    print_success "Application icon created"
}

create_desktop_entry() {
    print_status "Creating desktop entry..."
    
    cat > "$DESKTOP_DIR/$APP_NAME.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Quick OCR
Comment=Quick OCR application with screenshot capture
Exec=$BIN_DIR/$APP_NAME
Icon=$APP_NAME
Categories=Utility;Graphics;Office;
StartupNotify=false
NoDisplay=false
Terminal=false
Keywords=OCR;Screenshot;Text;Recognition;
EOF
    
    chmod 644 "$DESKTOP_DIR/$APP_NAME.desktop"
    
    print_success "Desktop entry created"
}

create_uninstaller() {
    print_status "Creating uninstaller script..."
    
    cat > "$INSTALL_DIR/uninstall.sh" << 'EOF'
#!/bin/bash

# Quick OCR Application - Uninstaller Script

APP_NAME="quick-ocr"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="/usr/share/icons/hicolor/48x48/apps"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root (use sudo)"
        echo "Usage: sudo $0"
        exit 1
    fi
}

main() {
    check_root
    
    print_status "Uninstalling Quick OCR Application..."
    
    # Stop any running instances
    print_status "Stopping any running instances..."
    pkill -f "python3.*main.py" || true
    
    # Remove files
    print_status "Removing application files..."
    rm -rf "$INSTALL_DIR"
    rm -f "$BIN_DIR/$APP_NAME"
    rm -f "$DESKTOP_DIR/$APP_NAME.desktop"
    rm -f "$ICON_DIR/$APP_NAME.svg"
    
    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
    fi
    
    print_success "Quick OCR Application has been uninstalled"
    print_status "Python dependencies were not removed. To remove them manually:"
    echo "  pip3 uninstall PyQt5 pytesseract Pillow pyperclip"
}

main "$@"
EOF
    
    chmod +x "$INSTALL_DIR/uninstall.sh"
    
    print_success "Uninstaller created at $INSTALL_DIR/uninstall.sh"
}

update_system() {
    print_status "Updating system databases..."
    
    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
    fi
    
    # Update icon cache
    if command -v gtk-update-icon-cache &> /dev/null; then
        gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
    fi
    
    print_success "System databases updated"
}

main() {
    echo "=============================================="
    echo "        Quick OCR Application Installer"
    echo "=============================================="
    echo
    
    check_root
    
    print_status "Starting installation process..."
    
    install_system_dependencies
    install_python_dependencies
    create_directories
    copy_application_files
    create_launcher_script
    create_icon
    create_desktop_entry
    create_uninstaller
    update_system
    
    echo
    print_success "Installation completed successfully!"
    echo
    echo "You can now:"
    echo "  • Run from command line: $APP_NAME"
    echo "  • Find it in your application menu as 'Quick OCR'"
    echo "  • Use direct OCR: $APP_NAME ocr"
    echo "  • Use with language: $APP_NAME ocr --lang chi_sim"
    echo
    echo "To uninstall: sudo $INSTALL_DIR/uninstall.sh"
    echo
}

main "$@"
