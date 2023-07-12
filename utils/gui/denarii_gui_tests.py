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
from lang_select_screen import LangSelectScreen
from local_wallet_screen import LocalWalletScreen
from remote_wallet_screen import RemoteWalletScreen
from restore_wallet_screen import RestoreWalletScreen
from set_wallet_screen import SetWalletScreen
from user_info_screen import UserInfoScreen
from wallet_info_screen import WalletInfoScreen


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


def create_remote_wallet(user, denarii_mobile_client, wallet):
    success, create_user_res = denarii_mobile_client.get_user_id(
        user.name, user.email, user.password
    )

    assert success
    assert len(create_user_res) > 0

    user_id = create_user_res[0]["user_id"]
    other_success, create_wallet_res = denarii_mobile_client.create_wallet(
        user_id, wallet.name, wallet.password
    )

    assert other_success

    only_res = create_wallet_res[0]
    wallet.phrase = only_res['seed']
    wallet.address = only_res['wallet_address']

    return create_wallet_res


class DenariiDesktopGUICreateWalletScreenTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.gui_user = GuiUser()
        self.gui_user.name = f"create_wallet_screen_name_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = f"create_wallet_screen_email_{self._testMethodName}@email.com"

        self.remote_wallet = Wallet(name="remote", password="remote_password")
        self.local_wallet = Wallet(name="local", password="local_password")

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

        print("Setting up create wallet")
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
        print("Finished setting up create wallet")

    def tearDown(self):
        super().tearDown()

    def test_setup(self):
        print("before setup")
        self.create_wallet_screen.setup()
        print("after setup")

    def test_teardown(self):
        self.create_wallet_screen.teardown()

    def test_create_local_wallet(self):
        self.create_wallet_screen.which_wallet = LOCAL_WALLET

        self.create_wallet_screen.name_line_edit.text_inner = "Name"
        self.create_wallet_screen.password_line_edit.text_inner = "Password"

        self.create_wallet_screen.create_wallet()

        # Best we can do is check that they have a seed
        self.assertIsNotNone(self.create_wallet_screen.wallet_info_text_box.text)
        self.assertNotEqual(self.create_wallet_screen.wallet_info_text_box.text, "")

        self.assertIsNotNone(self.create_wallet_screen.wallet_save_file_text_box.text)
        self.assertRegex(
            self.create_wallet_screen.wallet_save_file_text_box.text,
            "Wallet saved to:.*",
        )

        self.assertIsNotNone(self.create_wallet_screen.create_wallet_text_box.text)
        self.assertEqual(
            self.create_wallet_screen.create_wallet_text_box.text,
            "Success. Make sure to write down your information. \n It will not be saved on this device.",
        )

    def test_create_remote_wallet(self):
        self.create_wallet_screen.which_wallet = REMOTE_WALLET

        self.create_wallet_screen.name_line_edit.text_inner = "Name"
        self.create_wallet_screen.password_line_edit.text_inner = "Password"

        self.create_wallet_screen.create_wallet()

        # Best we can do is check that they have a seed
        self.assertIsNotNone(self.create_wallet_screen.wallet_info_text_box.text)
        self.assertNotEqual(self.create_wallet_screen.wallet_info_text_box.text, "")

        # We dont save a file with create wallet when its remote
        self.assertEqual(self.create_wallet_screen.wallet_save_file_text_box.text, "")

        self.assertIsNotNone(self.create_wallet_screen.create_wallet_text_box.text)
        self.assertEqual(
            self.create_wallet_screen.create_wallet_text_box.text,
            "Success. Make sure to write down your information. \n It will not be saved on this device.",
        )


class DenariiDesktopGUILanguageSelectScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name="remote", password="remote_password")
        self.local_wallet = Wallet(name="local", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"language_select_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = f"language_select_screen_email_{self._testMethodName}@email.com"

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

    def test_setup(self):
        self.lang_select_screen.setup()

    def test_teardown(self):
        self.lang_select_screen.teardown()

    def test_on_submit_clicked_with_no_user_language(self):
        self.lang_select_screen.on_submit_clicked()

        self.assertFalse(self.lang_select_screen.next_button.is_visible)

    def test_on_submit_clicked_with_user_language(self):
        self.gui_user.language = "English"

        self.lang_select_screen.on_submit_clicked()

        self.assertTrue(self.lang_select_screen.next_button.is_visible)


class DenariiDesktopGUILocalWalletScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name="remote", password="remote_password")
        self.local_wallet = Wallet(name="local", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"local_wallet_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = f"local_wallet_screen_email_{self._testMethodName}@email.com"

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
        )

    def tearDown(self):
        super().tearDown()

    def test_setup(self):
        self.local_wallet_screen.setup()

    def test_teardown(self):
        self.local_wallet_screen.teardown()

    def test_create_sub_address(self):
        self.assertEqual(len(self.local_wallet_screen.sub_address_text_boxes), 0)

        self.local_wallet_screen.create_sub_address()

        self.assertEqual(len(self.local_wallet_screen.sub_address_text_boxes), 1)

        self.assertEqual(
            self.local_wallet_screen.wallet_info_status_text_box.text,
            "Success creating sub address. \n Use this to send denarii to other people.",
        )

    def test_mining(self):
        self.local_wallet_screen.start_mining()

        self.assertEqual(
            self.local_wallet_screen.wallet_info_status_text_box.text, "Started mining"
        )

        self.local_wallet_screen.stop_mining()

        self.assertEqual(
            self.local_wallet_screen.wallet_info_status_text_box.text, "Stopped mining"
        )

    def test_stop_mining_without_starting(self):
        self.local_wallet_screen.stop_mining()

        self.assertEqual(
            self.local_wallet_screen.wallet_info_status_text_box.text,
            "Failed to stop mining",
        )


class DenariiDesktopGUIRemoteWalletScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name="remote", password="remote_password")
        self.local_wallet = Wallet(name="local", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"remote_wallet_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = f"remote_wallet_screen_password_{self._testMethodName}@email.com"

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
        )

    def tearDown(self):
        super().tearDown()

    def test_setup(self):
        self.remote_wallet_screen.setup()

    def test_teardown(self):
        self.remote_wallet_screen.teardown()


class DenariiDesktopGUIRestoreWalletScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name="remote", password="remote_password")
        self.local_wallet = Wallet(name="local", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"restore_wallet_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = f"restore_wallet_screen_email_{self._testMethodName}@email.com"

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

        self.assertIsNotNone(self.restore_wallet_screen.restore_wallet_text_box.text)
        self.assertEqual(
            self.restore_wallet_screen.restore_wallet_text_box.text,
            "Success",
        )

    def test_restore_remote_wallet(self):
        self.restore_wallet_screen.which_wallet = REMOTE_WALLET

        self.restore_wallet_screen.name_line_edit.text_inner = self.remote_wallet.name
        self.restore_wallet_screen.password_line_edit.text_inner = (
            self.remote_wallet.password
        )
        self.restore_wallet_screen.seed_line_edit.text_inner = self.remote_wallet.phrase

        self.restore_wallet_screen.restore_wallet()

        self.assertIsNotNone(self.restore_wallet_screen.restore_wallet_text_box.text)
        self.assertEqual(
            self.restore_wallet_screen.restore_wallet_text_box.text,
            "Success",
        )


class DenariiDesktopGUISetWalletScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name="remote", password="remote_password")
        self.local_wallet = Wallet(name="local", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"set_wallet_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = f"set_wallet_screen_email_{self._testMethodName}@email.com"

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
            self.set_wallet_screen.set_wallet_text_box.text, "Success. Your seed is: .*"
        )
    
    def test_set_remote_wallet(self):

        self.set_wallet_screen.which_wallet = REMOTE_WALLET

        self.set_wallet_screen.name_line_edit.text_inner = self.remote_wallet.name
        self.set_wallet_screen.password_line_edit.text_inner = (
            self.remote_wallet.password
        )

        self.set_wallet_screen.set_wallet()

        self.assertIsNotNone(self.set_wallet_screen.set_wallet_text_box.text)
        self.assertRegex(
            self.set_wallet_screen.set_wallet_text_box.text, "Success. Your seed is: .*"
        )


class DenariiDesktopGUIUserInfoScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name="remote", password="remote_password")
        self.local_wallet = Wallet(name="local", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"user_info_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = f"user_info_screen_email_{self._testMethodName}@email.com"

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

        self.user_info_screen = UserInfoScreen(
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

    def test_setup(self):
        self.user_info_screen.setup()

    def test_teardown(self):
        self.user_info_screen.teardown()

    def test_store_user_info_with_matching_passwords(self):
        self.user_info_screen.name_line_edit.text_inner = "Name"
        self.user_info_screen.email_line_edit.text_inner = "email@email.com"
        self.user_info_screen.password_line_edit.text_inner = "pass"
        self.user_info_screen.confirm_password_line_edit.text_inner = "confirm_pass"

        self.user_info_screen.store_user_info()

        self.assertIsNotNone(self.user_info_screen.user_info_status_text_box.text)
        self.assertEqual(
            self.user_info_screen.user_info_status_text_box.text,
            "Failure: passwords did not match",
        )

    def test_store_user_info_with_not_matching_passwords(self):
        self.user_info_screen.name_line_edit.text_inner = "Name"
        self.user_info_screen.email_line_edit.text_inner = "email@email.com"
        self.user_info_screen.password_line_edit.text_inner = "pass"
        self.user_info_screen.confirm_password_line_edit.text_inner = "pass"

        self.user_info_screen.store_user_info()

        self.assertIsNotNone(self.user_info_screen.user_info_status_text_box.text)
        self.assertEqual(
            self.user_info_screen.user_info_status_text_box.text, "Success"
        )


class DenariiDesktopGUIWalletInfoScreenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.window = Window()
        self.main_widget = Widget()
        self.main_widget.setMainLayout(HBoxLayout())
        self.window.setCentralWidget(self.main_widget)

        self.denarii_mobile_client = DenariiMobileClient()
        self.denarii_client = DenariiClient()

        self.remote_wallet = Wallet(name="remote", password="remote_password")
        self.local_wallet = Wallet(name="local", password="local_password")

        self.gui_user = GuiUser()
        self.gui_user.name = f"wallet_info_screen_user_{self._testMethodName}"
        self.gui_user.password = "password"
        self.gui_user.email = f"wallet_info_screen_email_{self._testMethodName}@email.com"

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

    def test_setup(self):
        self.wallet_info_screeen.setup()

    def test_teardown(self):
        self.wallet_info_screeen.teardown()


if __name__ == "__main__":
    # We need to remove all denarii specific test arguments for this to not fail.
    unittest.main(
        argv=list((arg for arg in sys.argv if not arg.startswith("--denarii")))
    )
