from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QPainterPath, QPainter
from PyQt5.QtCore import Qt

class ProfilePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Profile Picture Placeholder
        self.profile_picture_label = QLabel()
        self.profile_picture_label.setFixedSize(150, 150)
        self.profile_picture_label.setStyleSheet("""
            border-radius: 75px; 
            border: 2px solid #2C3E50; 
            background-color: #BDC3C7;
            color: #7F8C8D;
            font-size: 12px;
            font-weight: bold;
        """)
        self.profile_picture_label.setAlignment(Qt.AlignCenter)
        self.profile_picture_label.setText("No Picture")

        # Upload Button
        upload_button = QPushButton("Upload Picture")
        upload_button.setStyleSheet("""
            QPushButton {
                background-color: #1ABC9C;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
        """)
        upload_button.clicked.connect(self.upload_picture)

        # Spacer between sections
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # User Info Section
        user_info = QLabel("""
            <p style="font-size: 16px; font-weight: bold; color: #2C3E50;">John Doe</p>
            <p style="font-size: 14px; color: #7F8C8D;">Email: johndoe@example.com</p>
        """)
        user_info.setAlignment(Qt.AlignCenter)
        user_info.setStyleSheet("background-color: #ECF0F1; border-radius: 10px; padding: 10px;")

        # Add Widgets to Layout
        layout.addWidget(self.profile_picture_label, alignment=Qt.AlignCenter)
        layout.addWidget(upload_button, alignment=Qt.AlignCenter)
        layout.addSpacerItem(spacer)
        layout.addWidget(user_info)

        self.setLayout(layout)

    def upload_picture(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Upload Profile Picture", "", "Images (*.png *.xpm *.jpg *.jpeg)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.set_rounded_profile_picture(pixmap)

    def set_rounded_profile_picture(self, pixmap):
        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        rounded_pixmap = QPixmap(150, 150)
        rounded_pixmap.fill(Qt.transparent)

        painter = QPainter(rounded_pixmap)
        path = QPainterPath()
        path.addEllipse(0, 0, 150, 150)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        self.profile_picture_label.setPixmap(rounded_pixmap)
        self.profile_picture_label.setStyleSheet("border-radius: 75px; border: 2px solid #2C3E50;")
