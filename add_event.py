import sqlite3
from PyQt5 import QtWidgets
from utils import session


class AddEventPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Add Event")
        self.resize(400, 400)  # Adjusted height for additional fields

        layout = QtWidgets.QVBoxLayout()

        # Title Input
        self.title_input = QtWidgets.QLineEdit()
        self.title_input.setPlaceholderText("Event Title")
        layout.addWidget(self.title_input)

        # Description Input
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Event Description")
        layout.addWidget(self.description_input)

        # Date Input
        self.date_input = QtWidgets.QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(self.date_input)

        # Time Input
        self.time_input = QtWidgets.QTimeEdit()
        self.time_input.setDisplayFormat("HH:mm")
        layout.addWidget(self.time_input)

        # Venue Input
        self.venue_input = QtWidgets.QLineEdit()
        self.venue_input.setPlaceholderText("Event Venue")
        layout.addWidget(self.venue_input)

        # Add Event Button
        self.add_event_button = QtWidgets.QPushButton("Add Event")
        self.add_event_button.clicked.connect(self.add_event)
        layout.addWidget(self.add_event_button)

        # Cancel Button
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close_page)
        layout.addWidget(self.cancel_button)

        # Set Layout and Styling
        self.setLayout(layout)
        self.setStyleSheet("""
            QLineEdit, QTextEdit, QDateEdit, QTimeEdit {
                font-size: 14px; 
                padding: 5px; 
                border: 1px solid #BDC3C7; 
                border-radius: 5px;
            }
            QPushButton {
                font-size: 14px; 
                padding: 8px; 
                background-color: #3498DB; 
                color: white; 
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)

    def add_event(self):
        if not session.is_authenticated():
            QtWidgets.QMessageBox.warning(None, "Access Denied", "You must log in to add events.")
            return

        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()
        date = self.date_input.text()
        time = self.time_input.text()
        venue = self.venue_input.text().strip()

        if not title or not description or not venue:
            QtWidgets.QMessageBox.warning(None, "Missing Fields", "All fields must be filled out.")
            return

        try:
            with sqlite3.connect("users.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO events (user_id, title, description, date, time, venue)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (session.user_id, title, description, date, time, venue))
                connection.commit()

            QtWidgets.QMessageBox.information(None, "Event Added", "Your event has been successfully added!")
            self.close()

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(None, "Database Error", "An error occurred while adding the event. Please try again.")

    def close_page(self):
        reply = QtWidgets.QMessageBox.question(
            self, "Confirm Cancel", "Are you sure you want to cancel adding this event?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            super().close()
