import re
import sqlite3

from PyQt5 import QtCore, QtWidgets
from passlib.context import CryptContext

from utils import session
from dashboard import DashboardPage


class LoginPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("LoginWindow")
        self.resize(500, 400)

        # Central Widget
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")

        # Email Input
        self.email_input_widget = QtWidgets.QWidget(self.central_widget)
        self.email_input_widget.setGeometry(QtCore.QRect(50, 50, 341, 41))
        self.email_input_layout = QtWidgets.QHBoxLayout(self.email_input_widget)
        self.email_input_layout.setContentsMargins(0, 0, 0, 0)

        self.email_label = QtWidgets.QLabel(self.email_input_widget)
        self.email_label.setText("Email:")
        self.email_input_layout.addWidget(self.email_label)

        self.email_input = QtWidgets.QLineEdit(self.email_input_widget)
        self.email_input_layout.addWidget(self.email_input)

        # Password Input
        self.password_input_widget = QtWidgets.QWidget(self.central_widget)
        self.password_input_widget.setGeometry(QtCore.QRect(50, 120, 341, 41))
        self.password_input_layout = QtWidgets.QHBoxLayout(self.password_input_widget)
        self.password_input_layout.setContentsMargins(0, 0, 0, 0)

        self.password_label = QtWidgets.QLabel(self.password_input_widget)
        self.password_label.setText("Password:")
        self.password_input_layout.addWidget(self.password_label)

        self.password_input = QtWidgets.QLineEdit(self.password_input_widget)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input_layout.addWidget(self.password_input)

        # Buttons
        self.login_button = QtWidgets.QPushButton(self.central_widget)
        self.login_button.setGeometry(QtCore.QRect(50, 200, 100, 30))
        self.login_button.setText("Login")
        self.login_button.clicked.connect(self.login_user)

        self.cancel_button = QtWidgets.QPushButton(self.central_widget)
        self.cancel_button.setGeometry(QtCore.QRect(300, 200, 100, 30))
        self.cancel_button.setText("Cancel")
        self.cancel_button.mousePressEvent = self.close

        # Signup Section
        self.signup_widget = QtWidgets.QWidget(self.central_widget)
        self.signup_widget.setGeometry(QtCore.QRect(130, 270, 201, 31))
        self.signup_layout = QtWidgets.QHBoxLayout(self.signup_widget)
        self.signup_layout.setContentsMargins(0, 0, 0, 0)

        self.signup_prompt_label = QtWidgets.QLabel(self.signup_widget)
        self.signup_prompt_label.setText("Don't have an account?")
        self.signup_layout.addWidget(self.signup_prompt_label)

        self.signup_label = QtWidgets.QLabel(self.signup_widget)
        self.signup_label.setStyleSheet("color: blue;")
        self.signup_label.setText("Signup")
        self.signup_layout.addWidget(self.signup_label)

        self.setCentralWidget(self.central_widget)

        # Signals
        self.signup_label.mousePressEvent = self.open_register

    def open_register(self, event):
        self.close()
        self.register_window.show()

    def open_dashboard(self):
        self.dashboard_window = DashboardPage()
        self.dashboard_window.show()
        self.close()

    def login_user(self):
        # Get input values
        email = self.email_input.text()
        password = self.password_input.text()

        # Validate inputs
        if not email or not password:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Both fields are required!")
            return

        # Validate email format
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            QtWidgets.QMessageBox.warning(self, "Invalid Email",
                                          '''
The email must contain '@' and '.'  
For example: test@example.com
                                          ''')
            return

        # Check credentials in the database
        try:
            connection = sqlite3.connect("users.db")
            cursor = connection.cursor()

            # Retrieve the stored hashed password for the given email
            # Retrieve the stored hashed password for the given email
            cursor.execute("""
                    SELECT id, username, password, picture FROM users WHERE email = ?
                """, (email,))
            result = cursor.fetchone()
            connection.close()

            if result is None:
                print("No such user found!")
                return None

            user_id, username, stored_password, picture = result

            session.picture = picture

            # Verify the provided password against the stored hash
            if session.pwd_context.verify(password, stored_password):
                session.start_session(user_id, username, email)
                QtWidgets.QMessageBox.information(self, "Success", "Login successful!")
                self.open_dashboard()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Invalid email or password!")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
