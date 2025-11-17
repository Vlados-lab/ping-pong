import sys
from PyQt5.QtWidgets import (QApplication,
                             QMainWindow, QWidget, QVBoxLayout, QLabel)
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer


class CelebrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎂 С Днём Рождения!")
        self.setFixedSize(500, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #FF6B6B, stop:1 #764ba2);
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.title_label = QLabel("С Днём Рождения!")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #FF6B6B, stop:0.5 #4ECDC4, stop:1 #45B7D1);
                color: white;
                border-radius: 15px;
                padding: 20px;
                font-size: 24px;
                font-weight: bold;
            }
        """)

        self.message_label = QLabel()
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("""
            QLabel {
                background: white;
                color: #2D3436;
                border-radius: 10px;
                padding: 20px;
                font-size: 14px;
                border: 2px solid #E17055;
            }
        """)

        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)

        central_widget.setLayout(layout)

        self.set_congratulation_text()


    def set_congratulation_text(self):
        congratulation_text = """
        Уважаемый Артём Викторович!

        От всей души поздравляю вас с Днём Рождения! 🎉

        Желаю вам крепкого здоровья, невероятного счастья,
        исполнения всех заветных желаний и ярких впечатлений!

        Пусть каждый день приносит радость!

        Наилучших вам пожеланий! 💖
        """
        self.message_label.setText(congratulation_text)

    def setup_animations(self):
        self.setWindowOpacity(0.0)

        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(1500)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)

        QTimer.singleShot(100, self.fade_animation.start)


def main():
    app = QApplication(sys.argv)
    window = CelebrationWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
