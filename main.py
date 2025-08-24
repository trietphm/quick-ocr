#!/usr/bin/env python3
"""
Quick OCR Application
A system tray application with OCR functionality using Tesseract.
"""

import sys
import os
import argparse
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, QAction, 
                             QMessageBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QPainter
import pytesseract
from PIL import Image
import pyperclip
import subprocess
import tempfile


class OCREngine:
    """Core OCR functionality without GUI dependencies"""
    
    def __init__(self):
        self.current_language = 'eng'  # Default to English
        self.languages = {
            'English': 'eng', 
            'Chinese': 'chi_sim',
            'English + Chinese': 'eng+chi_sim'
        }
    
    def set_language(self, lang_code):
        """Set the OCR language"""
        self.current_language = lang_code
        print(f"OCR language set to: {lang_code}")
    
    def capture_and_ocr(self):
        """Capture screenshot and perform OCR"""
        try:
            # Take screenshot using area selection
            screenshot = self.take_screenshot()
            
            if screenshot:
                # Perform OCR
                text = self.perform_ocr(screenshot)
                
                if text.strip():
                    # Copy to clipboard
                    pyperclip.copy(text)
                    print(f"OCR Result copied to clipboard:\n{text}")
                    return text
                else:
                    print("No text detected in the captured area")
                    return None
            else:
                print("Failed to capture screenshot")
                return None
                
        except Exception as e:
            print(f"Error in OCR process: {e}")
            return None
            
    def take_screenshot(self):
        """Take screenshot using area selection"""
        try:
            # Use gnome-screenshot for area selection
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                temp_path = tmp_file.name
                
            # Command to capture area selection
            cmd = [
                'gnome-screenshot',
                '--area',
                '--file', temp_path
            ]
            
            # Alternative: use grim for Wayland if gnome-screenshot is not available
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=30)
                if result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, cmd)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback to grim (Wayland screenshot tool) with slurp for area selection
                try:
                    # First get the area using slurp
                    slurp_result = subprocess.run(['slurp'], capture_output=True, timeout=30, text=True)
                    if slurp_result.returncode != 0:
                        raise subprocess.CalledProcessError(slurp_result.returncode, ['slurp'])
                    
                    area = slurp_result.stdout.strip()
                    
                    # Then capture with grim
                    cmd = ['grim', '-g', area, temp_path]
                    result = subprocess.run(cmd, capture_output=True, timeout=10)
                    if result.returncode != 0:
                        raise subprocess.CalledProcessError(result.returncode, cmd)
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Final fallback to simple grim (full screen)
                    cmd = ['grim', temp_path]
                    result = subprocess.run(cmd, capture_output=True, timeout=10)
                    if result.returncode != 0:
                        raise subprocess.CalledProcessError(result.returncode, cmd)
            
            # Load the image
            if os.path.exists(temp_path):
                image = Image.open(temp_path)
                os.unlink(temp_path)  # Clean up temp file
                return image
            else:
                return None
                
        except Exception as e:
            print(f"Screenshot capture error: {e}")
            return None
            
    def perform_ocr(self, image):
        """Perform OCR on the captured image"""
        try:
            # Configure tesseract
            custom_config = r'--oem 3 --psm 6'
            
            # Perform OCR
            text = pytesseract.image_to_string(
                image, 
                lang=self.current_language,
                config=custom_config
            )
            
            return text.strip()
            
        except Exception as e:
            print(f"OCR error: {e}")
            return ""


