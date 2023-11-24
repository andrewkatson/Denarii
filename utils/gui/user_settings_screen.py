from gui_user import GuiUser
from screen import *

if TESTING:
    from denarii_testing_font import Font
    from denarii_testing_label import Label
    from denarii_testing_line_edit import LineEdit
    from denarii_testing_message_box import MessageBox
    from denarii_testing_push_button import PushButton
    from denarii_testing_qt import (
        TextSelectableByMouse,
        AlignRight,
        AlignBottom,
        AlignCenter,
        AlignLeft,
    )
    from denarii_testing_radio_button import RadioButton
else:
    from font import *
    from label import *
    from line_edit import *
    from message_box import MessageBox
    from push_button import *
    from qt import (
        TextSelectableByMouse,
        AlignRight,
        AlignBottom,
        AlignCenter,
        AlignLeft,
    )
    from radio_button import *


class UserSettingsScreen(Screen):
    """
    A screen that allows a user to delete their account and set settings
    """

    def __init__(
            self,
            main_layout,
            deletion_func,
            denarii_client,
            gui_user,
            denarii_mobile_client,
            **kwargs
    ):
        self.remote_wallet_screen_push_button = None
        self.sell_screen_push_button = None
        self.buy_screen_push_button = None
        self.credit_card_info_screen_push_button = None
        self.verification_screen_push_button = None
        self.support_ticket_screen_push_button = None
        self.delete_account_push_button = None
        self.logout_push_button = None

        self.user_settings_label = None

        self.on_login_or_register_screen_clicked = kwargs['on_login_or_register_screen_clicked']

        super().__init__(
            self.user_settings_screen_name,
            main_layout=main_layout,
            deletion_func=deletion_func,
            denarii_client=denarii_client,
            gui_user=gui_user,
            denarii_mobile_client=denarii_mobile_client,
            **kwargs
        )

    def init(self, **kwargs):
        super().init(**kwargs)

        self.next_button.setVisible(False)

        self.user_settings_label = Label("User Settings")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.user_settings_label.setFont(font)

        self.remote_wallet_screen_push_button = PushButton("Wallet", kwargs["parent"])
        self.remote_wallet_screen_push_button.clicked.connect(
            lambda: kwargs["on_remote_wallet_screen_clicked"]()
        )
        self.remote_wallet_screen_push_button.setVisible(False)
        self.remote_wallet_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.local_wallet_screen_push_button = PushButton("Wallet", kwargs["parent"])
        self.local_wallet_screen_push_button.clicked.connect(
            lambda: kwargs["on_local_wallet_screen_clicked"]()
        )
        self.local_wallet_screen_push_button.setVisible(False)
        self.local_wallet_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.sell_screen_push_button = PushButton("Sell Denarii", kwargs["parent"])
        self.sell_screen_push_button.clicked.connect(
            lambda: kwargs["on_sell_screen_clicked"]()
        )
        self.sell_screen_push_button.setVisible(False)
        self.sell_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.credit_card_info_screen_push_button = PushButton(
            "Credit Card", kwargs["parent"]
        )
        self.credit_card_info_screen_push_button.clicked.connect(
            lambda: kwargs["on_credit_card_info_screen_clicked"]()
        )
        self.credit_card_info_screen_push_button.setVisible(False)
        self.credit_card_info_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.verification_screen_push_button = PushButton(
            "Verification", kwargs["parent"]
        )
        self.verification_screen_push_button.clicked.connect(
            lambda: kwargs["on_verification_screen_clicked"]()
        )
        self.verification_screen_push_button.setVisible(False)
        self.verification_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.buy_screen_push_button = PushButton("Buy Denarii", kwargs["parent"])
        self.buy_screen_push_button.clicked.connect(
            lambda: kwargs["on_buy_screen_clicked"]()
        )
        self.buy_screen_push_button.setVisible(False)
        self.buy_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.support_ticket_screen_push_button = PushButton("Support Tickets", kwargs["parent"])
        self.support_ticket_screen_push_button.clicked.connect(
            lambda: kwargs["on_support_ticket_screen_clicked"]()
        )
        self.support_ticket_screen_push_button.setVisible(False)
        self.support_ticket_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.delete_account_push_button = PushButton("Delete Account", kwargs["parent"])
        self.delete_account_push_button.clicked.connect(
            lambda: self.on_delete_account_clicked()
        )
        self.delete_account_push_button.setVisible(False)
        self.delete_account_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.logout_push_button = PushButton("Logout", kwargs["parent"])
        self.logout_push_button.clicked.connect(
            lambda: self.on_logout_clicked()
        )
        self.logout_push_button.setVisible(False)
        self.logout_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

    def setup(self):
        super().setup()

        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.vertical_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)

        parent = self.kwargs_passed["parent"]

        if parent.wallet == REMOTE_WALLET:
            self.remote_wallet_screen_push_button.setVisible(True)
            self.sell_screen_push_button.setVisible(True)
            self.credit_card_info_screen_push_button.setVisible(True)
            self.verification_screen_push_button.setVisible(True)
            self.buy_screen_push_button.setVisible(True)
            self.support_ticket_screen_push_button.setVisible(True)
            self.logout_push_button.setVisible(True)
            self.delete_account_push_button.setVisible(True)
        elif parent.wallet == LOCAL_WALLET:
            self.local_wallet_screen_push_button.setVisible(True)
            self.logout_push_button.setVisible(True)
            self.delete_account_push_button.setVisible(True)

        self.first_horizontal_layout.addWidget(self.user_settings_label, alignment=AlignCenter)
        self.vertical_layout.addWidget(self.support_ticket_screen_push_button, alignment=AlignCenter)
        self.vertical_layout.addWidget(self.logout_push_button, alignment=AlignCenter)
        self.vertical_layout.addWidget(self.delete_account_push_button, alignment=AlignCenter)

        self.second_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )
        self.second_horizontal_layout.addWidget(
            self.remote_wallet_screen_push_button, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.local_wallet_screen_push_button, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.buy_screen_push_button, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.credit_card_info_screen_push_button, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.verification_screen_push_button, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.sell_screen_push_button, alignment=AlignCenter
        )

    def teardown(self):
        super().teardown()

    def on_logout_clicked(self):
        try:

            success, res = self.denarii_mobile_client.logout(self.gui_user.user_id)

            parent = self.kwargs_passed["parent"]

            local_success = True
            if parent.wallet == LOCAL_WALLET:
                local_success, res = self.denarii_client.logout()

            if success and local_success:
                self.status_message_box("Successfully Logged Out")
                self.clear_user()
                self.on_login_or_register_screen_clicked()
            else:
                self.status_message_box("Failed to logoout.")

        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

    def on_delete_account_clicked(self):
        try:

            success = self.cancel_all_asks()

            if not success:
                self.status_message_box("Failed to cancel all asks. Cannot delete user")
                return

            success = self.cancel_all_buys()

            if not success:
                self.status_message_box("Failed to cancel all buys. Cannot delete user")
                return

            success = self.denarii_mobile_client.delete_user(self.gui_user.user_id)

            parent = self.kwargs_passed["parent"]

            local_success = True
            if parent.wallet == LOCAL_WALLET:
                local_success, res = self.denarii_client.delete_user()

            if success and local_success:
                self.status_message_box("Deleted user successfully")
                self.clear_user()
                self.on_login_or_register_screen_clicked()
            else:
                self.status_message_box("Failed to delete user")


        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

    def cancel_all_asks(self):

        success, res = self.denarii_mobile_client.get_all_asks(self.gui_user.user_id)

        if not success:
            return False

        for ask in res:
            success, res = self.denarii_mobile_client.cancel_sell(self.gui_user.user_id, ask['ask_id'])

            if not success:
                return False

        return True

    def cancel_all_buys(self):
        success, res = self.denarii_mobile_client.get_all_buys(self.gui_user.user_id)

        if not success:
            return False

        for ask in res:
            success, res = self.denarii_mobile_client.cancel_buy_of_ask(self.gui_user.user_id, ask['ask_id'])

            if not success:
                return False

        return True

    def clear_user(self):
        self.gui_user.name = ""
        self.gui_user.user_id = ""
        self.gui_user.password = ""
        self.gui_user.email = ""
        self.gui_user.local_wallet = None
        self.gui_user.remote_wallet = None
