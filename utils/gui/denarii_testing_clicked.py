class Clicked:
    def __init__(self):
        self.callback = None

    def connect(self, func):
        self.callback = func

    def click(self):
        self.callback()
