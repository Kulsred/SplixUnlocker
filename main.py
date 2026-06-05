import sys
import os
import time
import ctypes
import hashlib
import json

if sys.platform == 'win32':
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, 0)

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog,
    QLineEdit, QMessageBox, QComboBox, QGridLayout, QFrame
)
from PyQt5.QtGui import QPixmap, QMovie, QIcon, QFont
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt, QSize
from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.afc import AfcService
from pymobiledevice3.services.diagnostics import DiagnosticsService

SUPPORTED_DEVICES = {
    'iPhone4,1',
    'iPad2,1', 'iPad2,2', 'iPad2,3', 'iPad2,4',
    'iPad2,5', 'iPad2,6', 'iPad2,7',
    'iPad3,1', 'iPad3,2', 'iPad3,3',
    'iPod5,1'
}

SUPPORTED_VERSIONS = {'8.4.1', '9.3.5', '9.3.6'}

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

USERS_FILE = "users.json"
SETTINGS_FILE = "settings.json"

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {'language': 'en'}
    return {'language': 'en'}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

TRANSLATIONS = {
    'en': {
        'app_title': "Splix Unlocker",
        'login_title': "Sign in to continue",
        'username_placeholder': "Username",
        'password_placeholder': "Password",
        'sign_in': "Sign In",
        'create_account': "Create Account",
        'error': "Error",
        'success': "Success",
        'info': "Info",
        'no_device': "No device connected",
        'connected': "Connected:\n{} ({})",
        'unsupported_ios': "Unsupported iOS:\n{}",
        'unsupported_device': "Unsupported Device:\n{}",
        'activate_btn': "Activate Device",
        'tg_link': "t.me/MyProvodok",
        'already_activated': "Already activated",
        'not_a5': "Not A5",
        'not_supported': "Not supported.",
        'done': "Done!",
        'error_occured': "Error.",
        'settings': "Settings",
        'language': "Language",
        'tips': "Tips",
        'english': "English",
        'russian': "Russian",
        'account_created': "Account created! You can now sign in.",
        'wrong_password': "Wrong password!",
        'account_not_found': "Account not found. Please create an account.",
        'enter_creds': "Please enter username and password",
        'username_short': "Username must be at least 3 characters",
        'password_short': "Password must be at least 4 characters",
        'account_exists': "Account already exists",
        'wifi_msg': "The activation will begin now. Please MAKE SURE your device is connected to Wi-Fi.",
        'activation_failed': "Activation failed. Make sure your device is connected to Wi-Fi.",
        'activating': "Activating...",
        'waiting': "Waiting for device \nto return...",
        'fixing': "Fixing activation\n(Attempt {}/5)...",
        'settings_title': "Settings",
        'tips_title': "Tips",
        'tip1': "Tip 1",
        'tip2': "Tip 2",
        'tip3': "Tip 3",
        'tip4': "Tip 4",
        'tip1_text': "You can fill this text yourself",
        'tip2_text': "You can fill this text yourself",
        'tip3_text': "You can fill this text yourself",
        'tip4_text': "You can fill this text yourself",
        'tip_header': "Tips & Tricks"
    },
    'ru': {
        'app_title': "Splix Unlocker",
        'login_title': "Войдите, чтобы продолжить",
        'username_placeholder': "Имя пользователя",
        'password_placeholder': "Пароль",
        'sign_in': "Войти",
        'create_account': "Создать аккаунт",
        'error': "Ошибка",
        'success': "Успешно",
        'info': "Информация",
        'no_device': "Устройство не подключено",
        'connected': "Подключено:\n{} ({})",
        'unsupported_ios': "Неподдерживаемая iOS:\n{}",
        'unsupported_device': "Неподдерживаемое устройство:\n{}",
        'activate_btn': "Активировать устройство",
        'tg_link': "t.me/MyProvodok",
        'already_activated': "Уже активировано",
        'not_a5': "Не A5",
        'not_supported': "Не поддерживается.",
        'done': "Готово!",
        'error_occured': "Ошибка.",
        'settings': "Настройки",
        'language': "Язык",
        'tips': "Советы",
        'english': "Английский",
        'russian': "Русский",
        'account_created': "Аккаунт создан! Теперь вы можете войти.",
        'wrong_password': "Неверный пароль!",
        'account_not_found': "Аккаунт не найден. Пожалуйста, создайте аккаунт.",
        'enter_creds': "Пожалуйста, введите имя пользователя и пароль",
        'username_short': "Имя пользователя должно быть не менее 3 символов",
        'password_short': "Пароль должен быть не менее 4 символов",
        'account_exists': "Аккаунт уже существует",
        'wifi_msg': "Активация начнется сейчас. УБЕДИТЕСЬ, что устройство подключено к Wi-Fi.",
        'activation_failed': "Ошибка активации. Убедитесь, что устройство подключено к Wi-Fi.",
        'activating': "Активация...",
        'waiting': "Ожидание возврата \nустройства...",
        'fixing': "Исправление активации\n(Попытка {}/5)...",
        'settings_title': "Настройки",
        'tips_title': "Советы",
        'tip1': "Совет 1",
        'tip2': "Совет 2",
        'tip3': "Совет 3",
        'tip4': "Совет 4",
        'tip1_text': "Рекомендуем вам скачать также 3utools чтобы после активации сделать скип экрана!",
        'tip2_text': "Лучше запускать main.py а не ехе",
        'tip3_text': "Внимательно проверьте свой провод!",
        'tip4_text': "Заходите в наш телеграмм канал чтобы поддержать нас!",
        'tip_header': "Советы и хитрости"
    }
}

