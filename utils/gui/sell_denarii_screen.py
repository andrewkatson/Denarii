import sys
import threading
import time

from screen import *
from stoppable_thread import StoppableThread

if TESTING:
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


class SellDenariiScreen(Screen):
    """
    A screen that allows the user to sell denarii with their credit card to other users
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
        self.sell_denarii_label = None

        self.buy_screen_push_button = None
        self.remote_wallet_screen_push_button = None
        self.credit_card_info_screen_push_button = None
        self.user_settings_screen_push_button = None
        self.verification_screen_push_button = None

        self.submit_push_button = None

        self.amount_line_edit = None
        self.price_line_edit = None

        self.all_asks_label = None
        self.amount_col_label = None
        self.price_col_label = None
        self.amount_bought_col_label = None
        self.bought_asks_label = None
        self.cancel_ask_col_label = None
        self.own_asks_label = None
        self.going_price_label = None

        self.current_asks = []
        self.own_asks = []
        self.bought_asks = []
        
        self.current_asks_artifacts = []
        self.own_asks_artifacts = []
        self.bought_asks_artifacts = []

        self.asks_refresh_thread = StoppableThread(target=self.refresh_all_prices, name="sell_denarii_asks_refresh_thread")

        self.completed_transactions_thread = StoppableThread(
            target=self.refresh_completed_transactions
        )
        self.own_asks_thread = StoppableThread(target=self.refresh_own_asks, name="own_asks_thread")
        self.populate_thread = StoppableThread(target=self.populate_sell_denarii_screen, name="populate_thread")
        self.refresh_asks_in_escrow_thread = StoppableThread(
            target=self.refresh_asks_in_escrow, name="refresh_asks_in_escrow"
        )
        self.refresh_going_price_thread = StoppableThread(target=self.refresh_going_price, name="refresh_going_price")

        self.lock = threading.Lock()

        self.parent = kwargs["parent"]

        super().__init__(
            self.sell_denarii_screen_name,
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

        self.sell_denarii_label = Label("Sell Denarii")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.sell_denarii_label.setFont(font)

        self.remote_wallet_screen_push_button = PushButton("Wallet", kwargs["parent"])
        self.remote_wallet_screen_push_button.clicked.connect(
            lambda: kwargs["on_remote_wallet_screen_clicked"]()
        )
        self.remote_wallet_screen_push_button.setVisible(False)
        self.remote_wallet_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.buy_screen_push_button = PushButton("Buy Denarii", kwargs["parent"])
        self.buy_screen_push_button.clicked.connect(
            lambda: kwargs["on_buy_screen_clicked"]()
        )
        self.buy_screen_push_button.setVisible(False)
        self.buy_screen_push_button.setStyleSheet(
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

        self.all_asks_label = Label("All Asks")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.all_asks_label.setFont(font)


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

        self.own_asks_label = Label("Own Asks")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.own_asks_label.setFont(font)

        self.amount_col_label_two = Label("Amount")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.amount_col_label_two.setFont(font)

        self.price_col_label_two = Label("Price")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.price_col_label_two.setFont(font)

        self.amount_bought_col_label = Label("Amount Bought")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.amount_bought_col_label.setFont(font)

        self.cancel_ask_col_label = Label("Cancel Ask")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.cancel_ask_col_label.setFont(font)

        self.bought_asks_label = Label("Bought Asks")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.bought_asks_label.setFont(font)


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

        self.going_price_label = Label("Going Price: ")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.going_price_label.setFont(font)

    def setup(self):
        super().setup()

        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.fourth_horizontal_layout)
        self.main_layout.addLayout(self.fifth_horizontal_layout)
        self.main_layout.addLayout(self.second_grid_layout)
        self.main_layout.addLayout(self.sixth_horizontal_layout)
        self.main_layout.addLayout(self.third_grid_layout)
        self.main_layout.addLayout(self.seventh_horizontal_layout)

        self.remote_wallet_screen_push_button.setVisible(True)
        self.buy_screen_push_button.setVisible(True)
        self.credit_card_info_screen_push_button.setVisible(True)
        self.user_settings_screen_push_button.setVisible(True)
        self.verification_screen_push_button.setVisible(True)
        self.submit_push_button.setVisible(True)

        self.first_horizontal_layout.addWidget(self.sell_denarii_label, alignment=AlignCenter)

        self.second_horizontal_layout.addWidget(self.going_price_label, alignment=AlignCenter)

        self.third_horizontal_layout.addWidget(self.all_asks_label, alignment=AlignCenter)

        self.grid_layout.addWidget(self.amount_col_label_one, 0, 0)
        self.grid_layout.addWidget(self.price_col_label_one, 0, 1)

        self.form_layout.addRow("Amount", self.amount_line_edit)
        self.form_layout.addRow("Price", self.price_line_edit)

        self.fourth_horizontal_layout.addWidget(self.submit_push_button, alignment=AlignCenter)

        self.fifth_horizontal_layout.addWidget(self.own_asks_label, alignment=AlignCenter)

        self.second_grid_layout.addWidget(self.amount_col_label_two, 0, 0)
        self.second_grid_layout.addWidget(self.price_col_label_two, 0, 1)
        self.second_grid_layout.addWidget(self.cancel_ask_col_label, 0, 2)

        self.sixth_horizontal_layout.addWidget(self.bought_asks_label, alignment=AlignCenter)

        self.third_grid_layout.addWidget(self.amount_col_label, 0, 0)
        self.third_grid_layout.addWidget(self.price_col_label, 0, 1)
        self.third_grid_layout.addWidget(self.amount_bought_col_label, 0, 2)

        self.seventh_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )
        self.seventh_horizontal_layout.addWidget(
            self.remote_wallet_screen_push_button, alignment=AlignCenter
        )
        self.seventh_horizontal_layout.addWidget(
            self.buy_screen_push_button, alignment=AlignCenter
        )
        self.seventh_horizontal_layout.addWidget(
            self.credit_card_info_screen_push_button, alignment=AlignCenter
        )
        self.seventh_horizontal_layout.addWidget(
            self.user_settings_screen_push_button, alignment=AlignCenter
        )
        self.seventh_horizontal_layout.addWidget(
            self.verification_screen_push_button, alignment=AlignCenter
        )        

        self.asks_refresh_thread.start()
        self.own_asks_thread.start()
        self.completed_transactions_thread.start()
        self.populate_thread.start()

    def teardown(self):
        super().teardown()

        self.own_asks_thread.stop()
        self.populate_thread.stop()
        self.asks_refresh_thread.stop()
        self.completed_transactions_thread.stop()

        if self.own_asks_thread.is_alive():
            self.own_asks_thread.join()
        if self.populate_thread.is_alive():
            self.populate_thread.join()
        if self.asks_refresh_thread.is_alive():
            self.asks_refresh_thread.join()
        if self.completed_transactions_thread.is_alive():
            self.completed_transactions_thread.join()

    def depopulate_sell_denarii_screen(self): 
        try: 
            self.lock.acquire()
            
            for artifact in self.current_asks_artifacts: 
                artifact.setVisible(False)
                
            for artifact in self.own_asks_artifacts: 
                artifact.setVisible(False)
                
            for artifact in self.bought_asks_artifacts: 
                artifact.setVisible(False)
            
        finally: 
            self.lock.release()

    def populate_sell_denarii_screen(self):
        while not self.populate_thread.stopped():
            try:
                self.depopulate_sell_denarii_screen()
                self.lock.acquire()

                # First we populate the all asks grid
                row = 1
                new_current_asks_artifacts = []
                for ask in self.current_asks:
                    ask_amount_label = Label(str(ask["amount"]))
                    font = Font()
                    font.setFamily("Arial")
                    font.setPixelSize(50)
                    ask_amount_label.setFont(font)
                    new_current_asks_artifacts.append(ask_amount_label)

                    self.grid_layout.addWidget(ask_amount_label, row, 0)

                    ask_price_label = Label(str(ask["asking_price"]))
                    font = Font()
                    font.setFamily("Arial")
                    font.setPixelSize(50)
                    ask_price_label.setFont(font)
                    new_current_asks_artifacts.append(ask_price_label)

                    self.grid_layout.addWidget(ask_price_label, row, 1)
                    row += 1
                
                self.current_asks_artifacts = new_current_asks_artifacts

                # Then we populate the own asks grid
                row = 1
                new_own_asks_artifacts = []
                for ask in self.own_asks:
                    ask_amount_label = Label(str(ask["amount"]))
                    font = Font()
                    font.setFamily("Arial")
                    font.setPixelSize(50)
                    ask_amount_label.setFont(font)
                    new_own_asks_artifacts.append(ask_amount_label)

                    self.second_grid_layout.addWidget(ask_amount_label, row, 0)

                    ask_price_label = Label(str(ask["asking_price"]))
                    font = Font()
                    font.setFamily("Arial")
                    font.setPixelSize(50)
                    ask_price_label.setFont(font)
                    new_own_asks_artifacts.append(ask_price_label)

                    self.second_grid_layout.addWidget(ask_price_label, row, 1)

                    cancel_ask_push_button = PushButton("Cancel Ask", self.parent)
                    cancel_ask_push_button.clicked.connect(
                        lambda: self.on_cancel_ask_clicked(str(ask["ask_id"]))
                    )
                    cancel_ask_push_button.setVisible(True)
                    cancel_ask_push_button.setStyleSheet(
                        "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
                    )
                    new_own_asks_artifacts.append(cancel_ask_push_button)

                    self.second_grid_layout.addWidget(cancel_ask_push_button, row, 2)

                    row += 1
                
                self.own_asks_artifacts = new_own_asks_artifacts

                # Lastly we populate the bought asks grid
                row = 1
                new_bought_asks_artifacts = []
                for ask in self.bought_asks:
                    ask_amount_label = Label(str(ask["amount"]))
                    font = Font()
                    font.setFamily("Arial")
                    font.setPixelSize(50)
                    ask_amount_label.setFont(font)
                    new_bought_asks_artifacts.append(ask_amount_label)

                    self.third_grid_layout.addWidget(ask_amount_label, row, 0)

                    ask_price_label = Label(str(ask["asking_price"]))
                    font = Font()
                    font.setFamily("Arial")
                    font.setPixelSize(50)
                    ask_price_label.setFont(font)
                    new_bought_asks_artifacts.append(ask_price_label)

                    self.third_grid_layout.addWidget(ask_price_label, row, 1)

                    amount_bought_label = Label(str(ask["amount_bought"]))
                    font = Font()
                    font.setFamily("Arial")
                    font.setPixelSize(50)
                    amount_bought_label.setFont(font)
                    new_bought_asks_artifacts.append(amount_bought_label)

                    self.third_grid_layout.addWidget(amount_bought_label, row, 2)

                    row += 1
                self.bought_asks_artifacts = new_bought_asks_artifacts

            finally:
                self.lock.release()

            time.sleep(1)

    def refresh_all_prices(self):
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
                print(f"Refresh all prices {e}")
                
            time.sleep(5)

    def refresh_completed_transactions(self):
        while not self.completed_transactions_thread.stopped():
            try:
                self.lock.acquire()

                (
                    success,
                    res,
                ) = self.denarii_mobile_client.poll_for_completed_transaction(
                    self.gui_user.user_id
                )

                if success:
                    ask_ids_settled = []
                    for ask in res:
                        ask_ids_settled.append(ask["ask_id"])

                    new_bought_asks = []
                    for ask in self.bought_asks:
                        if ask["ask_id"] not in ask_ids_settled:
                            new_bought_asks.append(ask)
                        else:
                            self.send_money_to_seller(ask)

                    self.bought_asks = new_bought_asks

            except Exception as e:
                print(f"Refresh completed transactins {e}")
                
            finally:
                self.lock.release()
            time.sleep(5)

    def refresh_asks_in_escrow(self):
        while not self.refresh_asks_in_escrow_thread.stopped():
            try:
                self.lock.acquire()

                success, res = self.denarii_mobile_client.poll_for_escrowed_transaction(self.gui_user.user_id)

                if success: 
                    self.bought_asks = res
                    
            except Exception as e:
                print(f"Refresh asks in escrow {e}")
            finally:
                self.lock.release()

            time.sleep(5)

    def refresh_own_asks(self):
        while not self.own_asks_thread.stopped():
            try:
                self.lock.acquire()

                success, res = self.denarii_mobile_client.get_all_asks(self.gui_user.user_id)

                if success: 
                    self.own_asks = res

            except Exception as e:
                print(f"Refresh own asks {e}")
            finally:
                self.lock.release()

            time.sleep(5)
            
    def refresh_going_price(self): 
        while not self.refresh_going_price_thread.stopped():
            try:
                self.lock.acquire()
                
                # Just a big number since python doesnt really have a max int
                going_price = 99999999999999999
                for ask in self.current_asks: 
                    if going_price > ask["asking_price"]: 
                        going_price = ask["asking_price"] 

                self.going_price_label(f"Going Price: {going_price}")

            except Exception as e:
                print(f"Refresh going price {e}")
            finally:
                self.lock.release()

            time.sleep(5)

    def on_submit_clicked(self):
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
                    make_success, _ = self.denarii_mobile_client.make_denarii_ask(self.gui_user.user_id, self.amount_line_edit.text(), self.price_line_edit.text())

                    if make_success: 
                        self.status_message_box("Created denarii ask!")
                    else: 
                        self.status_message_box("Failed to create denarii ask")
                else: 
                    self.status_message_box("Failed to create denarii ask because the user either didn't have credit card info or wasnt verified")
            
            else: 
                self.status_message_box("Failed to create denarii ask because we couldn't determine if the user had credit card info or was verified")


        except Exception as e:
            print(f"On submit clicked {e}")
            self.status_message_box("Failed: unknown error")

        finally:
            self.lock.release()

    def on_cancel_ask_clicked(self, ask_id_to_cancel):
        try: 
            success, _ = self.denarii_mobile_client.cancel_ask(self.gui_user.user_id, ask_id_to_cancel)

            if success: 
                self.status_message_box("Cancelled ask!")
            else: 
                self.status_message_box("Failed to cancel ask")
        except Exception as e:
            print(f"On cancel ask clicked {e}")
            self.status_message_box("Failed: unknown error")

    def send_money_to_seller(self, ask):
        try: 
            # TODO use a different currency when applicable
            success, _ = self.denarii_mobile_client.send_money_to_seller(self.gui_user.user_id, ask['amount_bought'], "usd")

            if success: 
                # Do nothing so we don't bother the user
                pass
            else: 
                self.completely_reverse_transaction([ask])

        except Exception as e:
            print(f"Send money to seller {e}")

    def completely_reverse_transaction(self, ask_to_reverse):
        """
        Transfers denarii back to seller, and sends money back to buyer
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
            print(f"Completely reverse transaction {e}")
            self.status_message_box("Failed: unknown error")

    def reverse_transactions(self, asks_to_reverse):
        """
        Sends money back to buyer
        """
        for ask in asks_to_reverse:
            try:
                success = self.denarii_mobile_client.send_money_back_to_buyer(
                    self.gui_user.user_id, ask["amount_bought"], "usd"
                )

                if success:
                    pass
                else:
                    self.status_message_box(
                        f"Failed to send money back to buyer for ask: {ask['ask_id']}. Copy that down and file a support ticket."
                    )

            except Exception as e:
                print(f"Reverse transactions {e}")
                self.status_message_box("Failed: unknown error")
