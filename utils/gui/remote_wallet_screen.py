from wallet_screen import *

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




class RemoteWalletScreen(WalletScreen):
    """
    A screen that allows the user to interact with a remote wallet. Aka one that allows the buying and selling of
    denarii and stores the data in the cloud.
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
        
        self.buy_screen_push_button = None
        self.sell_screen_push_button = None 
        self.credit_card_info_screen_push_button = None 
        self.on_credit_card_info_screen_clicked = kwargs['on_credit_card_info_screen_clicked']
        self.on_buy_screen_clicked = kwargs['on_buy_screen_clicked']
        self.on_sell_screen_clicked = kwargs['on_sell_screen_clicked']
        super().__init__(
            main_layout=main_layout,
            deletion_func=deletion_func,
            denarii_client=denarii_client,
            gui_user=gui_user,
            suffix=self.remote_wallet_suffix,
            denarii_mobile_client=denarii_mobile_client,
            **kwargs
        )

    def init(self, **kwargs):
        super().init(**kwargs)

        self.wallet = kwargs["remote_wallet"]

        self.buy_screen_push_button = PushButton("Buy Denarii", kwargs["parent"])
        self.buy_screen_push_button.clicked.connect(
            lambda: self.on_buy_screen_clicked()
        )
        self.buy_screen_push_button.setVisible(False)
        self.buy_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.sell_screen_push_button = PushButton("Sell Denarii", kwargs["parent"])
        self.sell_screen_push_button.clicked.connect(
            lambda: self.on_sell_screen_clicked()
        )
        self.sell_screen_push_button.setVisible(False)
        self.sell_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.on_credit_card_info_screen_clicked = PushButton("Credit Card", kwargs["parent"])
        self.on_credit_card_info_screen_clicked.clicked.connect(
            lambda: self.on_credit_card_info_screen_clicked()
        )
        self.on_credit_card_info_screen_clicked.setVisible(False)
        self.on_credit_card_info_screen_clicked.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

    def setup(self):
        super().setup()
        
        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)
        self.main_layout.addLayout(self.fourth_horizontal_layout)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.fifth_horizontal_layout)


        self.transfer_push_button.setVisible(True)
        self.buy_screen_push_button.setVisible(True)
        self.sell_screen_push_button.setVisible(True)
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

        self.form_layout.addRow("Address", self.address_line_edit)
        self.form_layout.addRow("Amount", self.amount_line_edit)
        self.fourth_horizontal_layout.addWidget(
            self.transfer_push_button, alignment=AlignCenter
        )

        self.fifth_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )
        self.fifth_horizontal_layout.addWidget(self.buy_screen_push_button, alignment=AlignCenter)
        self.fifth_horizontal_layout.addWidget(self.sell_screen_push_button, alignment=AlignCenter)
        self.fifth_horizontal_layout.addWidget(self.credit_card_info_screen_push_button, alignment=AlignCenter)

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

            if self.gui_user.user_id is None:
                success, res = self.denarii_mobile_client.get_user_id(self.gui_user.name, self.gui_user.email, self.gui_user.password)
                if success: 
                    self.gui_user.user_id = res[0]['user_id']
                    success, res = self.try_to_get_balance_of_remote_wallet()

                    if success: 
                        self.balance = res[0]['balance']
            else: 
                success, res = self.try_to_get_balance_of_remote_wallet()

                if success: 
                        self.balance = res[0]['balance']

        except Exception as e:
            print(e)

        if success:
            self.set_wallet_balance()
            self.address_text_box.setText(str(self.wallet.address))

            self.status_message_box("Success loading wallet info")
        else:
            self.status_message_box("Failure loading wallet info")
