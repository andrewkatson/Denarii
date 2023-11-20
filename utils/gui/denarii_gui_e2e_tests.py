import sys
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

class DenariiE2ETests(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        self.test_name = f"{self.id()}-{self._testMethodName}"

        print(f"Running {self.test_name}")

        self.window = Window()
        self.main_widget = TestingMain()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.name = f"{self.test_name}_user"
        self.email = f"{self.test_name}_email@email.com"
        self.password = f"{self.test_name}_password"
        self.wallet_name = f"{self.test_name}_wallet"
        self.wallet_password = f"{self.test_name}_wallet_password"
        self.new_password = f"{self.test_name}_new_password"

        self.other_name = f"other_{self.test_name}_user"
        self.other_email = f"other_{self.test_name}_email@email.com"
        self.other_password = f"other_{self.test_name}_password"
        self.other_wallet_name = f"other_{self.test_name}_wallet"
        self.other_wallet_password = f"other_{self.test_name}_wallet_password"
        self.other_new_password = f"other_{self.test_name}_new_password"


    def tearDown(self):
        super().tearDown()

        # We need to teardown the widget in case there are threads running.
        self.main_widget.shutdown_all_screens()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def logout(self):

        current_widget = self.main_widget.current_widget

        current_widget.kwargs_passed["on_user_settings_screen_clicked"]()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.USER_SETTINGS_SCREEN.screen_name)

        user_settings_screen = self.main_widget.USER_SETTINGS_SCREEN

        user_settings_screen.on_logout_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.LOGIN_OR_REGISTER.screen_name)

    def get_address(self, wallet_type, name): 

        if wallet_type == LOCAL_WALLET: 
            return self.main_widget.denarii_client.get_address_for_name(name)
        elif wallet_type == REMOTE_WALLET:
            return self.main_widget.denarii_mobile_client.get_address_for_name(name)

    def navigate_to_login_or_register(self):

        # Some tests reuse the register function but start on the login or register screen so just return in those cases
        if self.main_widget.current_widget.screen_name == self.main_widget.LOGIN_OR_REGISTER.screen_name: 
            return

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

    def register_with_denarii(self, name, email, password):

        self.navigate_to_login_or_register()
        
        login_or_register_screen = self.main_widget.LOGIN_OR_REGISTER

        on_register_clicked = login_or_register_screen.kwargs_passed["on_register_clicked"]

        on_register_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.REGISTER_SCREEN.screen_name)

        register_screen = self.main_widget.REGISTER_SCREEN

        name_line_edit = register_screen.name_line_edit
        name_line_edit.typeText(name)

        email_line_edit = register_screen.email_line_edit
        email_line_edit.typeText(email)
        
        password_line_edit = register_screen.password_line_edit
        password_line_edit.typeText(password)

        confirm_password_line_edit = register_screen.confirm_password_line_edit
        confirm_password_line_edit.typeText(password)

        register_screen.on_submit_clicked()

        self.assertEqual(register_screen.status_msg.text, "Success")

        self.main_widget.next_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.LOGIN_SCREEN.screen_name)

    def strictly_login_with_denarii(self, name, email, password): 

        login_screen = self.main_widget.LOGIN_SCREEN

        name_line_edit = login_screen.name_line_edit
        name_line_edit.typeText(name)

        email_line_edit = login_screen.email_line_edit
        email_line_edit.typeText(email)
        
        password_line_edit = login_screen.password_line_edit
        password_line_edit.typeText(password)

        login_screen.on_submit_clicked()

        self.assertEqual(login_screen.status_msg.text, "Success")

        self.main_widget.next_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.WALLET_INFO.screen_name)


    def login_with_denarii(self, name, email, password):
        self.register_with_denarii(name, email, password)

        self.strictly_login_with_denarii(name, email, password)

    def strictly_create_wallet(self, wallet_type):

        wallet_decision_screen = self.main_widget.WALLET_INFO

        create_wallet_button = wallet_decision_screen.kwargs_passed["on_create_wallet_clicked"]

        create_wallet_button()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.CREATE_WALLET.screen_name)

        create_wallet_screen = self.main_widget.CREATE_WALLET

        name_line_edit = create_wallet_screen.name_line_edit
        name_line_edit.typeText(self.wallet_name)

        password_line_edit = create_wallet_screen.password_line_edit
        password_line_edit.typeText(self.wallet_password)

        if wallet_type == LOCAL_WALLET: 
            create_wallet_screen.local_wallet_radio_button.on_wallet_type_clicked()
        elif wallet_type == REMOTE_WALLET:
            create_wallet_screen.remote_wallet_radio_button.on_wallet_type_clicked()

        create_wallet_screen.on_create_wallet_submit_clicked()
        
        self.assertRegex(create_wallet_screen.status_msg.text, "Success. *")

        seed = create_wallet_screen.wallet_info_text_box.text

        self.main_widget.next_clicked()
        
        if wallet_type == LOCAL_WALLET: 
            self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.LOCAL_WALLET_SCREEN.screen_name)

        elif wallet_type == REMOTE_WALLET:
            self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.REMOTE_WALLET_SCREEN.screen_name)

        return seed


    def create_wallet(self, wallet_type, name, email, password):
        self.login_with_denarii(name, email, password)

        return self.strictly_create_wallet(wallet_type)


    def restore_wallet(self, wallet_type, name, email, password):
        seed = self.create_wallet(wallet_type, name, email, password)

        wallet_decision_screen = self.main_widget.WALLET_INFO

        restore_wallet_button = wallet_decision_screen.kwargs_passed["on_restore_wallet_clicked"]

        restore_wallet_button()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.RESTORE_WALLET.screen_name)

        restore_wallet_screen = self.main_widget.RESTORE_WALLET

        name_line_edit = restore_wallet_screen.name_line_edit
        name_line_edit.typeText(self.wallet_name)

        password_line_edit = restore_wallet_screen.password_line_edit
        password_line_edit.typeText(self.wallet_password)

        seed_line_edit = restore_wallet_screen.seed_line_edit
        seed_line_edit.typeText(seed)

        if wallet_type == LOCAL_WALLET: 
            restore_wallet_screen.local_wallet_radio_button.on_wallet_type_clicked()
        elif wallet_type == REMOTE_WALLET:
            restore_wallet_screen.remote_wallet_radio_button.on_wallet_type_clicked()

        restore_wallet_screen.on_restore_wallet_submit_clicked()
        
        self.assertRegex(restore_wallet_screen.status_msg.text, "Success. *")

        self.main_widget.next_clicked()

        if wallet_type == LOCAL_WALLET: 
            self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.LOCAL_WALLET_SCREEN.screen_name)

        elif wallet_type == REMOTE_WALLET:
            self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.REMOTE_WALLET_SCREEN.screen_name)

    def strictly_open_wallet(self, wallet_type):

        wallet_decision_screen = self.main_widget.WALLET_INFO

        open_wallet_button = wallet_decision_screen.kwargs_passed["on_set_wallet_clicked"]

        open_wallet_button()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.SET_WALLET.screen_name)

        open_wallet_screen = self.main_widget.SET_WALLET

        name_line_edit = open_wallet_screen.name_line_edit
        name_line_edit.typeText(self.wallet_name)

        password_line_edit = open_wallet_screen.password_line_edit
        password_line_edit.typeText(self.wallet_password)

        if wallet_type == LOCAL_WALLET: 
            open_wallet_screen.local_wallet_radio_button.on_wallet_type_clicked()
        elif wallet_type == REMOTE_WALLET:
            open_wallet_screen.remote_wallet_radio_button.on_wallet_type_clicked()

        open_wallet_screen.on_set_wallet_submit_clicked()
        
        self.assertRegex(open_wallet_screen.status_msg.text, "Success. *")

        self.main_widget.next_clicked()

        if wallet_type == LOCAL_WALLET: 
            self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.LOCAL_WALLET_SCREEN.screen_name)

        elif wallet_type == REMOTE_WALLET:
            self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.REMOTE_WALLET_SCREEN.screen_name)

    def open_wallet(self, wallet_type, name, email, password):
        _ = self.create_wallet(wallet_type, name, email, password)

        self.strictly_open_wallet(wallet_type)

    def reset_password(self, name, email, password, new_password):

        self.register_with_denarii(name, email, password)

        login_screen = self.main_widget.LOGIN_SCREEN

        login_screen.kwargs_passed["on_forgot_password_clicked"]()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.REQUEST_RESET_SCREEN.screen_name)

        request_reset_screen = self.main_widget.REQUEST_RESET_SCREEN

        name_or_email_line_edit = request_reset_screen.name_or_email_line_edit
        name_or_email_line_edit.typeText(self.name)

        request_reset_screen.on_submit_clicked()

        self.assertEqual(request_reset_screen.status_msg.text, "Success")

        self.main_widget.next_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.VERIFY_RESET_SCREEN.screen_name)

        verify_reset_screen = self.main_widget.VERIFY_RESET_SCREEN

        reset_id_line_edit = verify_reset_screen.reset_id_line_edit
        # A static reset id is set in TESTING mode
        reset_id_line_edit.typeText("4")

        verify_reset_screen.on_submit_clicked()

        self.assertEqual(verify_reset_screen.status_msg.text, "Success")

        self.main_widget.next_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.RESET_PASSWORD_SCREEN.screen_name)

        reset_password_screen = self.main_widget.RESET_PASSWORD_SCREEN

        name_line_edit = reset_password_screen.name_line_edit
        name_line_edit.typeText(name)

        email_line_edit = reset_password_screen.email_line_edit
        email_line_edit.typeText(email)

        password_line_edit = reset_password_screen.password_line_edit
        password_line_edit.typeText(new_password)

        confirm_password_line_edit = reset_password_screen.confirm_password_line_edit
        confirm_password_line_edit.typeText(new_password)

        reset_password_screen.on_submit_clicked()

        self.assertEqual(reset_password_screen.status_msg.text, "Success")

        self.main_widget.next_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.LOGIN_SCREEN.screen_name)

        self.strictly_login_with_denarii(name, email, new_password)

    def send_denarii(self, wallet_type, name, email, password, other_name, other_email, other_password):
        self.create_wallet(wallet_type, other_name, other_email, other_password)

        self.logout()

        self.create_wallet(wallet_type, name, email, password)
        
        wallet_screen = None 
        if wallet_type == LOCAL_WALLET: 
            wallet_screen = self.main_widget.LOCAL_WALLET_SCREEN
        elif wallet_type == REMOTE_WALLET:
            wallet_screen = self.main_widget.REMOTE_WALLET_SCREEN

        address = self.get_address(wallet_type, other_name)

        address_line_edit = wallet_screen.address_line_edit
        address_line_edit.typeText(address)
        
        amount_line_edit = wallet_screen.amount_line_edit
        amount_line_edit.typeText("2")

        wallet_screen.on_transfer_clicked()

        self.assertEqual(wallet_screen.status_msg.text, "Success transferring money")

        self.logout()

        self.strictly_login_with_denarii(other_name, other_email, other_password)

        self.strictly_open_wallet(wallet_type)

        wallet_screen = None 
        if wallet_type == LOCAL_WALLET: 
            wallet_screen = self.main_widget.LOCAL_WALLET_SCREEN
        elif wallet_type == REMOTE_WALLET:
            wallet_screen = self.main_widget.REMOTE_WALLET_SCREEN

        self.assertGreaterEqual(wallet_screen.balance, "3")

    def mine_denarii(self, name, email, password):
        self.create_wallet(LOCAL_WALLET, name, email, password)
        
        wallet_screen = self.main_widget.LOCAL_WALLET_SCREEN

        wallet_screen.start_mining()

        time.sleep(3)

        wallet_screen.stop_mining()       

        self.assertGreaterEqual(wallet_screen.balance, "3")
                
    def sell_denarii(self, name, email, password):
        self.create_wallet(REMOTE_WALLET, name, email, password)

        wallet_screen = self.main_widget.REMOTE_WALLET_SCREEN

        wallet_screen.kwargs_passed["on_sell_screen_clicked"]()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.SELL_DENARII.screen_name)

        sell_denarii_screen = self.main_widget.SELL_DENARII

        amount_line_edit = sell_denarii_screen.amount_line_edit
        amount_line_edit.typeText("2")

        price_line_edit = sell_denarii_screen.price_line_edit
        price_line_edit.typeText("100")

        sell_denarii_screen.on_submit_clicked()

        self.assertEqual(sell_denarii_screen.status_msg.text, "Created denarii ask!")

        time.sleep(6)

        self.assertEqual(len(sell_denarii_screen.own_asks), 1)


    def buy_denarii(self, name, email, password):
        self.create_wallet(REMOTE_WALLET, name, email, password)

        wallet_screen = self.main_widget.REMOTE_WALLET_SCREEN

        wallet_screen.kwargs_passed["on_buy_screen_clicked"]()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.BUY_DENARII.screen_name)

        buy_denarii_screen = self.main_widget.BUY_DENARII

        amount_line_edit = buy_denarii_screen.amount_line_edit
        amount_line_edit.typeText("1")

        price_line_edit = buy_denarii_screen.price_line_edit
        price_line_edit.typeText("110")

        buy_denarii_screen.on_submit_clicked()

        self.assertNotRegex(buy_denarii_screen.status_msg.text, "Failed *")

        time.sleep(6)

        self.assertEqual(len(buy_denarii_screen.queued_buys), 1)


    def cancel_buy_denarii(self, name, email, password):
        self.buy_denarii(name, email, password)

        buy_denarii_screen = self.main_widget.BUY_DENARII

        ask_id = buy_denarii_screen.queued_buys[0]["ask_id"]

        buy_denarii_screen.on_cancel_buy_clicked(ask_id)

        self.assertNotRegex(buy_denarii_screen.status_msg.text, "Failed *")

        time.sleep(6)

        self.assertEqual(len(buy_denarii_screen.queued_buys), 0)


    def cancel_buy(self, name, email, password, other_name, other_email, other_password):
        self.sell_denarii(other_name, other_email, other_password)

        self.logout()

        self.cancel_buy_denarii(name, email, password)

    def create_support_ticket(self, name, email, password):
        self.create_wallet(REMOTE_WALLET, name, email, password)

        wallet_screen = self.main_widget.REMOTE_WALLET_SCREEN

        wallet_screen.kwargs_passed["on_user_settings_screen_clicked"]()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.USER_SETTINGS_SCREEN.screen_name)

        user_settings_screen = self.main_widget.USER_SETTINGS_SCREEN

        user_settings_screen.kwargs_passed["support_ticket_screen_push_button"]()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.SUPPORT_TICKET_SCREEN.screen_name)

        support_ticket_screen = self.main_widget.SUPPORT_TICKET_SCREEN

        support_ticket_screen.kwargs_passed["on_support_ticket_creation_screen_clicked"]()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.SUPPORT_TICKET_CREATION_SCREEN.screen_name)

        support_ticket_creation_screen = self.main_widget.SUPPORT_TICKET_CREATION_SCREEN

        title_line_edit = support_ticket_creation_screen.title_line_edit
        title_line_edit.typeText("title")

        description_line_edit = support_ticket_creation_screen.description_text_edit
        description_line_edit.typeText("description")

        support_ticket_creation_screen.on_submit_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.SUPPORT_TICKET_DETAILS_SCREEN.screen_name)

    
    def comment_on_support_ticket(self):
        
        support_ticket_details_screen = self.main_widget.SUPPORT_TICKET_DETAILS_SCREEN

        comment_line_edit = support_ticket_details_screen.new_comment_plain_text_edit
        comment_line_edit.typeText("comment")

        support_ticket_details_screen.on_submit_clicked()

        self.assertEqual(support_ticket_details_screen.status_msg.text, "Created comment successfully")

        time.sleep(6)

        self.assertEqual(len(support_ticket_details_screen.comment_section.comments), 1)


    def resolve_support_ticket(self):
        support_ticket_details_screen = self.main_widget.SUPPORT_TICKET_DETAILS_SCREEN

        support_ticket_details_screen.on_resolve_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.SUPPORT_TICKET_SCREEN.screen_name)


    def comment_on_resolve_support_ticket(self, name, email, password):
        self.create_support_ticket(name, email, password)

        self.comment_on_support_ticket()

        self.resolve_support_ticket()

    def delete_support_ticket(self):
        support_ticket_details_screen = self.main_widget.SUPPORT_TICKET_DETAILS_SCREEN

        support_ticket_details_screen.on_delete_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.SUPPORT_TICKET_SCREEN.screen_name)

    def comment_on_delete_support_ticket(self, name, email, password):
        self.create_support_ticket(name, email, password)

        self.comment_on_support_ticket()

        self.delete_support_ticket()

    def delete_account(self, name, email, password):
        self.create_wallet(REMOTE_WALLET, name, email, password)

        wallet_screen = self.main_widget.REMOTE_WALLET_SCREEN

        wallet_screen.kwargs_passed["on_user_settings_screen_clicked"]()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.USER_SETTINGS_SCREEN.screen_name)

        user_settings_screen = self.main_widget.USER_SETTINGS_SCREEN

        user_settings_screen.on_delete_account_clicked()

        self.assertEqual(self.main_widget.current_widget.screen_name, self.main_widget.LOGIN_OR_REGISTER.screen_name)


