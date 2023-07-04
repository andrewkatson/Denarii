from screen import *
from font import *
from label import *
from PyQt5.QtCore import *
from push_button import *
from line_edit import *


class RestoreWalletScreen(Screen):
    """
    A screen that allows a user to choose to restore a wallet that exists on another computer.
    """

    def __init__(self, main_layout, deletion_func, **kwargs):
        super().__init__(self.restore_wallet_screen_name, main_layout, deletion_func, **kwargs)

        self.restore_wallet_label = Label("Restore Wallet")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.restore_wallet_label.setFont(font)

        self.wallet_save_file_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_save_file_text_box.setFont(font)
        self.wallet_save_file_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.restore_wallet_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.restore_wallet_text_box.setFont(font)

        self.restore_wallet_submit_push_button = PushButton("Submit", kwargs['parent'])
        self.restore_wallet_submit_push_button.clicked.connect(kwargs['on_restore_wallet_submit_clicked'])
        self.restore_wallet_submit_push_button.setVisible(False)
        self.restore_wallet_submit_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.name_line_edit = LineEdit()
        self.password_line_edit = LineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        self.seed_line_edit = LineEdit()

    def setup(self):
        super().setup()
