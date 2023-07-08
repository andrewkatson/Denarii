from denarii_testing_clicked import Clicked

class PushButton: 

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.clicked = Clicked()
        self.style_sheet = []
        self.is_visible = False

    def click(self):
        self.clicked.click()

    def setStyleSheet(self, add_to_sheet):
        self.style_sheet.append(add_to_sheet)

    def setVisible(self, visible):
        self.is_visible = visible
