import sqlite3
from datetime import datetime
from passlib.context import CryptContext
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QApplication


class NotificationManager:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(QIcon("icon.png"))  # Use your app's icon
        self.tray_icon.show()  # Ensure the tray icon is always visible

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_notifications)
        self.timer.start(60000)  # Check every 60 seconds

    def check_notifications(self):
        if not session.is_authenticated():
            return

        # Check for upcoming events
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT title, date, time 
                FROM events 
                WHERE user_id = ? 
                AND datetime(date || ' ' || time) > datetime('now') 
                AND datetime(date || ' ' || time) <= datetime('now', '+30 minutes')
            """, (session.user_id,))
            upcoming_events = cursor.fetchall()

            if upcoming_events:
                for event in upcoming_events:
                    title, date, time = event
                    self.show_notification(f"Upcoming Event: {title}", f"Scheduled for {date} at {time}")
        finally:
            connection.close()

    def show_notification(self, title, message):
        self.tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.Information,
            5000  # Display for 5 seconds
        )




def get_event_count(user_id):
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        # Query to count events for the specific user
        cursor.execute("""
            SELECT COUNT(*) FROM events WHERE user_id = ?
        """, (user_id,))
        count = cursor.fetchone()[0]

        connection.close()
        return count
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return 0


def get_upcoming_events(user_id):
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        # Query to get upcoming events
        cursor.execute("""
            SELECT title, description, date, time, venue 
            FROM events 
            WHERE user_id = ? AND date >= ? 
            ORDER BY date ASC, time ASC
        """, (user_id, datetime.now().date()))
        events = cursor.fetchall()

        connection.close()
        return events
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []


def get_all_events(user_id):
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        # Query to get upcoming events
        cursor.execute("""
            SELECT title, description, date, time, venue 
            FROM events 
            WHERE user_id = ? 
            ORDER BY date ASC, time ASC
        """, (user_id))
        events = cursor.fetchall()

        connection.close()
        return events
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []


class SessionManager:
    def __init__(self):
        self.user_id = None
        self.username = None
        self.email = None
        self.picture = None
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def start_session(self, user_id, username, email):
        self.user_id = user_id
        self.username = str(username).capitalize()
        self.email = email

    def end_session(self):
        self.user_id = None
        self.username = None
        self.email = None
        self.picture = None
        self.pwd_context = None

    def is_authenticated(self):
        return self.user_id is not None


session = SessionManager()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Start the notification manager
    notification_manager = NotificationManager()

    # Keep the application running
    sys.exit(app.exec_())
