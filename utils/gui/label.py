from PyQt5.QtWidgets import *


class Label(QLabel):

    def __init__(self, name):
        super().__init__()
        self.setText(name)
