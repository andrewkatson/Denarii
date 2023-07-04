from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class RadioButton(QRadioButton):

    def __init__(self, text, parent, user, store_user_func):
        super().__init__(text=text, parent=parent)
        self.user = user
        self.store_user_func = store_user_func

    @pyqtSlot()
    def on_lang_select_clicked(self):
        """
        Set the user's language when they choose one
        """
        button = self.sender()

        self.user.language = button.language

        self.store_user_func()
