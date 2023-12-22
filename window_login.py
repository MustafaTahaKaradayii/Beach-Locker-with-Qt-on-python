from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from class_user import User
from window_boxes import BoxesWindow
from window_signup import SignupWindow

from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Title and Main Layout as Vertical:
        self.setWindowTitle('BeachBox Authentication Window')
        self.layout = QVBoxLayout()


        # Username Widgets:
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)


        # Password Widgets:
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)





        # Log In Button
        self.login_button = QPushButton('Log In')
        self.layout.addWidget(self.login_button)



        # Sign Up Button
        self.signup_button = QPushButton('Sign Up')
        self.layout.addWidget(self.signup_button)


        # Button Click Actions:
        self.login_button.clicked.connect(self.log_in_clicked)
        self.signup_button.clicked.connect(self.sign_up_clicked)
    

        # Show Window:
        self.setLayout(self.layout)
        self.show()


    # When Log In Clicked
    def log_in_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = User.authenticate_user(username, password)

        if user:
            self.close()
            self.open_boxes_window(user)
            print("Works")
        else:
            self.username_input.clear()
            self.password_input.clear()
            self.show_alert_message("Invalid username or password.")
            



    # When Sign Up Clicked
    def sign_up_clicked(self):
        # Add your desired action here for the sign-up functionality
        self.close()
        self.open_signup_window()

   # Show alert message function
    def show_alert_message(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.exec_()
    
    def open_boxes_window(self, user):
        self.boxes_window = BoxesWindow(user)
        self.boxes_window.show()

    def open_signup_window(self):
        self.signup_window = SignupWindow()
        self.signup_window.show()
