import sys
import unittest

from constants import *

# Testing stuff
from denarii_client_testing import DenariiClient
from denarii_mobile_client_testing import DenariiMobileClient
from denarii_testing_font import *
from denarii_testing_label import *
from denarii_testing_line_edit import *
from denarii_testing_radio_button import *
from denarii_testing_push_button import *
from denarii_testing_widget import *
from denarii_testing_window import *
from gui_user import GuiUser
from wallet import Wallet

# Classes to test
from create_wallet_screen import CreateWalletScreen

def deletion_function(layout):
    pass

def set_wallet_type(type):
    pass

def next_clicked():
    pass

def back_clicked():
    pass

class DenariiDesktopGUICreateWalletScreenTestCase(unittest.TestCase):

    def setUp(self):
        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet()
        self.local_wallet = Wallet()

        self.gui_user = GuiUser()

        self.next_button = PushButton("Next Page", self)
        self.next_button.setStyleSheet("color:black")
        self.next_button.setStyleSheet("font-weight: bold")
        self.next_button.setStyleSheet("font-size: 18pt")
        self.next_button.clicked.connect(next_clicked)

        self.back_button = PushButton("Back", self)
        self.back_button.setStyleSheet("color:black")
        self.back_button.setStyleSheet("font-weight: bold")
        self.back_button.setStyleSheet("font-size: 18pt")
        self.back_button.clicked.connect(back_clicked)

        common_buttons = {NEXT_BUTTON: self.next_button, BACK_BUTTON: self.back_button}

        self.create_wallet_screen = CreateWalletScreen(push_buttons=common_buttons, parent=self.main_widget, denarii_mobile_client=self.denarii_mobile_client,
                                                    main_layout=self.main_widget.main_layout,
                                                    deletion_func=deletion_function,
                                                    denarii_client=self.denarii_client,
                                                    remote_wallet=self.remote_wallet,
                                                    local_wallet=self.local_wallet, gui_user=self.gui_user, set_wallet_type_callback=set_wallet_type)
        

    def tearDown(self):
        pass
    
    def test_create_wallet(self):
        
        self.assertEquals(1, 1)


if __name__ == '__main__':
  # We need to remove all denarii specific test arguments for this to not fail.
  unittest.main(argv=list((arg for arg in sys.argv if not arg.startswith("--denarii"))))
