class MessageBox:
    def __init__(self):
        self.title = ""
        self.text = ""

    def setWindowTitle(self, title):
        self.title = title

    def setText(self, text):
        self.text = text

    def exec_(self):
        pass
