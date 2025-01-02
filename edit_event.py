import sqlite3
from datetime import datetime

from PyQt5.QtCore import QTime, QDate, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QTextEdit, QDateEdit, QTimeEdit,
    QPushButton, QMessageBox
)


def edit_event(event_id, title, description, date, time, venue):
    """
    Edit the details of an existing event.

    Args:
        event_id (int): The ID of the event to edit.
        title (str): The new title of the event.
        description (str): The new description of the event.
        date (str): The new date of the event in YYYY-MM-DD format.
        time (str): The new time of the event in HH:MM format.
        venue (str): The new venue of the event.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE events
            SET title = ?, description = ?, date = ?, time = ?, venue = ?
            WHERE id = ?
        """, (title, description, date, time, venue, event_id))
        connection.commit()

        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        connection.close()


class EditEventPage(QWidget):
    event_modified = pyqtSignal()  # Signal to notify parent when event is updated

    def __init__(self, event_id, current_details):
        super().__init__()
        self.event_id = event_id
        self.current_details = current_details

        self.setWindowTitle("Edit Event")
        self.resize(400, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title Input
        self.title_input = QLineEdit(self.current_details['title'])
        self.title_input.setPlaceholderText("Event Title")
        layout.addWidget(self.title_input)

        # Description Input
        self.description_input = QTextEdit(self.current_details['description'])
        self.description_input.setPlaceholderText("Event Description")
        layout.addWidget(self.description_input)

        # Date Input
        date_object = QDate.fromString(self.current_details['date'], "yyyy-MM-dd")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(date_object if date_object.isValid() else QDate.currentDate())
        layout.addWidget(self.date_input)

        # Time Input
        time_object = QTime.fromString(self.current_details['time'], "HH:mm")
        self.time_input = QTimeEdit()
        self.time_input.setTime(time_object if time_object.isValid() else QTime.currentTime())
        layout.addWidget(self.time_input)

        # Venue Input
        self.venue_input = QLineEdit(self.current_details['venue'])
        self.venue_input.setPlaceholderText("Event Venue")
        layout.addWidget(self.venue_input)

        # Save Button
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

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

    def save_changes(self):
        new_title = self.title_input.text()
        new_description = self.description_input.toPlainText()
        new_date = self.date_input.date().toString("yyyy-MM-dd")
        new_time = self.time_input.time().toString("HH:mm")
        new_venue = self.venue_input.text()

        if edit_event(self.event_id, new_title, new_description, new_date, new_time, new_venue):
            QMessageBox.information(self, "Success", "Event updated successfully!")
            self.event_modified.emit()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Failed to update the event.")
