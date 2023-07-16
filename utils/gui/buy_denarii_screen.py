import threading
import time

from screen import *
from stoppable_thread import StoppableThread

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
        **kwargs
    ):
        self.remote_wallet_screen_push_button = None
        self.sell_screen_push_button = None
        self.credit_card__info_screen_push_button = None
        self.buy_denarii_label = None
        self.submit_push_button = None
        self.amount_line_edit = None
        self.price_line_edit = None
        self.amount_label = None
        self.price_label = None
        self.asks_label = None
        self.amount_col_label = None
        self.price_col_label = None
        self.amount_bought_col_label = None
        self.queued_buys_label = None
        self.buy_regardless_of_price_radio_button = None 
        self.dont_buy_regardless_or_price_radio_button = None 
        self.fail_if_full_amount_cant_be_bought_radio_button = None
        self.succeed_even_when_full_amount_cant_be_bought_radio_button = None
        self.buy_regardless_of_price_label = None 
        self.fail_if_full_amount_isnt_met_label = None

        self.buy_regardless_of_price = False
        self.fail_if_full_amount_isnt_met = True

        self.current_asks = []
        self.queued_buys = []

        self.keep_refreshing_prices = False

        self.asks_refresh_thread = StoppableThread(target=self.refresh_prices)

        self.keep_refreshing_settled_transactions = False

        self.settled_transactions_thread = StoppableThread(
            target=self.refresh_settled_transactions
        )

        self.current_asks_lock = threading.Lock()
        self.queued_buys_lock = threading.Lock()

        super().__init__(
            self.buy_denarii_screen_name,
            main_layout=main_layout,
            deletion_func=deletion_func,
            denarii_client=denarii_client,
            gui_user=gui_user,
            denarii_mobile_client=denarii_mobile_client,
            **kwargs
        )

    def init(self, **kwargs):
        super().init(**kwargs)

        self.next_button.setVisible(False)
        self.back_button.setVisible(False)

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

        self.credit_card_info_screen_push_button = PushButton("Credit Card", kwargs["parent"])
        self.credit_card_info_screen_push_button.clicked.connect(
            lambda: kwargs["on_credit_card_info_screen_clicked"]()
        )
        self.credit_card_info_screen_push_button.setVisible(False)
        self.credit_card_info_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.submit_push_button = PushButton("Submit", kwargs["parent"])
        self.submit_push_button.clicked.connect(lambda: self.on_submit_clicked())
        self.submit_push_button.setVisible(False)
        self.submit_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.amount_label = Label("Amount: ")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.amount_label.setFont(font)

        self.price_label = Label("Price: ")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.price_label.setFont(font)

        self.amount_line_edit = LineEdit()
        self.price_line_edit = LineEdit()

        self.asks_label = Label("Asks")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.asks_label.setFont(font)

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

        self.fail_if_full_amount_isnt_met_label = Label("Fail if Full Amount Cannot Be Bought")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.fail_if_full_amount_isnt_met_label.setFont(font)

        self.buy_regardless_of_price_radio_button = RadioButton(
            "True", kwargs["parent"], buy_regardless_of_price_callback=self.set_buy_regardless_or_price
        )
        self.buy_regardless_of_price_radio_button.toggled.connect(
            self.buy_regardless_of_price_radio_button.on_buy_regardless_of_price_clicked
        )
        self.buy_regardless_of_price_radio_button.buy_regardless_of_price_option = True
        self.buy_regardless_of_price_radio_button.setVisible(False)
        self.buy_regardless_of_price_radio_button.setStyleSheet(
            "QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};"
        )

        self.dont_buy_regardless_or_price_radio_button = RadioButton(
            "False", kwargs["parent"], buy_regardless_of_price_callback=self.set_buy_regardless_or_price
        )
        self.dont_buy_regardless_or_price_radio_button.toggled.connect(
            self.dont_buy_regardless_or_price_radio_button.on_wallet_type_clicked
        )
        self.dont_buy_regardless_or_price_radio_button.buy_regardless_of_price_option = False
        self.dont_buy_regardless_or_price_radio_button.setChecked(True)
        self.dont_buy_regardless_or_price_radio_button.setVisible(False)
        self.dont_buy_regardless_or_price_radio_button.setStyleSheet(
            "QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};"
        )

        self.fail_if_full_amount_cant_be_bought_radio_button = RadioButton(
            "True", kwargs["parent"], wallet_type_callback=self.set_fail_if_full_amount_isnt_met
        )
        self.fail_if_full_amount_cant_be_bought_radio_button.toggled.connect(
            self.fail_if_full_amount_cant_be_bought_radio_button.on_fail_if_full_amount_isnt_met
        )
        self.fail_if_full_amount_cant_be_bought_radio_button.fail_if_full_amount_isnt_met_option = True
        self.fail_if_full_amount_cant_be_bought_radio_button.setChecked(True)
        self.fail_if_full_amount_cant_be_bought_radio_button.setVisible(False)
        self.fail_if_full_amount_cant_be_bought_radio_button.setStyleSheet(
            "QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};"
        )

        self.succeed_even_when_full_amount_cant_be_bought_radio_button = RadioButton(
            "False", kwargs["parent"], wallet_type_callback=self.set_fail_if_full_amount_isnt_met
        )
        self.succeed_even_when_full_amount_cant_be_bought_radio_button.toggled.connect(
            self.succeed_even_when_full_amount_cant_be_bought_radio_button.on_fail_if_full_amount_isnt_met
        )
        self.succeed_even_when_full_amount_cant_be_bought_radio_button.fail_if_full_amount_isnt_met_option = False
        self.succeed_even_when_full_amount_cant_be_bought_radio_button.setVisible(False)
        self.succeed_even_when_full_amount_cant_be_bought_radio_button.setStyleSheet(
            "QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};"
        )

    def setup(self):
        super().setup()

        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)
        self.main_layout.addLayout(self.fourth_horizontal_layout)
        self.main_layout.addLayout(self.fifth_horizontal_layout)
        self.main_layout.addLayout(self.sixth_horizontal_layout)
        self.main_layout.addLayout(self.seventh_horizontal_layout)
        self.main_layout.addLayout(self.eight_horizontal_layout)
        self.main_layout.addLayout(self.ninth_horizontal_layout)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addLayout(self.tenth_horizontal_layout)
        self.main_layout.addLayout(self.second_grid_layout)
        self.main_layout.addLayout(self.eleventh_horizontal_layout)

        self.remote_wallet_screen_push_button.setVisible(True)
        self.sell_screen_push_button.setVisible(True)
        self.submit_push_button.setVisible(True)
        self.fail_if_full_amount_cant_be_bought_radio_button.setVisible(True)
        self.succeed_even_when_full_amount_cant_be_bought_radio_button.setVisible(True)
        self.buy_regardless_of_price_radio_button.setVisible(True)
        self.dont_buy_regardless_or_price_radio_button.setVisible(True)

        self.first_horizontal_layout.addWidget(
            self.buy_denarii_label, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.amount_label, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(
            self.amount_line_edit, alignment=AlignCenter
        )
        self.third_horizontal_layout.addWidget(self.price_label, alignment=AlignCenter)
        self.third_horizontal_layout.addWidget(
            self.price_line_edit, alignment=AlignCenter
        )
        self.fourth_horizontal_layout.addWidget(
            self.submit_push_button, alignment=AlignCenter
        )
        self.fifth_horizontal_layout.addWidget(self.asks_label, alignment=AlignCenter)
        self.sixth_horizontal_layout.addWidget(self.buy_regardless_of_price_label, alignment=AlignCenter)
        self.seventh_horizontal_layout.addWidget(self.buy_regardless_of_price_radio_button, alignment=AlignCenter)
        self.seventh_horizontal_layout.addWidget(self.dont_buy_regardless_or_price_radio_button, alignment=AlignCenter)
        self.eight_horizontal_layout.addWidget(self.fail_if_full_amount_isnt_met_label, alignment=AlignCenter)
        self.ninth_horizontal_layout.addWidget(self.fail_if_full_amount_cant_be_bought_radio_button, alignment=AlignCenter)
        self.ninth_horizontal_layout.addWidget(self.succeed_even_when_full_amount_cant_be_bought_radio_button, alignment=AlignCenter)
        self.grid_layout.addWidget(self.amount_col_label, 0, 0)
        self.grid_layout.addWidget(self.price_col_label, 0, 1)
        self.tenth_horizontal_layout.addWidget(
            self.queued_buys_label, alignment=AlignCenter
        )
        self.second_grid_layout.addWidget(self.amount_col_label, 0, 0)
        self.second_grid_layout.addWidget(self.price_col_label, 0, 1)
        self.second_grid_layout.addWidget(self.amount_bought_col_label, 0, 2)
        self.eleventh_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )
        self.eleventh_horizontal_layout.addWidget(
            self.remote_wallet_screen_push_button, alignment=AlignCenter
        )
        self.eleventh_horizontal_layout.addWidget(
            self.sell_screen_push_button, alignment=AlignCenter
        )
        self.eleventh_horizontal_layout.addWidget(
            self.credit_card__info_screen_push_button, alignment=AlignCenter
        )

        self.keep_refreshing_prices = True
        self.keep_refreshing_settled_transactions = True

        self.asks_refresh_thread.start()
        self.settled_transactions_thread.start()

        self.populate_buy_denarii_screen()

    def teardown(self):
        super().teardown()

        self.keep_refreshing_prices = False
        self.keep_refreshing_settled_transactions = False

    def on_submit_clicked(self):
        """
        Attempt to buy some denarii asks and set them in queued_buys. Then get money from the buyer (i.e. schedule it to be transferred). Then have the denarii be transferred over.
        """

        try: 
            self.current_asks_lock.acquire()
            self.queued_buys_lock.acquire()

            success, first_res = self.denarii_mobile_client.has_credit_card_info(self.gui_user.user_id)

            if success: 
                has_credit_card_info = first_res[0]["has_credit_card_info"]

                if has_credit_card_info:
                    
                    success, second_res = self.denarii_mobile_client.buy_denarii(self.gui_user.user_id, self.amount_line_edit.text(), self.price_line_edit.text(), self.buy_regardless_of_price, self.fail_if_full_amount_isnt_met)

                    if success: 
                        
                        # TODO: change to use other currencies.
                        success, third_res = self.denarii_mobile_client.get_money_from_buyer(self.gui_user.user_id, self.amount_line_edit.text(), "usd")
                        
                        if success:
                            
                            succeeded_asks = []
                            for ask in second_res:

                                success, fourth_res = self.denarii_mobile_client.transfer_denarii(self.gui_user.user_id, ask['ask_id'])

                                if success: 
                                    current_ask = self.get_current_ask(ask['ask_id'])
                                    self.queued_buys.append({'ask_id': ask['ask_id'], 'amount_bought': fourth_res[0]['amount_bought'], 'amount': current_ask['amount']})
                                    succeeded_asks.append(ask['ask_id'])
                                else: 
                                    self.status_message_box("Failed one of the denarii transfers. Will refund money and transfer denarii back to seller.")
                                    self.reverse_transaction(succeeded_asks)
                                    break

                            else: 
                                self.status_message_box("Failed to get your money to transfer the denarii")
                    else: 
                        self.status_message_box("Failed to buy denarii")

                else: 
                    self.status_message_box("Failed to buy denarii because there was no credit card info on file")
            else: 
                self.status_message_box("Failed to buy denarii because we could not determine if there was credit card info")


        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

        finally: 
            self.current_asks_lock.release()
            self.queued_buys_lock.release()

    def populate_buy_denarii_screen(self):
        """
        Get every amount + price pair and populate the grid layout with them for asks and queued buys.
        """

        # First we populate the asks grid
        row = 1
        self.current_asks_lock.acquire()
        for ask in self.current_asks:
            ask_amount_label = Label(str(ask["amount"]))
            font = Font()
            font.setFamily("Arial")
            font.setPixelSize(50)
            ask_amount_label.setFont(font)

            self.grid_layout.addWidget(ask_amount_label, row, 0)

            ask_price_label = Label(str(ask["asking_price"]))
            font = Font()
            font.setFamily("Arial")
            font.setPixelSize(50)
            ask_price_label.setFont(font)

            self.grid_layout.addWidget(ask_price_label, row, 1)

            row += 1
        self.current_asks_lock.release()

        # Then we populate the queued asks grid (which are just asks that we are buying)
        row = 1
        self.queued_buys_lock.acquire()
        for buy in self.queued_buys:
            ask_amount_label = Label(str(buy["amount"]))
            font = Font()
            font.setFamily("Arial")
            font.setPixelSize(50)
            ask_amount_label.setFont(font)

            self.grid_layout.addWidget(ask_amount_label, row, 0)

            ask_price_label = Label(str(buy["asking_price"]))
            font = Font()
            font.setFamily("Arial")
            font.setPixelSize(50)
            ask_price_label.setFont(font)

            self.grid_layout.addWidget(ask_price_label, row, 1)

            amount_bought_label = Label(str(buy["amount_bought"]))
            font = Font()
            font.setFamily("Arial")
            font.setPixelSize(50)
            amount_bought_label.setFont(font)

            self.grid_layout.addWidget(amount_bought_label, row, 2)

            row += 1
        self.queued_buys_lock.release()

    def refresh_prices(self):
        while self.keep_refreshing_prices:
            time.sleep(5)

            try:
                success, res = self.denarii_mobile_client.get_prices(
                    self.gui_user.user_id
                )

                if success:
                    self.current_asks_lock.acquire()
                    self.current_asks = res
                    self.current_asks_lock.release()
                    # No status message when things go well on purpose so the user doesn't get annoyed.
                else:
                    self.status_message_box("Failed to get denarii asks")
            except Exception as e:
                print(e)
                self.status_message_box("Failed: unknown error")

    def refresh_settled_transactions(self):
        
        while self.keep_refreshing_settled_transactions:
            time.sleep(5)

            try: 
                self.queued_buys_lock.acquire()
                ask_ids_to_remove = []
                
                # Check to see what buys are settled
                for buy in self.queued_buys:
                    success, res = self.denarii_mobile_client.is_transaction_settled(self.gui_user.user_id, buy['ask_id'])

                    if success: 
                        was_settled = res[0]['transaction_was_settled']

                        if was_settled: 
                            ask_ids_to_remove.append(buy['ask_id'])


                # Remove the ones that are settled
                new_queued_buys = []
                for buy in self.queued_buys: 

                    if buy['ask_id'] not in ask_ids_to_remove: 
                        new_queued_buys.append(buy)

                self.queued_buys = new_queued_buys


            except Exception as e: 
                print(e)
                self.status_message_box("Failed: unknown error")
            finally:
                self.queued_buys_lock.release()

    def set_fail_if_full_amount_isnt_met(self, fail_if_full_amount_isnt_met):
        self.fail_if_full_amount_isnt_met = fail_if_full_amount_isnt_met

    def set_buy_regardless_or_price(self, buy_regardless_of_price):
        self.buy_regardless_of_price = buy_regardless_of_price

    def get_current_ask(self, ask_id):

        for ask in self.current_asks:

            if ask['ask_id'] == ask_id:
                return ask

        # If we can't find the current ask with the ask id then just return a -1 amount since we know how much was bought
        # TODO: change to an API call that grabs the ask with this id
        return {'amount': -1}
    
    def reverse_transaction(self, asks_ids_to_reverse):
        # TODO: add in two API calls here to first transfer denarii back to affected sellers then refund the buyer.
        pass
