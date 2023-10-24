from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

def security():
    class PasswordProtectedProgram(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("LOGIN")
            self.setWindowIcon(QIcon("lock_icon.png"))
            self.setGeometry(100, 700, 400, 200)
            self.label = QLabel("Login to Access Library", self)
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setFont(QFont("Arial", 14))

            self.username_input = QLineEdit(self)
            self.username_input.setPlaceholderText("Username")

            self.password_input = QLineEdit(self)
            self.password_input.setEchoMode(QLineEdit.Password)
            self.password_input.setPlaceholderText("Password")

            self.login_button = QPushButton("Login", self)
            self.login_button.clicked.connect(self.authenticate)

            layout = QVBoxLayout(self)
            layout.addWidget(self.label)
            layout.addWidget(self.username_input)
            layout.addWidget(self.password_input)
            layout.addWidget(self.login_button)
            layout.addStretch()

        def authenticate(self):
            entered_username = self.username_input.text()
            entered_password = self.password_input.text()

            # Replace 'admin' with your desired username and password
            if entered_username == "admin" and entered_password == "123456":
                QMessageBox.information(self, "Success", "Authentication Successful!")
                # You can open the protected program here
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Incorrect Username or Password!")

    app = QApplication([])  # Create a QApplication instance
    window = PasswordProtectedProgram()  # Create an instance of your PasswordProtectedProgram
    window.show()  # Display the window

    app.exec_()  # Start the application event loop

security()
