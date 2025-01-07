from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QListWidget, QStackedWidget,
    QFrame, QWidget, QPushButton, QSpacerItem, QSizePolicy, QMessageBox
)

from events import EventsPage
from home import HomePage
from user_profile import ProfilePage
from utils import session
from settings import SettingsPage


class DashboardPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Event Management Dashboard")
        self.setGeometry(100, 100, 900, 600)

        # Main Layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            background-color: #34495E;
            border-right: 2px solid #2C3E50;
        """)
        sidebar_layout = QVBoxLayout(sidebar)

        menu = QListWidget()
        menu.setStyleSheet("""
            QListWidget {
                background-color: #2C3E50;
                color: white;
                font-size: 14px;
                border: none;
                padding: 10px;
            }
            QListWidget::item {
                margin: 10px 0;
                padding: 8px;
                border-radius: 5px;
            }
            QListWidget::item:selected {
                background-color: #1ABC9C;
                color: black;
            }
            QListWidget::item:hover {
                background-color: #16A085;
                color: white;
            }
        """)

        # Add menu items
        menu_items = ["Dashboard", "Events", "Settings", "Profile"]
        for item in menu_items:
            menu.addItem(item)
        sidebar_layout.addWidget(menu)

        # Spacer to push logout button to the bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        sidebar_layout.addSpacerItem(spacer)

        # Logout Button
        logout_button = QPushButton("Logout")
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        logout_button.clicked.connect(self.logout)
        sidebar_layout.addWidget(logout_button)

        # Main Content Area
        main_content = QStackedWidget()
        main_content.addWidget(HomePage())
        main_content.addWidget(EventsPage())
        main_content.addWidget(SettingsPage())
        main_content.addWidget(ProfilePage())

        # Menu Navigation
        menu.currentRowChanged.connect(main_content.setCurrentIndex)

        # Add Sidebar and Content to Layout
        content_layout = QVBoxLayout()
        content_layout.addWidget(main_content)

        main_layout.addWidget(sidebar)
        main_layout.addLayout(content_layout)

    def logout(self):
        session.end_session()
        QMessageBox.information(None, "Logout Successful", "You have been logged out.")
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    dashboard = DashboardPage()
    dashboard.show()
    app.exec_()
