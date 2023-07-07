import threading
import time

from PyQt5.QtCore import *

from font import *
from label import *
from line_edit import *
from push_button import *
from screen import *
from wallet import *

class WalletScreen(Screen):
    """
    A class that allows a user to interact with the common features of a wallet e.g. checking balance and transferring
    denarii between wallets.
    """

    remote_wallet_suffix = "REMOTE_WALLET_SUFFIX"
    local_wallet_suffix = "LOCAL_WALLET_SUFFIX"

    def __init__(self, main_layout, deletion_func, denarii_client, gui_user, **kwargs):
        super().__init__(self.wallet_screen_name, main_layout=main_layout,
                         deletion_func=deletion_func, denarii_client=denarii_client, gui_user=gui_user, **kwargs)

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
        # Wallet is set in the specific wallet screen
        self.wallet = None
        self.keep_refreshing_balance = True
        self.balance_refresh_thread = threading.Thread(target=self.refresh_balance)
        self.balance_refresh_thread.start()
        self.balance = 0

    def init(self, **kwargs):
        super().init(**kwargs)

        self.next_button.setVisible(False)

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
        self.transfer_push_button.clicked.connect(lambda: self.on_transfer_clicked())
        self.transfer_push_button.setVisible(False)
        self.transfer_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

    def setup(self):
        super().setup()
        self.deletion_func(self.main_layout)

    def teardown(self):
        super().teardown()

    def populate_wallet_screen(self):
        pass

    def transfer_money(self):
        """
        Transfer money between two wallets.
        """
        success = False

        other_wallet = Wallet()
        other_wallet.address = bytes(self.address_line_edit.text(), 'utf-8')

        try:
            success = self.denarii_client.transfer_money(int(self.amount_line_edit.text()), self.wallet,
                                                         other_wallet)
            print_status("Transfer money ", success)
        except Exception as e:
            print(e)

        if success:
            self.wallet_transfer_status_text_box.setText("Success transferring money")
        else:
            self.wallet_transfer_status_text_box.setText("Failure transferring money")

    def refresh_balance(self):
        while self.keep_refreshing_balance:
            # Need time for wallet to be set
            time.sleep(10)
            if self.wallet is None:
                continue

            try:
                self.balance = self.denarii_client.get_balance_of_wallet(self.wallet)
                self.set_wallet_balance()

            except Exception as e:
                print(e)

    @pyqtSlot()
    def on_transfer_clicked(self):
        """
        Transfer money to another person's wallet
        """
        self.transfer_money()

    def set_wallet_balance(self):
        # We need to adjust the balance because it is in picomonero
        self.balance_text_box.setText(str(self.balance * 0.000000000001))
