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



class WalletInfoScreen(Screen):
    """
    A screen that allows the user to choose whether to open, create, or restore a wallet. Yes it is terribly named.
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

        self.wallet_info_label = None
        self.create_wallet_push_button = None
        self.restore_wallet_push_button = None
        self.set_wallet_push_button = None

        super().__init__(
            self.wallet_info_screen_name,
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

        self.wallet_info_label = Label("Choose Wallet")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_info_label.setFont(font)

        self.create_wallet_push_button = PushButton("Create wallet", kwargs["parent"])
        self.create_wallet_push_button.clicked.connect(
            kwargs["on_create_wallet_clicked"]
        )
        self.create_wallet_push_button.setVisible(False)
        self.create_wallet_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.restore_wallet_push_button = PushButton("Restore wallet", kwargs["parent"])
        self.restore_wallet_push_button.clicked.connect(
            kwargs["on_restore_wallet_clicked"]
        )
        self.restore_wallet_push_button.setVisible(False)
        self.restore_wallet_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.set_wallet_push_button = PushButton("Set wallet", kwargs["parent"])
        self.set_wallet_push_button.clicked.connect(kwargs["on_set_wallet_clicked"])
        self.set_wallet_push_button.setVisible(False)
        self.set_wallet_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

    def setup(self):
        super().setup()

        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)

        self.create_wallet_push_button.setVisible(True)
        self.restore_wallet_push_button.setVisible(True)
        self.set_wallet_push_button.setVisible(True)

        self.first_horizontal_layout.addWidget(
            self.wallet_info_label, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.create_wallet_push_button, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.restore_wallet_push_button, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.set_wallet_push_button, alignment=AlignCenter
        )
        self.third_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )

    def teardown(self):
        super().teardown()
