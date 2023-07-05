from wallet_screen import *


class LocalWalletScreen(WalletScreen):
    """
    A screen that lets the user interact with a purely local wallet. Aka one that allows mining, and creating
    subaddresses,  and keeps all data on the computer
    """

    def __init__(self, main_layout, deletion_func, **kwargs):
        super().__init__(main_layout, deletion_func, suffix=self.local_wallet_suffix, **kwargs)

        self.your_sub_address_label = None
        self.sub_address_text_boxes = None
        self.create_sub_address_push_button = None
        self.start_mining_push_button = None
        self.stop_mining_push_button = None

    def init(self, **kwargs):
        super().init(**kwargs)

        self.wallet = kwargs['local_wallet']

        self.your_sub_address_label = Label("Your Subaddresses:")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.your_sub_address_label.setFont(font)
        self.sub_address_text_boxes = []

        self.create_sub_address_push_button = PushButton("Create subaddress", kwargs['parent'])
        self.create_sub_address_push_button.clicked.connect(self.on_create_sub_address_clicked)
        self.create_sub_address_push_button.setVisible(False)
        self.create_sub_address_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.start_mining_push_button = PushButton("Start mining", kwargs['parent'])
        self.start_mining_push_button.clicked.connect(self.start_mining_push_button)
        self.start_mining_push_button.setVisible(False)
        self.start_mining_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.stop_mining_push_button = PushButton("Stop mining", kwargs['parent'])
        self.stop_mining_push_button.clicked.connect(self.stop_mining_push_button)
        self.stop_mining_push_button.setVisible(False)
        self.stop_mining_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

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
        self.next_button.setVisible(False)

        self.first_horizontal_layout.addWidget(self.wallet_header_label, alignment=Qt.AlignCenter)
        self.second_horizontal_layout.addWidget(self.your_balance_label, alignment=Qt.AlignCenter)
        self.second_horizontal_layout.addWidget(self.balance_text_box, alignment=Qt.AlignCenter)
        self.third_horizontal_layout.addWidget(self.your_address_label, alignment=Qt.AlignCenter)
        self.third_horizontal_layout.addWidget(self.address_text_box, alignment=Qt.AlignCenter)
        self.fourth_horizontal_layout.addWidget(self.your_sub_address_label, alignment=Qt.AlignCenter)
        self.fourth_horizontal_layout.addWidget(self.create_sub_address_push_button, alignment=Qt.AlignCenter)
        self.form_layout.addRow("Address", self.address_line_edit)
        self.form_layout.addRow("Amount", self.amount_line_edit)
        self.fifth_horizontal_layout.addWidget(self.transfer_push_button, alignment=Qt.AlignCenter)
        self.sixth_horizontal_layout.addWidget(self.start_mining_push_button, alignment=Qt.AlignCenter)
        self.sixth_horizontal_layout.addWidget(self.stop_mining_push_button, alignment=Qt.AlignCenter)
        self.seventh_horizontal_layout.addWidget(self.wallet_transfer_status_text_box, alignment=Qt.AlignCenter)
        self.eight_horizontal_layout.addWidget(self.wallet_info_status_text_box, alignment=Qt.AlignCenter)
        self.ninth_horizontal_layout.addWidget(self.back_button, alignment=(Qt.AlignLeft | Qt.AlignBottom))

        self.populate_wallet_screen()

    def teardown(self):
        super().teardown()

    def populate_wallet_screen(self):
        """
        Populate the wallet scene with user wallet information
        """

        super().populate_wallet_screen()

        success = False
        balance = 0
        try:
            success = self.denarii_client.get_address(self.wallet)

            balance = self.denarii_client.get_balance_of_wallet(self.wallet)
        except Exception as e:
            print(e)

        if success:
            # We need to adjust the balance because it is in picomonero
            self.balance_text_box.setText(str(balance * 0.000000000001))
            self.address_text_box.setText(str(self.wallet.address))

            # Add all the subaddresses to the vertical layout
            for sub_address in self.wallet.sub_addresses:
                sub_address_text_box = Label(str(sub_address))
                font = Font()
                font.setFamily("Arial")
                font.setPixelSize(50)
                sub_address_text_box.setFont(font)
                sub_address_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
                self.vertical_layout.addWidget(sub_address_text_box, alignment=Qt.AlignCenter)
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
            sub_address_text_box = Label(str(self.wallet.sub_addresses[len(self.wallet.sub_addresses) - 1]))
            font = Font()
            font.setFamily("Arial")
            font.setPixelSize(50)
            sub_address_text_box.setFont(font)
            sub_address_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.vertical_layout.addWidget(sub_address_text_box, alignment=Qt.AlignCenter)
            self.sub_address_text_boxes.append(sub_address_text_box)
            self.wallet_info_status_text_box.setText(
                "Success creating sub address. Use this to send to other people.")
        else:
            self.wallet_info_status_text_box.setText("Failure creating sub address.")

    def start_mining(self):
        """
        Start mining
        """

        success = False

        try:
            success = self.denarii_client.start_mining(True, False, multiprocessing.cpu_count() - 2)
        except Exception as e:
            print(e)

        if success:
            self.wallet_info_status_text_box.setText("Started mining")
        else:
            self.wallet_info_status_text_box.setText("Failed to start mining")

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
            self.wallet_info_status_text_box.setText("Stopped mining")
        else:
            self.wallet_info_status_text_box.setText("Failed to stop mining")

    @pyqtSlot()
    def on_create_sub_address_clicked(self):
        """
        Create a subaddress
        """
        self.create_sub_address()

    @pyqtSlot()
    def on_start_mining_clicked(self):
        """
        Start mining
        """
        self.start_mining()

    @pyqtSlot()
    def on_stop_mining_clicked(self):
        """
        Stop mining
        """
        self.stop_mining()
