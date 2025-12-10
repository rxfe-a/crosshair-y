from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPixmap, QGuiApplication
from PyQt6.QtCore import Qt, QTimer
import sys

class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        # window flags (i think i did it wrong tho)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        original = QPixmap("assets/menu_sprite.png")
        scale_factor = 1.3
        self.image = original.scaled(
            int(original.width() * scale_factor),
            int(original.height() * scale_factor),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.show_image = True

        screen = QGuiApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        QTimer.singleShot(0, self.update_loop)

    def update_loop(self):
        self.update()
        QTimer.singleShot(16, self.update_loop)  # ~60fps

    def paintEvent(self, event):
        if not self.show_image:
            return

        painter = QPainter(self)
        img_w = self.image.width()
        img_h = self.image.height()
        x = self.width() - img_w - 20
        y = 20

        painter.drawPixmap(x, y, self.image)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F2:
            self.show_image = not self.show_image
            self.update()

        if event.key() == Qt.Key.Key_F3:
            QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()
    sys.exit(app.exec())
