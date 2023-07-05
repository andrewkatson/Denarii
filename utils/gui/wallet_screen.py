from screen import *
from font import *
from label import *
from PyQt5.QtCore import *
from line_edit import *
from push_button import *


class WalletScreen(Screen):
    """
    A class that allows a user to interact with the common features of a wallet e.g. checking balance and transferring
    denarii between wallets.
    """

    remote_wallet_suffix = "REMOTE_WALLET_SUFFIX"
    local_wallet_suffix = "LOCAL_WALLET_SUFFIX"

    def __init__(self, main_layout, deletion_func, **kwargs):
        super().__init__(self.wallet_screen_name, main_layout, deletion_func, **kwargs)

        self.wallet_header_label = None
        self.your_address_label = None
        self.your_balance_label = None
        self.balance_text_box = None
        self.address_text_box = None
        self.wallet_info_status_text_box = None
        self.wallet_transfer_status_text_box = None
        self.address_line_edit = None
        self.amount_line_edit = None
        self.transfer_push_button = None
        self.wallet = kwargs['wallet']

    def init(self, **kwargs):
        super().init(**kwargs)

        self.wallet_header_label = Label("Wallet")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_header_label.setFont(font)

        self.your_balance_label = Label("Your Balance:")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.your_balance_label.setFont(font)

        self.your_address_label = Label("Your Address:")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.your_address_label.setFont(font)

        self.balance_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.balance_text_box.setFont(font)

        self.address_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.address_text_box.setFont(font)
        self.address_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.wallet_info_status_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_info_status_text_box.setFont(font)

        self.wallet_transfer_status_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_transfer_status_text_box.setFont(font)

        self.address_line_edit = LineEdit()
        self.amount_line_edit = LineEdit()

        self.transfer_push_button = PushButton("Transfer", kwargs['parent'])
        self.transfer_push_button.clicked.connect(kwargs['on_transfer_clicked'])
        self.transfer_push_button.setVisible(False)
        self.transfer_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

    def setup(self):
        super().setup()
        self.remove_all_widgets(self.main_layout)

    def teardown(self):
        super().teardown()

    def populate_wallet_screen(self):
        pass
