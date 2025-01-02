from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
import sqlite3

from event_detail import EventDetailsPage
from utils import session


def fetch_events():
    try:
        with sqlite3.connect("users.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT title, date, id FROM events WHERE user_id = ?
            """, (session.user_id,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []


class EventsPage(QWidget):
    event_modified = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("My Events")
        self.resize(500, 600)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Scroll Area for Events
        self.events_scroll = QScrollArea()
        self.events_scroll.setWidgetResizable(True)
        self.events_widget = QWidget()
        self.events_layout = QVBoxLayout(self.events_widget)
        self.events_layout.setContentsMargins(10, 10, 10, 10)
        self.events_layout.setSpacing(15)

        # Populate Events
        self.refresh_events()

        # Set up the scroll area
        self.events_widget.setLayout(self.events_layout)
        self.events_scroll.setWidget(self.events_widget)
        self.main_layout.addWidget(self.events_scroll)

    def create_event_card(self, title, date, event_id):
        """Creates a styled event card."""
        event_card = QFrame()
        event_card.setStyleSheet("""
            QFrame {
                background-color: #ECF0F1; 
                border: 1px solid #BDC3C7; 
                border-radius: 8px; 
                padding: 15px;
            }
        """)
        event_card_layout = QVBoxLayout(event_card)
        event_card_layout.setContentsMargins(10, 10, 10, 10)
        event_card_layout.setSpacing(5)

        # Title Label
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2C3E50;")
        event_card_layout.addWidget(title_label)

        # Date Label
        date_label = QLabel(f"Date: {date}")
        date_label.setStyleSheet("font-size: 14px; color: #7F8C8D;")
        event_card_layout.addWidget(date_label)

        # View Details Button
        view_details_button = QPushButton("View Details")
        view_details_button.setStyleSheet("""
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
        view_details_button.clicked.connect(lambda: self.open_event_details(event_id))
        event_card_layout.addWidget(view_details_button, alignment=Qt.AlignRight)

        return event_card

    def open_event_details(self, event_id):
        """Navigates to the event details page."""
        self.event_details_page = EventDetailsPage(event_id)
        self.event_details_page.event_modified.connect(self.refresh_events)
        self.event_modified.emit()
        self.event_details_page.show()

    def refresh_events(self):
        """Refresh the event list."""
        # Clear the current layout
        for i in reversed(range(self.events_layout.count())):
            widget = self.events_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Fetch updated events
        self.events = fetch_events()

        # Repopulate the layout
        if not self.events:
            # No events placeholder
            no_event_label = QLabel("No events found.")
            no_event_label.setStyleSheet("font-size: 16px; color: #7F8C8D; margin: 10px;")
            no_event_label.setAlignment(Qt.AlignCenter)
            self.events_layout.addWidget(no_event_label)
        else:
            for event in self.events:
                title, date, event_id = event
                self.events_layout.addWidget(self.create_event_card(title, date, event_id))
