import json
import threading
import time

from screen import *
from stoppable_thread import StoppableThread

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


class VerificationScreen(Screen):
    """
    A screen that allows the user to verify their identity
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
        self.credit_card_info_screen_name = None

        self.submit_push_button = None

        self.verification_label = None
        self.status_label = None

        self.first_name_line_edit = None
        self.middle_initial_line_edit = None
        self.last_name_line_edit = None
        self.email_line_edit = None
        self.date_of_birth_line_edit = None
        self.social_security_number_line_edit = None
        self.zipcode_line_edit = None
        self.phone_number_line_edit = None
        self.work_location_city_line_edit = None
        self.work_location_state_line_edit = None
        self.work_location_country_line_edit = None

        self.status = "Unknown"

        # We need to explicitly set the gui_user since we use it in lookup_verification_status*
        self.gui_user = gui_user

        # We need to explicitly set the denarii mobile client since we call it in lookup_verification_status*
        self.denarii_mobile_client = denarii_mobile_client


        self.lock = threading.Lock()
        self.lookup_status_thread = StoppableThread(
            target=self.lookup_verification_status, name="lookup_status_thread"
        )

        super().__init__(
            self.verification_screen_name,
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

        self.verification_label = Label("Verification")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.verification_label.setFont(font)

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

        self.status_label = Label(self.format_status())
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.status_label.setFont(font)

        self.first_name_line_edit = LineEdit()
        self.middle_initial_line_edit = LineEdit()
        self.last_name_line_edit = LineEdit()
        self.email_line_edit = LineEdit()
        self.date_of_birth_line_edit = LineEdit()
        self.social_security_number_line_edit = LineEdit()
        self.zipcode_line_edit = LineEdit()
        self.phone_number_line_edit = LineEdit()
        self.work_location_city_line_edit = LineEdit()
        self.work_location_state_line_edit = LineEdit()
        self.work_location_country_line_edit = LineEdit()

    def setup(self):
        super().setup()

        self.refresh_screen()

        self.lookup_status_thread.start()

    def teardown(self):
        super().teardown()

        self.lookup_status_thread.stop()

        if self.lookup_status_thread.is_alive():
            self.lookup_status_thread.join()

    def format_status(self):
        if self.status == "is_verified":
            return "Status: Verified"
        elif self.status == "failed_verification":
            return "Status: Failed Verification"
        elif self.status == "verification_pending":
            return "Status: Verification Pending"
        elif self.status == "is_not_verified":
            return "Status: Not Verified Yet"
        else:
            return "Status: Unknown"
        
    def lookup_verification_status_once(self):
        try:
            success, res = self.denarii_mobile_client.is_a_verified_person(
                self.gui_user.user_id
            )

            if success:
                self.stautus = res[0]["verification_status"]

                if self.status == "is_verified":
                    self.refresh_screen()

            else:
                self.status = "is_not_verified"

            self.status_label.setText(self.format_status())
        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

    def lookup_verification_status(self):
        while not self.lookup_status_thread.stopped():
            try:
                self.lock.acquire()

                self.lookup_verification_status_once()

            except Exception as e:
                print(e)
                self.status_message_box("Failed: unknown error")
            finally:
                self.lock.release()

            time.sleep(5)

    def on_submit_clicked(self):
        invalid_fields = []
        
        if not is_valid_pattern(self.first_name_line_edit.text(), Patterns.name):
            invalid_fields.append(Params.first_name)
            
        if not is_valid_pattern(self.middle_initial_line_edit.text(), Patterns.single_letter):
            invalid_fields.append(Params.middle_name)
            
        if not is_valid_pattern(self.last_name_line_edit.text(), Patterns.name):
            invalid_fields.append(Params.last_name)
            
        if not is_valid_pattern(self.email_line_edit.text(), Patterns.email):
            invalid_fields.append(Params.email)
            
        if not is_valid_pattern(self.date_of_birth_line_edit_text.text(), Patterns.slash_date):
            invalid_fields.append(Params.dob)
            
        if not is_valid_pattern(self.social_security_number_line_edit.text(), Patterns.digits_and_dashes):
            invalid_fields.append(Params.ssn)
            
        if not is_valid_pattern(self.zipcode_line_edit.text(), Patterns.digits_and_dashes):
            invalid_fields.append(Params.zipcode)
            
        if not is_valid_pattern(self.phone_number_line_edit.text(), Patterns.phone_number):
            invalid_fields.append(Params.phone_number)
            
        if not is_valid_pattern(self.format_work_locations(), Patterns.json_dict_of_upper_and_lower_case_chars):
            invalid_fields.append(Params.work_locations)
            
        if len(invalid_fields) > 0:
            self.status_message_box(f"Failed: Invalid Fields {invalid_fields}")
            return
        
        try:
            self.lock.acquire()

            success, res = self.denarii_mobile_client.verify_identity(
                self.gui_user.user_id,
                self.first_name_line_edit.text(),
                self.middle_initial_line_edit.text(),
                self.last_name_line_edit.text(),
                self.email_line_edit.text(),
                self.date_of_birth_line_edit.text(),
                self.social_security_number_line_edit.text(),
                self.zipcode_line_edit.text(),
                self.phone_number_line_edit.text(),
                self.format_work_location(),
            )

            if success:
                self.stautus = res[0]["verification_status"]

                self.status_message_box("Successfully sent verification info")

                if self.status == "is_verified":
                    self.refresh_screen()

            else:
                self.status = "is_not_verified"
                self.status_message_box("Failed to send verification info")

            self.status_label.setText(self.format_status())

        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")
        finally:
            self.lock.release()

    def refresh_screen(self):
        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)

        if self.status != "is_verified":
            self.main_layout.addLayout(self.form_layout)
            self.main_layout.addLayout(self.third_horizontal_layout)

        self.main_layout.addLayout(self.fourth_horizontal_layout)

        self.remote_wallet_screen_push_button.setVisible(True)
        self.sell_screen_push_button.setVisible(True)
        self.credit_card_info_screen_push_button.setVisible(True)
        self.user_settings_screen_push_button.setVisible(True)
        self.buy_screen_push_button.setVisible(True)

        if self.status != "is_verified":
            self.submit_push_button.setVisible(True)

        self.first_horizontal_layout.addWidget(
            self.verification_label, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.status_label, alignment=AlignCenter
        )

        if self.status != "is_verified":
            self.form_layout.addRow("First Name", self.first_name_line_edit)
            self.form_layout.addRow("Middle Initial", self.middle_initial_line_edit)
            self.form_layout.addRow("Last Name", self.last_name_line_edit)
            self.form_layout.addRow("Email", self.email_line_edit)
            self.form_layout.addRow("SSN", self.social_security_number_line_edit)
            self.form_layout.addRow("Zipcode", self.zipcode_line_edit)
            self.form_layout.addRow("Phone Number", self.phone_number_line_edit)
            self.form_layout.addRow("Work City", self.work_location_city_line_edit)
            self.form_layout.addRow("Work State", self.work_location_state_line_edit)
            self.form_layout.addRow(
                "Work Country", self.work_location_country_line_edit
            )

            self.third_horizontal_layout.addWidget(
                self.submit_push_button, alignment=AlignCenter
            )

        self.fourth_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )
        self.fourth_horizontal_layout.addWidget(
            self.remote_wallet_screen_push_button, alignment=AlignCenter
        )
        self.fourth_horizontal_layout.addWidget(
            self.buy_screen_push_button, alignment=AlignCenter
        )
        self.fourth_horizontal_layout.addWidget(
            self.credit_card_info_screen_push_button, alignment=AlignCenter
        )
        self.fourth_horizontal_layout.addWidget(
            self.user_settings_screen_push_button, alignment=AlignCenter
        )
        self.fourth_horizontal_layout.addWidget(
            self.sell_screen_push_button, alignment=AlignCenter
        )

    def format_work_location(self):
        return json.dumps(
            [
                {
                    "country": self.work_location_country_line_edit.text(),
                    "state": self.work_location_state_line_edit.text(),
                    "city": self.work_location_city_line_edit.text(),
                }
            ]
        )
