import sys
import threading
import time
import unittest

from constants import *

# Testing stuff
from denarii_client_testing import DenariiClient
from denarii_mobile_client_testing import DenariiMobileClient
from denarii_testing_font import *
from denarii_testing_label import *
from denarii_testing_line_edit import *
from denarii_testing_main import *
from denarii_testing_radio_button import *
from denarii_testing_push_button import *
from denarii_testing_widget import *
from denarii_testing_window import *
from gui_user import GuiUser
from wallet import Wallet

# Classes to test
from buy_denarii_screen import BuyDenariiScreen
from create_wallet_screen import CreateWalletScreen
from credit_card_info_screen import CreditCardInfoScreen
from lang_select_screen import LangSelectScreen
from local_wallet_screen import LocalWalletScreen
from login_or_register_screen import LoginOrRegisterScreen
from login_screen import LoginScreen
from register_screen import RegisterScreen
from remote_wallet_screen import RemoteWalletScreen
from request_reset_screen import RequestResetScreen
from reset_password_screen import ResetPasswordScreen
from restore_wallet_screen import RestoreWalletScreen
from sell_denarii_screen import SellDenariiScreen
from set_wallet_screen import SetWalletScreen
from support_ticket_creation_screen import SupportTicketCreationScreen
from support_ticket_details_screen import SupportTicketDetailsScreen
from support_ticket_screen import SupportTicketScreen
from user_settings_screen import UserSettingsScreen
from verification_screen import VerificationScreen
from verify_reset_screen import VerifyResetScreen
from wallet_info_screen import WalletInfoScreen

class DenariiIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = TestingMain()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

    def tearDown(self):
        super().tearDown()

        # We need to teardown the widget in case there are threads running.
        self.main_widget.shutdown_all_screens()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_navigate_to_login_or_register(self):
        pass

    def test_navigate_to_local_wallet_screen(self):
        pass

    def test_navigate_to_remote_wallet_screen(self):
        pass


if __name__ == "__main__":
    # We need to remove all denarii specific test arguments for this to not fail.
    unittest.main(
        argv=list((arg for arg in sys.argv if not arg.startswith("--denarii")))
    )