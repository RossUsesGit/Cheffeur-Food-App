from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import sys

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(850, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("""
            QWidget {
                background-image: url('imgs/brown_ls.png');
                background-repeat: no-repeat;
                background-position: center;
                background-color: #1E1E1E;
                color: white;
                border-radius: 15px;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel("🍔 Calorie Tracker Loading...")
        self.title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4CAF50;
                border-radius: 8px;
                text-align: center;
                background-color: #2E2E2E;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
                margin: 1px;
            }
        """)

        layout.addWidget(self.title)
        layout.addWidget(self.progress)
        self.setLayout(layout)

        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.load)
        self.timer.start(50)

    def load(self):
        self.counter += 2
        self.progress.setValue(self.counter)
        if self.counter >= 100:
            self.timer.stop()
            self.close()
