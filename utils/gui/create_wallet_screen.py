from screen import *
from label import *
from font import *
from push_button import *
from line_edit import *
from radio_button import *


class CreateWalletScreen(Screen):
    """
    Screen that displays gui that lets user create a wallet
    """

    def __init__(self, main_layout, deletion_func, denarii_client, gui_user, **kwargs):
        super().__init__(screen_name=self.create_wallet_screen_name, main_layout=main_layout,
                         deletion_func=deletion_func, denarii_client=denarii_client, gui_user=gui_user, **kwargs)

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
        self.which_wallet = None
        self.pick_wallet_type = None
        self.remote_wallet_radio_button = None
        self.local_wallet_radio_button = None

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

        self.pick_wallet_type = Label("Pick a Wallet Type")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.pick_wallet_type.setFont(font)

        self.remote_wallet_radio_button = RadioButton("Remote", kwargs['parent'],
                                                      wallet_type_callback=self.set_which_wallet)
        self.remote_wallet_radio_button.toggled.connect(self.remote_wallet_radio_button.on_wallet_type_clicked)
        self.remote_wallet_radio_button.wallet_type_option = "Remote"
        self.remote_wallet_radio_button.setVisible(False)
        self.remote_wallet_radio_button.setStyleSheet(
            'QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};')

        self.local_wallet_radio_button = RadioButton("Local", kwargs['parent'],
                                                     wallet_type_callback=self.set_which_wallet)
        self.local_wallet_radio_button.toggled.connect(self.local_wallet_radio_button.on_wallet_type_clicked)
        self.local_wallet_radio_button.wallet_type_option = "Local"
        self.local_wallet_radio_button.setVisible(False)
        self.local_wallet_radio_button.setStyleSheet(
            'QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};')

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
        self.main_layout.addLayout(self.seventh_horizontal_layout)
        self.main_layout.addLayout(self.eight_horizontal_layout)

        self.create_wallet_submit_push_button.setVisible(True)
        self.local_wallet_radio_button.setVisible(True)
        self.remote_wallet_radio_button.setVisible(True)

        self.first_horizontal_layout.addWidget(self.create_wallet_label, alignment=Qt.AlignCenter)
        self.form_layout.addRow("Name", self.name_line_edit)
        self.form_layout.addRow("Password", self.password_line_edit)
        self.second_horizontal_layout.addWidget(self.wallet_info_text_box, alignment=Qt.AlignCenter)
        self.third_horizontal_layout.addWidget(self.wallet_save_file_text_box, alignment=Qt.AlignCenter)
        self.fourth_horizontal_layout.addWidget(self.create_wallet_text_box, alignment=Qt.AlignCenter)
        self.fifth_horizontal_layout.addWidget(self.create_wallet_submit_push_button, alignment=Qt.AlignCenter)
        self.sixth_horizontal_layout.addWidget(self.pick_wallet_type, alignment=Qt.AlignCenter)
        self.seventh_horizontal_layout.addWidget(self.remote_wallet_radio_button, alignment=Qt.AlignCenter)
        self.seventh_horizontal_layout.addWidget(self.local_wallet_radio_button, alignment=Qt.AlignCenter)
        self.eight_horizontal_layout.addWidget(self.back_button, alignment=(Qt.AlignLeft | Qt.AlignBottom))
        self.eight_horizontal_layout.addWidget(self.next_button, alignment=(Qt.AlignRight | Qt.AlignBottom))

    def teardown(self):
        super().teardown()

    @pyqtSlot()
    def on_create_wallet_submit_clicked(self):
        """
        Create the wallet based on the user's input information
        """
        if self.which_wallet is None:
            self.create_wallet_text_box.setText("Failure: need to set the wallet type")
            return

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
        if self.which_wallet is None:
            return self.local_wallet

        if self.which_wallet == REMOTE_WALLET:
            return self.remote_wallet
        elif self.which_wallet == LOCAL_WALLET:
            return self.local_wallet
        return self.local_wallet

    def set_which_wallet(self, which_wallet):
        self.which_wallet = which_wallet
