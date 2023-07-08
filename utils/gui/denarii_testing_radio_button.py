from constants import REMOTE_WALLET, LOCAL_WALLET
from denarii_testing_toggled import Toggled


class RadioButton:
    def __init__(self, text, parent, user=None, wallet_type_callback=None):
        self.text = text
        self.parent = parent
        self.user = user
        self.wallet_type_callback = wallet_type_callback
        self.style_sheet = []
        self.is_visible = False
        self.toggled = Toggled()
        self.wallet_type_option = LOCAL_WALLET
        self.alignment = None

    def setStyleSheet(self, add_to_sheet):
        self.style_sheet.append(add_to_sheet)

    def setVisible(self, visible):
        self.is_visible = visible

    def on_lang_select_clicked(self):
        self.user.language = "English"

    def on_wallet_type_clicked(self):
        self.wallet_type_option = REMOTE_WALLET
        self.wallet_type_callback(self.wallet_type_option)

    def setAlignment(self, alignment):
        self.alignment = alignment