import sqlite3

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QFrame, QLabel, QLineEdit,
    QPushButton, QCheckBox, QHBoxLayout, QMessageBox
)

from utils import session


def toggle_password_visibility(show: bool, *inputs):
    """Toggle visibility of password fields."""
    for input_field in inputs:
        input_field.setEchoMode(QLineEdit.Normal if show else QLineEdit.Password)


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        # Create a Scroll Area for Settings
        settings_page = QScrollArea()
        settings_page.setWidgetResizable(True)
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)

        # Change Password Section
        change_password_card = QFrame()
        change_password_card.setStyleSheet("""
            background-color: #F7F9F9; 
            border-radius: 8px; 
            margin: 10px; 
            padding: 20px;
        """)
        change_password_layout = QVBoxLayout(change_password_card)

        change_password_label = QLabel("Change Password")
        change_password_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50; margin-bottom: 10px;")

        # New Password Section
        new_password_layout = QHBoxLayout()
        new_password_label = QLabel("New Password:")
        new_password_label.setStyleSheet("font-size: 14px; color: #7F8C8D;")
        new_password_input = QLineEdit()
        new_password_input.setEchoMode(QLineEdit.Password)
        new_password_input.setStyleSheet("""
            padding: 8px; 
            border: none; 
            border-bottom: 2px solid #BDC3C7; 
            background-color: transparent; 
            color: black;
        """)

        new_password_layout.addWidget(new_password_label)
        new_password_layout.addWidget(new_password_input)

        # Confirm Password Section
        confirm_password_layout = QHBoxLayout()
        confirm_password_label = QLabel("Confirm Password:")
        confirm_password_label.setStyleSheet("font-size: 14px; color: #7F8C8D;")
        confirm_password_input = QLineEdit()
        confirm_password_input.setEchoMode(QLineEdit.Password)
        confirm_password_input.setStyleSheet("""
            padding: 8px; 
            border: none; 
            border-bottom: 2px solid #BDC3C7; 
            background-color: transparent; 
            color: black;
        """)

        confirm_password_layout.addWidget(confirm_password_label)
        confirm_password_layout.addWidget(confirm_password_input)

        # Show Password Toggle
        show_password_checkbox = QCheckBox("Show Password")
        show_password_checkbox.setStyleSheet("font-size: 14px; color: #7F8C8D;")
        show_password_checkbox.stateChanged.connect(
            lambda: toggle_password_visibility(
                show_password_checkbox.isChecked(), new_password_input, confirm_password_input
            )
        )

        # Change Password Button
        change_password_button = QPushButton("Change Password")
        change_password_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB; 
                color: white; 
                padding: 10px 20px; 
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        change_password_button.clicked.connect(
            lambda: self.change_password(new_password_input, confirm_password_input)
        )

        change_password_layout.addWidget(change_password_label)
        change_password_layout.addLayout(new_password_layout)
        change_password_layout.addLayout(confirm_password_layout)
        change_password_layout.addWidget(show_password_checkbox)
        change_password_layout.addWidget(change_password_button)

        change_password_card.setLayout(change_password_layout)
        settings_layout.addWidget(change_password_card)

        # Main Layout for the Page
        settings_widget.setLayout(settings_layout)
        settings_page.setWidget(settings_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(settings_page)
        self.setLayout(main_layout)

    def change_password(self, new_password_input, confirm_password_input):
        """Validate and change password."""
        new_password = new_password_input.text()
        confirm_password = confirm_password_input.text()

        if len(new_password) < 6:
            self.show_error_message("Password must be at least 6 characters long.")
            return
        if new_password != confirm_password:
            self.show_error_message("Passwords do not match.")
            return

        connection = sqlite3.connect('users.db')

        cursor = connection.cursor()

        # Assuming password is successfully changed
        cursor.execute("""
               SELECT password FROM users WHERE id = ?
           """, (session.user_id,))
        result = cursor.fetchone()
        connection.close()

        if result is None:
            QMessageBox.warning(self, "Error", "User not found!")
            return

        stored_password = result[0]

        # Verify current password
        if not session.pwd_context.verify(new_password_input, stored_password):
            QMessageBox.warning(self, "Error", "Current password is incorrect!")
            return

        # Hash new password
        hashed_new_password = session.pwd_context.hash(new_password)

        # Update password in the database
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute("""
               UPDATE users SET password = ? WHERE id = ?
           """, (hashed_new_password, session.user_id))
        connection.commit()
        connection.close()
        self.show_success_message("Password changed successfully!")

    def show_error_message(self, message):
        """Show error message in a pop-up."""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.warning(self, "Validation Error", message)

    def show_success_message(self, message):
        """Show success message in a pop-up."""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Success", message)
