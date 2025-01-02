from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QPushButton

import utils


class ViewEventsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("All Events")
        self.resize(600, 400)

        main_layout = QVBoxLayout()

        # Title
        title_label = QLabel("All Events")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Scroll Area for Events
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Fetch events from the database
        events = utils.get_all_events(utils.session.user_id)
        if events:
            for event in events:
                event_frame = QFrame()
                event_frame.setStyleSheet("""
                    background-color: #ECF0F1; 
                    border: 1px solid #BDC3C7; 
                    border-radius: 8px; 
                    margin: 10px; 
                    padding: 15px;
                """)
                event_layout = QVBoxLayout(event_frame)

                # Display event details
                title_label = QLabel(f"Title: {event[1]}")
                title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
                event_layout.addWidget(title_label)

                description_label = QLabel(f"Description: {event[2]}")
                event_layout.addWidget(description_label)

                date_label = QLabel(f"Date: {event[3]}")
                event_layout.addWidget(date_label)

                time_label = QLabel(f"Time: {event[4]}")
                event_layout.addWidget(time_label)

                venue_label = QLabel(f"Venue: {event[5]}")
                event_layout.addWidget(venue_label)

                scroll_layout.addWidget(event_frame)
        else:
            no_events_label = QLabel("No events found.")
            no_events_label.setStyleSheet("font-size: 16px; color: #7F8C8D;")
            scroll_layout.addWidget(no_events_label, alignment=Qt.AlignCenter)

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Back Button
        back_button = QPushButton("Back to Home")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB; 
                color: white; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        back_button.clicked.connect(self.close)
        main_layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
