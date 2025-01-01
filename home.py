from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QPushButton
from PyQt5.QtCore import Qt


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout for the home page
        main_layout = QVBoxLayout()

        # Header Section with a Welcome message
        header_layout = QHBoxLayout()
        welcome_label = QLabel("Welcome Back, User!")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50;")
        header_layout.addWidget(welcome_label, alignment=Qt.AlignLeft)

        # Add a small "Quick Access" or "Recent Activity" message
        recent_activity_label = QLabel("Quick Overview: Recent Events and Activities")
        recent_activity_label.setStyleSheet("font-size: 16px; color: #7F8C8D;")
        header_layout.addWidget(recent_activity_label, alignment=Qt.AlignRight)

        main_layout.addLayout(header_layout)

        # Create a summary stats section
        stats_layout = QGridLayout()

        # Dummy stats for demonstration
        event_count_frame = QFrame()
        event_count_frame.setStyleSheet("""
            background-color: #3498DB; 
            color: white; 
            border-radius: 8px; 
            padding: 20px;
        """)
        event_count_label = QLabel("Total Events")
        event_count_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        event_count_value = QLabel("25")  # Example event count
        event_count_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        event_count_frame_layout = QVBoxLayout(event_count_frame)
        event_count_frame_layout.addWidget(event_count_label)
        event_count_frame_layout.addWidget(event_count_value)

        stats_layout.addWidget(event_count_frame, 0, 0, 1, 1)

        upcoming_events_frame = QFrame()
        upcoming_events_frame.setStyleSheet("""
            background-color: #F39C12; 
            color: white; 
            border-radius: 8px; 
            padding: 20px;
        """)
        upcoming_events_label = QLabel("Upcoming Events")
        upcoming_events_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        upcoming_events_value = QLabel("5")  # Example upcoming events
        upcoming_events_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        upcoming_events_frame_layout = QVBoxLayout(upcoming_events_frame)
        upcoming_events_frame_layout.addWidget(upcoming_events_label)
        upcoming_events_frame_layout.addWidget(upcoming_events_value)

        stats_layout.addWidget(upcoming_events_frame, 1, 0, 1, 1)

        # New Section: Recent Activities
        recent_activities_frame = QFrame()
        recent_activities_frame.setStyleSheet("""
            background-color: #9B59B6; 
            color: white; 
            border-radius: 8px; 
            padding: 20px;
        """)
        recent_activities_label = QLabel("Recent Activities")
        recent_activities_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        recent_activities_value = QLabel("2")  # Example recent activities count
        recent_activities_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        recent_activities_frame_layout = QVBoxLayout(recent_activities_frame)
        recent_activities_frame_layout.addWidget(recent_activities_label)
        recent_activities_frame_layout.addWidget(recent_activities_value)

        stats_layout.addWidget(recent_activities_frame, 2, 0, 1, 1)

        main_layout.addLayout(stats_layout)

        # Quick Action Buttons
        actions_layout = QHBoxLayout()

        create_event_button = QPushButton("Create New Event")
        create_event_button.setStyleSheet("""
            background-color: #3498DB; 
            color: white; 
            padding: 12px 20px; 
            border-radius: 5px;
        """)

        view_events_button = QPushButton("View All Events")
        view_events_button.setStyleSheet("""
            background-color: #2ECC71; 
            color: white; 
            padding: 12px 20px; 
            border-radius: 5px;
        """)

        actions_layout.addWidget(create_event_button)
        actions_layout.addWidget(view_events_button)

        main_layout.addLayout(actions_layout)

        # Set main layout
        self.setLayout(main_layout)