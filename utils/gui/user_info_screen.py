from screen import *

if TESTING:
    from denarii_testing_font import Font
    from denarii_testing_label import Label
    from denarii_testing_line_edit import LineEdit
    from denarii_testing_qt import (
        AlignRight,
        AlignBottom,
        AlignCenter,
        AlignLeft,
    )
    from denarii_testing_push_button import PushButton
    from denarii_testing_radio_button import RadioButton
else:
    from font import *
    from label import *
    from line_edit import *
    from qt import (
        AlignRight,
        AlignBottom,
        AlignCenter,
        AlignLeft,
    )
    from push_button import *
    from radio_button import *

class UserInfoScreen(Screen):
    """
    A screen that allows the user to enter in their information for later usage.
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
        self.name_line_edit = None
        self.email_line_edit = None
        self.password_line_edit = None
        self.confirm_password_line_edit = None
        self.user_info_status_text_box = None
        self.submit_button = None

        super().__init__(
            self.user_info_screen_name,
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

        self.user_info_label = Label("Input Your Information")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.user_info_label.setFont(font)

        self.name_line_edit = LineEdit()
        self.email_line_edit = LineEdit()
        self.password_line_edit = LineEdit()
        self.password_line_edit.setEchoMode(LineEdit.Password)
        self.confirm_password_line_edit = LineEdit()
        self.confirm_password_line_edit.setEchoMode(LineEdit.Password)

        self.user_info_status_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.user_info_status_text_box.setFont(font)

        self.submit_button = PushButton("Submit", kwargs["parent"])
        self.submit_button.clicked.connect(lambda: self.on_submit_clicked())
        self.submit_button.setVisible(False)
        self.submit_button.setStyleSheet(
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

        self.first_horizontal_layout.addWidget(
            self.user_info_label, alignment=AlignCenter
        )
        self.form_layout.addRow("Name", self.name_line_edit)
        self.form_layout.addRow("Email", self.email_line_edit)
        self.form_layout.addRow("Password", self.password_line_edit)
        self.form_layout.addRow("Confirm Password", self.confirm_password_line_edit)
        self.second_horizontal_layout.addWidget(
            self.submit_button, alignment=AlignCenter
        )
        self.third_horizontal_layout.addWidget(
            self.user_info_status_text_box, alignment=AlignCenter
        )
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
        if (
            self.password_line_edit.text() != ""
            and self.confirm_password_line_edit.text() != ""
            and self.password_line_edit.text() != self.confirm_password_line_edit.text()
        ):
            _ = ShowText(self.user_info_status_text_box, "Failure: passwords did not match")
        else:
            _ = ShowText(self.user_info_status_text_box, "Success")
            self.gui_user.name = self.name_line_edit.text()
            self.gui_user.email = self.email_line_edit.text()
            self.gui_user.password = self.password_line_edit.text()
            self.next_button.setVisible(True)

    def on_submit_clicked(self):
        self.store_user_info()
