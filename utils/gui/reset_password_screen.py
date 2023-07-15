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


class ResetPasswordScreen(Screen):
    def __init__(
        self,
        main_layout,
        deletion_func,
        denarii_client,
        gui_user,
        denarii_mobile_client,
        **kwargs
    ):
        self.reset_password_label = None
        self.name_line_edit = None
        self.password_line_edit = None
        self.email_line_edit = None
        self.confirm_password_line_edit = None
        self.submit_button = None

        super().__init__(
            self.reset_password_screen_name,
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
        self.back_button.setVisible(True)

        self.reset_password_label = Label("Reset Password")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.reset_password_label.setFont(font)

        self.name_line_edit = LineEdit()
        self.email_line_edit = LineEdit()
        self.password_line_edit = LineEdit()
        self.password_line_edit.setEchoMode(LineEdit.Password)
        self.confirm_password_line_edit = LineEdit()
        self.confirm_password_line_edit.setEchoMode(LineEdit.Password)

        self.submit_button = PushButton("Submit", kwargs["parent"])
        self.submit_button.clicked.connect(lambda: self.on_submit_clicked())
        self.submit_button.setVisible(False)
        self.submit_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

    def setup(self):
        super().setup()

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)

        self.submit_button.setVisible(True)

        self.first_horizontal_layout.addWidget(
            self.reset_password_label, alignment=AlignCenter
        )
        self.form_layout.addRow("Name:", self.name_line_edit)
        self.form_layout.addRow("Email:", self.email_line_edit)
        self.form_layout.addRow("Password:", self.password_line_edit)
        self.form_layout.addRow("Confirm Password:", self.confirm_password_line_edit)
        self.second_horizontal_layout.addWidget(
            self.submit_button, alignment=AlignCenter
        )
        self.third_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )
        self.third_horizontal_layout.addWidget(
            self.next_button, alignment=(AlignRight | AlignBottom)
        )

    def teardown(self):
        super().teardown()

    def on_submit_clicked(self):
        if (
            self.password_line_edit.text() != ""
            and self.confirm_password_line_edit.text() != ""
            and self.password_line_edit.text() == self.confirm_password_line_edit.text()
        ):
            try:
                success = self.denarii_mobile_client.reset_password(
                    self.name_line_edit.text(),
                    self.email_line_edit.text(),
                    self.password_line_edit.text(),
                )

                if success:
                    self.status_message_box("Success")
                    self.next_button.setVisible(True)
                else:
                    self.status_message_box("Failure: could not reset password")
            except Exception as e:
                print(e)
                self.status_message_box("Failure: unknown error")

        else:
            self.status_message_box("Failure: passwords do not match")
