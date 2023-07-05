from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from constants import *

class RadioButton(QRadioButton):

    def __init__(self, text, parent, user=None, store_user_func=None, wallet_type_callback=None):
        super().__init__(text=text, parent=parent)
        self.user = user
        self.store_user_func = store_user_func
        self.wallet_type_callback = wallet_type_callback

    @pyqtSlot()
    def on_lang_select_clicked(self):
        """
        Set the user's language when they choose one
        """
        button = self.sender()

        self.user.language = button.language

        self.store_user_func()

    @pyqtSlot
    def on_wallet_type_clicked(self):

        button = self.sender()

        if button.wallet_type_option == 'Remote':
            self.wallet_type_callback(REMOTE_WALLET)
        elif button.wallet_type_option == 'Local':
            self.wallet_type_callback(LOCAL_WALLET)
        self.wallet_type_callback(LOCAL_WALLET)
