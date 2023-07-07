
class DenariiMobileClient:
    def __init__(self):
        pass

    def get_user_id(self, username, email, password):
        pass

    def reset_password(self, username, email, password):
        pass

    def request_reset(self, username_or_email):
        pass

    def verify_reset(self, username_or_email, reset_id):
        pass

    def create_wallet(self, user_id, wallet_name, password):
        pass

    def restore_wallet(self, user_id, wallet_name, password, seed):
        pass

    def open_wallet(self, user_id, wallet_name, password):
        pass

    def get_balance(self, user_id, wallet_name):
        pass

    def send_denarii(self, user_id, wallet_name, address, amount):
        pass

    def get_prices(self, user_id):
        pass

    def buy_denarii(self, user_id, amount, bid_price, buy_regardless_of_price, fail_if_full_amount_isnt_met):
        pass

    def transfer_denarii(self, user_id, ask_id):
        pass

    def make_denarii_ask(self, user_id, amount, asking_price):
        pass

    def poll_for_completed_transaction(self, user_id):
        pass

    def cancel_ask(self, user_id, ask_id):
        pass

    def has_credit_card_info(self, user_id):
        pass

    def set_credit_card_info(self, user_id, card_number, expiration_date_month, expiration_date_year, security_code):
        pass
    
    def clear_credit_card_info(self, user_id):
        pass

    def get_money_from_buyer(self, user_id, amount, currency):
        pass

    def send_money_to_seller(self, user_id, amount, currency):
        pass

