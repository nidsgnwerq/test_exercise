

class Client:

    def __init__(self, client_id):
        self.client_id = client_id
        self.available = 0
        self.held = 0
        self.total = 0
        self.locked = False

    def get_client_id(self):
        return self.client_id

    def get_available(self):
        return self.available

    def lock_client(self):
        self.locked = True

    def unlock_client(self):
        self.locked = False

    def modify_available(self, value):
        self.available = self.available + value

    def modify_held(self, value):
        self.held = self.held + value

    def modify_total(self, value):
        self.total = self.total + value

    def get_client_data(self):
        return self.client_id, self.available, self.held, self.total, self.locked
