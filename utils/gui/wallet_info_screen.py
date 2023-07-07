from PyQt5.QtCore import *
from PyQt5.QtGui import *

from font import *
from label import *
from push_button import *
from screen import *

class WalletInfoScreen(Screen):
    """
    A screen that allows the user to choose whether to open, create, or restore a wallet
    """

    def __init__(self, main_layout, deletion_func, denarii_client, gui_user, **kwargs):
        super().__init__(self.wallet_info_screen_name, main_layout=main_layout,
                         deletion_func=deletion_func, denarii_client=denarii_client, gui_user=gui_user, **kwargs)

        self.wallet_info_label = None
        self.create_wallet_push_button = None
        self.restore_wallet_push_button = None
        self.set_wallet_push_button = None

    def init(self, **kwargs):
        super().init(**kwargs)

        self.next_button.setVisible(False)

        self.wallet_info_label = Label("Choose Wallet")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_info_label.setFont(font)

        self.create_wallet_push_button = PushButton("Create wallet", kwargs['parent'])
        self.create_wallet_push_button.clicked.connect(kwargs['on_create_wallet_clicked'])
        self.create_wallet_push_button.setVisible(False)
        self.create_wallet_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.restore_wallet_push_button = PushButton("Restore wallet", kwargs['parent'])
        self.restore_wallet_push_button.clicked.connect(kwargs['on_restore_wallet_clicked'])
        self.restore_wallet_push_button.setVisible(False)
        self.restore_wallet_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.set_wallet_push_button = PushButton("Set wallet", kwargs['parent'])
        self.set_wallet_push_button.clicked.connect(kwargs['on_set_wallet_clicked'])
        self.set_wallet_push_button.setVisible(False)
        self.set_wallet_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

    def setup(self):
        super().setup()

        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)

        self.create_wallet_push_button.setVisible(True)
        self.restore_wallet_push_button.setVisible(True)
        self.set_wallet_push_button.setVisible(True)

        self.first_horizontal_layout.addWidget(self.wallet_info_label, alignment=Qt.AlignCenter)
        self.second_horizontal_layout.addWidget(self.create_wallet_push_button, alignment=Qt.AlignCenter)
        self.second_horizontal_layout.addWidget(self.restore_wallet_push_button, alignment=Qt.AlignCenter)
        self.second_horizontal_layout.addWidget(self.set_wallet_push_button, alignment=Qt.AlignCenter)
        self.third_horizontal_layout.addWidget(self.back_button, alignment=(Qt.AlignLeft | Qt.AlignBottom))

    def teardown(self):
        super().teardown()
