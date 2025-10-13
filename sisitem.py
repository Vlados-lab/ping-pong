import sys
import hashlib
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QMessageBox, QTableWidget, QTableWidgetItem, 
                             QTabWidget, QDialog, QHeaderView)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QBrush, QPainter, QPen


DB_FILE = "ping_pong.db"

class Database:
    @staticmethod
    def init_db():
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                registration_date TEXT NOT NULL
            )
        ''')
        
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                game_date TEXT NOT NULL,
                player1_score INTEGER NOT NULL,
                player2_score INTEGER NOT NULL,
                winner TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_FILE)
    
    @staticmethod
    def user_exists(username):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    @staticmethod
    def create_user(username, password_hash):
        conn = Database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password_hash, registration_date)
                VALUES (?, ?, ?)
            ''', (username, password_hash, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False
    
    @staticmethod
    def verify_user(username, password_hash):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM users 
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    @staticmethod
    def save_game_result(username, player1_score, player2_score, winner):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO game_history (username, game_date, player1_score, player2_score, winner)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
              player1_score, player2_score, winner))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_user_games(username):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT game_date, player1_score, player2_score, winner 
            FROM game_history 
            WHERE username = ? 
            ORDER BY game_date DESC
        ''', (username,))
        games = cursor.fetchall()
        conn.close()
        return games

class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Пинг-Понг - Авторизация')
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:1 #3498db);
            }
            QWidget {
                background: transparent;
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #34495e;
                border-radius: 8px;
                font-size: 14px;
                background: rgba(255,255,255,0.9);
            }
            QPushButton {
                padding: 12px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #c0392b, stop:1 #e74c3c);
            }
            QTabWidget::pane {
                border: 2px solid #34495e;
                border-radius: 8px;
                background: rgba(52, 73, 94, 0.8);
            }
            QTabBar::tab {
                background: #34495e;
                color: white;
                padding: 10px;
                margin: 2px;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #e74c3c;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        title = QLabel('ПИНГ-ПОНГ')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title)

        self.tabs = QTabWidget()
        
        login_tab = QWidget()
        login_layout = QVBoxLayout(login_tab)
        login_layout.setSpacing(15)
        
        login_layout.addWidget(QLabel('Логин:'))
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText('Введите логин')
        login_layout.addWidget(self.login_username)
        
        login_layout.addWidget(QLabel('Пароль:'))
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText('Введите пароль')
        self.login_password.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(self.login_password)
        
        self.login_btn = QPushButton('Войти')
        self.login_btn.clicked.connect(self.login)
        login_layout.addWidget(self.login_btn)
        
        register_tab = QWidget()
        register_layout = QVBoxLayout(register_tab)
        register_layout.setSpacing(15)
        
        register_layout.addWidget(QLabel('Логин:'))
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText('Придумайте логин')
        register_layout.addWidget(self.register_username)
        
        register_layout.addWidget(QLabel('Пароль:'))
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText('Придумайте пароль')
        self.register_password.setEchoMode(QLineEdit.Password)
        register_layout.addWidget(self.register_password)
        
        register_layout.addWidget(QLabel('Подтвердите пароль:'))
        self.register_confirm = QLineEdit()
        self.register_confirm.setPlaceholderText('Повторите пароль')
        self.register_confirm.setEchoMode(QLineEdit.Password)
        register_layout.addWidget(self.register_confirm)
        
        self.register_btn = QPushButton('Зарегистрироваться')
        self.register_btn.clicked.connect(self.register)
        register_layout.addWidget(self.register_btn)
        
        self.tabs.addTab(login_tab, "Вход")
        self.tabs.addTab(register_tab, "Регистрация")
        layout.addWidget(self.tabs)
        
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self):
        username = self.login_username.text()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля!')
            return
        
        password_hash = self.hash_password(password)
        
        if Database.verify_user(username, password_hash):
            self.current_user = username
            self.open_game_window()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль!')
    
    def register(self):
        username = self.register_username.text()
        password = self.register_password.text()
        confirm = self.register_confirm.text()
        
        if not username or not password or not confirm:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля!')
            return
        
        if password != confirm:
            QMessageBox.warning(self, 'Ошибка', 'Пароли не совпадают!')
            return
        
        if len(password) < 4:
            QMessageBox.warning(self, 'Ошибка', 'Пароль должен содержать минимум 4 символа!')
            return
        
        if Database.user_exists(username):
            QMessageBox.warning(self, 'Ошибка', 'Пользователь с таким логином уже существует!')
            return
        
        password_hash = self.hash_password(password)
        
        if Database.create_user(username, password_hash):
            QMessageBox.information(self, 'Успех', 'Регистрация прошла успешно!')
            self.register_username.clear()
            self.register_password.clear()
            self.register_confirm.clear()           
            self.tabs.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, 'Ошибка', 'Ошибка при регистрации пользователя!')
    
    def open_game_window(self):
        self.game_window = GameWindow(self.current_user)
        self.game_window.show()
        self.hide()

class GameWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.initUI()
        self.initGame()
        
    def initUI(self):
        self.setWindowTitle(f'Пинг-Понг - Игрок: {self.username}')
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                padding: 10px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #c0392b, stop:1 #e74c3c);
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.score_layout = QHBoxLayout()
        self.player1_score = QLabel('Игрок 1: 0')
        self.player2_score = QLabel('Игрок 2: 0')
        self.score_layout.addWidget(self.player1_score)
        self.score_layout.addStretch()
        self.score_layout.addWidget(self.player2_score)
        layout.addLayout(self.score_layout)
       
        self.game_widget = GameWidget(self)
        self.game_widget.setFixedSize(800, 500)
        layout.addWidget(self.game_widget)
        
        control_layout = QHBoxLayout()
        self.start_btn = QPushButton('Начать игру')
        self.start_btn.clicked.connect(self.start_game)
        self.pause_btn = QPushButton('Пауза')
        self.pause_btn.clicked.connect(self.pause_game)
        self.pause_btn.setEnabled(False)
        self.history_btn = QPushButton('История игр')
        self.history_btn.clicked.connect(self.show_history)
        self.logout_btn = QPushButton('Выйти')
        self.logout_btn.clicked.connect(self.logout)
        
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.history_btn)
        control_layout.addWidget(self.logout_btn)
        layout.addLayout(control_layout)
        
    def initGame(self):
        self.game_widget.ball_x = 400
        self.game_widget.ball_y = 250
        self.game_widget.ball_dx = 5
        self.game_widget.ball_dy = 5
        self.game_widget.ball_size = 15
        
        self.game_widget.paddle1_y = 210
        self.game_widget.paddle2_y = 210
        self.game_widget.paddle_width = 10
        self.game_widget.paddle_height = 80
        
        self.score1 = 0
        self.score2 = 0
        self.game_active = False
        self.game_paused = False
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
    
    def start_game(self):
        self.game_active = True
        self.game_paused = False
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.timer.start(16) 
        
    def pause_game(self):
        if self.game_paused:
            self.timer.start(16)
            self.pause_btn.setText('Пауза')
            self.game_paused = False
        else:
            self.timer.stop()
            self.pause_btn.setText('Продолжить')
            self.game_paused = True
    
    def update_game(self):
        if not self.game_active:
            return
            
        game = self.game_widget
        
        game.ball_x += game.ball_dx
        game.ball_y += game.ball_dy
        
        if game.ball_y <= 0 or game.ball_y >= 500 - game.ball_size:
            game.ball_dy *= -1  
      
        if (game.ball_x <= 20 + game.paddle_width and 
            game.ball_x >= 20 and
            game.paddle1_y <= game.ball_y <= game.paddle1_y + game.paddle_height):
            game.ball_dx = abs(game.ball_dx)
            game.ball_dy += 1 if game.ball_dy > 0 else -1
        
        if (game.ball_x >= 800 - 20 - game.paddle_width - game.ball_size and 
            game.ball_x <= 800 - 20 and
            game.paddle2_y <= game.ball_y <= game.paddle2_y + game.paddle_height):
            game.ball_dx = -abs(game.ball_dx)
            game.ball_dy += 1 if game.ball_dy > 0 else -1
        
        if game.ball_x < 0:
            self.score2 += 1
            self.reset_ball()
        elif game.ball_x > 800:
            self.score1 += 1
            self.reset_ball()
      
        self.player1_score.setText(f'Игрок 1: {self.score1}')
        self.player2_score.setText(f'Игрок 2: {self.score2}')
      
        if self.score1 >= 5 or self.score2 >= 5:
            self.end_game()
            
        self.game_widget.update()
    
    def reset_ball(self):
        game = self.game_widget
        game.ball_x = 400
        game.ball_y = 250
        game.ball_dx *= -1
        game.ball_dy = 5 if game.ball_dy > 0 else -5
    
    def end_game(self):
        self.game_active = False
        self.timer.stop()
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        
        winner = "Игрок 1" if self.score1 > self.score2 else "Игрок 2"
        Database.save_game_result(self.username, self.score1, self.score2, winner)
        
        QMessageBox.information(self, 'Игра окончена', f'Победил: {winner}\nСчет: {self.score1}:{self.score2}')
        
        self.score1 = 0
        self.score2 = 0
        self.player1_score.setText('Игрок 1: 0')
        self.player2_score.setText('Игрок 2: 0')
        self.reset_ball()
    
    def keyPressEvent(self, event):
        if not self.game_active or self.game_paused:
            return
            
        game = self.game_widget
        if event.key() == Qt.Key_W and game.paddle1_y > 0:
            game.paddle1_y -= 20
        elif event.key() == Qt.Key_S and game.paddle1_y < 500 - game.paddle_height:
            game.paddle1_y += 20
        elif event.key() == Qt.Key_O and game.paddle2_y > 0:
            game.paddle2_y -= 20
        elif event.key() == Qt.Key_L and game.paddle2_y < 500 - game.paddle_height:
            game.paddle2_y += 20
    
    def show_history(self):
        self.history_window = HistoryWindow(self.username)
        self.history_window.show()
    
    def logout(self):
        self.auth_window = AuthWindow()
        self.auth_window.show()
        self.close()

class GameWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("background: black;")
        
        self.ball_x = 400
        self.ball_y = 250
        self.ball_dx = 5
        self.ball_dy = 5
        self.ball_size = 15
        
        self.paddle1_y = 210
        self.paddle2_y = 210
        self.paddle_width = 10
        self.paddle_height = 80
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(self.ball_x, self.ball_y, self.ball_size, self.ball_size)
        
        painter.drawRect(20, self.paddle1_y, self.paddle_width, self.paddle_height)
        painter.drawRect(800 - 20 - self.paddle_width, self.paddle2_y, self.paddle_width, self.paddle_height)
       
        pen = QPen(Qt.white, 2, Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(400, 0, 400, 500)

class HistoryWindow(QDialog):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.initUI()
        self.load_history()
        
    def initUI(self):
        self.setWindowTitle('История игр')
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
            }
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
            QTableWidget {
                background: white;
                border: 2px solid #34495e;
                border-radius: 8px;
                font-size: 12px;
            }
            QHeaderView::section {
                background: #e74c3c;
                color: white;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton {
                padding: 10px 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #c0392b, stop:1 #e74c3c);
            }
        """)
        
        layout = QVBoxLayout()
       
        title = QLabel(f'История игр - {self.username}')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
    
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Дата и время', 'Игрок 1', 'Игрок 2', 'Счет', 'Победитель'])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        
        close_btn = QPushButton('Закрыть')
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        self.setLayout(layout)
    
    def load_history(self):
        games = Database.get_user_games(self.username)
        self.table.setRowCount(len(games))
        for row, game in enumerate(games):
            game_date, player1_score, player2_score, winner = game
            self.table.setItem(row, 0, QTableWidgetItem(game_date))
            self.table.setItem(row, 1, QTableWidgetItem(self.username))
            self.table.setItem(row, 2, QTableWidgetItem('Компьютер'))
            self.table.setItem(row, 3, QTableWidgetItem(f"{player1_score}:{player2_score}"))
            self.table.setItem(row, 4, QTableWidgetItem(winner))

def main():
    app = QApplication(sys.argv)
    Database.init_db()
    auth_window = AuthWindow()
    auth_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()