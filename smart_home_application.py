import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from smart_home.monitoring_dashboard import SmartHomeGUI
from smart_home.central_automation_system import CentralAutomationSystem
from database import DatabaseManager

class CustomMessageBox(QMessageBox):
    """Custom QMessageBox with styled buttons."""
    def __init__(self, title, message):
        super().__init__()
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(title)
        self.setText(message)
        self.setStandardButtons(QMessageBox.Ok)
        self.setStyleSheet(
            """
            QMessageBox {
                background-color: #f2f2f2;
                color: #333333;
            }

            QMessageBox QPushButton {
                background-color: #4CAF50; /* Green */
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                margin: 4px;
            }

            QMessageBox QPushButton:hover {
                background-color: #45a049; /* Darker Green */
            }
            """
        )

class SmartHomeApplication:
    def __init__(self):
        self.db_manager = DatabaseManager()  # Connect to the database
        self.app = QApplication(sys.argv)
        self.login_window = QWidget()
        self.registration_window = QWidget()
        self.dashboard = None  # Initialize dashboard as None

        self.setup_login_window()
        self.setup_registration_window()

    def setup_login_window(self):
        self.login_window.setWindowTitle("HomeMate - Make Your Life Easier")
        self.login_window.setWindowIcon(QIcon('C:/Users/milan/Desktop/SmartHomeApplication/R.png'))
        self.login_window.setStyleSheet("background-color: #f2f2f2;")

        layout = QVBoxLayout()

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap('C:/Users/milan/Desktop/SmartHomeApplication/R.png')
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label, 30)

        # Welcome message
        welcome_label = QLabel("<h1>Welcome to HomeMate!</h1>")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("color: #ff6600;")  # Orange color
        layout.addWidget(welcome_label)

        # Username and password input fields
        username_label = QLabel("<h1>Username:</h1>")
        self.username_textfield = QLineEdit()
        self.username_textfield.setPlaceholderText("Enter your username")
        layout.addWidget(username_label)
        layout.addWidget(self.username_textfield)

        password_label = QLabel("<h1>Password:</h1>")
        self.password_textfield = QLineEdit()
        self.password_textfield.setPlaceholderText("Enter your password")
        self.password_textfield.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_textfield)

        # Login button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login_clicked)
        login_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        layout.addWidget(login_button)

        # Registration button
        register_button = QPushButton("Register")
        register_button.clicked.connect(self.show_registration)  # Connect to show_registration method
        register_button.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        layout.addWidget(register_button)

        self.login_window.setLayout(layout)

    def setup_registration_window(self):
        self.registration_window.setWindowTitle("HomeMate - Registration")
        self.registration_window.setWindowIcon(QIcon('C:/Users/milan/Desktop/SmartHomeApplication/R.png'))
        self.registration_window.setStyleSheet("background-color: #f2f2f2;")

        layout = QVBoxLayout()

        title_label = QLabel("<h1>Create a new account</h1>")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Username field
        username_label = QLabel("Username:")
        self.reg_username_textfield = QLineEdit()
        self.reg_username_textfield.setPlaceholderText("Enter your username")
        layout.addWidget(username_label)
        layout.addWidget(self.reg_username_textfield)

        # Password field
        password_label = QLabel("Password:")
        self.reg_password_textfield = QLineEdit()
        self.reg_password_textfield.setPlaceholderText("Enter your password")
        self.reg_password_textfield.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.reg_password_textfield)

        # Confirm password field
        confirm_password_label = QLabel("Confirm Password:")
        self.confirm_password_textfield = QLineEdit()
        self.confirm_password_textfield.setPlaceholderText("Confirm your password")
        self.confirm_password_textfield.setEchoMode(QLineEdit.Password)
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_textfield)

        # Register button
        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register_clicked)
        register_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        layout.addWidget(register_button)

        # Back to login button
        back_button = QPushButton("Back to Login")
        back_button.clicked.connect(self.show_login)
        back_button.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        layout.addWidget(back_button)

        self.registration_window.setLayout(layout)

    def login_clicked(self):
        username = self.username_textfield.text()
        password = self.password_textfield.text()

        # Perform login authentication
        authenticated = self.db_manager.authenticate(username, password)
        if authenticated:
            # If login is successful, load the dashboard
            self.load_dashboard()
        else:
            CustomMessageBox("Login Failed", "Invalid username or password. Please try again.").exec_()

    def load_dashboard(self):
        # Close login window
        self.login_window.close()
        # Initialize and display the dashboard
        self.dashboard = SmartHomeGUI(CentralAutomationSystem())
        self.dashboard.show()

    def register_clicked(self):
        username = self.reg_username_textfield.text()
        password = self.reg_password_textfield.text()
        confirm_password = self.confirm_password_textfield.text()

        # Perform registration validation
        if password != confirm_password:
            CustomMessageBox("Registration Failed", "Passwords do not match. Please try again.").exec_()
            return

        # Register user
        registration_successful = self.db_manager.register_user(username, password)
        if registration_successful:
            self.load_dashboard()  # Load dashboard after successful registration
        else:
            CustomMessageBox("Registration Failed", "Username already exists. Please choose a different username.").exec_()

    def show_registration(self):
        self.login_window.hide()  # Hide login window
        self.registration_window.show()  # Show registration window

    def show_login(self):
        self.registration_window.hide()  # Hide registration window
        self.login_window.show()  # Show login window

if __name__ == "__main__":
    smart_home_app = SmartHomeApplication()
    smart_home_app.login_window.show()
    sys.exit(smart_home_app.app.exec_())
