from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame, QLabel, QPushButton
from PyQt5.QtCore import Qt


class EventsPage(QWidget):
    def __init__(self):
        super().__init__()

        # Create a Scroll Area for Events
        events_page = QScrollArea()
        events_page.setWidgetResizable(True)
        events_widget = QWidget()
        events_layout = QVBoxLayout(events_widget)

        # Dummy Events
        for i in range(10):  # Example: 10 events
            event_card = QFrame()
            event_card.setStyleSheet("""
                background-color: #ECF0F1; 
                border: 1px solid #BDC3C7; 
                border-radius: 8px; 
                margin: 10px; 
                padding: 15px;
            """)
            event_card_layout = QVBoxLayout(event_card)

            event_name = QLabel(f"Event {i + 1}")
            event_name.setStyleSheet("font-size: 16px; font-weight: bold; color: #2C3E50;")

            event_details = QLabel(f"Details for Event {i + 1}: Date, Time, Venue")
            event_details.setStyleSheet("font-size: 12px; color: #7F8C8D; margin-top: 5px;")

            view_details_button = QPushButton("View Details")
            view_details_button.setStyleSheet("""
                QPushButton {
                    background-color: #3498DB; 
                    color: white; 
                    padding: 8px 12px; 
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #2980B9;
                }
            """)
            view_details_button.setFixedWidth(120)

            event_card_layout.addWidget(event_name)
            event_card_layout.addWidget(event_details)
            event_card_layout.addWidget(view_details_button, alignment=Qt.AlignRight)
            event_card.setLayout(event_card_layout)

            events_layout.addWidget(event_card)

        events_widget.setLayout(events_layout)
        events_page.setWidget(events_widget)

        # Main Layout for the Page
        main_layout = QVBoxLayout()
        main_layout.addWidget(events_page)
        self.setLayout(main_layout)
