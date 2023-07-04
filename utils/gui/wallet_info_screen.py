from screen import *
from label import *
from font import *
from push_button import *


class WalletInfoScreen(Screen):
    """
    A screen that allows the user to choose whether to open, create, or restore a wallet
    """

    def __init__(self, main_layout, deletion_func, **kwargs):
        super().__init__(self.wallet_info_screen_name, main_layout, deletion_func, **kwargs)

        self.wallet_info_label = Label("Choose Wallet")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_info_label.setFont(font)

        self.create_wallet_push_button = PushButton("Create wallet", kwargs['parent'])
        self.create_wallet_push_button.clicked.connect(kwargs['on_create_wallet_clicked'])
        self.create_wallet_push_button.setVisible(False)
        self.create_wallet_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.restore_wallet_push_button = PushButton("Restore wallet", kwargs['parent'])
        self.restore_wallet_push_button.clicked.connect(kwargs['on_restore_wallet_clicked'])
        self.restore_wallet_push_button.setVisible(False)
        self.restore_wallet_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.set_wallet_push_button = PushButton("Set wallet", kwargs['parent'])
        self.set_wallet_push_button.clicked.connect(kwargs['on_set_wallet_clicked'])
        self.set_wallet_push_button.setVisible(False)
        self.set_wallet_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

    def setup(self):
        super().setup()
