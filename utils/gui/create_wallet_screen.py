from screen import *
from label import *
from font import *
from PyQt5.QtCore import *
from push_button import *
from line_edit import *


class CreateWalletScreen(Screen):
    """
    Screen that displays gui that lets user create a wallet
    """

    def __init__(self, main_layout, deletion_func, **kwargs):
        super().__init__(self.create_wallet_screen_name, main_layout, deletion_func, **kwargs)

        self.create_wallet_label = Label("Create Wallet")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.create_wallet_label.setFont(font)

        self.wallet_seed_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_seed_text_box.setFont(font)
        self.wallet_seed_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.wallet_save_file_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_save_file_text_box.setFont(font)
        self.wallet_save_file_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.create_wallet_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.create_wallet_text_box.setFont(font)

        self.create_wallet_submit_push_button = PushButton("Submit", kwargs['parent'])
        self.create_wallet_submit_push_button.clicked.connect(kwargs['on_create_wallet_submit_clicked'])
        self.create_wallet_submit_push_button.setVisible(False)
        self.create_wallet_submit_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.name_line_edit = LineEdit()
        self.password_line_edit = LineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.Password)

    def setup(self):
        super().setup()
