from denarii_testing_font import Font
from denarii_testing_label import Label
from denarii_testing_qt import (
    AlignCenter,
    AlignLeft,
)

class Widget:
    def __init__(self):
        self.main_layout = None
        self.child_layouts = []
        self.alignment = None

    def setMainLayout(self, layout):
        self.main_layout = layout

    def addLayout(self, layout):
        self.child_layouts.append(layout)

    def setAlignment(self, alignment):
        self.alignment = alignment


class HBoxLayout:
    def __init__(self) -> None:
        self.widgets = []
        self.child_layouts = []

    def addWidget(self, new_widget, alignment):
        new_widget.setAlignment(alignment)
        self.widgets.append(new_widget)

    def addLayout(self, layout):
        self.child_layouts.append(layout)


class VBoxLayout:
    def __init__(self) -> None:
        self.widgets = []
        self.child_layouts = []

    def addWidget(self, new_widget, alignment):
        new_widget.setAlignment(alignment)
        self.widgets.append(new_widget)

    def addLayout(self, layout):
        self.child_layouts.append(layout)


class FormLayout:
    def __init__(self) -> None:
        self.text = ""
        self.line_edit = None
        self.child_layouts = []

    def addRow(self, text, line_edit):
        self.text = text
        self.line_edit = line_edit

class GridLayout:

    def __init__(self) -> None:
        self.widgets = []

    def addWidget(self, new_widget, row, col, alignment=None):
        new_widget.setAlignment(alignment)
        self.widgets.append(new_widget)

class ScrollArea: 

    def __init__(self) -> None:
        self.alignment = None
        self.widget = None
        self.horizontal_policy = None 
        self.vertical_policy = None

    def setAlignment(self, alignment):
        self.alignment = alignment

    def setWidget(self, widget):
        self.widget = widget

    def setVerticalScrollBarPolicy(self, policy):
        self.vertical_policy = policy

    def setHorizontalScrollBarPolicy(self, policy):
        self.horizontal_policy = policy

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
