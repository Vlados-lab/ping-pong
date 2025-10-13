import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QFont


class PongGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initGame()
        
    def initUI(self):
        self.setWindowTitle('Пинг-Понг')
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: black;")
        
        main_layout = QVBoxLayout()

        self.score_layout = QHBoxLayout()
        self.player1_score_label = QLabel('Игрок 1: 0')
        self.player2_score_label = QLabel('Игрок 2: 0')
        
        score_style = "color: white; font-size: 18px; font-weight: bold;"
        self.player1_score_label.setStyleSheet(score_style)
        self.player2_score_label.setStyleSheet(score_style)
        
        self.score_layout.addWidget(self.player1_score_label)
        self.score_layout.addStretch()
        self.score_layout.addWidget(self.player2_score_label)
        
        button_layout = QHBoxLayout()
        self.start_button = QPushButton('Старт')
        self.pause_button = QPushButton('Пауза')
        self.reset_button = QPushButton('Сброс')
        

        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """
        self.start_button.setStyleSheet(button_style)
        self.pause_button.setStyleSheet(button_style)
        self.reset_button.setStyleSheet(button_style)
        
        self.pause_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.reset_button)
        
        main_layout.addLayout(self.score_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        self.start_button.clicked.connect(self.startGame)
        self.pause_button.clicked.connect(self.pauseGame)
        self.reset_button.clicked.connect(self.resetGame)
        
    def initGame(self):
        self.paddle_width = 15
        self.paddle_height = 100
        self.ball_size = 15
        
        self.player1_y = 250
        self.player2_y = 250
        
        self.ball_x = 400
        self.ball_y = 300
                
        self.ball_speed_x = 5
        self.ball_speed_y = 5
              
        self.player1_score = 0
        self.player2_score = 0
        
        self.game_running = False
        self.game_paused = False
       
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateGame)
        
    def startGame(self):
        if not self.game_running:
            self.game_running = True
            self.game_paused = False
            self.start_button.setEnabled(False)
            self.pause_button.setEnabled(True)
            self.timer.start(16) 
            
    def pauseGame(self):
        if self.game_running:
            if self.game_paused:
                self.game_paused = False
                self.pause_button.setText('Пауза')
                self.timer.start(16)
            else:
                self.game_paused = True
                self.pause_button.setText('Продолжить')
                self.timer.stop()
                
    def resetGame(self):
        self.timer.stop()
        self.initGame()
        self.updateScores()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.pause_button.setText('Пауза')
        self.update()
        
    def updateGame(self):
        if not self.game_running or self.game_paused:
            return
            
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y
        

        if self.ball_y <= 0 or self.ball_y >= 600 - self.ball_size:
            self.ball_speed_y = -self.ball_speed_y
            

        if (self.ball_x <= 20 + self.paddle_width and 
            self.ball_y + self.ball_size >= self.player1_y and 
            self.ball_y <= self.player1_y + self.paddle_height):
            self.ball_speed_x = abs(self.ball_speed_x)
            self.ball_speed_y += random.uniform(-1, 1)
            

        if (self.ball_x >= 800 - 20 - self.paddle_width - self.ball_size and 
            self.ball_y + self.ball_size >= self.player2_y and 
            self.ball_y <= self.player2_y + self.paddle_height):
            self.ball_speed_x = -abs(self.ball_speed_x)  
            self.ball_speed_y += random.uniform(-1, 1)
            
        if self.ball_x < 0:
            self.player2_score += 1
            self.resetBall()
        elif self.ball_x > 800:
            self.player1_score += 1
            self.resetBall()
            
        self.updateScores()
        self.update()
        
    def resetBall(self):
        self.ball_x = 400
        self.ball_y = 300
        self.ball_speed_x = random.choice([-5, 5])
        self.ball_speed_y = random.uniform(-3, 3)
        
    def updateScores(self):
        self.player1_score_label.setText(f'Игрок 1: {self.player1_score}')
        self.player2_score_label.setText(f'Игрок 2: {self.player2_score}')
        
    def keyPressEvent(self, event):
        if not self.game_running or self.game_paused:
            return
            
        # Управление для игрока 1 
        if event.key() == Qt.Key_W and self.player1_y > 0:
            self.player1_y -= 20
        elif event.key() == Qt.Key_S and self.player1_y < 600 - self.paddle_height:
            self.player1_y += 20
            
        # Управление для игрока 2 
        if event.key() == Qt.Key_I and self.player2_y > 0:
            self.player2_y -= 20
        elif event.key() == Qt.Key_K and self.player2_y < 600 - self.paddle_height:
            self.player2_y += 20
            
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        

        painter.setPen(QColor(255, 255, 255))
        painter.drawLine(400, 0, 400, 600)
        
    
        painter.fillRect(20, self.player1_y, self.paddle_width, self.paddle_height, QColor(0, 255, 0))
        

        painter.fillRect(800 - 20 - self.paddle_width, self.player2_y, self.paddle_width, self.paddle_height, QColor(0, 0, 255))
        

        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(int(self.ball_x), int(self.ball_y), self.ball_size, self.ball_size)
        
   
        if self.game_paused:
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont('Arial', 24))
            painter.drawText(self.rect(), Qt.AlignCenter, "ПАУЗА")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = PongGame()
    game.show()
    sys.exit(app.exec_())