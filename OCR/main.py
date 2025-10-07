import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from PIL import Image
import pytesseract
import io

class OCRApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local OCR Tool")
        self.resize(700, 700)

        self.layout = QVBoxLayout()

        self.label = QLabel("No image selected or pasted")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setScaledContents(True)
        self.layout.addWidget(self.label)

        self.textbox = QTextEdit()
        self.layout.addWidget(self.textbox)

        # Buttons
        self.btn_load = QPushButton("Load Image from File")
        self.btn_load.clicked.connect(self.load_image)
        self.layout.addWidget(self.btn_load)

        self.btn_paste = QPushButton("Paste Image from Clipboard")
        self.btn_paste.clicked.connect(self.paste_image)
        self.layout.addWidget(self.btn_paste)

        self.btn_ocr = QPushButton("Run OCR")
        self.btn_ocr.clicked.connect(self.run_ocr)
        self.layout.addWidget(self.btn_ocr)

        self.setLayout(self.layout)

        self.image_path = None
        self.pasted_image = None

        # optional: specify tesseract path if needed
        # pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.image_path = file_path
            self.pasted_image = None
            self.label.setPixmap(QPixmap(file_path))
            self.textbox.setPlainText("")

    def paste_image(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasImage():
            qimage = clipboard.image()
            self.pasted_image = qimage
            self.image_path = None
            pixmap = QPixmap.fromImage(qimage)
            self.label.setPixmap(pixmap)
            self.textbox.setPlainText("")
        else:
            self.textbox.setPlainText("No image found in clipboard.")

    def run_ocr(self):
        if self.image_path:
            text = pytesseract.image_to_string(Image.open(self.image_path))
            self.textbox.setPlainText(text)

        elif self.pasted_image:
            # Convert QImage → PIL Image
            buffer = QImageToPIL(self.pasted_image)
            text = pytesseract.image_to_string(buffer)
            self.textbox.setPlainText(text)

        else:
            self.textbox.setPlainText("Please load or paste an image first.")

def QImageToPIL(qimage: QImage):
    """Convert a QImage to a PIL Image"""
    buffer = qimage.bits().asstring(qimage.width() * qimage.height() * 4)
    pil_image = Image.frombuffer(
        "RGBA", (qimage.width(), qimage.height()), buffer, "raw", "RGBA", 0, 1
    )
    return pil_image

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec())
