
import json
import bcrypt
from datetime import datetime

class Box:
    def __init__(self, box_id):
        self.box_id = box_id
        self.user_id = None
        self.password = None
        self.start_time = None

    def rent(self, user_id, password):
        self.user_id = user_id
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.start_time = datetime.now().isoformat()

    def end_rental(self, password):
        if bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')):
            duration = (datetime.now() - datetime.fromisoformat(self.start_time)).total_seconds()
            self.user_id = None
            self.password = None
            self.start_time = None
            return duration
        else:
            raise ValueError("Incorrect password.")



    @staticmethod
    def load_boxes():
        # Load the boxes from the json file
        try:
            with open('boxes.json', 'r') as file:
                data = json.load(file)["Boxes"]
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            # If there is an error or file not found, return an empty list
            return [{"box_id": i, "user_id": None, "password": None, "start_time": None} for i in range(1, 101)]



    @staticmethod
    def save_boxes(boxes):
        with open('boxes.json', 'w') as file:
            json.dump({"Boxes": boxes}, file, indent=4)