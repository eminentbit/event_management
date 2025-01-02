from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QFrame, QPushButton

import utils
from add_event import AddEventPage
from utils import session
from view_event import ViewEventsPage


def create_action_button(text, color, callback):
    button = QPushButton(text)
    button.setStyleSheet(f"""
        QPushButton {{
            background-color: {color}; 
            color: white; 
            padding: 12px 20px; 
            border-radius: 5px;
        }}
        QPushButton:hover {{
            background-color: {color};
            opacity: 0.85;
        }}
    """)
    button.clicked.connect(callback)
    return button


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout for the home page
        main_layout = QVBoxLayout()

        # Header Section with a Welcome message
        header_layout = QHBoxLayout()
        welcome_label = QLabel(f"Welcome Back, {session.username}!")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        header_layout.addWidget(welcome_label, alignment=Qt.AlignLeft)

        recent_activity_label = QLabel("Quick Overview: Recent Events and Activities")
        recent_activity_label.setStyleSheet("font-size: 16px; color: #7F8C8D;")
        header_layout.addWidget(recent_activity_label, alignment=Qt.AlignRight)

        main_layout.addLayout(header_layout)

        # Stats Section
        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)

        event_count_frame = self.create_stat_frame(
            "Total Events",
            utils.get_event_count(session.user_id),
            "#3498DB"
        )
        stats_layout.addWidget(event_count_frame, 0, 0)

        upcoming_events_frame = self.create_stat_frame(
            "Upcoming Events",
            len(utils.get_upcoming_events(session.user_id)),
            "#F39C12"
        )
        stats_layout.addWidget(upcoming_events_frame, 0, 1)

        recent_activities_frame = self.create_stat_frame(
            "Recent Activities",
            "2",  # Example
            "#9B59B6"
        )
        stats_layout.addWidget(recent_activities_frame, 0, 2)

        main_layout.addLayout(stats_layout)

        # Quick Action Buttons
        actions_layout = QHBoxLayout()
        create_event_button = create_action_button("Create New Event", "#3498DB", self.open_add_event)
        view_events_button = create_action_button("View All Events", "#2ECC71", self.open_view_events)

        actions_layout.addWidget(create_event_button)
        actions_layout.addWidget(view_events_button)
        main_layout.addLayout(actions_layout)

        self.setLayout(main_layout)

    @staticmethod
    def create_stat_frame(title, value, bg_color):
        frame = QFrame()
        frame.setStyleSheet(f"""
            background-color: {bg_color}; 
            color: white; 
            border-radius: 8px; 
            padding: 20px;
        """)
        layout = QVBoxLayout(frame)
        label = QLabel(title)
        label.setStyleSheet("font-size: 18px; font-weight: bold;")
        value_label = QLabel(str(value))
        value_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(label)
        layout.addWidget(value_label)
        return frame

    def open_add_event(self):
        self.add_event_window = AddEventPage()
        self.add_event_window.show()

    def open_view_events(self):
        self.view_events_window = ViewEventsPage()
        self.view_events_window.show()
