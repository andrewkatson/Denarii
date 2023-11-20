class PlainTextEdit:
    def __init__(self) -> None:
        self.text = ""

    def toPlainText(self):
        return self.text
    
    def typeText(self, new_text):
        self.text = new_text
