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


class LoginScreen(Screen):
    """
    A screen that allows the user to login
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

        self.user_info_label = None
        self.username_or_email_line_edit = None
        self.password_line_edit = None
        self.submit_button = None
        self.forgot_password_button = None

        super().__init__(
            self.login_screen_name,
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
        self.back_button.setVisible(True)

        self.user_info_label = Label("Login")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.user_info_label.setFont(font)

        self.username_or_email_line_edit = LineEdit()
        self.password_line_edit = LineEdit()
        self.password_line_edit.setEchoMode(LineEdit.Password)

        self.submit_button = PushButton("Submit", kwargs["parent"])
        self.submit_button.clicked.connect(lambda: self.on_submit_clicked())
        self.submit_button.setVisible(False)
        self.submit_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.forgot_password_button = PushButton("Forgot Password", kwargs["parent"])
        self.forgot_password_button.clicked.connect(lambda: kwargs["on_forgot_password_clicked"])
        self.forgot_password_button.setVisible(False)
        self.forgot_password_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

    def setup(self):
        super().setup()

        # Remove anything on the screen
        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)
        self.main_layout.addLayout(self.fourth_horizontal_layout)

        self.submit_button.setVisible(True)
        self.forgot_password_button.setVisible(True)

        self.first_horizontal_layout.addWidget(
            self.user_info_label, alignment=AlignCenter
        )
        self.form_layout.addRow("Name or Email", self.username_or_email_line_edit)
        self.form_layout.addRow("Password", self.password_line_edit)
        self.second_horizontal_layout.addWidget(
            self.submit_button, alignment=AlignCenter
        )
        self.third_horizontal_layout.addWidget(self.forgot_password_button, alignment=AlignCenter)
        self.fourth_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )
        self.fourth_horizontal_layout.addWidget(
            self.next_button, alignment=(AlignRight | AlignBottom)
        )

    def teardown(self):
        super().teardown()

    def store_user_info(self):
        """
        Store the user's input information in the user proto
        """
        success = False
        
        invalid_fields = []
        
        if not is_valid_pattern(self.username_or_email_line_edit.text(), Patterns.alphanumeric) and not is_valid_pattern(self.username_or_email.text(), Patterns.email):
            invalid_fields.append(Params.username_or_email)
            
        if not is_valid_pattern(self.password_line_edit.text(), Patterns.password): 
            invalid_fields.append(Params.password)
            
        if len(invalid_fields) > 0:
            self.status_message_box(f"Failed: Invalid Fields {invalid_fields}")
            return
        
        try:
            success, res = self.denarii_mobile_client.login(self.username_or_email_line_edit.text(),
                                                                  self.password_line_edit.text())
            if success:
                self.gui_user.user_id = res[0]['user_id']
            else:
                self.status_message_box("Failed: could not login user")
                self.next_button.setVisible(False)
        except Exception as create_remote_wallet_e:
            print(create_remote_wallet_e)
            self.status_message_box("Failed: unknown error")
            self.next_button.setVisible(False)
        if success:
            self.status_message_box("Success")
            if is_valid_pattern(self.username_or_email_line_edit.text(), Patterns.alphanumeric):
                self.gui_user.name = self.username_or_email_line_edit.text()
            if is_valid_pattern(self.username_or_email_line_edit.text(), Patterns.email):
                self.gui_user.email = self.username_or_email_line_edit.text()
            self.gui_user.password = self.password_line_edit.text()
            self.next_button.setVisible(True)

    def on_submit_clicked(self):
        self.store_user_info()
