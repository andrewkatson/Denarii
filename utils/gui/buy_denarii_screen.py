import threading
import time

from screen import *
from stoppable_thread import StoppableThread

if TESTING:
    from denarii_testing_button_group import ButtonGroup
    from denarii_testing_font import Font
    from denarii_testing_icon import Icon
    from denarii_testing_label import Label
    from denarii_testing_line_edit import LineEdit
    from denarii_testing_message_box import MessageBox
    from denarii_testing_pixmap import Pixmap
    from denarii_testing_push_button import PushButton
    from denarii_testing_qt import (
        TextSelectableByMouse,
        AlignRight,
        AlignBottom,
        AlignCenter,
        AlignLeft,
    )
    from denarii_testing_radio_button import RadioButton
    from denarii_testing_size import Size

else:
    from button_group import ButtonGroup
    from font import *
    from icon import Icon
    from label import *
    from line_edit import *
    from message_box import MessageBox
    from pixmap import Pixmap
    from push_button import *
    from qt import (
        TextSelectableByMouse,
        AlignRight,
        AlignBottom,
        AlignCenter,
        AlignLeft,
    )
    from radio_button import *
    from size import Size


class BuyDenariiScreen(Screen):
    """
    A screen that allows the user to buy denarii with their credit card from other users
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
        self.remote_wallet_screen_push_button = None
        self.sell_screen_push_button = None
        self.credit_card_info_screen_push_button = None
        self.user_settings_screen_push_button = None
        self.verification_screen_push_button = None
        self.buy_denarii_label = None
        self.submit_push_button = None
        self.amount_line_edit = None
        self.price_line_edit = None
        self.asks_label = None
        self.amount_col_label = None
        self.price_col_label = None
        self.amount_bought_col_label = None
        self.queued_buys_label = None
        self.buy_regardless_of_price_radio_button = None
        self.dont_buy_regardless_or_price_radio_button = None
        self.buy_regardles_of_price_button_group = None
        self.fail_if_full_amount_cant_be_bought_radio_button = None
        self.succeed_even_when_full_amount_cant_be_bought_radio_button = None
        self.fail_if_full_amount_cant_be_bought_button_group = None
        self.buy_regardless_of_price_label = None
        self.fail_if_full_amount_isnt_met_label = None
        self.cancel_buy_col_label = None

        self.buy_regardless_of_price = False
        self.fail_if_full_amount_isnt_met = True

        self.current_asks = []
        self.queued_buys = []
        
        self.current_asks_artifacts = []
        self.queued_buys_artifacts = []

        self.asks_refresh_thread = StoppableThread(target=self.refresh_prices)

        self.settled_transactions_thread = StoppableThread(
            target=self.refresh_settled_transactions
        )
        self.populate_thread = StoppableThread(target=self.populate_buy_denarii_screen)

        self.lock = threading.Lock()

        self.parent = kwargs["parent"]

        super().__init__(
            self.buy_denarii_screen_name,
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

        self.buy_denarii_label = Label("Buy Denarii")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.buy_denarii_label.setFont(font)

        self.remote_wallet_screen_push_button = PushButton("Wallet", kwargs["parent"])
        self.remote_wallet_screen_push_button.clicked.connect(
            lambda: kwargs["on_remote_wallet_screen_clicked"]()
        )
        self.remote_wallet_screen_push_button.setVisible(False)
        self.remote_wallet_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.sell_screen_push_button = PushButton("Sell Denarii", kwargs["parent"])
        self.sell_screen_push_button.clicked.connect(
            lambda: kwargs["on_sell_screen_clicked"]()
        )
        self.sell_screen_push_button.setVisible(False)
        self.sell_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.credit_card_info_screen_push_button = PushButton(
            "Credit Card", kwargs["parent"]
        )
        self.credit_card_info_screen_push_button.clicked.connect(
            lambda: kwargs["on_credit_card_info_screen_clicked"]()
        )
        self.credit_card_info_screen_push_button.setVisible(False)
        self.credit_card_info_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.user_settings_screen_push_button = PushButton(
            "User Settings", kwargs["parent"]
        )
        self.user_settings_screen_push_button.clicked.connect(
            lambda: kwargs["on_user_settings_screen_clicked"]()
        )
        self.user_settings_screen_push_button.setVisible(False)
        self.user_settings_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.verification_screen_push_button = PushButton(
            "Identity Verification", kwargs["parent"]
        )
        self.verification_screen_push_button.clicked.connect(
            lambda: kwargs["on_verification_screen_clicked"]()
        )
        self.verification_screen_push_button.setVisible(False)
        self.verification_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.submit_push_button = PushButton("Submit", kwargs["parent"])
        self.submit_push_button.clicked.connect(lambda: self.on_submit_clicked())
        self.submit_push_button.setVisible(False)
        self.submit_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.amount_line_edit = LineEdit()
        self.price_line_edit = LineEdit()

        self.asks_label = Label("Asks")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.asks_label.setFont(font)

        self.amount_col_label_one = Label("Amount")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.amount_col_label_one.setFont(font)

        self.price_col_label_one = Label("Price")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.price_col_label_one.setFont(font)

        self.amount_col_label = Label("Amount")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.amount_col_label.setFont(font)

        self.price_col_label = Label("Price")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.price_col_label.setFont(font)

        self.amount_bought_col_label = Label("Amount Bought")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.amount_bought_col_label.setFont(font)

        self.cancel_buy_col_label = Label("Cancel Buy")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.cancel_buy_col_label.setFont(font)

        self.queued_buys_label = Label("Queued Buys")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.queued_buys_label.setFont(font)

        self.buy_regardless_of_price_label = Label("Buy Regardless of Asking Price")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.buy_regardless_of_price_label.setFont(font)

        self.fail_if_full_amount_isnt_met_label = Label(
            "Fail if Full Amount Cannot Be Bought"
        )
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.fail_if_full_amount_isnt_met_label.setFont(font)

        self.buy_regardless_of_price_radio_button = RadioButton(
            "True",
            kwargs["parent"],
            buy_regardless_of_price_callback=self.set_buy_regardless_or_price,
        )
        self.buy_regardless_of_price_radio_button.buy_regardless_of_price_option = True
        self.buy_regardless_of_price_radio_button.toggled.connect(
            self.buy_regardless_of_price_radio_button.on_buy_regardless_of_price_clicked
        )
        self.buy_regardless_of_price_radio_button.setVisible(False)
        self.buy_regardless_of_price_radio_button.setStyleSheet(
            "QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};"
        )

        self.dont_buy_regardless_or_price_radio_button = RadioButton(
            "False",
            kwargs["parent"],
            buy_regardless_of_price_callback=self.set_buy_regardless_or_price,
        )
        self.dont_buy_regardless_or_price_radio_button.buy_regardless_of_price_option = (
            False
        )
        self.dont_buy_regardless_or_price_radio_button.toggled.connect(
            self.dont_buy_regardless_or_price_radio_button.on_buy_regardless_of_price_clicked
        )
        self.dont_buy_regardless_or_price_radio_button.setChecked(True)
        self.dont_buy_regardless_or_price_radio_button.setVisible(False)
        self.dont_buy_regardless_or_price_radio_button.setStyleSheet(
            "QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};"
        )

        self.buy_regardles_of_price_button_group = ButtonGroup()
        self.buy_regardles_of_price_button_group.addButton(self.buy_regardless_of_price_radio_button)
        self.buy_regardles_of_price_button_group.addButton(self.dont_buy_regardless_or_price_radio_button)


        self.fail_if_full_amount_cant_be_bought_radio_button = RadioButton(
            "True",
            kwargs["parent"],
            fail_if_full_amount_isnt_met_callback=self.set_fail_if_full_amount_isnt_met,
        )
        self.fail_if_full_amount_cant_be_bought_radio_button.fail_if_full_amount_isnt_met_option = (
            True
        )
        self.fail_if_full_amount_cant_be_bought_radio_button.toggled.connect(
            self.fail_if_full_amount_cant_be_bought_radio_button.on_fail_if_full_amount_isnt_met
        )
        self.fail_if_full_amount_cant_be_bought_radio_button.setChecked(True)
        self.fail_if_full_amount_cant_be_bought_radio_button.setVisible(False)
        self.fail_if_full_amount_cant_be_bought_radio_button.setStyleSheet(
            "QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};"
        )

        self.succeed_even_when_full_amount_cant_be_bought_radio_button = RadioButton(
            "False",
            kwargs["parent"],
            fail_if_full_amount_isnt_met_callback=self.set_fail_if_full_amount_isnt_met,
        )
        self.succeed_even_when_full_amount_cant_be_bought_radio_button.fail_if_full_amount_isnt_met_option = (
            False
        )
        self.succeed_even_when_full_amount_cant_be_bought_radio_button.toggled.connect(
            self.succeed_even_when_full_amount_cant_be_bought_radio_button.on_fail_if_full_amount_isnt_met
        )
        self.succeed_even_when_full_amount_cant_be_bought_radio_button.setVisible(False)
        self.succeed_even_when_full_amount_cant_be_bought_radio_button.setStyleSheet(
            "QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};"
        )

        self.fail_if_full_amount_cant_be_bought_button_group = ButtonGroup()
        self.fail_if_full_amount_cant_be_bought_button_group.addButton(self.fail_if_full_amount_cant_be_bought_radio_button)
        self.fail_if_full_amount_cant_be_bought_button_group.addButton(self.succeed_even_when_full_amount_cant_be_bought_radio_button)

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
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addLayout(self.eight_horizontal_layout)
        self.main_layout.addLayout(self.second_grid_layout)
        self.main_layout.addLayout(self.ninth_horizontal_layout)

        self.remote_wallet_screen_push_button.setVisible(True)
        self.sell_screen_push_button.setVisible(True)
        self.credit_card_info_screen_push_button.setVisible(True)
        self.user_settings_screen_push_button.setVisible(True)
        self.verification_screen_push_button.setVisible(True)
        self.submit_push_button.setVisible(True)
        self.fail_if_full_amount_cant_be_bought_radio_button.setVisible(True)
        self.succeed_even_when_full_amount_cant_be_bought_radio_button.setVisible(True)
        self.buy_regardless_of_price_radio_button.setVisible(True)
        self.dont_buy_regardless_or_price_radio_button.setVisible(True)

        self.first_horizontal_layout.addWidget(
            self.buy_denarii_label, alignment=AlignCenter
        )
        self.form_layout.addRow("Amount", self.amount_line_edit)
        self.form_layout.addRow("Price", self.price_line_edit)

        self.second_horizontal_layout.addWidget(
            self.buy_regardless_of_price_label, alignment=AlignCenter
        )
        self.third_horizontal_layout.addWidget(
            self.buy_regardless_of_price_radio_button, alignment=AlignCenter
        )
        self.third_horizontal_layout.addWidget(
            self.dont_buy_regardless_or_price_radio_button, alignment=AlignCenter
        )
        self.fourth_horizontal_layout.addWidget(
            self.fail_if_full_amount_isnt_met_label, alignment=AlignCenter
        )
        self.fifth_horizontal_layout.addWidget(
            self.fail_if_full_amount_cant_be_bought_radio_button, alignment=AlignCenter
        )
        self.fifth_horizontal_layout.addWidget(
            self.succeed_even_when_full_amount_cant_be_bought_radio_button,
            alignment=AlignCenter,
        )

        self.sixth_horizontal_layout.addWidget(
            self.submit_push_button, alignment=AlignCenter
        )

        self.seventh_horizontal_layout.addWidget(self.asks_label, alignment=AlignCenter)
        # Grid with all the asks made by other users
        self.grid_layout.addWidget(self.amount_col_label_one, 0, 0)
        self.grid_layout.addWidget(self.price_col_label_one, 0, 1)

        self.eight_horizontal_layout.addWidget(
            self.queued_buys_label, alignment=AlignCenter
        )
        # Grid with all the queued buys for the current user
        self.second_grid_layout.addWidget(self.amount_col_label, 0, 0)
        self.second_grid_layout.addWidget(self.price_col_label, 0, 1)
        self.second_grid_layout.addWidget(self.amount_bought_col_label, 0, 2)
        self.second_grid_layout.addWidget(self.cancel_buy_col_label, 0, 3)

        self.ninth_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )
        self.ninth_horizontal_layout.addWidget(
            self.remote_wallet_screen_push_button, alignment=AlignCenter
        )
        self.ninth_horizontal_layout.addWidget(
            self.sell_screen_push_button, alignment=AlignCenter
        )
        self.ninth_horizontal_layout.addWidget(
            self.credit_card_info_screen_push_button, alignment=AlignCenter
        )
        self.ninth_horizontal_layout.addWidget(
            self.user_settings_screen_push_button, alignment=AlignCenter
        )
        self.ninth_horizontal_layout.addWidget(
            self.verification_screen_push_button, alignment=AlignCenter
        )

        self.asks_refresh_thread.start()
        self.settled_transactions_thread.start()
        self.populate_thread.start()

    def teardown(self):
        super().teardown()

        self.asks_refresh_thread.stop()
        self.settled_transactions_thread.stop()
        self.populate_thread.stop()

        if self.asks_refresh_thread.is_alive():
            self.asks_refresh_thread.join()
        if self.settled_transactions_thread.is_alive():
            self.settled_transactions_thread.join()
        if self.populate_thread.is_alive():
            self.populate_thread.join()

    def on_submit_clicked(self):
        """
        Attempt to buy some denarii asks and set them in queued_buys. Then get money from the buyer (i.e. schedule it to be transferred). Then have the denarii be transferred over.
        """

        try:
            self.lock.acquire()

            success, first_res = self.denarii_mobile_client.has_credit_card_info(
                self.gui_user.user_id
            )
            
            other_success, other_res = self.denarii_mobile_client.is_a_verified_person(self.gui_user.user_id)

            if success and other_success:
                has_credit_card_info = first_res[0]["has_credit_card_info"]
                is_verified = other_res[0]["verification_status"] == "is_verified"

                if has_credit_card_info and is_verified:
                    success, second_res = self.denarii_mobile_client.buy_denarii(
                        self.gui_user.user_id,
                        self.amount_line_edit.text(),
                        self.price_line_edit.text(),
                        self.buy_regardless_of_price,
                        self.fail_if_full_amount_isnt_met,
                    )

                    if success:
                        # TODO: change to use other currencies.
                        (
                            success
                        ) = self.denarii_mobile_client.get_money_from_buyer(
                            self.gui_user.user_id, self.amount_line_edit.text(), "usd"
                        )

                        if success:
                            succeeded_asks = []
                            any_ask_failed = false
                            for ask in second_res:
                                (
                                    success,
                                    fourth_res,
                                ) = self.denarii_mobile_client.transfer_denarii(
                                    self.gui_user.user_id, ask["ask_id"]
                                )

                                if success:
                                    current_ask = self.get_current_ask(ask["ask_id"])
                                    self.queued_buys.append(
                                        {
                                            "ask_id": ask["ask_id"],
                                            "amount_bought": fourth_res[0][
                                                "amount_bought"
                                            ],
                                            "amount": current_ask["amount"],
                                            "asking_price": current_ask["asking_price"]
                                        }
                                    )
                                    succeeded_asks.append(ask)
                                else: 
                                    any_ask_failed = True
                                    break
                            if any_ask_failed:
                                self.status_message_box(
                                    "Failed one of the denarii transfers. Will refund money and transfer denarii back to seller."
                                )
                                self.reverse_transactions(succeeded_asks)
                                break
                        else:
                            ask_ids_to_cancel = []
                            for ask in second_res:
                                ask_ids_to_cancel.append(ask['ask_id'])
                            self.cancel_buys(ask_ids_to_cancel)
                    else:
                        self.status_message_box("Failed to buy denarii")

                else:
                    self.status_message_box(
                        "Failed to buy denarii because there was no credit card info on file or the user was not verified"
                    )
            else:
                self.status_message_box(
                    "Failed to buy denarii because we could not determine if there was credit card info or we could not determine if the user was verified"
                )

        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

        finally:
            self.lock.release()
            
    def depopulate_buy_denarii_screen(self): 
        try:
            # First we de-populate the asks grid
            self.lock.acquire()
            
            for artifact in self.current_asks_artifacts: 
                artifact.setVisible(False)
                
            # Then we de-populate the queued buys grid
            for artifact in self.queued_buys_artifacts: 
                artifact.setVisible(False)
            
        finally:
            self.lock.release()


    def populate_buy_denarii_screen(self):
        while not self.populate_thread.stopped():
            try:
                # First we populate the asks grid
                row = 1
                self.depopulate_buy_denarii_screen()
                self.lock.acquire()
                new_current_asks_artifacts = []
                for ask in self.current_asks:
                    ask_amount_label = Label(str(ask["amount"]))
                    font = Font()
                    font.setFamily("Arial")
                    font.setPixelSize(50)
                    ask_amount_label.setFont(font)

                    self.grid_layout.addWidget(ask_amount_label, row, 0)
                    new_current_asks_artifacts.append(ask_amount_label)

                    ask_price_label = Label(str(ask["asking_price"]))
                    font = Font()
                    font.setFamily("Arial")
                    font.setPixelSize(50)
                    ask_price_label.setFont(font)
                    new_current_asks_artifacts.append(ask_price_label)

                    self.grid_layout.addWidget(ask_price_label, row, 1)

                    row += 1
                
                self.current_asks_artifacts = new_current_asks_artifacts
                
                # Then we populate the queued asks grid (which are just asks that we are buying)
                row = 1
                new_queued_buys_artifacts = []
                
                for buy in self.queued_buys:
                    ask_amount_label = Label(str(buy["amount"]))
                    font = Font()
                    font.setFamily("Arial")
                    font.setPixelSize(50)
                    ask_amount_label.setFont(font)
                    new_queued_buys_artifacts.append(ask_amount_label)

                    self.second_grid_layout.addWidget(ask_amount_label, row, 0)

                    ask_price_label = Label(str(buy["asking_price"]))
                    font = Font()
                    font.setFamily("Arial")
                    font.setPixelSize(50)
                    ask_price_label.setFont(font)
                    new_queued_buys_artifacts.append(ask_price_label)

                    self.second_grid_layout.addWidget(ask_price_label, row, 1)

                    amount_bought_label = Label(str(buy["amount_bought"]))
                    font = Font()
                    font.setFamily("Arial")
                    font.setPixelSize(50)
                    amount_bought_label.setFont(font)
                    new_queued_buys_artifacts.append(amount_bought_label)

                    self.second_grid_layout.addWidget(amount_bought_label, row, 2)

                    cancel_buy_push_button = PushButton("Cancel Buy", self.parent)
                    cancel_buy_push_button.clicked.connect(
                        lambda: self.on_cancel_buy_clicked(str(buy["ask_id"]))
                    )
                    cancel_buy_push_button.setVisible(True)
                    cancel_buy_push_button.setStyleSheet(
                        "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
                    )
                    new_queued_buys_artifacts.append(cancel_buy_push_button)

                    self.second_grid_layout.addWidget(cancel_buy_push_button, row, 3)
                    row += 1
                    
                self.queued_buys_artifacts = new_queued_buys_artifacts
            finally:
                self.lock.release()

            time.sleep(1)

    def refresh_prices(self):
        while not self.asks_refresh_thread.stopped():
            try:
                success, res = self.denarii_mobile_client.get_prices(
                    self.gui_user.user_id
                )

                if success:
                    try:
                        self.lock.acquire()
                        self.current_asks = res
                    finally:
                        self.lock.release()
                    # No status message when things go well on purpose so the user doesn't get annoyed.
            except Exception as e:
                print(e)

            time.sleep(5)

    def refresh_settled_transactions(self):
        while not self.settled_transactions_thread.stopped():
            try:
                self.lock.acquire()
                ask_ids_to_remove = []

                # Check to see what buys are settled
                for buy in self.queued_buys:
                    success, res = self.denarii_mobile_client.is_transaction_settled(
                        self.gui_user.user_id, buy["ask_id"]
                    )

                    if success:
                        was_settled = res[0]["transaction_was_settled"]

                        if was_settled:
                            ask_ids_to_remove.append(buy["ask_id"])
                    else:
                        self.completely_reverse_transaction(buy)

                # Remove the ones that are settled
                new_queued_buys = []
                for buy in self.queued_buys:
                    if buy["ask_id"] not in ask_ids_to_remove:
                        new_queued_buys.append(buy)

                self.queued_buys = new_queued_buys

            except Exception as e:
                print(e)
            finally:
                self.lock.release()

            time.sleep(5)

    def set_fail_if_full_amount_isnt_met(self, fail_if_full_amount_isnt_met):
        self.fail_if_full_amount_isnt_met = fail_if_full_amount_isnt_met

    def set_buy_regardless_or_price(self, buy_regardless_of_price):
        self.buy_regardless_of_price = buy_regardless_of_price

    def get_current_ask(self, ask_id):
        for ask in self.current_asks:
            if ask["ask_id"] == ask_id:
                return ask
        try:
            success, res = self.denarii_mobile_client.get_ask_with_identifier(
                self.gui_user.user_id, ask_id
            )

            if success:
                return res
            else:
                return {"amount": -1, "ask_id": ask_id, "amount_bought": 0}
        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")
            return {"amount": -1, "ask_id": ask_id, "amount_bought": 0}

    def completely_reverse_transaction(self, ask_to_reverse):
        """
        Transfers denarii back to seller, sends money back to buyer, and cancels the buy
        """

        try:
            success, res = self.denarii_mobile_client.transfer_denarii_back_to_seller(
                self.gui_user.user_id, ask_to_reverse["ask_id"]
            )

            if success:
                self.reverse_transactions([ask_to_reverse])
            else:
                self.status_message_box(
                    f"Failed to transfer denarii back to seller for ask: {ask_to_reverse['ask_id']}. Copy that down and file a support ticket."
                )

        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

    def reverse_transactions(self, asks_to_reverse):
        """
        Sends money back to buyer and cancels the buy
        """
        for ask in asks_to_reverse:
            try:
                success = self.denarii_mobile_client.send_money_back_to_buyer(
                    self.gui_user.user_id, ask["amount_bought"], "usd"
                )

                if success:
                    self.cancel_buys([ask["ask_id"]])
                else:
                    self.status_message_box(
                        f"Failed to send money back to buyer and cancel ask: {ask['ask_id']}. Copy that down and file a support ticket."
                    )

            except Exception as e:
                print(e)
                self.status_message_box("Failed: unknown error")

    def cancel_buys(self, ask_ids_to_cancel):
        for ask_id in ask_ids_to_cancel:
            try:
                success = self.denarii_mobile_client.cancel_buy_of_ask(
                    self.gui_user.user_id, ask_id
                )

                if success:
                    self.queued_buys = [
                        buy for buy in self.queued_buys if ask_id != buy["ask_id"]
                    ]
                else:
                    # TODO use a message box that makes the user accept before continuing
                    self.status_message_box(
                        f"Failed to cancel buy of ask: {ask_id}. Copy that down and file a support ticket."
                    )
                    time.sleep(3)

            except Exception as e:
                print(e)
                self.status_message_box("Failed: unknown error")

    def on_cancel_buy_clicked(self, ask_id_to_cancel):
        self.cancel_buys([ask_id_to_cancel])
