import json
import bcrypt
import re


class User:

    def __init__(self, username, email, user_type,  user_id=None, password=None):

        if not password:
            self.id = user_id if user_id else self.get_next_id()
            self.username = username
            self.email = email
            self.user_type = user_type
        else:
            self.id = user_id if user_id else self.get_next_id()
            self.username = username
            self.email = email
            self.user_type = 'user'
            self.password_hash = self._hash_password(password)
            self.user_type = user_type
        

    def __str__(self):
            return f"User(username={self.username}, email={self.email}, user_type={self.user_type}, id={self.id})"
        

    @staticmethod
    def get_next_id():
        try:
            with open('users.json', 'r') as file:
                data = json.load(file)["Users"]
                if data:
                    return max(user['id'] for user in data) + 1
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return 1



    @staticmethod
    def is_unique(field, value):
        try:
            with open('users.json', 'r') as file:
                data = json.load(file)["Users"]
                return all(user[field] != value for user in data)
        except (json.JSONDecodeError, FileNotFoundError):
            return True

    # pwd hash
    def _hash_password(self, password):
        salt = bcrypt.gensalt()
        password = password.encode('utf-8')
        password_hash = bcrypt.hashpw(password, salt)
        return password_hash

    @staticmethod
    def is_valid_email(email):
        """Check if the email is in a valid format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


    @staticmethod
    def create_user_entry(username, email, password):

        #checks if e-mail is valid or not ends with .com or not?
        if not User.is_valid_email(email):
            return 'invalid_email'
        # checks if user name or email is taken or not
        if not User.is_unique('username', username):
            return 'username_exists'
        if not User.is_unique('email', email):
            return 'email_exists'

        user = User(username, email, "user", User.get_next_id(), password)
        # Load the existing data from the JSON file
        try:
            with open('users.json', 'r') as file:
                data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            data = {"Users": []}

        # Append the new user to the existing data
        data["Users"].append({'id': user.id, 'username': user.username, 'email': user.email, 'user_type': user.user_type, 'password_hash': user.password_hash.decode('utf-8')})


        # Write the updated data back to the JSON file
        with open('users.json', 'w') as file:
            json.dump(data, file, indent=4)


        return user
    

    @staticmethod
    def authenticate_user(username, password):
        # Load the data from the JSON file
        try:
            with open('users.json', 'r') as file:
                data = json.load(file)["Users"]
        except (json.JSONDecodeError, FileNotFoundError):
            data = []

        for user_data in data:
            if user_data['username'] == username:
                password_hash = user_data['password_hash'].encode('utf-8')
                print(f'password_hash = {password_hash}')
                print(f'user_data[\'password_hash\'] = {user_data["password_hash"]}')
                if bcrypt.checkpw(password.encode('utf-8'), password_hash):
                    user = User(
                        user_data['username'],
                        user_data['email'], 
                        user_data['user_type'],
                        user_data['id'])
                    return user

        return None
    

    @staticmethod
    def get_user(user_id):
        # Load the data from the JSON file
        try:
            with open('users.json', 'r') as file:
                data = json.load(file)["Users"]
        except (json.JSONDecodeError, FileNotFoundError):
            data = []

        for user_data in data:
            if user_data['id'] == user_id:
                user = User(
                    user_data['username'],
                    user_data['email'],
                    user_data['user_type'],
                    user_data['id']
                )
                return user

        return None