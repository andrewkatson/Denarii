from constants import REMOTE_WALLET, LOCAL_WALLET
from denarii_testing_toggled import Toggled


class RadioButton:
    def __init__(
        self,
        text,
        parent,
        user=None,
        wallet_type_callback=None,
        buy_regardless_of_price_callback=None,
        fail_if_full_amount_isnt_met_callback=None,
    ):
        self.text = text
        self.parent = parent
        self.user = user
        self.wallet_type_callback = wallet_type_callback
        self.style_sheet = []
        self.is_visible = False
        self.toggled = Toggled()
        self.wallet_type_option = LOCAL_WALLET
        self.alignment = None
        self.buy_regardless_of_price_callback = buy_regardless_of_price_callback
        self.fail_if_full_amount_isnt_met_callback = (
            fail_if_full_amount_isnt_met_callback
        )
        self.is_checked = False


    def setStyleSheet(self, add_to_sheet):
        self.style_sheet.append(add_to_sheet)

    def setVisible(self, visible):
        self.is_visible = visible

    def on_lang_select_clicked(self):
        self.user.language = "English"

    def on_wallet_type_clicked(self):
        self.wallet_type_callback(self.wallet_type_option)

    def on_buy_regardless_of_price_clicked(self):
        self.buy_regardless_of_price_callback(False)

    def on_fail_if_full_amount_isnt_met(self):
        self.fail_if_full_amount_isnt_met_callback(True)

    def setAlignment(self, alignment):
        self.alignment = alignment

    def setChecked(self, checked):
        self.is_checked = checked
