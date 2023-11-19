from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from constants import *


class RadioButton(QRadioButton):
    def __init__(
        self,
        text,
        parent,
        user=None,
        wallet_type_callback=None,
        buy_regardless_of_price_callback=None,
        fail_if_full_amount_isnt_met_callback=None,
    ):
        super().__init__(text=text, parent=parent)
        self.user = user
        self.wallet_type_callback = wallet_type_callback
        self.buy_regardless_of_price_callback = buy_regardless_of_price_callback
        self.fail_if_full_amount_isnt_met_callback = (
            fail_if_full_amount_isnt_met_callback
        )

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

        if button.wallet_type_option == REMOTE_WALLET:
            self.wallet_type_callback(REMOTE_WALLET)
        else:
            self.wallet_type_callback(LOCAL_WALLET)

    @pyqtSlot()
    def on_buy_regardless_of_price_clicked(self):
        """
        Sets whether we want to be buying an ask regardless of its price
        """
        button = self.sender()

        self.buy_regardless_of_price_callback(button.buy_regardless_of_price_option)

    @pyqtSlot()
    def on_fail_if_full_amount_isnt_met(self):
        """
        Sets whether we want to be failing a buy if we cant buy the full amount
        """
        button = self.sender()

        self.fail_if_full_amount_isnt_met_callback(button.fail_if_full_amount_isnt_met_option)
