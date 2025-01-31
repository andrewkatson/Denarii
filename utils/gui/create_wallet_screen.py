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


class CreateWalletScreen(Screen):
    """
    Screen that displays gui that lets user create a wallet
    """

    def __init__(
        self,
        main_layout,
        deletion_func,
        denarii_client,
        gui_user,
        denarii_mobile_client,
        **kwargs,
    ):
        self.create_wallet_label = None
        self.wallet_seed_text_box = None
        self.wallet_save_file_text_box = None
        self.create_wallet_text_box = None
        self.create_wallet_submit_push_button = None
        self.name_line_edit = None
        self.password_line_edit = None
        self.confirm_password_line_edit = None
        self.wallet_info_text_box = None
        self.remote_wallet = kwargs["remote_wallet"]
        self.local_wallet = kwargs["local_wallet"]
        self.which_wallet = None
        self.pick_wallet_type = None
        self.remote_wallet_radio_button = None
        self.local_wallet_radio_button = None
        self.set_wallet_type_callback = kwargs["set_wallet_type_callback"]

        super().__init__(
            screen_name=self.create_wallet_screen_name,
            main_layout=main_layout,
            deletion_func=deletion_func,
            denarii_client=denarii_client,
            gui_user=gui_user,
            denarii_mobile_client=denarii_mobile_client,
            **kwargs,
        )


    def init(self, **kwargs):
        super().init(**kwargs)

        self.next_button.setVisible(False)

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
        self.wallet_seed_text_box.setTextInteractionFlags(TextSelectableByMouse)

        self.wallet_save_file_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_save_file_text_box.setFont(font)
        self.wallet_save_file_text_box.setTextInteractionFlags(TextSelectableByMouse)

        self.wallet_info_text_box = Label("")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_info_text_box.setFont(font)
        self.wallet_info_text_box.setTextInteractionFlags(TextSelectableByMouse)

        self.create_wallet_submit_push_button = PushButton("Submit", kwargs["parent"])
        self.create_wallet_submit_push_button.clicked.connect(
            lambda: self.on_create_wallet_submit_clicked()
        )
        self.create_wallet_submit_push_button.setVisible(False)
        self.create_wallet_submit_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.name_line_edit = LineEdit()
        self.password_line_edit = LineEdit()
        self.password_line_edit.setEchoMode(LineEdit.Password)
        self.confirm_password_line_edit = LineEdit()
        self.confirm_password_line_edit.setEchoMode(LineEdit.Password)

        self.pick_wallet_type = Label("Pick a Wallet Type")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.pick_wallet_type.setFont(font)

        self.remote_wallet_radio_button = RadioButton(
            "Remote", kwargs["parent"], wallet_type_callback=self.set_which_wallet
        )
        self.remote_wallet_radio_button.toggled.connect(
            self.remote_wallet_radio_button.on_wallet_type_clicked
        )
        self.remote_wallet_radio_button.wallet_type_option = REMOTE_WALLET
        self.remote_wallet_radio_button.setVisible(False)
        self.remote_wallet_radio_button.setStyleSheet(
            "QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};"
        )

        self.local_wallet_radio_button = RadioButton(
            "Local", kwargs["parent"], wallet_type_callback=self.set_which_wallet
        )
        self.local_wallet_radio_button.toggled.connect(
            self.local_wallet_radio_button.on_wallet_type_clicked
        )
        self.local_wallet_radio_button.wallet_type_option = LOCAL_WALLET
        self.local_wallet_radio_button.setVisible(False)
        self.local_wallet_radio_button.setStyleSheet(
            "QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};"
        )

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

        self.create_wallet_submit_push_button.setVisible(True)
        self.local_wallet_radio_button.setVisible(True)
        self.remote_wallet_radio_button.setVisible(True)

        self.first_horizontal_layout.addWidget(
            self.create_wallet_label, alignment=AlignCenter
        )
        self.form_layout.addRow("Name", self.name_line_edit)
        self.form_layout.addRow("Password", self.password_line_edit)
        self.form_layout.addRow("Confirm Password", self.confirm_password_line_edit)
        self.second_horizontal_layout.addWidget(
            self.wallet_info_text_box, alignment=AlignCenter
        )
        self.third_horizontal_layout.addWidget(
            self.wallet_save_file_text_box, alignment=AlignCenter
        )
        self.fourth_horizontal_layout.addWidget(
            self.create_wallet_submit_push_button, alignment=AlignCenter
        )
        self.fifth_horizontal_layout.addWidget(
            self.pick_wallet_type, alignment=AlignCenter
        )
        self.sixth_horizontal_layout.addWidget(
            self.remote_wallet_radio_button, alignment=AlignCenter
        )
        self.sixth_horizontal_layout.addWidget(
            self.local_wallet_radio_button, alignment=AlignCenter
        )
        self.seventh_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )
        self.seventh_horizontal_layout.addWidget(
            self.next_button, alignment=(AlignRight | AlignBottom)
        )

    def teardown(self):
        super().teardown()

    def on_create_wallet_submit_clicked(self):
        """
        Create the wallet based on the user's input information
        """
        if self.which_wallet is None:
            self.status_message_box("Failure: need to set the wallet type")
            return

        self.create_wallet()

    def create_wallet(self):
        """
        Try to create a denarii wallet
        """

        password = self.password_line_edit.text()
        confirm_password = self.confirm_password_line_edit.text()

        if password != confirm_password: 
            self.status_message_box("Failed: passwords need to match")
            return
        
        invalid_fields = []
        
        if not is_valid_pattern(self.name_line_edit.text(), Patterns.alphanumeric):
            invalid_fields.append(Params.username)
        
        if not is_valid_pattern(self.password_line_edit.text(), Patterns.password): 
            invalid_fields.append(Params.password)
            
        if not is_valid_pattern(self.confirm_password_line_edit.text(), Patterns.password): 
            invalid_fields.append(Params.confirm_password)
            
        if len(invalid_fields) > 0:
            self.status_message_box(f"Failed: Invalid Fields {invalid_fields}")
            return

        self.wallet.name = self.name_line_edit.text()
        self.wallet.password = self.password_line_edit.text()
        self.wallet.phrase = ""

        success = False

        if self.which_wallet == REMOTE_WALLET:
            try: 
                success, res = self.denarii_mobile_client.create_wallet(self.gui_user.user_id, self.wallet.name, self.wallet.password)

                if success: 
                    only_res = res[0]
                    self.wallet.phrase = only_res['seed']
                    self.wallet.address = only_res['wallet_address']
                    self.display_seed(self.wallet.phrase)
                    self.status_message_box("Success. Make sure to write down your information. \n It will not be "
                                            "saved on this device.")
                    self.next_button.setVisible(True)
                else: 
                    self.status_message_box("Failed: could not create remote wallet")
                    self.next_button.setVisible(False)
            except Exception as create_remote_wallet_e:
                print(create_remote_wallet_e)
                self.status_message_box("Failed: unknown error")
                self.next_button.setVisible(False)
        elif self.which_wallet == LOCAL_WALLET:
            try:
                success = self.denarii_client.create_wallet(self.wallet)
                success = self.denarii_client.query_seed(self.wallet) and success
                if success:
                    self.next_button.setVisible(True)
            except Exception as create_wallet_e:
                print(create_wallet_e)
                self.status_message_box("Failed: unknown error")
                self.next_button.setVisible(False)

            if success:
                self.display_seed(self.wallet.phrase)
                self.wallet_save_file_text_box.setText("Wallet saved to: \n " + DENARIID_WALLET_PATH)
                self.status_message_box("Success. Make sure to write down your information. \n It will not be saved on this device.")
            else:   
                self.status_message_box("Failed: could not create local wallet")
                self.next_button.setVisible(False)
        else: 
            self.status_message_box("Failed: need to set the wallet type")
            self.next_button.setVisible(False)

    @property
    def wallet(self):
        if self.which_wallet is None:
            return None 

        if self.which_wallet == REMOTE_WALLET:
            return self.remote_wallet
        elif self.which_wallet == LOCAL_WALLET:
            return self.local_wallet
        return None

    def set_which_wallet(self, which_wallet):
        self.which_wallet = which_wallet

        self.set_wallet_type_callback(self.which_wallet)

    def display_seed(self, seed):
        split = seed.split()
        thirds = int(len(split) / 3)
        first = " ".join(split[:thirds])
        second = " ".join(split[thirds : thirds * 2])
        third = " ".join(split[thirds * 2 :])

        self.wallet_info_text_box.setText(f"{first}\n{second}\n{third}")
