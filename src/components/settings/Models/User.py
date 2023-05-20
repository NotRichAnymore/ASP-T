class User:
    def __init__(self):
        self.name = None
        self.password = None

    def get_username(self):
        return self.name

    def get_password(self):
        return self.password

    def set_username(self, name):
        self.name = name

    def set_password(self, password):
        self.password = password

    def create_user_details(self, username, password):
        self.set_username(username)
        self.password(password)

        return self
