from screen import *
from label import *
from font import *
from PyQt5.QtCore import *
from push_button import *
from line_edit import *
from constants import *


class CreateWalletScreen(Screen):
    """
    Screen that displays gui that lets user create a wallet
    """

    def __init__(self, main_layout, deletion_func, **kwargs):
        super().__init__(self.create_wallet_screen_name, main_layout, deletion_func, **kwargs)

        self.create_wallet_label = None
        self.wallet_seed_text_box = None
        self.wallet_save_file_text_box = None
        self.create_wallet_text_box = None
        self.create_wallet_submit_push_button = None
        self.name_line_edit = None
        self.password_line_edit = None
        self.wallet_info_text_box = None
        self.remote_wallet = kwargs['remote_wallet']
        self.local_wallet = kwargs['local_wallet']
        self.which_wallet = kwargs['which_wallet']

    def init(self, **kwargs):
        super().init(**kwargs)

        self.create_wallet_label = Label("Create Wallet")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.create_wallet_label.setFont(font)

        self.wallet_seed_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_seed_text_box.setFont(font)
        self.wallet_seed_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.wallet_save_file_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_save_file_text_box.setFont(font)
        self.wallet_save_file_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.create_wallet_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.create_wallet_text_box.setFont(font)

        self.wallet_info_text_box = Label("")
        font = QFont()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_info_text_box.setFont(font)
        self.wallet_info_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.create_wallet_submit_push_button = PushButton("Submit", kwargs['parent'])
        self.create_wallet_submit_push_button.clicked.connect(self.on_create_wallet_submit_clicked)
        self.create_wallet_submit_push_button.setVisible(False)
        self.create_wallet_submit_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.name_line_edit = LineEdit()
        self.password_line_edit = LineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.Password)

    def setup(self):
        super().setup()

        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)
        self.main_layout.addLayout(self.fourth_horizontal_layout)
        self.main_layout.addLayout(self.fifth_horizontal_layout)
        self.main_layout.addLayout(self.sixth_horizontal_layout)

        self.create_wallet_submit_push_button.setVisible(True)

        self.first_horizontal_layout.addWidget(self.create_wallet_label, alignment=Qt.AlignCenter)
        self.form_layout.addRow("Name", self.name_line_edit)
        self.form_layout.addRow("Password", self.password_line_edit)
        self.second_horizontal_layout.addWidget(self.wallet_info_text_box, alignment=Qt.AlignCenter)
        self.third_horizontal_layout.addWidget(self.wallet_save_file_text_box, alignment=Qt.AlignCenter)
        self.fourth_horizontal_layout.addWidget(self.create_wallet_text_box, alignment=Qt.AlignCenter)
        self.fifth_horizontal_layout.addWidget(self.create_wallet_submit_push_button, alignment=Qt.AlignCenter)
        self.sixth_horizontal_layout.addWidget(self.next_button, alignment=(Qt.AlignRight | Qt.AlignBottom))

    def teardown(self):
        super().teardown()

    @pyqtSlot()
    def on_create_wallet_submit_clicked(self):
        """
        Create the wallet based on the user's input information
        """
        self.create_wallet()

    def create_wallet(self):
        """
        Try to create a denarii wallet
        """
        self.wallet.name = self.name_line_edit.text()
        self.wallet.password = self.password_line_edit.text()

        success = False
        try:
            success = self.denarii_client.create_wallet(self.wallet)
            print_status("Create wallet ", success)
            success = self.denarii_client.query_seed(self.wallet) and success
            print_status("Query seed ", success)
        except Exception as create_wallet_e:
            print(create_wallet_e)

        if success:
            self.wallet_info_text_box.setText(self.wallet.phrase)
            self.wallet_save_file_text_box.setText("Wallet saved to: " + DENARIID_WALLET_PATH)
            self.create_wallet_text_box.setText(
                "Success. Make sure to write down your information. It will not be saved on this device.")
        else:
            self.create_wallet_text_box.setText("Failure")

    @property
    def wallet(self):
        if self.which_wallet == REMOTE_WALLET:
            return self.remote_wallet
        elif self.which_wallet == LOCAL_WALLET:
            return self.local_wallet
        return self.local_wallet
