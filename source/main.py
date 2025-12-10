from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPixmap, QGuiApplication
from PyQt6.QtCore import Qt, QTimer
import sys

class Overlay(QWidget): ##test widget obv gonna be rewritten for the crosshair
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.image = QPixmap("assets/menu_sprite.png")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()
    sys.exit(app.exec())
