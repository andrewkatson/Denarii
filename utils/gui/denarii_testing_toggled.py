class Toggled:

    def __init__(self):
        self.callback = None

    def connect(self, func):
        self.callback = func

    def toggle(self):
        self.callback()