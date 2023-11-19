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

gui_user = GuiUser()

class TestingMain(Widget):

    def __init__(self):
        self.denarii_client = DenariiClient()
        self.denarii_mobile_client = DenariiMobileClient()

        self.main_layout = VBoxLayout()
        self.setLayout(self.main_layout)

        self.local_wallet = Wallet()
        self.remote_wallet = Wallet()
        self.which_wallet = None

        # Common buttons
        self.next_button = PushButton("Next Page", self)
        self.next_button.clicked.connect(self.next_clicked)

        self.back_button = PushButton("Back", self)
        self.back_button.clicked.connect(self.back_clicked)

        common_buttons = {
            NEXT_BUTTON: self.next_button,
            BACK_BUTTON: self.back_button,
        }

        self.kwargs = {
            "push_buttons": common_buttons,
            "gui_user": gui_user,
            "parent": self,
            "main_layout": self.main_layout,
            "deletion_func": self.remove_all_widgets,
            "denarii_client": self.denarii_client,
            "on_create_wallet_clicked": self.on_create_wallet_clicked,
            "on_restore_wallet_clicked": self.on_restore_wallet_pushed,
            "on_set_wallet_clicked": self.on_set_wallet_pushed,
            "remote_wallet": self.remote_wallet,
            "local_wallet": self.local_wallet,
            "set_wallet_type_callback": self.set_wallet_type,
            "denarii_mobile_client": self.denarii_mobile_client,
            "on_sell_screen_clicked": self.on_sell_denarii_screen_pushed,
            "on_buy_screen_clicked": self.on_buy_denarii_screen_pushed,
            "on_remote_wallet_screen_clicked": self.on_remote_wallet_screen_pushed,
            "on_login_clicked": self.on_login_pushed,
            "on_register_clicked": self.on_register_pushed,
            "on_verification_screen_clicked": self.on_verification_screen_pushed,
            "on_credit_card_info_screen_clicked": self.on_credit_card_info_screen_pushed,
            "on_user_settings_screen_clicked": self.on_user_settings_screen_pushed,
            "on_support_ticket_screen_clicked": self.on_support_ticket_screen_pushed,
            "on_support_ticket_creation_screen_clicked": self.on_support_ticket_creation_screen_pushed,
            "on_support_ticket_details_screen_clicked": lambda support_ticket_id: self.on_support_ticket_details_screen_pushed(
                support_ticket_id
            ),
            "get_current_support_ticket_id": self.get_current_support_ticket_id,
            "on_login_or_register_screen_clicked": self.on_login_or_register_screen_pushed,
            "on_forgot_password_clicked": self.on_forgot_password_pushed
        }

        self.current_support_ticket = None

        # Widgets
        self.LANG_SELECT = LangSelectScreen(
            push_buttons=common_buttons,
            gui_user=gui_user,
            parent=self,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_mobile_client=self.denarii_mobile_client,
            denarii_client=self.denarii_client,
        )
        self.WALLET_INFO = WalletInfoScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            on_create_wallet_clicked=self.on_create_wallet_clicked,
            on_restore_wallet_clicked=self.on_restore_wallet_pushed,
            on_set_wallet_clicked=self.on_set_wallet_pushed,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            gui_user=gui_user,
        )
        self.CREATE_WALLET = CreateWalletScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
            set_wallet_type_callback=self.set_wallet_type,
        )
        self.RESTORE_WALLET = RestoreWalletScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
            set_wallet_type_callback=self.set_wallet_type,
        )
        self.SET_WALLET = SetWalletScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
            set_wallet_type_callback=self.set_wallet_type,
        )
        self.LOGIN_OR_REGISTER = LoginOrRegisterScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
            on_login_clicked=self.on_login_pushed,
            on_register_clicked=self.on_register_pushed,
        )
        self.LOGIN_SCREEN = LoginScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
            on_forgot_password_clicked=self.on_forgot_password_pushed
        )
        self.REGISTER_SCREEN = RegisterScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
        )
        self.CURRENT_WALLET = None
        self.LOCAL_WALLET_SCREEN = LocalWalletScreen(
            push_buttons=common_buttons,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            parent=self,
            denarii_client=self.denarii_client,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
        )
        self.REMOTE_WALLET_SCREEN = RemoteWalletScreen(
            push_buttons=common_buttons,
            main_layout=self.main_layout,
            denarii_mobile_client=self.denarii_mobile_client,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            parent=self,
            remote_wallet=self.remote_wallet,
            gui_user=gui_user,
            on_buy_screen_clicked=self.on_buy_denarii_screen_pushed,
            on_sell_screen_clicked=self.on_sell_denarii_screen_pushed,
            on_credit_card_info_screen_clicked=self.on_credit_card_info_screen_pushed,
            on_verification_screen_clicked=self.on_verification_screen_pushed,
            on_user_settings_screen_clicked=self.on_user_settings_screen_pushed,
        )
        self.BUY_DENARII = BuyDenariiScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
            on_remote_wallet_screen_clicked=self.on_remote_wallet_screen_pushed,
            on_sell_screen_clicked=self.on_sell_denarii_screen_pushed,
            on_credit_card_info_screen_clicked=self.on_credit_card_info_screen_pushed,
            on_verification_screen_clicked=self.on_verification_screen_pushed,
            on_user_settings_screen_clicked=self.on_user_settings_screen_pushed,
        )
        self.SELL_DENARII = SellDenariiScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
            on_remote_wallet_screen_clicked=self.on_remote_wallet_screen_pushed,
            on_buy_screen_clicked=self.on_buy_denarii_screen_pushed,
            on_credit_card_info_screen_clicked=self.on_credit_card_info_screen_pushed,
            on_verification_screen_clicked=self.on_verification_screen_pushed,
            on_user_settings_screen_clicked=self.on_user_settings_screen_pushed,
        )
        self.CREDIT_CARD_INFO_SCREEN = CreditCardInfoScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
            on_remote_wallet_screen_clicked=self.on_remote_wallet_screen_pushed,
            on_buy_screen_clicked=self.on_buy_denarii_screen_pushed,
            on_sell_screen_clicked=self.on_sell_denarii_screen_pushed,
            on_verification_screen_clicked=self.on_verification_screen_pushed,
            on_user_settings_screen_clicked=self.on_user_settings_screen_pushed,
        )
        self.REQUEST_RESET_SCREEN = RequestResetScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
        )
        self.RESET_PASSWORD_SCREEN = ResetPasswordScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
        )
        self.VERIFY_RESET_SCREEN = VerifyResetScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
        )
        self.USER_SETTINGS_SCREEN = UserSettingsScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
            on_remote_wallet_screen_clicked=self.on_remote_wallet_screen_pushed,
            on_buy_screen_clicked=self.on_buy_denarii_screen_pushed,
            on_sell_screen_clicked=self.on_sell_denarii_screen_pushed,
            on_credit_card_info_screen_clicked=self.on_credit_card_info_screen_pushed,
            on_verification_screen_clicked=self.on_verification_screen_pushed,
            on_support_ticket_screen_clicked=self.on_support_ticket_screen_pushed,
            on_login_or_register_screen_clicked=self.on_login_or_register_screen_pushed,
        )
        self.VERIFICATION_SCREEN = VerificationScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
            on_remote_wallet_screen_clicked=self.on_remote_wallet_screen_pushed,
            on_buy_screen_clicked=self.on_buy_denarii_screen_pushed,
            on_sell_screen_clicked=self.on_sell_denarii_screen_pushed,
            on_credit_card_info_screen_clicked=self.on_credit_card_info_screen_pushed,
            on_user_settings_screen_clicked=self.on_user_settings_screen_pushed,
        )
        self.SUPPORT_TICKET_SCREEN = SupportTicketScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
            on_user_settings_screen_clicked=self.on_user_settings_screen_pushed,
            on_support_ticket_creation_screen_clicked=self.on_support_ticket_creation_screen_pushed,
            on_support_ticket_details_screen_clicked=lambda support_ticket_id: self.on_support_ticket_details_screen_pushed(
                support_ticket_id
            ),
        )
        self.SUPPORT_TICKET_CREATION_SCREEN = SupportTicketCreationScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
            on_support_ticket_screen_clicked=self.on_support_ticket_screen_pushed,
            on_support_ticket_details_screen_clicked=lambda support_ticket_id: self.on_support_ticket_details_screen_pushed(
                support_ticket_id
            ),
        )
        self.SUPPORT_TICKET_DETAILS_SCREEN = SupportTicketDetailsScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_layout,
            deletion_func=self.remove_all_widgets,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=gui_user,
            on_support_ticket_screen_clicked=self.on_support_ticket_screen_pushed,
            get_current_support_ticket_id=self.get_current_support_ticket_id,
        )

        self.last_widget_stack = []

        self.current_widget = self.LANG_SELECT
        # Determine what scene we are on based on what info the stored user has
        if (gui_user.language is None or gui_user.language == "") and (
            gui_user.name is None or gui_user.name == ""
        ):
            self.current_widget = self.LANG_SELECT
        elif (
            gui_user.language is not None
            and gui_user.language != ""
            and (gui_user.name is None or gui_user.name == "")
        ):
            self.current_widget = self.LOGIN_OR_REGISTER

        self.setup_current_widget()

        self.success = False

    def get_last_widget(self):
        if len(self.last_widget_stack) == 0:
            return None
        return self.last_widget_stack[len(self.last_widget_stack) - 1]

    def pop_last_widget(self):
        if len(self.last_widget_stack) == 0:
            return self.current_widget
        return self.last_widget_stack.pop()

    def remove_all_widgets(self, layout):
        """
        Remove all widgets and layouts
        """
        layout.child_widgets = []
        layout.child_layouts = []

    def shutdown_all_screens(self):
        # We should only have to turn down the current one.
        if self.current_widget is not None:
            self.current_widget.teardown()

    def next_clicked(self):
        """
        What to do when the next page button is clicked depending on the current screen
        """
        self.last_widget_stack.append(self.current_widget)
        if self.current_widget == self.LANG_SELECT:
            self.current_widget = self.LOGIN_OR_REGISTER
        elif self.current_widget == self.LOGIN_SCREEN:
            self.current_widget = self.WALLET_INFO
        elif self.current_widget == self.REGISTER_SCREEN:
            self.current_widget = self.LOGIN_SCREEN
        elif self.current_widget == self.REQUEST_RESET_SCREEN:
            self.current_widget = self.VERIFY_RESET_SCREEN
        elif self.current_widget == self.VERIFY_RESET_SCREEN:
            self.current_widget = self.RESET_PASSWORD_SCREEN
        elif self.current_widget == self.RESET_PASSWORD_SCREEN:
            self.current_widget = self.LOGIN_SCREEN
        elif self.current_widget == self.WALLET_INFO:
            # The next button on the wallet info screen should do nothing
            self.current_widget = self.WALLET_INFO
        elif self.current_widget == self.CREATE_WALLET:
            self.current_widget = self.current_wallet_widget
        elif self.current_widget == self.RESTORE_WALLET:
            self.current_widget = self.current_wallet_widget
        elif self.current_widget == self.SET_WALLET:
            self.current_widget = self.current_wallet_widget

        self.setup_current_widget()

    def back_clicked(self):
        """
        What to do when the back_button button is clicked depending on the current screen
        """

        self.current_widget = self.pop_last_widget()
        self.setup_current_widget()

    def go_to_this_widget(self, widget):
        self.last_widget_stack.append(self.current_widget)
        self.current_widget = widget
        self.setup_current_widget()

    def on_create_wallet_clicked(self):
        """
        Setup the wallet creation screen when the user decides to create one
        """
        self.go_to_this_widget(self.CREATE_WALLET)

    def on_restore_wallet_pushed(self):
        """
        Setup the restore wallet screen when the user decides to restore one
        """
        self.go_to_this_widget(self.RESTORE_WALLET)

    def on_set_wallet_pushed(self):
        """
        Setup the set wallet to set one saved to disk
        """
        self.go_to_this_widget(self.SET_WALLET)

    def on_buy_denarii_screen_pushed(self):
        """
        Navigate to the buy denarii screen of the remote wallet
        """
        self.go_to_this_widget(self.BUY_DENARII)

    def on_sell_denarii_screen_pushed(self):
        """
        Navigate to the sell denarii screen of the remote wallet
        """
        self.go_to_this_widget(self.SELL_DENARII)

    def on_remote_wallet_screen_pushed(self):
        """
        Navigate to the remote wallet screen
        """
        self.go_to_this_widget(self.REMOTE_WALLET_SCREEN)

    def on_login_pushed(self):
        """
        Navigate to the login screen
        """
        self.go_to_this_widget(self.LOGIN_SCREEN)

    def on_register_pushed(self):
        """
        Navigate to the register screen
        """
        self.go_to_this_widget(self.REGISTER_SCREEN)

    def on_credit_card_info_screen_pushed(self):
        """
        Navigate to the credit card info screen
        """
        self.go_to_this_widget(self.CREDIT_CARD_INFO_SCREEN)

    def on_user_settings_screen_pushed(self):
        """
        Navigate to the user settings screen
        """
        self.go_to_this_widget(self.USER_SETTINGS_SCREEN)

    def on_verification_screen_pushed(self):
        """
        Navigate to the verification screen
        """
        self.go_to_this_widget(self.VERIFICATION_SCREEN)

    def on_support_ticket_screen_pushed(self):
        """
        Navigate to the support ticket screen
        """
        self.go_to_this_widget(self.SUPPORT_TICKET_SCREEN)

    def on_support_ticket_creation_screen_pushed(self):
        """
        Navigate to the support ticket creation screen
        """
        self.go_to_this_widget(self.SUPPORT_TICKET_CREATION_SCREEN)

    def on_support_ticket_details_screen_pushed(self, current_support_ticket_id):
        """
        Navigate to the support ticket details screen
        """
        self.current_support_ticket = current_support_ticket_id
        self.go_to_this_widget(self.SUPPORT_TICKET_SCREEN)

    def on_login_or_register_screen_pushed(self):
        """
        Navigate to the login or register screen
        """
        self.go_to_this_widget(self.LOGIN_OR_REGISTER)

    def on_forgot_password_pushed(self):
        """
        Navigate to the request reset screen
        """
        self.go_to_this_widget(self.REQUEST_RESET_SCREEN)
 

    def get_current_support_ticket_id(self):
        return self.current_support_ticket

    def setup_current_widget(self):
        if self.get_last_widget() is not None:
            self.get_last_widget().teardown()

        if self.current_widget is not None:
            self.current_widget.init(**self.kwargs)

            self.current_widget.setup()

    @property
    def wallet(self):
        if self.which_wallet is None:
            return self.local_wallet

        if self.which_wallet == REMOTE_WALLET:
            return self.remote_wallet
        elif self.which_wallet == LOCAL_WALLET:
            return self.local_wallet
        return self.local_wallet

    @property
    def current_wallet_widget(self):
        if self.which_wallet is None:
            return self.LOCAL_WALLET_SCREEN

        if self.which_wallet == REMOTE_WALLET:
            return self.REMOTE_WALLET_SCREEN
        elif self.which_wallet == LOCAL_WALLET:
            return self.LOCAL_WALLET_SCREEN
        return self.LOCAL_WALLET_SCREEN

    def set_wallet_type(self, wallet_type):
        if wallet_type == REMOTE_WALLET:
            self.which_wallet = REMOTE_WALLET
        else:
            self.which_wallet = LOCAL_WALLET
