from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QProgressBar, QVBoxLayout, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
import sys

class SplashScreen1(QWidget):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        # Window Setup
        self.setFixedSize(850, 700)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Background Image
        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(
            QPixmap(r"assets\imgs\brown_ls.png").scaled(
                self.size(),
                Qt.AspectRatioMode.IgnoreAspectRatio,   # Fill entire screen
                Qt.TransformationMode.SmoothTransformation
            )
        )
        self.bg_label.setGeometry(0, 0, 850, 700)  # Fill whole window

        # Overlay Layout
        self.overlay = QWidget(self)
        self.overlay.setGeometry(0, 0, 850, 700)
        self.overlay.setStyleSheet("background: transparent;")  # Invisible overlay

        overlay_layout = QVBoxLayout(self.overlay)
        overlay_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        overlay_layout.setContentsMargins(0, 0, 0, 40)  # Add bottom spacing for text and bar

        # Text Label
        self.label = QLabel("Preparing food...", self.overlay)
        self.label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.label.setStyleSheet("color: white")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Progress Bar
        self.progress = QProgressBar(self.overlay)
        self.progress.setFixedWidth(400)
        self.progress.setFixedHeight(20)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)

        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.15);
                border: none;
                border-radius: 10px;
            }
            QProgressBar::chunk {
                background-color: white;
                border-radius: 10px;
                margin: 0px; 
            }
        """)

        # Add widgets to overlay
        overlay_layout.addWidget(self.progress)
        overlay_layout.addWidget(self.label)

        # Fade in Animation
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

        # Timer
        self.counter = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.Loading)
        self.timer.start(30)

    def Loading(self):
        self.counter += 1
        self.progress.setValue(self.counter)
        if self.counter >= 100:
            self.timer.stop()
            self.close()
            self.finished.emit()
