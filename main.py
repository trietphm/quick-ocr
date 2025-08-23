#!/usr/bin/env python3
"""
Transparent OCR Application
A transparent window application with OCR functionality using Tesseract.
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, 
                             QVBoxLayout, QHBoxLayout, QComboBox, QLabel)
from PyQt5.QtCore import Qt, QRect, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QKeySequence, QIcon, QFont
from PyQt5.Qt import QShortcut
import pytesseract
from PIL import Image
import pyperclip
import subprocess
import tempfile


class FloatingButton(QPushButton):
    """Custom floating button with fixed position relative to parent"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(40, 40)
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(70, 130, 180, 200);
                border: 2px solid rgba(255, 255, 255, 150);
                border-radius: 20px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(100, 149, 237, 220);
                border: 2px solid rgba(255, 255, 255, 200);
            }
            QPushButton:pressed {
                background-color: rgba(65, 105, 225, 240);
            }
        """)


class LanguageButton(QPushButton):
    """Language selection button"""
    
    language_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.languages = {'EN': 'eng', 'CN': 'chi_sim'}
        self.current_lang = 'EN'
        self.setText(self.current_lang)
        self.setFixedSize(40, 40)
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 140, 0, 200);
                border: 2px solid rgba(255, 255, 255, 150);
                border-radius: 20px;
                color: white;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 165, 0, 220);
                border: 2px solid rgba(255, 255, 255, 200);
            }
            QPushButton:pressed {
                background-color: rgba(255, 69, 0, 240);
            }
        """)
        self.clicked.connect(self.toggle_language)
    
    def toggle_language(self):
        """Toggle between English and Chinese"""
        self.current_lang = 'CN' if self.current_lang == 'EN' else 'EN'
        self.setText(self.current_lang)
        self.language_changed.emit(self.languages[self.current_lang])


class TransparentOCRWindow(QMainWindow):
    """Main transparent window with OCR functionality"""
    
    def __init__(self):
        super().__init__()
        self.current_language = 'eng'  # Default to English
        self.drag_start_position = None
        self.init_ui()
        self.setup_shortcuts()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Transparent OCR")
        self.setGeometry(100, 100, 800, 600)
        
        # Make window transparent but keep native frame
        self.setWindowFlags(
            Qt.Window | 
            Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create button container at top-right
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(5, 5, 5, 5)
        button_layout.setSpacing(10)
        
        # Language selection button
        self.lang_button = LanguageButton(self)
        self.lang_button.language_changed.connect(self.set_language)
        
        # OCR capture button
        self.ocr_button = FloatingButton("📷", self)
        self.ocr_button.clicked.connect(self.capture_and_ocr)
        self.ocr_button.setToolTip("Capture OCR (Ctrl+Enter)")
        
        # Add buttons to layout
        button_layout.addStretch()  # Push buttons to the right
        button_layout.addWidget(self.lang_button)
        button_layout.addWidget(self.ocr_button)
        
        # Create compact button container with background
        self.button_container = QWidget()
        self.button_container.setLayout(button_layout)
        self.button_container.setFixedHeight(50)
        self.button_container.setStyleSheet("""
            QWidget {
                background-color: rgba(45, 45, 45, 200);
                border-radius: 5px;
                margin: 5px;
            }
        """)
        
        # Main content area (transparent)
        content_widget = QWidget()
        content_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0);
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.button_container)
        main_layout.addWidget(content_widget)
        
        central_widget.setLayout(main_layout)
        
        # Style the main window (transparent background)
        self.setStyleSheet("""
            QMainWindow {
                background-color: rgba(0, 0, 0, 0);
            }
        """)
        
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Ctrl+Enter for OCR capture
        ocr_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        ocr_shortcut.activated.connect(self.capture_and_ocr)
        
        # Escape to close
        close_shortcut = QShortcut(QKeySequence("Escape"), self)
        close_shortcut.activated.connect(self.close)
        
    def set_language(self, lang_code):
        """Set the OCR language"""
        self.current_language = lang_code
        print(f"OCR language set to: {lang_code}")
        
    def capture_and_ocr(self):
        """Capture screenshot of the window area and perform OCR"""
        try:
            # Get window geometry
            geometry = self.geometry()
            
            # Hide window temporarily for clean screenshot
            self.hide()
            
            # Wait a bit for window to disappear
            QTimer.singleShot(200, lambda: self._perform_capture(geometry))
            
        except Exception as e:
            print(f"Error in capture_and_ocr: {e}")
            self.show()
            
    def _perform_capture(self, geometry):
        """Perform the actual screenshot capture and OCR"""
        try:
            # Take screenshot of the specified area
            screenshot = self.take_screenshot(geometry)
            
            if screenshot:
                # Perform OCR
                text = self.perform_ocr(screenshot)
                
                if text.strip():
                    # Copy to clipboard
                    pyperclip.copy(text)
                    print(f"OCR Result copied to clipboard:\n{text}")
                    
                    # Visual feedback
                    self.show_feedback("OCR copied to clipboard!")
                else:
                    print("No text detected in the captured area")
                    self.show_feedback("No text detected")
            else:
                print("Failed to capture screenshot")
                self.show_feedback("Capture failed")
                
        except Exception as e:
            print(f"Error in OCR process: {e}")
            self.show_feedback(f"Error: {str(e)}")
        finally:
            # Show window again
            self.show()
            
    def take_screenshot(self, geometry):
        """Take screenshot of specified area using gnome-screenshot"""
        try:
            # Use gnome-screenshot for Wayland compatibility
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                temp_path = tmp_file.name
                
            # Command to capture specific area
            cmd = [
                'gnome-screenshot',
                '--area',
                '--file', temp_path
            ]
            
            # Alternative: use grim for Wayland if gnome-screenshot is not available
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=10)
                if result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, cmd)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback to grim (Wayland screenshot tool)
                cmd = [
                    'grim', '-g', 
                    f"{geometry.x()},{geometry.y()} {geometry.width()}x{geometry.height()}",
                    temp_path
                ]
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
            
    def show_feedback(self, message):
        """Show visual feedback to user"""
        print(f"Feedback: {message}")
        # You could implement a temporary tooltip or notification here
        



def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Check if tesseract is installed
    try:
        pytesseract.get_tesseract_version()
    except Exception as e:
        print(f"Tesseract not found: {e}")
        print("Please install tesseract-ocr:")
        print("sudo dnf install tesseract tesseract-langpack-eng tesseract-langpack-chi-sim")
        sys.exit(1)
    
    # Create and show the main window
    window = TransparentOCRWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