class OCRTrayIcon(QSystemTrayIcon):
    """System tray icon with OCR functionality"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ocr_engine = OCREngine()
        self.current_language = 'eng'  # Default to English
        self.languages = {
            'English': 'eng', 
            'Chinese': 'chi_sim',
            'English + Chinese': 'eng+chi_sim'
        }
        
        # Create tray icon
        self.setIcon(self.create_icon())
        self.setToolTip("Quick OCR")
        
        # Create context menu
        self.create_context_menu()
        
        # Show the tray icon
        self.show()
        
    def create_icon(self):
        """Create a simple icon for the system tray"""
        # Create a simple colored icon
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.blue)
        painter.setPen(Qt.white)
        painter.drawEllipse(0, 0, 16, 16)
        painter.drawText(4, 12, "O")
        painter.end()
        
        return QIcon(pixmap)
    
    def create_context_menu(self):
        """Create the context menu for the tray icon"""
        menu = QMenu()
        
        # OCR Capture action
        ocr_action = QAction("📷 Capture OCR", self)
        ocr_action.triggered.connect(self.capture_and_ocr)
        menu.addAction(ocr_action)
        
        menu.addSeparator()
        
        # Language selection submenu
        lang_menu = menu.addMenu("🌐 Language")
        
        for lang_name, lang_code in self.languages.items():
            lang_action = QAction(lang_name, self)
            lang_action.setCheckable(True)
            lang_action.setChecked(lang_code == self.current_language)
            lang_action.triggered.connect(lambda checked, code=lang_code: self.set_language(code))
            lang_menu.addAction(lang_action)
        
        menu.addSeparator()
        
        # Quit action
        quit_action = QAction("❌ Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(quit_action)
        
        self.setContextMenu(menu)
    
    def set_language(self, lang_code):
        """Set the OCR language and update menu"""
        self.current_language = lang_code
        self.ocr_engine.set_language(lang_code)
        
        # Update checkmarks in language menu
        lang_menu = self.contextMenu().actions()[2].menu()  # Language submenu
        for i, (lang_name, code) in enumerate(self.languages.items()):
            action = lang_menu.actions()[i]
            action.setChecked(code == lang_code)


    def capture_and_ocr(self):
        """Capture screenshot and perform OCR"""
        try:
            # Delegate to OCR engine
            text = self.ocr_engine.capture_and_ocr()
            
            if text:
                self.showMessage("OCR Success", f"Text copied to clipboard:\n{text[:100]}{'...' if len(text) > 100 else ''}", 
                               QSystemTrayIcon.Information, 3000)
            else:
                self.showMessage("OCR Result", "No text detected or capture failed", QSystemTrayIcon.Warning, 2000)
                
        except Exception as e:
            print(f"Error in OCR process: {e}")
            self.showMessage("OCR Error", f"Error: {str(e)}", QSystemTrayIcon.Critical, 3000)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Quick OCR Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py                        # Run in system tray mode
  python3 main.py ocr                    # Directly trigger OCR capture (English)
  python3 main.py ocr --lang eng         # OCR capture with English
  python3 main.py ocr --lang chi_sim     # OCR capture with Chinese
  python3 main.py ocr --lang eng+chi_sim # OCR capture with both languages
        """
    )
    parser.add_argument(
        'action', 
        nargs='?', 
        choices=['ocr'], 
        help='Action to perform (ocr: capture and perform OCR)'
    )
    parser.add_argument(
        '--lang', '--language',
        choices=['eng', 'chi_sim', 'eng+chi_sim'],
        default='eng',
        help='OCR language: eng (English), chi_sim (Chinese), or eng+chi_sim (both). Default: eng'
    )
    return parser.parse_args()


def run_direct_ocr(language='eng'):
    """Run OCR capture directly without GUI"""
    # Create a minimal QApplication for OCR functionality (needed for clipboard access)
    app = QApplication(sys.argv)
    
    # Check if tesseract is installed
    try:
        pytesseract.get_tesseract_version()
    except Exception as e:
        print(f"Tesseract not found: {e}")
        print("Please install tesseract-ocr:")
        print("sudo dnf install tesseract tesseract-langpack-eng tesseract-langpack-chi-sim")
        sys.exit(1)
    
    # Create OCR engine instance and set language
    ocr_engine = OCREngine()
    ocr_engine.set_language(language)
    
    # Run capture
    ocr_engine.capture_and_ocr()
    
    # Exit after OCR operation
    sys.exit(0)


def main():
    """Main application entry point"""
    args = parse_arguments()
    
    # If OCR action is specified, run direct OCR
    if args.action == 'ocr':
        run_direct_ocr(args.lang)
        return
    
    # Create QApplication for system tray mode
    app = QApplication(sys.argv)
    
    # Check if system tray is available
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "System Tray", 
                            "System tray is not available on this system.")
        sys.exit(1)
    
    # Check if tesseract is installed
    try:
        pytesseract.get_tesseract_version()
    except Exception as e:
        print(f"Tesseract not found: {e}")
        print("Please install tesseract-ocr:")
        print("sudo dnf install tesseract tesseract-langpack-eng tesseract-langpack-chi-sim")
        sys.exit(1)
    
    # Don't quit when last window is closed (for system tray apps)
    app.setQuitOnLastWindowClosed(False)
    
    # Create and show the system tray icon
    tray_icon = OCRTrayIcon()
    
    print("Quick OCR application started. Right-click the tray icon to access options.")
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
