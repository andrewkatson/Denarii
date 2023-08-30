from PyQt5.QtWidgets import *

from font import Font
from label import Label
from qt import (
    AlignCenter,
    AlignLeft,
)


class HBoxLayout(QHBoxLayout):
    pass


class VBoxLayout(QVBoxLayout):
    pass


class FormLayout(QFormLayout):
    pass

class GridLayout(QGridLayout):
    pass

class ScrollArea(QScrollArea):
    pass

class Widget(QWidget):
    pass

class CommentSection(Widget):

    def __init__(self):
        super().__init__()

        self.layout = VBoxLayout()

        self.comments = {}
    
    def addComment(self, author, body, updated_time):
        self.comments[f"{author}@{updated_time}"] = {"author": author, "body": body}

        author_label = Label(author)
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        author_label.setFont(font)

        body_label = Label(body)
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        body_label.setFont(font)
        body_label.setWordMap(True)

        self.layout.addWidget(author, alignment=AlignLeft)
        self.layout.addWidget(body_label, alignment=AlignCenter)