class SettingsDialog(QDialog):
    def __init__(self, parent, current_language):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle(self.parent.texts['settings_title'])
        self.setFixedSize(450, 350)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        wallpaper_path = resource_path('img/wall.jpg').replace('\\', '/')
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Container with background
        self.container = QWidget()
        self.container.setObjectName("DialogContainer")
        self.container.setStyleSheet(f"""
            #DialogContainer {{
                background-image: url({wallpaper_path});
                background-position: center;
                background-repeat: no-repeat;
                border-radius: 20px;
            }}
        """)
        
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel(self.parent.texts['settings_title'])
        title.setStyleSheet("""
            color: white; 
            font-size: 20pt; 
            font-weight: bold; 
            font-family: 'Segoe UI';
            background: transparent;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Language label
        lang_label = QLabel(self.parent.texts['language'] + " / Язык:")
        lang_label.setStyleSheet("""
            color: white; 
            font-size: 14pt; 
            font-family: 'Segoe UI';
            background: transparent;
        """)
        layout.addWidget(lang_label)
        
        # Combo box
        self.lang_combo = QComboBox()
        self.lang_combo.addItem(self.parent.texts['english'], "en")
        self.lang_combo.addItem(self.parent.texts['russian'], "ru")
        if current_language == 'ru':
            self.lang_combo.setCurrentIndex(1)
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(20, 2, 2, 200);
                color: white;
                border: 2px solid rgba(139, 0, 0, 150);
                border-radius: 10px;
                padding: 10px;
                font-family: 'Segoe UI';
                font-size: 13pt;
                min-height: 20px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: rgba(20, 2, 2, 220);
                color: white;
                selection-background-color: rgba(139, 0, 0, 200);
                border: 1px solid rgba(139, 0, 0, 100);
                border-radius: 5px;
                padding: 5px;
                font-size: 12pt;
            }
        """)
        layout.addWidget(self.lang_combo)
        
        layout.addSpacing(30)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        save_btn = QPushButton("💾 Save")
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(139, 0, 0, 200);
                color: white;
                border: 1px solid rgba(139, 0, 0, 100);
                border-radius: 10px;
                font-family: 'Segoe UI';
                font-size: 12pt;
                font-weight: bold;
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: rgba(180, 0, 0, 230);
                border: 1px solid rgba(255, 255, 255, 180);
            }
            QPushButton:pressed {
                background-color: rgba(100, 0, 0, 200);
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)
        
        close_btn = QPushButton("❌ Close")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(60, 60, 60, 200);
                color: white;
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 10px;
                font-family: 'Segoe UI';
                font-size: 12pt;
                font-weight: bold;
                padding: 10px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 230);
                border: 1px solid rgba(255, 255, 255, 80);
            }
            QPushButton:pressed {
                background-color: rgba(40, 40, 40, 200);
            }
        """)
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        main_layout.addWidget(self.container)
        
        # Close button on top right
        self.close_btn = QPushButton("✕", self.container)
        self.close_btn.setGeometry(410, 10, 30, 30)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 30);
                color: white;
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 15px;
                font-family: 'Segoe UI';
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: rgba(232, 17, 35, 200);
                border: 1px solid rgba(255, 255, 255, 180);
            }
        """)
        self.close_btn.clicked.connect(self.close)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()
    
    def save_settings(self):
        lang = self.lang_combo.currentData()
        self.parent.settings['language'] = lang
        save_settings(self.parent.settings)
        self.parent.lang = lang
        self.parent.update_ui_language()
        self.close()

