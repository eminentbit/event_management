import sqlite3

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QLabel, QPushButton

from utils import session


class EventDetailsPage(QWidget):
    event_modified = pyqtSignal()
    def __init__(self, event_id):
        super().__init__()
        self.event_id = event_id
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Event Details")
        self.resize(400, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Fetch Event Details
        self.fetch_event_details()

        if not self.event_data:
            QMessageBox.critical(
                self, "Error", "Could not fetch event details. Please try again later."
            )
            self.close()
            return

        # Event Title
        self.title_label = QLabel(self.event_data['title'])
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Event Description
        self.description_label = QLabel(f"Description:\n{self.event_data['description']}")
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("font-size: 14px; color: #7F8C8D; margin-top: 10px;")
        layout.addWidget(self.description_label)

        # Event Date and Time
        self.datetime_label = QLabel(
            f"Date: {self.event_data['date']}\nTime: {self.event_data['time']}"
        )
        self.datetime_label.setStyleSheet("font-size: 14px; color: #7F8C8D; margin-top: 10px;")
        layout.addWidget(self.datetime_label)

        # Event Venue
        self.venue_label = QLabel(f"Venue: {self.event_data['venue']}")
        self.venue_label.setStyleSheet("font-size: 14px; color: #7F8C8D; margin-top: 10px;")
        layout.addWidget(self.venue_label)

        # Action Buttons
        button_layout = QVBoxLayout()

        # Edit Button
        edit_button = QPushButton("Edit Event")
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB; 
                color: white; 
                font-size: 14px; 
                border-radius: 5px; 
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        edit_button.clicked.connect(self.open_edit_event_page)
        button_layout.addWidget(edit_button)

        # Delete Button
        delete_button = QPushButton("Delete Event")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C; 
                color: white; 
                font-size: 14px; 
                border-radius: 5px; 
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        delete_button.clicked.connect(self.delete_event)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        self.layout().update()

    def fetch_event_details(self):
        """Fetch event details from the database."""
        try:
            with sqlite3.connect("users.db") as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT title, description, date, time, venue 
                    FROM events 
                    WHERE id = ? AND user_id = ?
                """, (self.event_id, session.user_id))
                result = cursor.fetchone()
                if result:
                    self.event_data = {
                        "title": result[0],
                        "description": result[1],
                        "date": result[2],
                        "time": result[3],
                        "venue": result[4]
                    }
                else:
                    self.event_data = None  # Event not found
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred while fetching event details: {e}")
            self.event_data = None
    def open_edit_event_page(self):
        """Open the edit event page."""
        from edit_event import EditEventPage
        self.edit_event_window = EditEventPage(self.event_id, self.event_data)
        self.event_modified.emit()
        self.edit_event_window.event_modified.connect(self.refresh_event_details)
        self.edit_event_window.show()

    def refresh_event_details(self):
        """Refresh the event details and update the UI."""
        self.fetch_event_details()  # Fetch updated details
        self.update_ui()  # Update UI elements

    def update_ui(self):
        """Update the UI with the latest event data."""
        self.title_label.setText(self.event_data["title"])
        self.description_label.setText(f"Description:\n{self.event_data['description']}")
        self.datetime_label.setText(
            f"Date: {self.event_data['date']}\nTime: {self.event_data['time']}"
        )
        self.venue_label.setText(f"Venue: {self.event_data['venue']}")

    def delete_event(self):
        """Delete the event from the database."""
        reply = QMessageBox.question(
            self,
            "Delete Event",
            "Are you sure you want to delete this event? This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                with sqlite3.connect("users.db") as connection:
                    cursor = connection.cursor()
                    cursor.execute("""
                        DELETE FROM events WHERE id = ? AND user_id = ?
                    """, (self.event_id, session.user_id))
                    connection.commit()
                QMessageBox.information(self, "Event Deleted", "The event has been successfully deleted.")
                self.close()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", f"An error occurred while deleting the event: {e}")
