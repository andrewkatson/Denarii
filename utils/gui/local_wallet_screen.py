from wallet_screen import *


class LocalWalletScreen(WalletScreen):
    """
    A screen that lets the user interact with a purely local wallet. Aka one that allows mining, and creating
    subaddresses,  and keeps all data on the computer
    """

    def __init__(self, main_layout, deletion_func, **kwargs):
        super().__init__(main_layout, deletion_func, suffix=self.local_wallet_suffix, **kwargs)

        self.your_sub_address_label = Label("Your Subaddresses:")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.your_sub_address_label.setFont(font)
        self.sub_address_text_boxes = []

        self.create_sub_address_push_button = PushButton("Create subaddress", kwargs['parent'])
        self.create_sub_address_push_button.clicked.connect(kwargs['on_create_subaddress_clicked'])
        self.create_sub_address_push_button.setVisible(False)
        self.create_sub_address_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.start_mining_push_button = PushButton("Start mining", kwargs['parent'])
        self.start_mining_push_button.clicked.connect(kwargs['on_start_mining_clicked'])
        self.start_mining_push_button.setVisible(False)
        self.start_mining_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.stop_mining_push_button = PushButton("Stop mining", kwargs['parent'])
        self.stop_mining_push_button.clicked.connect(kwargs['on_stop_mining_clicked'])
        self.stop_mining_push_button.setVisible(False)
        self.stop_mining_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

    def setup(self):
        super().setup()
