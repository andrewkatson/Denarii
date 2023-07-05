from screen import *
from font import *
from label import *
from PyQt5.QtCore import *
from push_button import *
from line_edit import *


class RestoreWalletScreen(Screen):
    """
    A screen that allows a user to choose to restore a wallet that exists on another computer.
    """

    def __init__(self, main_layout, deletion_func, **kwargs):
        super().__init__(self.restore_wallet_screen_name, main_layout, deletion_func, **kwargs)

        self.restore_wallet_label = None
        self.wallet_save_file_text_box = None
        self.restore_wallet_text_box = None
        self.restore_wallet_submit_push_button = None
        self.name_line_edit = None
        self.password_line_edit = None
        self.seed_line_edit = None

    def init(self, **kwargs):
        super().init(**kwargs)

        self.restore_wallet_label = Label("Restore Wallet")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.restore_wallet_label.setFont(font)

        self.wallet_save_file_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_save_file_text_box.setFont(font)
        self.wallet_save_file_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.restore_wallet_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.restore_wallet_text_box.setFont(font)

        self.restore_wallet_submit_push_button = PushButton("Submit", kwargs['parent'])
        self.restore_wallet_submit_push_button.clicked.connect(kwargs['on_restore_wallet_submit_clicked'])
        self.restore_wallet_submit_push_button.setVisible(False)
        self.restore_wallet_submit_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.name_line_edit = LineEdit()
        self.password_line_edit = LineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        self.seed_line_edit = LineEdit()

    def setup(self):
        super().setup()

        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)
        self.main_layout.addLayout(self.fourth_horizontal_layout)
        self.main_layout.addLayout(self.fifth_horizontal_layout)

        self.restore_wallet_submit_push_button.setVisible(True)

        self.first_horizontal_layout.addWidget(self.restore_wallet_label, alignment=Qt.AlignCenter)
        self.form_layout.addRow("Name", self.name_line_edit)
        self.form_layout.addRow("Password", self.password_line_edit)
        self.form_layout.addRow("Seed", self.seed_line_edit)
        self.second_horizontal_layout.addWidget(self.wallet_save_file_text_box, alignment=Qt.AlignCenter)
        self.third_horizontal_layout.addWidget(self.restore_wallet_text_box, alignment=Qt.AlignCenter)
        self.fourth_horizontal_layout.addWidget(self.restore_wallet_submit_push_button, alignment=Qt.AlignCenter)
        self.fifth_horizontal_layout.addWidget(self.next_button, alignment=(Qt.AlignRight | Qt.AlignBottom))

    def teardown(self):
        super().teardown()
