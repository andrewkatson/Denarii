from screen import *
from font import *
from label import *
from push_button import *
from line_edit import *
from radio_button import *


class SetWalletScreen(Screen):
    """
    A screen that allows the user to open a wallet that was previously created or restored.
    """

    def __init__(self, main_layout, deletion_func, denarii_client, gui_user, **kwargs):
        super().__init__(self.set_wallet_screen_name, main_layout=main_layout,
                         deletion_func=deletion_func, denarii_client=denarii_client, gui_user=gui_user, **kwargs)

        self.set_wallet_label = None
        self.set_wallet_text_box = None
        self.set_wallet_submit_push_button = None
        self.name_line_edit = None
        self.password_line_edit = None
        self.remote_wallet = kwargs['remote_wallet']
        self.local_wallet = kwargs['local_wallet']
        self.which_wallet = None
        self.pick_wallet_type = None
        self.remote_wallet_radio_button = None
        self.local_wallet_radio_button = None
        self.set_wallet_type_callback = kwargs['set_wallet_type_callback']


    def init(self, **kwargs):
        super().init(**kwargs)

        self.next_button.setVisible(False)

        self.set_wallet_label = Label("Set Wallet")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.set_wallet_label.setFont(font)

        self.set_wallet_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.set_wallet_text_box.setFont(font)
        self.set_wallet_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.set_wallet_submit_push_button = PushButton("Submit", kwargs['parent'])
        self.set_wallet_submit_push_button.clicked.connect(lambda: self.on_set_wallet_submit_clicked())
        self.set_wallet_submit_push_button.setVisible(False)
        self.set_wallet_submit_push_button.setStyleSheet(
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
                                                      wallet_type_callback=self.set_which_wallet, next_button=self.next_button)
        self.remote_wallet_radio_button.toggled.connect(self.remote_wallet_radio_button.on_wallet_type_clicked)
        self.remote_wallet_radio_button.wallet_type_option = "Remote"
        self.remote_wallet_radio_button.setVisible(False)
        self.remote_wallet_radio_button.setStyleSheet(
            'QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};')

        self.local_wallet_radio_button = RadioButton("Local", kwargs['parent'],
                                                     wallet_type_callback=self.set_which_wallet, next_button=self.next_button)
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

        self.set_wallet_submit_push_button.setVisible(True)
        self.local_wallet_radio_button.setVisible(True)
        self.remote_wallet_radio_button.setVisible(True)

        self.first_horizontal_layout.addWidget(self.set_wallet_label, alignment=Qt.AlignCenter)
        self.form_layout.addRow("Name", self.name_line_edit)
        self.form_layout.addRow("Password", self.password_line_edit)
        self.second_horizontal_layout.addWidget(self.set_wallet_text_box, alignment=Qt.AlignCenter)
        self.third_horizontal_layout.addWidget(self.set_wallet_submit_push_button, alignment=Qt.AlignCenter)
        self.fourth_horizontal_layout.addWidget(self.pick_wallet_type, alignment=Qt.AlignCenter)
        self.fifth_horizontal_layout.addWidget(self.remote_wallet_radio_button, alignment=Qt.AlignCenter)
        self.fifth_horizontal_layout.addWidget(self.local_wallet_radio_button, alignment=Qt.AlignCenter)
        self.sixth_horizontal_layout.addWidget(self.back_button, alignment=(Qt.AlignLeft | Qt.AlignBottom))
        self.sixth_horizontal_layout.addWidget(self.next_button, alignment=(Qt.AlignRight | Qt.AlignBottom))


    def teardown(self):
        super().teardown()

    def set_wallet(self):
        """
        Open the wallet based on the user's information
        """

        self.wallet.name = self.name_line_edit.text()
        self.wallet.password = self.password_line_edit.text()

        success = False

        try:
            success = self.denarii_client.set_current_wallet(self.wallet)
            print_status("Set current wallet ", success)
            success = self.denarii_client.query_seed(self.wallet) and success
            print_status("Query seed ", success)
            if success:
                self.next_button.setVisible(True)
        except Exception as set_wallet_e:
            print(set_wallet_e)
            self.next_button.setVisible(False)

        if success:
            split = self.wallet.phrase.split()
            thirds = int(len(split) / 3)
            first = ' '.join(split[:thirds])
            second = ' '.join(split[thirds:thirds * 2])
            third = ''.join(split[thirds * 2:])

            self.set_wallet_text_box.setText(f"Success. Your seed is \n {first}\n{second}\n{third}" )
        else:
            self.set_wallet_text_box.setText("Failure")

    @pyqtSlot()
    def on_set_wallet_submit_clicked(self):
        """
        Set a wallet based on the user's input information
        """
        if self.which_wallet is None:
            self.set_wallet_text_box.setText("Failure: need to set the wallet type")
            return

        self.set_wallet()

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

        self.set_wallet_type_callback(self.which_wallet)
