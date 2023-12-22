
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtCore import pyqtSlot
import bcrypt
from datetime import datetime
from class_box import Box
from class_user import User

class BoxesWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        # (self, username, email, password, user_type, user_id=None):
        self.boxes = Box.load_boxes()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('BeachBox Boxes Window')
        self.layout = QVBoxLayout(self)
        
        
        # user info
        self.user_layout = QVBoxLayout()
        self.user_layout.addWidget(QLabel(f"User Name: {self.user.username}"))
        self.user_layout.addWidget(QLabel(f"User Email: {self.user.email}"))
        self.user_layout.addWidget(QLabel(f"User Type: {self.user.user_type}"))


        # Grid layout for boxes
        self.grid_layout = QGridLayout()
        self.box_buttons = {}

        for i in range(100):
            box_button = QPushButton(f'Box {i + 1}')
            box_button.clicked.connect(self.handle_box_click)
            box_button.setStyleSheet("background-color: green")
            self.grid_layout.addWidget(box_button, i // 10, i % 10)
            self.box_buttons[i] = box_button



        self.layout.addLayout(self.user_layout)
        self.layout.addLayout(self.grid_layout)
        self.setLayout(self.layout)
        self.update_boxes_status()
        self.show()


    #carry into box class and return true or false (!)
    def update_boxes_status(self):
        for box in self.boxes:
            box_id = box['box_id']
            if box['user_id'] is not None:
                self.box_buttons[box_id - 1].setStyleSheet("background-color: red")
            else:
                self.box_buttons[box_id - 1].setStyleSheet("background-color: green")


    @pyqtSlot()
    def handle_box_click(self):
        button = self.sender()
        box_id = int(button.text().split(' ')[1]) - 1
        box = self.boxes[box_id]
        if box['user_id'] is not None:
            if box['user_id'] == self.user.id:
                self.end_rental(box_id)
            elif (self.user.user_type == "admin"):
                self.end_rental(box_id)
            else:
                self.show_alert_message("This box is already rented by another user.")
        else:
            self.start_rental(box_id)


    #carry into box class (!)
    def start_rental(self, box_id):
        password, ok = QInputDialog.getText(self, 'Set Box Password', 'Enter a password for the box:')
        if ok and password:
            self.boxes[box_id]['password'] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            self.boxes[box_id]['user_id'] = self.user.id
            self.boxes[box_id]['start_time'] = datetime.now().isoformat()
            self.update_boxes_status()
            Box.save_boxes(self.boxes)

    def end_rental(self, box_id):
        box = self.boxes[box_id]

        if (self.user.user_type == "admin"):
            duration = (datetime.now() - datetime.fromisoformat(box['start_time'])).total_seconds()
            price = 1 + 0.25 * (duration // 60)  # Assuming duration is in seconds
            QMessageBox.information(self, 'Rental Ended', f'Customer\'s rental lasted {duration} seconds and cost €{price:.2f}')
            box['user_id'] = None
            box['password'] = None
            box['start_time'] = None
            self.update_boxes_status()
            Box.save_boxes(self.boxes)
        else:
            password, ok = QInputDialog.getText(self, 'Unlock Box', 'Enter your password:', QLineEdit.Password)
            # BY USER
            if ok and bcrypt.checkpw(password.encode('utf-8'), box['password'].encode('utf-8')):
                duration = (datetime.now() - datetime.fromisoformat(box['start_time'])).total_seconds()
                price = 1 + 0.25 * (duration // 60)  # Assuming duration is in seconds
                QMessageBox.information(self, 'Rental Ended', f'Your rental lasted {duration} seconds and cost €{price:.2f}')
                box['user_id'] = None
                box['password'] = None
                box['start_time'] = None
                self.update_boxes_status()
                Box.save_boxes(self.boxes)
            else:
                self.show_alert_message("Incorrect password.")


    def show_alert_message(self, message):
        alert = QMessageBox()
        alert.setText(message)
        alert.exec_()