class TipsWindow(QDialog):
    def __init__(self, parent, texts):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle(texts['tips_title'])
        self.setFixedSize(750, 550)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        wallpaper_path = resource_path('img/wall.jpg').replace('\\', '/')
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Container with background
        self.container = QWidget()
        self.container.setObjectName("DialogContainer")
        self.container.setStyleSheet(f"""
            #DialogContainer {{
                background-image: url({wallpaper_path});
                background-position: center;
                background-repeat: no-repeat;
                border-radius: 20px;
            }}
        """)
        
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel(texts['tip_header'])
        title.setStyleSheet("""
            color: white; 
            font-size: 22pt; 
            font-weight: bold; 
            font-family: 'Segoe UI';
            background: transparent;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Tips grid
        grid = QGridLayout()
        grid.setSpacing(15)
        
        for i in range(4):
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: rgba(20, 2, 2, 220);
                    border: 2px solid rgba(139, 0, 0, 100);
                    border-radius: 15px;
                    padding: 15px;
                }
            """)
            card_layout = QVBoxLayout(card)
            
            tip_title = QLabel(texts[f'tip{i+1}'])
            tip_title.setStyleSheet("""
                font-weight: bold; 
                font-size: 13pt; 
                color: #ff6b6b; 
                font-family: 'Segoe UI';
                background: transparent;
            """)
            tip_title.setAlignment(Qt.AlignCenter)
            card_layout.addWidget(tip_title)
            
            tip_text = QLabel(texts[f'tip{i+1}_text'])
            tip_text.setStyleSheet("""
                font-size: 11pt; 
                color: rgba(255,255,255,200); 
                font-family: 'Segoe UI';
                background: transparent;
            """)
            tip_text.setAlignment(Qt.AlignCenter)
            tip_text.setWordWrap(True)
            card_layout.addWidget(tip_text)
            
            grid.addWidget(card, i // 2, i % 2)
        
        layout.addLayout(grid)
        layout.addSpacing(20)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setFixedWidth(150)
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(139, 0, 0, 200);
                color: white;
                border: 1px solid rgba(139, 0, 0, 100);
                border-radius: 10px;
                font-family: 'Segoe UI';
                font-size: 13pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(180, 0, 0, 230);
                border: 1px solid rgba(255, 255, 255, 180);
            }
            QPushButton:pressed {
                background-color: rgba(100, 0, 0, 200);
            }
        """)
        close_btn.clicked.connect(self.close)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        main_layout.addWidget(self.container)
        
        # Close button on top right
        self.close_btn_top = QPushButton("✕", self.container)
        self.close_btn_top.setGeometry(710, 10, 30, 30)
        self.close_btn_top.setCursor(Qt.PointingHandCursor)
        self.close_btn_top.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 30);
                color: white;
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 15px;
                font-family: 'Segoe UI';
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: rgba(232, 17, 35, 200);
                border: 1px solid rgba(255, 255, 255, 180);
            }
        """)
        self.close_btn_top.clicked.connect(self.close)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.lang = self.settings.get('language', 'en')
        self.texts = TRANSLATIONS[self.lang]
        
        self.setWindowTitle("Splix Unlocker - Login")
        self.setWindowIcon(QIcon(resource_path('img/icon.ico')))
        self.setFixedSize(450, 600)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        wallpaper_path = resource_path('img/wall.jpg').replace('\\', '/')
        
        container = QWidget()
        container.setObjectName("Container")
        container.setStyleSheet(f"""
            #Container {{
                background-image: url({wallpaper_path});
                background-position: center;
                background-repeat: no-repeat;
                border-radius: 20px;
            }}
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 40, 40, 40)
        
        self.setCentralWidget(container)
        
        logo_label = QLabel()
        pixmap = QPixmap(resource_path('img/a5afterlife.png'))
        logo_label.setPixmap(pixmap.scaled(300, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        layout.addSpacing(20)
        
        title_label = QLabel(self.texts['app_title'])
        title_label.setStyleSheet("color: white; font-size: 24pt; font-weight: bold; font-family: 'Segoe UI';")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        subtitle_label = QLabel(self.texts['login_title'])
        subtitle_label.setStyleSheet("color: rgba(255,255,255,150); font-size: 12pt; font-family: 'Segoe UI';")
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
        layout.addSpacing(30)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(self.texts['username_placeholder'])
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(20, 2, 2, 150);
                color: white;
                border: 1px solid rgba(139, 0, 0, 100);
                border-radius: 10px;
                padding: 12px;
                font-size: 12pt;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border: 1px solid rgba(200, 0, 0, 200);
            }
        """)
        layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(self.texts['password_placeholder'])
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(20, 2, 2, 150);
                color: white;
                border: 1px solid rgba(139, 0, 0, 100);
                border-radius: 10px;
                padding: 12px;
                font-size: 12pt;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border: 1px solid rgba(200, 0, 0, 200);
            }
        """)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(20)
        
        self.login_btn = QPushButton(self.texts['sign_in'])
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(139, 0, 0, 200);
                color: white;
                border: 1px solid rgba(139, 0, 0, 100);
                border-radius: 10px;
                font-family: 'Segoe UI';
                font-size: 14pt;
                font-weight: bold;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: rgba(180, 0, 0, 230);
                border: 1px solid rgba(255, 255, 255, 180);
            }
            QPushButton:pressed {
                background-color: rgba(100, 0, 0, 200);
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)
        
        self.register_btn = QPushButton(self.texts['create_account'])
        self.register_btn.setCursor(Qt.PointingHandCursor)
        self.register_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgba(255,255,255,150);
                border: none;
                font-family: 'Segoe UI';
                font-size: 11pt;
                padding: 8px;
            }
            QPushButton:hover {
                color: white;
            }
        """)
        self.register_btn.clicked.connect(self.handle_register)
        layout.addWidget(self.register_btn)
        
        layout.addStretch()
        
        # Close button
        self.close_btn = QPushButton("✕", container)
        self.close_btn.setGeometry(410, 10, 30, 30)
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 30);
                color: white;
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 15px;
                font-family: 'Segoe UI';
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: rgba(232, 17, 35, 200);
                border: 1px solid rgba(255, 255, 255, 180);
            }
            QPushButton:pressed {
                background-color: rgba(180, 0, 0, 200);
            }
        """)
        self.close_btn.clicked.connect(self.close)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, self.texts['error'], self.texts['enter_creds'])
            return
        
        users = load_users()
        
        if username not in users:
            QMessageBox.warning(self, self.texts['error'], self.texts['account_not_found'])
            return
        
        if users[username] == hash_password(password):
            self.close()
            self.main_window = MainWindow(self.settings)
            self.main_window.show()
        else:
            QMessageBox.warning(self, self.texts['error'], self.texts['wrong_password'])

    def handle_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, self.texts['error'], self.texts['enter_creds'])
            return
        
        if len(username) < 3:
            QMessageBox.warning(self, self.texts['error'], self.texts['username_short'])
            return
        
        if len(password) < 4:
            QMessageBox.warning(self, self.texts['error'], self.texts['password_short'])
            return
        
        users = load_users()
        
        if username in users:
            QMessageBox.warning(self, self.texts['error'], self.texts['account_exists'])
            return
        
        users[username] = hash_password(password)
        save_users(users)
        
        QMessageBox.information(self, self.texts['success'], self.texts['account_created'])
        
        self.username_input.setText(username)
        self.password_input.setText("")

class MainWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.lang = self.settings.get('language', 'en')
        self.texts = TRANSLATIONS[self.lang]
        
        self.setWindowTitle("Splix A5 Afterlife")
        self.setWindowIcon(QIcon(resource_path('img/icon.ico')))
        self.setFixedSize(800, 500)
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.container = QWidget()
        self.container.setObjectName("Container")
        self.setCentralWidget(self.container)

        wallpaper_path = resource_path('img/wall.jpg').replace('\\', '/')
        self.setStyleSheet(f"""
            #Container {{
                background-image: url({wallpaper_path});
                background-position: center;
                background-repeat: no-repeat;
                border-radius: 20px;
            }}
        """)

        main_layout = QHBoxLayout(self.container)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)

        self.logo_label = QLabel()
        pixmap = QPixmap(resource_path('img/a5afterlife.png'))
        self.logo_label.setPixmap(pixmap.scaled(300, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.logo_label)

        self.status_label = QLabel(self.texts['no_device'])
        self.status_label.setStyleSheet("color: white; font-weight: bold; font-family: 'Segoe UI'; font-size: 14pt; background: transparent;")
        self.status_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.status_label)

        left_layout.addSpacing(10)

        self.btn_activate = QPushButton(self.texts['activate_btn'])
        self.btn_activate.setCursor(Qt.PointingHandCursor)
        self.btn_activate.setFixedHeight(50)
        self.btn_activate.setStyleSheet("""
            QPushButton {
                background-color: rgba(139, 0, 0, 200);
                color: white;
                border: 1px solid rgba(139, 0, 0, 100);
                border-radius: 12px;
                font-family: 'Segoe UI';
                font-size: 14pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(180, 0, 0, 230);
                border: 1px solid rgba(255, 255, 255, 180);
            }
            QPushButton:pressed {
                background-color: rgba(100, 0, 0, 200);
            }
            QPushButton:disabled {
                background-color: rgba(100, 100, 100, 100);
                color: rgba(200, 200, 200, 150);
            }
        """)
        self.btn_activate.clicked.connect(self.activate_device)
        left_layout.addWidget(self.btn_activate)

        left_layout.addSpacing(10)

        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(15)

        self.settings_btn = QPushButton("⚙️ " + self.texts['settings'])
        self.settings_btn.setCursor(Qt.PointingHandCursor)
        self.settings_btn.setFixedHeight(40)
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(40, 40, 40, 150);
                color: white;
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 8px;
                font-family: 'Segoe UI';
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(60, 60, 60, 200);
                border: 1px solid rgba(255, 255, 255, 80);
            }
        """)
        self.settings_btn.clicked.connect(self.open_settings)
        menu_layout.addWidget(self.settings_btn)

        self.tips_btn = QPushButton("💡 " + self.texts['tips'])
        self.tips_btn.setCursor(Qt.PointingHandCursor)
        self.tips_btn.setFixedHeight(40)
        self.tips_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(40, 40, 40, 150);
                color: white;
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 8px;
                font-family: 'Segoe UI';
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(60, 60, 60, 200);
                border: 1px solid rgba(255, 255, 255, 80);
            }
        """)
        self.tips_btn.clicked.connect(self.open_tips)
        menu_layout.addWidget(self.tips_btn)

        left_layout.addLayout(menu_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setAlignment(Qt.AlignCenter)

        self.device_image_label = QLabel()
        self.pixmap_disconnected = QPixmap(resource_path('img/disconnected.png')).scaled(250, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.pixmap_connected = QPixmap(resource_path('img/connected.png')).scaled(250, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.device_image_label.setPixmap(self.pixmap_disconnected)
        self.device_image_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.device_image_label)

        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(right_widget, 1)

        # Close button
        self.btn_close = QPushButton("✕", self.container)
        self.btn_close.setGeometry(770, 15, 30, 30)
        self.btn_close.setCursor(Qt.PointingHandCursor)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 30);
                color: white;
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 15px;
                font-family: 'Segoe UI';
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: rgba(232, 17, 35, 200);
                border: 1px solid rgba(255, 255, 255, 180);
            }
            QPushButton:pressed {
                background-color: rgba(180, 0, 0, 200);
            }
        """)
        self.btn_close.clicked.connect(QApplication.instance().quit)

        self.background_label = QLabel(self.container)
        self.background_movie = QMovie(resource_path('img/rocket.gif'))
        self.background_movie.setScaledSize(QSize(800, 500))
        self.background_label.setMovie(self.background_movie)
        self.background_movie.start()
        self.background_label.lower()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_device)
        self.timer.start(1000)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def update_ui_language(self):
        self.texts = TRANSLATIONS[self.lang]
        self.setWindowTitle(self.texts['app_title'])
        self.status_label.setText(self.texts['no_device'])
        self.btn_activate.setText(self.texts['activate_btn'])
        self.settings_btn.setText("⚙️ " + self.texts['settings'])
        self.tips_btn.setText("💡 " + self.texts['tips'])

    def open_settings(self):
        dialog = SettingsDialog(self, self.lang)
        dialog.exec_()

    def open_tips(self):
        dialog = TipsWindow(self, self.texts)
        dialog.exec_()

    def check_device(self):
        try:
            lockdown = create_using_usbmux()
            product = lockdown.get_value(key='ProductType')
            version = lockdown.get_value(key='ProductVersion')

            if product in SUPPORTED_DEVICES:
                if version in SUPPORTED_VERSIONS:
                    self.status_label.setText(self.texts['connected'].format(product, version))
                    self.btn_activate.setText(self.texts['activate_btn'])
                    self.btn_activate.setEnabled(True)
                else:
                    self.status_label.setText(self.texts['unsupported_ios'].format(version))
                    self.btn_activate.setText(self.texts['tg_link'])
                    self.btn_activate.setEnabled(False)
            else:
                self.status_label.setText(self.texts['unsupported_device'].format(product))
                self.btn_activate.setText(self.texts['tg_link'])
                self.btn_activate.setEnabled(False)
            
            self.device_image_label.setPixmap(self.pixmap_connected)

        except Exception:
            self.status_label.setText(self.texts['no_device'])
            self.btn_activate.setText(self.texts['tg_link'])
            self.btn_activate.setEnabled(False)
            self.device_image_label.setPixmap(self.pixmap_disconnected)

    def activate_device(self):
        QMessageBox.information(self, self.texts['info'], self.texts['wifi_msg'])
        
        self.timer.stop()
        self.btn_activate.setText(self.texts['tg_link'])
        self.btn_activate.setEnabled(False)
        
        self.thread = WorkerThread()
        self.thread.status_update.connect(self.update_status)
        self.thread.finished.connect(self.on_success)
        self.thread.error.connect(self.on_error)
        self.thread.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def on_success(self, message):
        self.status_label.setText(message)
        QMessageBox.information(self, self.texts['success'], message)
        self.btn_activate.setEnabled(True)
        self.timer.start(1000)

    def on_error(self, message):
        QMessageBox.critical(self, self.texts['error'], message)
        self.status_label.setText(self.texts['error_occured'])
        self.btn_activate.setEnabled(True)
        self.timer.start(1000)

