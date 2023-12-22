from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
from class_user import User
from window_boxes import BoxesWindow


class SignupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Title and Main Layout as Vertical:
        self.setWindowTitle('BeachBox Signup Window')
        self.layout = QVBoxLayout()


        # FirstName Widgets:
        # self.firstname_label = QLabel('First Name:')
        # self.firstname_input = QLineEdit()
        # self.layout.addWidget(self.firstname_label)
        # self.layout.addWidget(self.firstname_input)


        # Last Name Widgets:
        # self.lastname_label = QLabel('Last Name:')
        # self.lastname_input = QLineEdit()
        # self.layout.addWidget(self.lastname_label)
        # self.layout.addWidget(self.lastname_input)


        # Phone Number Widgets:
        # self.phonenumber_label = QLabel('Phone Number:')
        # self.phonenumber_input = QLineEdit()
        # self.layout.addWidget(self.phonenumber_label)
        # self.layout.addWidget(self.phonenumber_input)

        # Username Widgets:
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)


        # Email Widgets:
        self.email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_input)


        # Password Widgets:
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)


        # Sign Up Button
        self.signup_button = QPushButton('Sign Up')
        self.layout.addWidget(self.signup_button)


        # Button Click Actions:
        self.signup_button.clicked.connect(self.sign_up_clicked)
    

        # Show Window:
        self.setLayout(self.layout)
        self.show()




    # When Sign Up Clicked
    def sign_up_clicked(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        result = User.create_user_entry(username, email, password)
        if result == 'invalid_email':
            self.show_alert_message("Invalid email format. Please enter a valid email address.")
        elif result is None:
            self.show_alert_message("Username or email already exists.")
        elif isinstance(result, User):
            self.close()
            self.open_boxes_window(result)
            self.username_input.clear()
            self.email_input.clear()
            self.password_input.clear()
        else:
            self.show_alert_message("An unexpected error occurred. Please try again.")
            
        
    # show alert message
    def show_alert_message(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.exec_()

    
    def open_boxes_window(self, user):
        self.boxes_window = BoxesWindow(user)
        self.boxes_window.show()