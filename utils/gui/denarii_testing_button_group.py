
class ButtonGroup:

    def __init__(self) -> None:
        self.buttons = []
        self.exclusive = True
        
    def addButton(self, button):
        self.buttons.append(button)

    def setExclusive(self, exclusive):
        self.exclusive = exclusive
