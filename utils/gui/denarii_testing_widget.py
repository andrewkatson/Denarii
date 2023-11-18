from denarii_testing_font import Font
from denarii_testing_label import Label
from denarii_testing_qt import (
    AlignCenter,
    AlignLeft,
)

class Item:
    def __init(self, widget):
        self._widget = widget

    def widget(self): 
        return self._widget

    def layout(self):
        return self._widget.main_layout

class Widget:
    def __init__(self):
        self.main_layout = None
        self.child_layouts = []
        self.widgets = []
        self.alignment = None

    def setMainLayout(self, layout):
        self.main_layout = layout

    def addLayout(self, layout):
        self.child_layouts.append(layout)

    def setAlignment(self, alignment):
        self.alignment = alignment

    def setLayout(self, layout): 
        self.main_layout = layout

    def addWidget(self, new_widget):
        self.widgets.append(new_widget)

    def takeAt(self, index): 
        if index >= len(self.widgets):
            return Item(None)
        
        return Item(self.widgets.pop())

    @property
    def count(self):
        return len(self.widgets)

    @property
    def parent(self):
        return self.main_layout

class HBoxLayout(Widget):
    def __init__(self) -> None:
        super().__init__()

    def addWidget(self, new_widget, alignment):
        new_widget.setAlignment(alignment)
        self.widgets.append(new_widget)

    def addLayout(self, layout):
        self.child_layouts.append(layout)


class VBoxLayout(Widget):
    def __init__(self) -> None:
        super().__init__()

    def addWidget(self, new_widget, alignment):
        new_widget.setAlignment(alignment)
        self.widgets.append(new_widget)

    def addLayout(self, layout):
        self.child_layouts.append(layout)


class FormRow(Widget):
    def __init__(self, text, line_edit):
        super().__init__()
        self.text = text 
        self.line_edit = line_edit


class FormLayout(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.rows = []

    def addRow(self, text, line_edit):
        self.rows.append(FormRow(text, line_edit))

class GridBox:
    def __init__(self):
        self.widget = None

    def setWidget(self, widget):
        self.widget = widget

class GridRow(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.cols = []

    def addBox(self, col, new_widget):
        grid_col_box = None
        if len(self.cols) <= col:
            grid_col_box = GridBox()
            self.cols.append(grid_col_box)
        else: 
            grid_col_box = self.cols[col]

        grid_col_box.setWidget(new_widget) 


class GridLayout(Widget):

    def __init__(self) -> None:
        super().__init__()
        self.rows = []

    def addWidget(self, new_widget, row, col, alignment=None):
        new_widget.setAlignment(alignment)
        self.widgets.append(new_widget)

        grid_row = None
        if len(self.rows) <= row:
            grid_row = GridRow()
            self.rows.append(grid_row)
        else: 
            grid_row = self.rows[row]

        grid_row.addBox(col, new_widget)


class ScrollArea(Widget): 

    def __init__(self) -> None:
        super().__init__()
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
        
        self.comments[f"{author}@{updated_time}"] = {"author": author, "body": body, "author_label": author_label, "body_label": body_label}

        self.layout.addWidget(author, alignment=AlignLeft)
        self.layout.addWidget(body_label, alignment=AlignCenter)
        
    def clearComments(self):
        for _, comment in self.comments.items():
            for key, artifact in comment.items():
                if "label" in key: 
                    artifact.setVisible(False)

        self.comments = {}
