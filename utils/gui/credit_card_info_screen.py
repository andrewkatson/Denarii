from screen import *

if TESTING:
    from denarii_testing_font import Font
    from denarii_testing_label import Label
    from denarii_testing_line_edit import LineEdit
    from denarii_testing_message_box import MessageBox
    from denarii_testing_push_button import PushButton
    from denarii_testing_qt import (
        AlignBottom,
        AlignCenter,
        AlignLeft,
    )
else:
    from font import *
    from label import *
    from line_edit import *
    from message_box import MessageBox
    from push_button import *
    from qt import (
        AlignBottom,
        AlignCenter,
        AlignLeft,
    )
    from radio_button import *


class CreditCardInfoScreen(Screen):
    """
    A screen that allows the user to set or clear their credit card info
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
        self.user_settings_screen_push_button = None
        self.verification_screen_push_button = None

        self.submit_push_button = None
        self.clear_info_push_button = None

        self.credit_card_info_label = None

        # We need to explicitly set the gui_user since we use it in check_credit_card_info
        self.gui_user = gui_user

        # We need to explicitly set the denarii mobile client since we call it in check_credit_card_info
        self.denarii_mobile_client = denarii_mobile_client

        self.status = self.check_credit_card_info()

        self.status_label = None

        self.card_number_line_edit = None
        self.expiration_date_month_line_edit = None
        self.expiration_date_year_line_edit = None
        self.security_code_line_edit = None

        super().__init__(
            self.credit_card_info_screen_name,
            main_layout,
            deletion_func,
            denarii_client,
            gui_user,
            denarii_mobile_client,
            **kwargs
        )

    def init(self, **kwargs):
        super().init(**kwargs)
        self.next_button.setVisible(False)

        self.credit_card_info_label = Label("Credit Card Info")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.credit_card_info_label.setFont(font)

        self.remote_wallet_screen_push_button = PushButton("Wallet", kwargs["parent"])
        self.remote_wallet_screen_push_button.clicked.connect(
            lambda: kwargs["on_remote_wallet_screen_clicked"]()
        )
        self.remote_wallet_screen_push_button.setVisible(False)
        self.remote_wallet_screen_push_button.setStyleSheet(
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

        self.verification_screen_push_button = PushButton(
            "Identity Verification", kwargs["parent"]
        )
        self.verification_screen_push_button.clicked.connect(
            lambda: kwargs["on_verification_screen_clicked"]()
        )
        self.verification_screen_push_button.setVisible(False)
        self.verification_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.user_settings_screen_push_button = PushButton(
            "User Settings", kwargs["parent"]
        )
        self.user_settings_screen_push_button.clicked.connect(
            lambda: kwargs["on_user_settings_screen_clicked"]()
        )
        self.user_settings_screen_push_button.setVisible(False)
        self.user_settings_screen_push_button.setStyleSheet(
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

        self.submit_push_button = PushButton("Submit", kwargs["parent"])
        self.submit_push_button.clicked.connect(lambda: self.on_submit_clicked())
        self.submit_push_button.setVisible(False)
        self.submit_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.clear_info_push_button = PushButton("Clear Info", kwargs["parent"])
        self.clear_info_push_button.clicked.connect(
            lambda: self.on_clear_info_clicked()
        )
        self.clear_info_push_button.setVisible(False)
        self.clear_info_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.status_label = Label(self.format_status())
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.status_label.setFont(font)

        self.card_number_line_edit = LineEdit()
        self.expiration_date_month_line_edit = LineEdit()
        self.expiration_date_year_line_edit = LineEdit()
        self.security_code_line_edit = LineEdit()

    def setup(self):
        super().setup()

        self.refresh_screen()

    def teardown(self):
        super().teardown()

    def format_status(self):
        if self.status is True:
            return "Status: Have Info Set"
        else:
            return "Status: No Info Set"

    def on_submit_clicked(self):
        
        invalid_fields = []
        
        if not is_valid_pattern(self.card_number_line_edit.text(), Patterns.digits_and_dashes):
            invalid_fields.append(Params.card_number)
        
        if not is_valid_pattern(self.expiration_date_month_line_edit.text(), Patterns.digits_only): 
            invalid_fields.append(Params.expiration_date_month)
            
        if not is_valid_pattern(self.expiration_date_year_line_edit.text(), Patterns.digits_only): 
            invalid_fields.append(Params.expiration_date_year)
            
        if not is_valid_pattern(self.security_code_line_edit.text(), Patterns.digits_only): 
            invalid_fields.append(Params.security_code)
            
        if not len(invalid_fields) > 0:
            self.status_message_box(f"Failed: Invalid Fields {invalid_fields}")
            return
        
        try:
            success = self.denarii_mobile_client.set_credit_card_info(
                self.gui_user.user_id,
                self.card_number_line_edit.text(),
                self.expiration_date_month_line_edit.text(),
                self.expiration_date_year_line_edit.text(),
                self.security_code_line_edit.text(),
            )

            if success:
                self.status_message_box("Set credit card info")
            else:
                self.status_message_box("Failed to set credit card info")

            self.status = self.check_credit_card_info()
            self.status_label.setText(self.format_status())
            self.refresh_screen()
        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

    def on_clear_info_clicked(self):
        try:
            success = self.denarii_mobile_client.clear_credit_card_info(
                self.gui_user.user_id
            )

            if success:
                self.status_message_box("Cleared credit card info")
            else:
                self.status_message_box("Failed to clear credit card info")

            self.status = self.check_credit_card_info()
            self.status_label.setText(self.format_status())
            self.refresh_screen()
        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

    def check_credit_card_info(self):
        try:
            success, res = self.denarii_mobile_client.has_credit_card_info(
                self.gui_user.user_id
            )
            if success:
                return res[0]["has_credit_card_info"]
            else:
                return False
        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

    def refresh_screen(self):
        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)

        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)

        if self.status is True:
            self.main_layout.addLayout(self.fourth_horizontal_layout)

        self.main_layout.addLayout(self.fifth_horizontal_layout)

        self.remote_wallet_screen_push_button.setVisible(True)
        self.sell_screen_push_button.setVisible(True)
        self.verification_screen_push_button.setVisible(True)
        self.user_settings_screen_push_button.setVisible(True)
        self.buy_screen_push_button.setVisible(True)

        self.submit_push_button.setVisible(True)

        if self.status is True:
            self.clear_info_push_button.setVisible(True)

        self.first_horizontal_layout.addWidget(
            self.credit_card_info_label, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.status_label, alignment=AlignCenter
        )

        self.form_layout.addRow("Card Number", self.card_number_line_edit)
        self.form_layout.addRow(
            "Expiration Date Month", self.expiration_date_month_line_edit
        )
        self.form_layout.addRow(
            "Expiration Date Year", self.expiration_date_year_line_edit
        )
        self.form_layout.addRow("Security Code", self.security_code_line_edit)

        self.third_horizontal_layout.addWidget(
            self.submit_push_button, alignment=AlignCenter
        )

        if self.status is True:
            self.fourth_horizontal_layout.addWidget(
                self.clear_info_push_button, alignment=AlignCenter
            )

        self.fifth_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )
        self.fifth_horizontal_layout.addWidget(
            self.remote_wallet_screen_push_button, alignment=AlignCenter
        )
        self.fifth_horizontal_layout.addWidget(
            self.buy_screen_push_button, alignment=AlignCenter
        )
        self.fifth_horizontal_layout.addWidget(
            self.verification_screen_push_button, alignment=AlignCenter
        )
        self.fifth_horizontal_layout.addWidget(
            self.user_settings_screen_push_button, alignment=AlignCenter
        )
        self.fifth_horizontal_layout.addWidget(
            self.sell_screen_push_button, alignment=AlignCenter
        )
