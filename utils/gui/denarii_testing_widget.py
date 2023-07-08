
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

    def addWidgets(self, new_widget, alignment):
        self.widgets.append(new_widget)

class VBoxLayout:
      
    def __init__(self) -> None:
        self.widgets = []

    def addWidgets(self, new_widget, alignment):
        new_widget.setAlignment(alignment)
        self.widgets.append(new_widget)  

class FormLayout:
    
    def __init__(self) -> None:
        self.text = ""
        self.line_edit = None 

    def addRow(self, text, line_edit):
        self.text = text
        self.line_edit = line_edit