class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    status_update = pyqtSignal(str)

    def wait_for_device(self):
        self.status_update.emit("Waiting for device \nto return...")
        while True:
            try:
                lockdown = create_using_usbmux()
                if lockdown.get_value(key='ProductType'):
                    return lockdown
            except Exception:
                time.sleep(1)

    def run(self):
        try:
            lockdown = create_using_usbmux()
            
            activation_state = lockdown.get_value(key='ActivationState')
            if activation_state == 'Activated':
                self.finished.emit("Already activated")
                return

            product = lockdown.get_value(key='ProductType')
            if product not in SUPPORTED_DEVICES:
                self.finished.emit(f"Not A5")
                return

            version = lockdown.get_value(key='ProductVersion')
            if version not in SUPPORTED_VERSIONS:
                self.finished.emit(f"Not supported.")
                return

            self.status_update.emit("Activating...")
            
            payload_path = resource_path('payload')

            with AfcService(lockdown=lockdown) as afc:
                afc.set_file_contents(
                    'Downloads/downloads.28.sqlitedb',
                    open(payload_path, 'rb').read()
                )
            
            time.sleep(5)

            DiagnosticsService(lockdown=lockdown).restart()
            time.sleep(10)
            
            lockdown = self.wait_for_device()

            diag = DiagnosticsService(lockdown=lockdown)
            
            gestalt = diag.mobilegestalt(keys=['ShouldHactivate'])
            should_hactivate = gestalt.get('ShouldHactivate')

            if should_hactivate is False:
                for i in range(5):
                    self.status_update.emit(f"Fixing activation\n(Attempt {i+1}/5)...")
                    
                    with AfcService(lockdown=lockdown) as afc:
                        afc.set_file_contents(
                            'Downloads/downloads.28.sqlitedb',
                            open(payload_path, 'rb').read()
                        )
                    
                    time.sleep(5+i*5)

                    diag.restart()
                    time.sleep(10) 
                    
                    lockdown = self.wait_for_device()
                    
                    diag = DiagnosticsService(lockdown=lockdown)
                    gestalt = diag.mobilegestalt(keys=['ShouldHactivate'])
                    should_hactivate = gestalt.get('ShouldHactivate')
                    
                    if should_hactivate is not False:
                        break
                
                if should_hactivate is False:
                    self.error.emit("Activation failed. Make sure your device is connected to Wi-Fi.")
                    return
                
            DiagnosticsService(lockdown=lockdown).restart()
            self.finished.emit("Done!")
            
        except Exception as e:
            self.error.emit(repr(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