########################## TESTS ##########################

    def test_reset_password_local_wallet(self):
        self.reset_password(self.name, self.email, self.password, self.new_password)

        # We are left on wallet info screen so we need to make a wallet then logout 
        self.strictly_create_wallet(LOCAL_WALLET)

        self.logout()

    def test_reset_password_remote_wallet(self):
        self.reset_password(self.name, self.email, self.password, self.new_password)

        # We are left on wallet info screen so we need to make a wallet then logout 
        self.strictly_create_wallet(REMOTE_WALLET)

        self.logout()

    def test_create_wallet_local_wallet(self):
        self.create_wallet(LOCAL_WALLET, self.name, self.email, self.password)

        self.logout()
    
    def test_restore_wallet_local_wallet(self):
        self.restore_wallet(LOCAL_WALLET, self.name, self.email, self.password)

        self.logout()

    def test_open_wallet_local_wallet(self):
        self.open_wallet(LOCAL_WALLET)

        self.logout()

    def test_create_wallet_remote_wallet(self):
        self.create_wallet(REMOTE_WALLET, self.name, self.email, self.password)

        self.logout()
    
    def test_restore_wallet_remote_wallet(self):
        self.restore_wallet(REMOTE_WALLET, self.name, self.email, self.password)

        self.logout()

    def test_open_wallet_remote_wallet(self):
        self.open_wallet(REMOTE_WALLET, self.name, self.email, self.password)

        self.logout()

    def test_send_denarii_local_wallet(self):
        self.send_denarii(LOCAL_WALLET, self.name, self.email, self.password, self.other_name, self.other_email, self.other_password)

        self.logout()

    def test_send_denarii_remote_wallet(self):
        self.send_denarii(REMOTE_WALLET, self.name, self.email, self.password, self.other_name, self.other_email, self.other_password)

        self.logout()

    def test_mine_denarii_local_wallet(self):
        self.mine_denarii(self.name, self.email, self.password)

        self.logout()

    def test_cancel_buy_remote_wallet(self):
        self.cancel_buy(self.name, self.email, self.password, self.other_name, self.other_email, self.other_password)

        self.logout()

    def test_create_support_ticket_then_comment_on_it_then_resolve_it_remote_wallet(self):
        self.comment_on_resolve_support_ticket(self.name, self.email, self.password)

        self.logout()

    def test_create_support_ticket_then_comment_on_it_then_delete_it_remote_wallet(self):
        self.comment_on_delete_support_ticket(self.name, self.email, self.password)

        self.logout()


    def test_delete_account_remote_wallet(self):
        self.delete_account(self.name, self.email, self.password)


if __name__ == "__main__":
    # We need to remove all denarii specific test arguments for this to not fail.
    unittest.main(
        argv=list((arg for arg in sys.argv if not arg.startswith("--denarii")))
    )