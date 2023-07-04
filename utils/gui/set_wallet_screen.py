from screen import *
from font import *
from label import *
from PyQt5.QtCore import *
from push_button import *
from line_edit import *


class SetWalletScreen(Screen):
    """
    A screen that allows the user to open a wallet that was previously created or restored.
    """

    def __init__(self, main_layout, deletion_func, **kwargs):
        super().__init__(self.set_wallet_screen_name, main_layout, deletion_func, **kwargs)

        self.set_wallet_label = Label("Set Wallet")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.set_wallet_label.setFont(font)

        self.set_wallet_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.set_wallet_text_box.setFont(font)
        self.set_wallet_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.set_wallet_submit_push_button = PushButton("Submit", kwargs['parent'])
        self.set_wallet_submit_push_button.clicked.connect(kwargs['on_set_wallet_submit_clicked'])
        self.set_wallet_submit_push_button.setVisible(False)
        self.set_wallet_submit_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.name_line_edit = LineEdit()
        self.password_line_edit = LineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.Password)

    def setup(self):
        super().setup()
