class User:
    def __init__(self, name, password):
        self.username = name
        self.hashed_password = password

    def get_username(self):
        return self.username

    def get_password(self):
        return self.hashed_password

    def set_username(self, name):
        self.username = name

    def set_password(self, password):
        self.hashed_password = password
