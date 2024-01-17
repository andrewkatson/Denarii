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

        self.test_name = f"{self.id()}_{self._testMethodName}"
        self.test_name = self.test_name.replace(".", "_")

        print(f"Running {self.test_name}")

        self.window = Window()
        self.main_widget = TestingMain()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.name = f"{self.test_name}_user"
        self.email = f"{self.test_name}_email@email.com"
        self.password = f"{self.test_name}_password1#A"
        self.wallet_name = f"{self.test_name}_wallet"
        self.wallet_password = f"{self.test_name}_wallet_password2$B"

    def tearDown(self):
        super().tearDown()

        # We need to teardown the widget in case there are threads running.
        self.main_widget.shutdown_all_screens()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def navigate_to_login_or_register(self):

        lang_select_screen = self.main_widget.LANG_SELECT

        lang_select_screen.english_radio_button.on_lang_select_clicked()

        self.assertEqual(lang_select_screen.gui_user.language, "English")

        lang_select_screen.on_submit_clicked()

        self.assertEqual(lang_select_screen.status_msg.text, "Success")

        self.main_widget.next_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.LOGIN_OR_REGISTER.screen_name)

    def navigate_to_login(self):

        self.navigate_to_login_or_register()

        login_or_register_screen = self.main_widget.LOGIN_OR_REGISTER

        on_login_clicked = login_or_register_screen.kwargs_passed["on_login_clicked"]

        on_login_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.LOGIN_SCREEN.screen_name)

    def navigate_to_reset_password(self):

        self.navigate_to_login()

        login_screen = self.main_widget.LOGIN_SCREEN

        login_screen.kwargs_passed["on_forgot_password_clicked"]()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.REQUEST_RESET_SCREEN.screen_name)

    def register_with_denarii(self):

        self.navigate_to_login_or_register()
        
        login_or_register_screen = self.main_widget.LOGIN_OR_REGISTER

        on_register_clicked = login_or_register_screen.kwargs_passed["on_register_clicked"]

        on_register_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.REGISTER_SCREEN.screen_name)

        register_screen = self.main_widget.REGISTER_SCREEN

        name_line_edit = register_screen.name_line_edit
        name_line_edit.typeText(self.name)

        email_line_edit = register_screen.email_line_edit
        email_line_edit.typeText(self.email)
        
        password_line_edit = register_screen.password_line_edit
        password_line_edit.typeText(self.password)

        confirm_password_line_edit = register_screen.confirm_password_line_edit
        confirm_password_line_edit.typeText(self.password)

        register_screen.on_submit_clicked()

        self.assertEqual(register_screen.status_msg.text, "Success")

        self.main_widget.next_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.LOGIN_SCREEN.screen_name)


    def login_with_denarii(self):
        self.register_with_denarii()

        login_screen = self.main_widget.LOGIN_SCREEN

        name_line_edit = login_screen.name_line_edit
        name_line_edit.typeText(self.name)

        email_line_edit = login_screen.email_line_edit
        email_line_edit.typeText(self.email)
        
        password_line_edit = login_screen.password_line_edit
        password_line_edit.typeText(self.password)

        login_screen.on_submit_clicked()

        self.assertEqual(login_screen.status_msg.text, "Success")

        self.main_widget.next_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.WALLET_INFO.screen_name)


    def create_wallet(self, wallet_type):
        self.login_with_denarii()

        wallet_decision_screen = self.main_widget.WALLET_INFO

        create_wallet_button = wallet_decision_screen.kwargs_passed["on_create_wallet_clicked"]

        create_wallet_button()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.CREATE_WALLET.screen_name)

        create_wallet_screen = self.main_widget.CREATE_WALLET

        name_line_edit = create_wallet_screen.name_line_edit
        name_line_edit.typeText(self.wallet_name)

        password_line_edit = create_wallet_screen.password_line_edit
        password_line_edit.typeText(self.wallet_password)

        confirm_password_line_edit = create_wallet_screen.confirm_password_line_edit
        confirm_password_line_edit.typeText(self.wallet_password)

        if wallet_type == LOCAL_WALLET: 
            create_wallet_screen.local_wallet_radio_button.on_wallet_type_clicked()
        elif wallet_type == REMOTE_WALLET:
            create_wallet_screen.remote_wallet_radio_button.on_wallet_type_clicked()

        create_wallet_screen.on_create_wallet_submit_clicked()
        
        self.assertRegex(create_wallet_screen.status_msg.text, "Success. *")

        self.main_widget.next_clicked()


    def navigate_to_local_wallet_screen(self):
        self.create_wallet(LOCAL_WALLET)

    def navigate_to_remote_wallet_screen(self):
        self.create_wallet(REMOTE_WALLET)

########################## TESTS ##########################

    def test_navigate_to_login_or_register(self):
        self.navigate_to_login_or_register()

    def test_navigate_to_reset_password(self):
        self.navigate_to_reset_password()

    def test_navigate_to_local_wallet_screen(self):
        self.navigate_to_local_wallet_screen()

        self.assertEqual(self.main_widget.current_wallet_widget.screen_name, self.main_widget.LOCAL_WALLET_SCREEN.screen_name)

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.LOCAL_WALLET_SCREEN.screen_name)

    def test_navigate_to_remote_wallet_screen(self):
        self.navigate_to_remote_wallet_screen()

        self.assertEqual(self.main_widget.current_wallet_widget.screen_name, self.main_widget.REMOTE_WALLET_SCREEN.screen_name)

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.REMOTE_WALLET_SCREEN.screen_name)


if __name__ == "__main__":#
    # We need to remove all denarii specific test arguments for this to not fail.
    unittest.main(
        argv=list((arg for arg in sys.argv if not arg.startswith("--denarii")))
    )