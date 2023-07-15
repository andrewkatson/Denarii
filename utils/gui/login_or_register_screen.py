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


class LoginOrRegisterScreen(Screen):
    def __init__(
        self,
        main_layout,
        deletion_func,
        denarii_client,
        gui_user,
        denarii_mobile_client,
        **kwargs
    ):
    
        self.login_button = None
        self.register_button = None 

        super().__init__(
            self.login_or_register_screen_name,
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

        self.login_button = PushButton("Login", kwargs["parent"])
        self.login_button.clicked.connect(lambda: kwargs["on_login_clicked"]())
        self.login_button.setVisible(False)
        self.login_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.register_button = PushButton("Register", kwargs["parent"])
        self.register_button.clicked.connect(lambda: kwargs["on_register_clicked"]())
        self.register_button.setVisible(False)
        self.register_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

    def setup(self):
        super().setup()

        # Remove anything on the screen
        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)

        self.login_button.setVisible(True)
        self.register_button.setVisible(True)

        self.first_horizontal_layout.addWidget(self.login_button, alignment=AlignCenter)
        self.first_horizontal_layout.addWidget(self.register_button, alignment=AlignCenter)
        self.second_horizontal_layout.addWidget(self.back_button, alignment=(AlignBottom | AlignLeft))

    def teardown(self):
        super().teardown()
