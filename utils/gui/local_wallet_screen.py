import multiprocessing

from wallet_screen import *

if TESTING:
    from denarii_testing_font import Font
    from denarii_testing_label import Label
    from denarii_testing_qt import (
        TextSelectableByMouse,
        AlignBottom,
        AlignCenter,
        AlignLeft,
    )
    from denarii_testing_push_button import PushButton
else:
    from font import *
    from label import *
    from qt import (
        TextSelectableByMouse,
        AlignBottom,
        AlignCenter,
        AlignLeft,
    )
    from push_button import *


class LocalWalletScreen(WalletScreen):
    """
    A screen that lets the user interact with a purely local wallet. Aka one that allows mining, and creating
    subaddresses,  and keeps all data on the computer
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

        self.your_sub_address_label = None
        self.sub_address_text_boxes = None
        self.create_sub_address_push_button = None
        self.start_mining_push_button = None
        self.stop_mining_push_button = None

        super().__init__(
            main_layout=main_layout,
            deletion_func=deletion_func,
            denarii_client=denarii_client,
            gui_user=gui_user,
            suffix=self.local_wallet_suffix,
            denarii_mobile_client=denarii_mobile_client,
            **kwargs
        )

    def init(self, **kwargs):
        super().init(**kwargs)

        self.wallet = kwargs["local_wallet"]

        self.your_sub_address_label = Label("Your Subaddresses:")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.your_sub_address_label.setFont(font)
        self.sub_address_text_boxes = []

        self.create_sub_address_push_button = PushButton(
            "Create subaddress", kwargs["parent"]
        )
        self.create_sub_address_push_button.clicked.connect(
            lambda: self.on_create_sub_address_clicked()
        )
        self.create_sub_address_push_button.setVisible(False)
        self.create_sub_address_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.start_mining_push_button = PushButton("Start mining", kwargs["parent"])
        self.start_mining_push_button.clicked.connect(
            lambda: self.on_start_mining_clicked()
        )
        self.start_mining_push_button.setVisible(False)
        self.start_mining_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.stop_mining_push_button = PushButton("Stop mining", kwargs["parent"])
        self.stop_mining_push_button.clicked.connect(
            lambda: self.on_stop_mining_clicked()
        )
        self.stop_mining_push_button.setVisible(False)
        self.stop_mining_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

    def setup(self):
        super().setup()

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)
        self.main_layout.addLayout(self.fourth_horizontal_layout)
        self.main_layout.addLayout(self.vertical_layout)
        self.main_layout.addLayout(self.fifth_horizontal_layout)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.sixth_horizontal_layout)
        self.main_layout.addLayout(self.seventh_horizontal_layout)
        self.main_layout.addLayout(self.eight_horizontal_layout)
        self.main_layout.addLayout(self.ninth_horizontal_layout)

        self.transfer_push_button.setVisible(True)
        self.create_sub_address_push_button.setVisible(True)
        self.start_mining_push_button.setVisible(True)
        self.stop_mining_push_button.setVisible(True)
        self.back_button.setVisible(True)

        self.first_horizontal_layout.addWidget(
            self.wallet_header_label, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.your_balance_label, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.balance_text_box, alignment=AlignCenter
        )
        self.third_horizontal_layout.addWidget(
            self.your_address_label, alignment=AlignCenter
        )
        self.third_horizontal_layout.addWidget(
            self.address_text_box, alignment=AlignCenter
        )
        self.fourth_horizontal_layout.addWidget(
            self.your_sub_address_label, alignment=AlignCenter
        )
        self.fourth_horizontal_layout.addWidget(
            self.create_sub_address_push_button, alignment=AlignCenter
        )
        self.form_layout.addRow("Address", self.address_line_edit)
        self.form_layout.addRow("Amount", self.amount_line_edit)
        self.fifth_horizontal_layout.addWidget(
            self.transfer_push_button, alignment=AlignCenter
        )
        self.sixth_horizontal_layout.addWidget(
            self.start_mining_push_button, alignment=AlignCenter
        )
        self.sixth_horizontal_layout.addWidget(
            self.stop_mining_push_button, alignment=AlignCenter
        )
        self.seventh_horizontal_layout.addWidget(
            self.wallet_transfer_status_text_box, alignment=AlignCenter
        )
        self.eight_horizontal_layout.addWidget(
            self.wallet_info_status_text_box, alignment=AlignCenter
        )
        self.ninth_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )

        self.populate_wallet_screen()

    def teardown(self):
        super().teardown()

    def populate_wallet_screen(self):
        """
        Populate the wallet scene with user wallet information
        """

        super().populate_wallet_screen()

        success = False
        try:
            success = self.denarii_client.get_address(self.wallet)

            self.balance = self.denarii_client.get_balance_of_wallet(self.wallet)
        except Exception as e:
            print(e)

        if success:
            self.set_wallet_balance()
            self.address_text_box.setText(str(self.wallet.address))

            # Add all the subaddresses to the vertical layout
            for sub_address in self.wallet.sub_addresses:
                sub_address_text_box = Label(str(sub_address))
                font = Font()
                font.setFamily("Arial")
                font.setPixelSize(50)
                sub_address_text_box.setFont(font)
                sub_address_text_box.setTextInteractionFlags(TextSelectableByMouse)
                self.vertical_layout.addWidget(
                    sub_address_text_box, alignment=AlignCenter
                )
                self.sub_address_text_boxes.append(sub_address_text_box)

            self.wallet_info_status_text_box.setText("Success loading wallet info")
        else:
            self.wallet_info_status_text_box.setText("Failure loading wallet info")

    def create_sub_address(self):
        """
        Create a sub address
        """

        success = False

        try:
            success = self.denarii_client.create_no_label_address(self.wallet)
            print_status("Create subaddress ", success)
        except Exception as e:
            print(e)

        if success:
            sub_address_text_box = Label(
                str(self.wallet.sub_addresses[len(self.wallet.sub_addresses) - 1])
            )
            font = Font()
            font.setFamily("Arial")
            font.setPixelSize(50)
            sub_address_text_box.setFont(font)
            sub_address_text_box.setTextInteractionFlags(TextSelectableByMouse)
            self.vertical_layout.addWidget(
                sub_address_text_box, alignment=AlignCenter
            )
            self.sub_address_text_boxes.append(sub_address_text_box)

            _ = ShowText(self.wallet_info_status_text_box, "Success creating sub address. \n Use this to send denarii to other people.")
        else:
            _ = ShowText(self.wallet_info_status_text_box, "Failure creating sub address.")

    def start_mining(self):
        """
        Start mining
        """

        success = False

        try:
            success = self.denarii_client.start_mining(
                True, False, multiprocessing.cpu_count() - 2
            )
        except Exception as e:
            print(e)

        if success:
            _ = ShowText(self.wallet_info_status_text_box, "Started mining")
        else:
            _ = ShowText(self.wallet_info_status_text_box, "Failed to start mining")

    def stop_mining(self):
        """
        Stop mining
        """

        success = False

        try:
            success = self.denarii_client.stop_mining()
        except Exception as e:
            print(e)

        if success:
            _ = ShowText(self.wallet_info_status_text_box, "Stopped mining")
        else:
            _ = ShowText(self.wallet_info_status_text_box, "Failed to stop mining")

    def on_create_sub_address_clicked(self):
        """
        Create a subaddress
        """
        self.create_sub_address()

    def on_start_mining_clicked(self):
        """
        Start mining
        """
        self.start_mining()

    def on_stop_mining_clicked(self):
        """
        Stop mining
        """
        self.stop_mining()
