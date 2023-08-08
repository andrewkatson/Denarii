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
