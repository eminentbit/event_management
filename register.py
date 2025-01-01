from PyQt5 import QtWidgets, QtCore


class RegisterPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("RegisterWindow")
        self.resize(500, 600)

        # Central Widget
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")

        # Full Name Input
        self.name_input_widget = QtWidgets.QWidget(self.central_widget)
        self.name_input_widget.setGeometry(QtCore.QRect(50, 50, 341, 41))
        self.name_input_layout = QtWidgets.QHBoxLayout(self.name_input_widget)
        self.name_input_layout.setContentsMargins(0, 0, 0, 0)

        self.name_label = QtWidgets.QLabel(self.name_input_widget)
        self.name_label.setText("Full Name:")
        self.name_input_layout.addWidget(self.name_label)

        self.name_input = QtWidgets.QLineEdit(self.name_input_widget)
        self.name_input_layout.addWidget(self.name_input)

        # Email Input
        self.email_input_widget = QtWidgets.QWidget(self.central_widget)
        self.email_input_widget.setGeometry(QtCore.QRect(50, 120, 341, 41))
        self.email_input_layout = QtWidgets.QHBoxLayout(self.email_input_widget)
        self.email_input_layout.setContentsMargins(0, 0, 0, 0)

        self.email_label = QtWidgets.QLabel(self.email_input_widget)
        self.email_label.setText("Email:")
        self.email_input_layout.addWidget(self.email_label)

        self.email_input = QtWidgets.QLineEdit(self.email_input_widget)
        self.email_input_layout.addWidget(self.email_input)

        # Password Input
        self.password_input_widget = QtWidgets.QWidget(self.central_widget)
        self.password_input_widget.setGeometry(QtCore.QRect(50, 190, 341, 41))
        self.password_input_layout = QtWidgets.QHBoxLayout(self.password_input_widget)
        self.password_input_layout.setContentsMargins(0, 0, 0, 0)

        self.password_label = QtWidgets.QLabel(self.password_input_widget)
        self.password_label.setText("Password:")
        self.password_input_layout.addWidget(self.password_label)

        self.password_input = QtWidgets.QLineEdit(self.password_input_widget)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input_layout.addWidget(self.password_input)

        # Confirm Password Input
        self.confirm_password_widget = QtWidgets.QWidget(self.central_widget)
        self.confirm_password_widget.setGeometry(QtCore.QRect(50, 260, 341, 41))
        self.confirm_password_layout = QtWidgets.QHBoxLayout(self.confirm_password_widget)
        self.confirm_password_layout.setContentsMargins(0, 0, 0, 0)

        self.confirm_password_label = QtWidgets.QLabel(self.confirm_password_widget)
        self.confirm_password_label.setText("Confirm Password:")
        self.confirm_password_layout.addWidget(self.confirm_password_label)

        self.confirm_password_input = QtWidgets.QLineEdit(self.confirm_password_widget)
        self.confirm_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_layout.addWidget(self.confirm_password_input)

        # Buttons
        self.register_button = QtWidgets.QPushButton(self.central_widget)
        self.register_button.setGeometry(QtCore.QRect(50, 330, 100, 30))
        self.register_button.setText("Register")

        self.cancel_button = QtWidgets.QPushButton(self.central_widget)
        self.cancel_button.setGeometry(QtCore.QRect(300, 330, 100, 30))
        self.cancel_button.setText("Cancel")

        self.cancel_button.mousePressEvent = self.close

        # Login Section
        self.login_widget = QtWidgets.QWidget(self.central_widget)
        self.login_widget.setGeometry(QtCore.QRect(130, 400, 201, 31))
        self.login_layout = QtWidgets.QHBoxLayout(self.login_widget)
        self.login_layout.setContentsMargins(0, 0, 0, 0)

        self.login_prompt_label = QtWidgets.QLabel(self.login_widget)
        self.login_prompt_label.setText("Already have an account?")
        self.login_layout.addWidget(self.login_prompt_label)

        self.login_label = QtWidgets.QLabel(self.login_widget)
        self.login_label.setStyleSheet("color: blue;")
        self.login_label.setText("Login")
        self.login_layout.addWidget(self.login_label)

        self.setCentralWidget(self.central_widget)

        # Signals
        self.login_label.mousePressEvent = self.open_login

    def open_login(self, event):
        self.close()
        self.login_window.show()

    def close_page(self, event):
        self.close()
