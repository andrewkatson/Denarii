from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from constants import *


class RadioButton(QRadioButton):
    def __init__(self, text, parent, user=None, wallet_type_callback=None):
        super().__init__(text=text, parent=parent)
        self.user = user
        self.wallet_type_callback = wallet_type_callback

    @pyqtSlot()
    def on_lang_select_clicked(self):
        """
        Set the user's language when they choose one
        """
        button = self.sender()

        self.user.language = button.language

    @pyqtSlot()
    def on_wallet_type_clicked(self):
        """
        Set the wallet type to local or remote
        """
        button = self.sender()

        if button.wallet_type_option == "Remote":
            self.wallet_type_callback(REMOTE_WALLET)
        else:
            self.wallet_type_callback(LOCAL_WALLET)
