import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, 
    QMessageBox, QLabel, QTextEdit, QHBoxLayout, QTabWidget
)
from PyQt6.QtGui import QPixmap

class DotToPngApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DOT to PNG Converter")
        self.resize(600, 600)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # --- Tab 1: File input ---
        self.file_tab = QWidget()
        file_layout = QVBoxLayout()
        self.file_tab.setLayout(file_layout)
        self.tabs.addTab(self.file_tab, "File Input")

        self.open_btn = QPushButton("Select .dot File")
        file_layout.addWidget(self.open_btn)
        self.open_btn.clicked.connect(self.select_file)

        self.file_image_label = QLabel()
        file_layout.addWidget(self.file_image_label)

        # --- Tab 2: Text input ---
        self.text_tab = QWidget()
        text_layout = QVBoxLayout()
        self.text_tab.setLayout(text_layout)
        self.tabs.addTab(self.text_tab, "Paste DOT Text")

        self.dot_text_edit = QTextEdit()
        self.dot_text_edit.setPlaceholderText("Paste your .dot text here...")
        text_layout.addWidget(self.dot_text_edit)

        self.save_btn = QPushButton("Generate PNG")
        text_layout.addWidget(self.save_btn)
        self.save_btn.clicked.connect(self.save_dot_text_as_png)

        self.text_image_label = QLabel()
        text_layout.addWidget(self.text_image_label)

    # --- File input handler ---
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open DOT File", "", "DOT Files (*.dot)")
        if not file_path:
            return

        out_path = file_path + ".png"
        result = subprocess.run(["dot", "-Tpng", file_path, "-o", out_path],
                                capture_output=True, text=True)
        if result.returncode == 0:
            QMessageBox.information(self, "Success", f"PNG saved at:\n{out_path}")
            pixmap = QPixmap(out_path)
            self.file_image_label.setPixmap(pixmap)
        else:
            QMessageBox.critical(self, "Error", f"Failed to generate PNG:\n{result.stderr}")

    # --- Text input handler ---
    def save_dot_text_as_png(self):
        dot_text = self.dot_text_edit.toPlainText()
        if not dot_text.strip():
            QMessageBox.warning(self, "Warning", "DOT text is empty!")
            return

        out_path, _ = QFileDialog.getSaveFileName(self, "Save PNG As", "", "PNG Files (*.png)")
        if not out_path:
            return

        # Write temporary DOT content
        temp_dot_file = out_path + ".tmp.dot"
        with open(temp_dot_file, "w") as f:
            f.write(dot_text)

        # Generate PNG
        result = subprocess.run(["dot", "-Tpng", temp_dot_file, "-o", out_path],
                                capture_output=True, text=True)

        # Cleanup temp file
        import os
        os.remove(temp_dot_file)

        if result.returncode == 0:
            QMessageBox.information(self, "Success", f"PNG saved at:\n{out_path}")
            pixmap = QPixmap(out_path)
            self.text_image_label.setPixmap(pixmap)
        else:
            QMessageBox.critical(self, "Error", f"Failed to generate PNG:\n{result.stderr}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DotToPngApp()
    window.show()
    sys.exit(app.exec())
