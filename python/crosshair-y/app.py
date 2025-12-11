from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPixmap, QGuiApplication, QColor
from PyQt6.QtCore import Qt, QTimer
from pynput import keyboard
import sys
from pathlib import Path

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        original = QPixmap("menu_sprite.png")
        scale_factor = 1.3
        self.image = original.scaled(
            int(original.width() * scale_factor),
            int(original.height() * scale_factor),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.show_image = True
        self.crosshair_dir = Path("./crosshairs")
        self.crosshair_files = []
        self.load_crosshairs()
        
        self.current_shape_index = 0
        self.current_color_index = 0

        self.colors = [
            QColor(255, 255, 255, 255),  # White
            QColor(255, 0, 0, 255),      # Red
            QColor(0, 255, 0, 255),      # Green
            QColor(0, 0, 255, 255),      # Blue
            QColor(255, 255, 0, 255),    # Yellow
            QColor(255, 0, 255, 255),    # Magenta
            QColor(0, 255, 255, 255),    # Cyan
            QColor(255, 128, 0, 255),    # Orange
        ]

        self.crosshair_pixmap = None
        self.load_current_crosshair()

        screen = QGuiApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        QTimer.singleShot(0, self.update_loop)
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def load_crosshairs(self):
        if not self.crosshair_dir.exists():
            print(f"Warning: {self.crosshair_dir} directory not found")
            return
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
        self.crosshair_files = sorted([
            f for f in self.crosshair_dir.iterdir()
            if f.suffix.lower() in valid_extensions
        ])
        if not self.crosshair_files:
            print("Warning: No crosshair images found in ./crosshairs")

    def load_current_crosshair(self):
        if not self.crosshair_files:
            return
        crosshair_path = self.crosshair_files[self.current_shape_index]
        self.crosshair_pixmap = QPixmap(str(crosshair_path))

    def apply_color_to_crosshair(self):
        if not self.crosshair_pixmap:
            return None
        colored = QPixmap(self.crosshair_pixmap.size())
        colored.fill(Qt.GlobalColor.transparent)
        painter = QPainter(colored)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        painter.drawPixmap(0, 0, self.crosshair_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(colored.rect(), self.colors[self.current_color_index])
        painter.end()
        return colored

    def update_loop(self):
        self.update()
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        QTimer.singleShot(16, self.update_loop)  # ~60fps

    def paintEvent(self, event):
        painter = QPainter(self)
        # Crosshair
        if self.crosshair_pixmap:
            colored_crosshair = self.apply_color_to_crosshair()
            if colored_crosshair:
                x = (self.width() - colored_crosshair.width()) // 2
                y = (self.height() - colored_crosshair.height()) // 2
                painter.drawPixmap(x, y, colored_crosshair)
    
        if self.show_image:
            img_w = self.image.width()
            img_h = self.image.height()
            x = self.width() - img_w - 20
            y = 20
            painter.drawPixmap(x, y, self.image)

    def on_key_press(self, key):
        try:
            if key == keyboard.Key.f2:
                self.show_image = not self.show_image
            elif key == keyboard.Key.f3:
                QApplication.quit()
            elif key.char == 'z':
                self.current_color_index = (self.current_color_index + 1) % len(self.colors)
                print(f"Crosshair color: {self.colors[self.current_color_index].name()}")
            elif key.char == 'x':
                if self.crosshair_files:
                    self.current_shape_index = (self.current_shape_index + 1) % len(self.crosshair_files)
                    self.load_current_crosshair()
                    print(f"Crosshair shape: {self.crosshair_files[self.current_shape_index].name}")
        except AttributeError:
            pass 

        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()
    sys.exit(app.exec())