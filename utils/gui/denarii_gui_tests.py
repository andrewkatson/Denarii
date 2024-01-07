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


support_ticket_id = None


def deletion_function(layout):
    pass


def set_wallet_type(type):
    pass


def next_clicked():
    pass


def back_clicked():
    pass


def on_create_wallet_clicked():
    pass


def on_set_wallet_clicked():
    pass


def on_restore_wallet_clicked():
    pass


def on_buy_screen_clicked():
    pass


def on_sell_screen_clicked():
    pass


def on_remote_wallet_screen_clicked():
    pass


def on_login_clicked():
    pass


def on_register_clicked():
    pass


def on_credit_card_info_screen_clicked():
    pass


def on_user_settings_screen_clicked():
    pass


def on_verification_screen_clicked():
    pass


def on_support_ticket_clicked():
    pass


def get_current_support_ticket_id():
    return support_ticket_id


def on_support_ticket_details_screen_clicked(support_ticket_id):
    support_ticket_id = support_ticket_id


def on_support_ticket_creation_clicked():
    pass

def on_login_or_register_screen_clicked():
    pass

def on_local_wallet_screen_clicked():
    pass

def create_remote_user(user, denarii_mobile_client):
    success, create_user_res = denarii_mobile_client.get_user_id(
        user.name, user.email, user.password
    )

    assert success
    assert len(create_user_res) > 0

    user_id = create_user_res[0]["user_id"]

    user.user_id = user_id

    return user_id


def create_remote_wallet(user, denarii_mobile_client, wallet):
    user_id = create_remote_user(user, denarii_mobile_client)

    other_success, create_wallet_res = denarii_mobile_client.create_wallet(
        user_id, wallet.name, wallet.password
    )

    assert other_success

    only_res = create_wallet_res[0]
    wallet.phrase = only_res["seed"]
    wallet.address = only_res["wallet_address"]

    return create_wallet_res


class DenariiDesktopGUICreateWalletScreenTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.gui_user = GuiUser()
        self.gui_user.name = f"create_wallet_screen_name_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"create_wallet_screen_email_{self._testMethodName}@email.com"
        )

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        create_remote_user(self.gui_user, self.denarii_mobile_client)

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

        self.create_wallet_screen = CreateWalletScreen(
            push_buttons=common_buttons,
            parent=self.main_widget,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            set_wallet_type_callback=set_wallet_type,
        )

    def tearDown(self):
        super().tearDown()

        print(f"Finished Running {self.id()}-{self._testMethodName}")

        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.create_wallet_screen.setup()

    def test_teardown(self):
        self.create_wallet_screen.teardown()

    def test_create_local_wallet(self):
        self.create_wallet_screen.which_wallet = LOCAL_WALLET

        self.create_wallet_screen.name_line_edit.text_inner = "Name"
        self.create_wallet_screen.password_line_edit.text_inner = "Password"
        self.create_wallet_screen.confirm_password_line_edit.text_inner = "Password"

        self.create_wallet_screen.create_wallet()

        # Best we can do is check that they have a seed
        self.assertIsNotNone(self.create_wallet_screen.wallet_info_text_box.text)
        self.assertNotEqual(self.local_wallet.phrase, "")

        self.assertIsNotNone(self.create_wallet_screen.wallet_save_file_text_box.text)
        self.assertRegex(
            self.create_wallet_screen.wallet_save_file_text_box.text,
            "Wallet saved to:.*",
        )

        self.assertEqual(
            self.create_wallet_screen.status_msg.text,
            "Success. Make sure to write down your information. \n It will not be saved on this device.",
        )

    def test_create_remote_wallet(self):
        self.create_wallet_screen.which_wallet = REMOTE_WALLET

        self.create_wallet_screen.name_line_edit.text_inner = "Name"
        self.create_wallet_screen.password_line_edit.text_inner = "Password"
        self.create_wallet_screen.confirm_password_line_edit.text_inner = "Password"

        self.create_wallet_screen.create_wallet()

        # Best we can do is check that they have a seed
        self.assertIsNotNone(self.create_wallet_screen.wallet_info_text_box.text)
        self.assertNotEqual(self.remote_wallet.phrase, "")

        # We dont save a file with create wallet when its remote
        self.assertEqual(self.create_wallet_screen.wallet_save_file_text_box.text, "")

        self.assertEqual(
            self.create_wallet_screen.status_msg.text,
            "Success. Make sure to write down your information. \n It will not be saved on this device.",
        )


class DenariiDesktopGUILanguageSelectScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"language_select_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"language_select_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user,
            self.denarii_mobile_client,
            self.remote_wallet,
        )
        self.denarii_client.create_wallet(self.local_wallet)

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

        self.lang_select_screen = LangSelectScreen(
            push_buttons=common_buttons,
            gui_user=self.gui_user,
            parent=self.main_widget,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_mobile_client=self.denarii_mobile_client,
            denarii_client=self.denarii_client,
        )

    def tearDown(self):
        super().tearDown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.lang_select_screen.setup()

    def test_teardown(self):
        self.lang_select_screen.teardown()

    def test_on_submit_clicked_with_no_user_language(self):
        self.lang_select_screen.on_submit_clicked()

        self.assertFalse(self.lang_select_screen.next_button.is_visible)

        self.assertNotEqual(self.lang_select_screen.status_msg.text, "Success")

    def test_on_submit_clicked_with_user_language(self):
        self.gui_user.language = "English"

        self.lang_select_screen.on_submit_clicked()

        self.assertTrue(self.lang_select_screen.next_button.is_visible)

        self.assertEqual(self.lang_select_screen.status_msg.text, "Success")


class DenariiDesktopGUILocalWalletScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"local_wallet_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"local_wallet_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.local_wallet_screen = LocalWalletScreen(
            push_buttons=common_buttons,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            parent=self.main_widget,
            denarii_client=self.denarii_client,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            on_user_settings_screen_clicked=on_user_settings_screen_clicked
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.local_wallet_screen.teardown()

        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.local_wallet_screen.setup()

    def test_teardown(self):
        self.local_wallet_screen.teardown()

    def test_populate_wallet_screen(self):
        self.local_wallet_screen.populate_wallet_screen()

        self.assertIsNotNone(self.local_wallet_screen.balance_text_box)
        self.assertIsNotNone(self.local_wallet_screen.address_text_box)

        self.assertEqual(
            self.local_wallet_screen.status_msg.text, "Success loading wallet info"
        )

    def test_create_sub_address(self):
        self.assertEqual(len(self.local_wallet_screen.sub_address_text_boxes), 0)

        self.local_wallet_screen.create_sub_address()

        self.assertEqual(len(self.local_wallet_screen.sub_address_text_boxes), 1)

        self.assertEqual(
            self.local_wallet_screen.status_msg.text,
            "Success creating sub address. \n Use this to send denarii to other people.",
        )

    def test_mining(self):
        self.local_wallet_screen.start_mining()

        self.assertEqual(self.local_wallet_screen.status_msg.text, "Started mining")

        self.local_wallet_screen.stop_mining()

        self.assertEqual(self.local_wallet_screen.status_msg.text, "Stopped mining")

    def test_stop_mining_without_starting(self):
        self.local_wallet_screen.stop_mining()

        self.assertEqual(
            self.local_wallet_screen.status_msg.text, "Failed to stop mining"
        )


class DenariiDesktopGUIRemoteWalletScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"remote_wallet_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"remote_wallet_screen_password_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.remote_wallet_screen = RemoteWalletScreen(
            push_buttons=common_buttons,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            parent=self.main_widget,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            gui_user=self.gui_user,
            on_buy_screen_clicked=on_buy_screen_clicked,
            on_sell_screen_clicked=on_sell_screen_clicked,
            on_credit_card_info_screen_clicked=on_credit_card_info_screen_clicked,
            on_user_settings_screen_clicked=on_user_settings_screen_clicked,
            on_verification_screen_clicked=on_verification_screen_clicked,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.remote_wallet_screen.teardown()

        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.remote_wallet_screen.setup()

    def test_teardown(self):
        self.remote_wallet_screen.teardown()

    def test_populate_wallet_screen(self):
        self.remote_wallet_screen.populate_wallet_screen()

        self.assertIsNotNone(self.remote_wallet_screen.balance_text_box)
        self.assertIsNotNone(self.remote_wallet_screen.address_text_box)

        self.assertEqual(
            self.remote_wallet_screen.status_msg.text, "Success loading wallet info"
        )


class DenariiDesktopGUIRestoreWalletScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"restore_wallet_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"restore_wallet_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user,
            self.denarii_mobile_client,
            self.remote_wallet,
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.restore_wallet_screen = RestoreWalletScreen(
            push_buttons=common_buttons,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            parent=self.main_widget,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            set_wallet_type_callback=set_wallet_type,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.restore_wallet_screen.teardown()

        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.restore_wallet_screen.setup()

    def test_teardown(self):
        self.restore_wallet_screen.teardown()

    def test_restore_local_wallet(self):
        self.restore_wallet_screen.which_wallet = LOCAL_WALLET

        self.restore_wallet_screen.name_line_edit.text_inner = self.local_wallet.name
        self.restore_wallet_screen.password_line_edit.text_inner = (
            self.local_wallet.password
        )
        self.restore_wallet_screen.seed_line_edit.text_inner = self.local_wallet.phrase

        self.restore_wallet_screen.restore_wallet()

        self.assertIsNotNone(self.restore_wallet_screen.wallet_save_file_text_box.text)
        self.assertRegex(
            self.restore_wallet_screen.wallet_save_file_text_box.text,
            "Wallet saved to:.*",
        )

        self.assertEqual(self.restore_wallet_screen.status_msg.text, "Success")

    def test_restore_remote_wallet(self):
        self.restore_wallet_screen.which_wallet = REMOTE_WALLET

        self.restore_wallet_screen.name_line_edit.text_inner = self.remote_wallet.name
        self.restore_wallet_screen.password_line_edit.text_inner = (
            self.remote_wallet.password
        )
        self.restore_wallet_screen.seed_line_edit.text_inner = self.remote_wallet.phrase

        self.restore_wallet_screen.restore_wallet()

        self.assertEqual(self.restore_wallet_screen.status_msg.text, "Success")


class DenariiDesktopGUISetWalletScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"set_wallet_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"set_wallet_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

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

        self.set_wallet_screen = SetWalletScreen(
            push_buttons=common_buttons,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            parent=self.main_widget,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            set_wallet_type_callback=set_wallet_type,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.set_wallet_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.set_wallet_screen.setup()

    def test_teardown(self):
        self.set_wallet_screen.teardown()

    def test_set_local_wallet(self):
        self.set_wallet_screen.which_wallet = LOCAL_WALLET

        self.set_wallet_screen.name_line_edit.text_inner = self.local_wallet.name
        self.set_wallet_screen.password_line_edit.text_inner = (
            self.local_wallet.password
        )

        self.set_wallet_screen.set_wallet()

        self.assertIsNotNone(self.set_wallet_screen.set_wallet_text_box.text)
        self.assertRegex(
            self.set_wallet_screen.set_wallet_text_box.text, "Your seed is: .*"
        )

        self.assertEqual(self.set_wallet_screen.status_msg.text, "Success")

    def test_set_remote_wallet(self):
        self.set_wallet_screen.which_wallet = REMOTE_WALLET

        self.set_wallet_screen.name_line_edit.text_inner = self.remote_wallet.name
        self.set_wallet_screen.password_line_edit.text_inner = (
            self.remote_wallet.password
        )

        self.set_wallet_screen.set_wallet()

        self.assertIsNotNone(self.set_wallet_screen.set_wallet_text_box.text)
        self.assertRegex(
            self.set_wallet_screen.set_wallet_text_box.text, "Your seed is: .*"
        )

        self.assertEqual(self.set_wallet_screen.status_msg.text, "Success")


class DenariiDesktopGUILoginScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"login_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = f"login_screen_email_{self._testMethodName}@email.com"

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

        self.local_seed = self.denarii_client.query_seed(self.local_wallet)

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

        self.login_screen = LoginScreen(
            push_buttons=common_buttons,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            parent=self.main_widget,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.login_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.login_screen.setup()

    def test_teardown(self):
        self.login_screen.teardown()

    def test_store_user_info_with_matching_passwords(self):
        self.login_screen.name_line_edit.text_inner = "Name"
        self.login_screen.email_line_edit.text_inner = "email@email.com"
        self.login_screen.password_line_edit.text_inner = "password"
        

        self.login_screen.store_user_info()

        self.assertEqual(self.login_screen.status_msg.text, "Success")


class DenariiDesktopGUIRegisterScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"register_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = f"register_screen_email_{self._testMethodName}@email.com"

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

        self.local_seed = self.denarii_client.query_seed(self.local_wallet)

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

        self.register_screen = RegisterScreen(
            push_buttons=common_buttons,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            parent=self.main_widget,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.register_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.register_screen.setup()

    def test_teardown(self):
        self.register_screen.teardown()

    def test_store_user_info_with_matching_passwords(self):
        self.register_screen.name_line_edit.text_inner = "Name"
        self.register_screen.email_line_edit.text_inner = "email@email.com"
        self.register_screen.password_line_edit.text_inner = "pass"
        self.register_screen.confirm_password_line_edit.text_inner = "pass"

        self.register_screen.store_user_info()

        self.assertEqual(self.register_screen.status_msg.text, "Success")

    def test_store_user_info_with_not_matching_passwords(self):
        self.register_screen.name_line_edit.text_inner = "Name"
        self.register_screen.email_line_edit.text_inner = "email@email.com"
        self.register_screen.password_line_edit.text_inner = "pass"
        self.register_screen.confirm_password_line_edit.text_inner = "confirm"

        self.register_screen.store_user_info()

        self.assertEqual(
            self.register_screen.status_msg.text, "Failure: passwords did not match"
        )


class DenariiDesktopGUIWalletInfoScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"wallet_info_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"wallet_info_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

        self.local_seed = self.denarii_client.query_seed(self.local_wallet)

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

        self.wallet_info_screeen = WalletInfoScreen(
            push_buttons=common_buttons,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            parent=self.main_widget,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            on_create_wallet_clicked=on_create_wallet_clicked,
            on_set_wallet_clicked=on_set_wallet_clicked,
            on_restore_wallet_clicked=on_restore_wallet_clicked,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.wallet_info_screeen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.wallet_info_screeen.setup()

    def test_teardown(self):
        self.wallet_info_screeen.teardown()


class DenariiDesktopGUIBuyDenariiScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"buy_denarii_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"buy_denarii_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.buy_denarii_screen = BuyDenariiScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            on_remote_wallet_screen_clicked=on_remote_wallet_screen_clicked,
            on_sell_screen_clicked=on_sell_screen_clicked,
            on_credit_card_info_screen_clicked=on_credit_card_info_screen_clicked,
            on_user_settings_screen_clicked=on_user_settings_screen_clicked,
            on_verification_screen_clicked=on_verification_screen_clicked,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.buy_denarii_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.buy_denarii_screen.setup()

    def test_teardown(self):
        self.buy_denarii_screen.teardown()


class DenariiDesktopGUISellDenariiScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"sell_denarii_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"sell_denarii_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.sell_denarii_screen = SellDenariiScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            on_remote_wallet_screen_clicked=on_remote_wallet_screen_clicked,
            on_buy_screen_clicked=on_buy_screen_clicked,
            on_credit_card_info_screen_clicked=on_credit_card_info_screen_clicked,
            on_user_settings_screen_clicked=on_user_settings_screen_clicked,
            on_verification_screen_clicked=on_verification_screen_clicked,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.sell_denarii_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.sell_denarii_screen.setup()

    def test_teardown(self):
        self.sell_denarii_screen.teardown()


class DenariiDesktopGUILoginOrRegisterScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"login_or_register_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"login_or_register_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.login_or_register_screen = LoginOrRegisterScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            on_login_clicked=on_login_clicked,
            on_register_clicked=on_register_clicked,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.login_or_register_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.login_or_register_screen.setup()

    def test_teardown(self):
        self.login_or_register_screen.teardown()


class DenariiDesktopGUIRequestResetScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"request_reset_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"request_reset_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.request_reset_screen = RequestResetScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.request_reset_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.request_reset_screen.setup()

    def test_teardown(self):
        self.request_reset_screen.teardown()

    def test_request_reset(self):
        self.request_reset_screen.name_or_email_line_edit.text_inner = (
            self.gui_user.name
        )

        self.request_reset_screen.on_submit_clicked()

        self.assertEqual(self.request_reset_screen.status_msg.text, "Success")


class DenariiDesktopGUIResetPasswordScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"reset_password_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"reset_password_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.reset_password_screen = ResetPasswordScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.reset_password_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.reset_password_screen.setup()

    def test_teardown(self):
        self.reset_password_screen.teardown()

    def test_reset_password(self):
        self.reset_password_screen.name_line_edit.text_inner = self.gui_user.name
        self.reset_password_screen.email_line_edit.text_inner = self.gui_user.email
        self.reset_password_screen.password_line_edit.text_inner = (
            self.gui_user.password
        )
        self.reset_password_screen.confirm_password_line_edit.text_inner = (
            self.gui_user.password
        )

        self.reset_password_screen.on_submit_clicked()

        self.assertEqual(self.reset_password_screen.status_msg.text, "Success")


class DenariiDesktopGUIVerifyResetScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"verify_reset_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"verify_reset_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

        # We must request a reset
        self.denarii_mobile_client.request_reset(self.gui_user.name)

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

        self.verify_reset_screen = VerifyResetScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.verify_reset_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.verify_reset_screen.setup()

    def test_teardown(self):
        self.verify_reset_screen.teardown()

    def test_verify_reset(self):
        self.verify_reset_screen.reset_id_line_edit.text_inner = 4

        self.verify_reset_screen.on_submit_clicked()

        self.assertEqual(self.verify_reset_screen.status_msg.text, "Success")


class DenariiDesktopGUICreditCardInfoScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"credit_card_info_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"credit_card_info_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.credit_card_info_screen = CreditCardInfoScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            on_remote_wallet_screen_clicked=on_remote_wallet_screen_clicked,
            on_buy_screen_clicked=on_buy_screen_clicked,
            on_credit_card_info_screen_clicked=on_credit_card_info_screen_clicked,
            on_user_settings_screen_clicked=on_user_settings_screen_clicked,
            on_verification_screen_clicked=on_verification_screen_clicked,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.credit_card_info_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.credit_card_info_screen.setup()

    def test_teardown(self):
        self.credit_card_info_screen.teardown()


class DenariiDesktopGUISupportTicketScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"support_ticket_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"support_ticket_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.support_ticket_screen = SupportTicketScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            on_user_settings_screen_clicked=on_user_settings_screen_clicked,
            on_support_ticket_creation_screen_clicked=on_support_ticket_creation_clicked,
            on_support_ticket_details_screen_clicked=lambda support_ticket_id: on_support_ticket_details_screen_clicked(
                support_ticket_id
            ),
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.support_ticket_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.support_ticket_screen.setup()

    def test_teardown(self):
        self.support_ticket_screen.teardown()


class DenariiDesktopGUISupportTicketCreationScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = (
            f"support_ticket_creation_screen_user_{self._testMethodName}"
        )
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"support_ticket_creation_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.support_ticket_creation_screen = SupportTicketCreationScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            on_support_ticket_screen_clicked=on_support_ticket_clicked,
            on_support_ticket_details_screen_clicked=lambda support_ticket_id: on_support_ticket_details_screen_clicked(
                support_ticket_id
            ),
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.support_ticket_creation_screen.teardown()
        print(f"Finished  {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.support_ticket_creation_screen.setup()

    def test_teardown(self):
        self.support_ticket_creation_screen.teardown()


class DenariiDesktopGUISupportTicketDetailsScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = (
            f"support_ticket_details_screen_user_{self._testMethodName}"
        )
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"support_ticket_details_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.support_ticket_details_screen = SupportTicketDetailsScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            on_support_ticket_screen_clicked=on_support_ticket_clicked,
            get_current_support_ticket_id=get_current_support_ticket_id,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.support_ticket_details_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.support_ticket_details_screen.setup()

    def test_teardown(self):
        self.support_ticket_details_screen.teardown()


class DenariiDesktopGUIUserSettingsScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"user_settings_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"user_settings_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.wallet = REMOTE_WALLET

        self.user_settings_screen = UserSettingsScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            on_remote_wallet_screen_clicked=on_remote_wallet_screen_clicked,
            on_local_wallet_screen_clicked=on_local_wallet_screen_clicked,
            on_buy_screen_clicked=on_buy_screen_clicked,
            on_credit_card_info_screen_clicked=on_credit_card_info_screen_clicked,
            on_verification_screen_clicked=on_verification_screen_clicked,
            on_support_ticket_clicked=on_support_ticket_clicked,
            on_login_or_register_screen_clicked=on_login_or_register_screen_clicked
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.user_settings_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.user_settings_screen.setup()

    def test_teardown(self):
        self.user_settings_screen.teardown()


class DenariiDesktopGUIVerificationScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.start_time = time.time()

        print(f"Running {self.id()}-{self._testMethodName}")

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name=f"remote{self._testMethodName}", password="remote_password")
        self.local_wallet = Wallet(name=f"local{self._testMethodName}", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"verification_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = (
            f"verification_screen_email_{self._testMethodName}@email.com"
        )

        # We must create each wallet
        create_remote_wallet(
            self.gui_user, self.denarii_mobile_client, self.remote_wallet
        )
        self.denarii_client.create_wallet(self.local_wallet)

        # We must set the wallet to the local one
        self.denarii_client.set_current_wallet(self.local_wallet)

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

        self.verification_screen = VerificationScreen(
            push_buttons=common_buttons,
            parent=self,
            denarii_mobile_client=self.denarii_mobile_client,
            main_layout=self.main_widget.main_layout,
            deletion_func=deletion_function,
            denarii_client=self.denarii_client,
            remote_wallet=self.remote_wallet,
            local_wallet=self.local_wallet,
            gui_user=self.gui_user,
            on_remote_wallet_screen_clicked=on_remote_wallet_screen_clicked,
            on_buy_screen_clicked=on_buy_screen_clicked,
            on_credit_card_info_screen_clicked=on_credit_card_info_screen_clicked,
            on_user_settings_screen_clicked=on_user_settings_screen_clicked,
        )

    def tearDown(self):
        super().tearDown()

        # We need to teardown the screen in case there are threads running.
        self.verification_screen.teardown()
        print(f"Finished Running {self.id()}-{self._testMethodName}")
        t = time.time() - self.start_time
        print("%s: %.3f" % (self.id(), t))

    def test_setup(self):
        self.verification_screen.setup()

    def test_teardown(self):
        self.verification_screen.teardown()


if __name__ == "__main__":
    # We need to remove all denarii specific test arguments for this to not fail.
    unittest.main(
        argv=list((arg for arg in sys.argv if not arg.startswith("--denarii")))
    )
