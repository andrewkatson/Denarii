import datetime
import os
import pathlib
import pickle as pkl
import random
import requests
import string

from constants import *

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.splitlines()

used_identifiers = []


def generate_phrase(num_words):
    list_of_words = random.choices(WORDS, k=num_words)
    list_of_strings = [word.decode("utf8") for word in list_of_words]
    return " ".join(list_of_strings)


def generate_address(num_letters):
    list_of_letters = random.choices(string.ascii_letters, k=num_letters)
    return "".join(list_of_letters)


def store(thing, suffix):
    if TESTING:
        print(f"Testing so we are not going to store anything for suffix {suffix}")
    else:
        path = pathlib.Path(f"{TEST_STORE_PATH}/{thing.name}.{suffix}")
        with open(path, "wb") as output_file:
            pkl.dump(thing, output_file)


def store_user(user):
    store(user, "user")


def delete(thing, suffix):
    if TESTING:
        print(f"Testing so we are not going to delete anything for suffix {suffix}")
    else:
        path = pathlib.Path(f"{TEST_STORE_PATH}/{thing.name}.{suffix}")
        if os.path.exists(path):
            os.remove(path)


def delete_user(user):
    delete(user, "user")


def load(path):
    thing = None
    with open(path, "rb") as input_file:
        thing = pkl.load(input_file)
    return thing


def generate_random_ask():
    return DenariiAsk(random.uniform(1, 10000), random.uniform(1, 1000))


def generate_random_asks(num_asks):
    asks = []
    for i in range(num_asks):
        asks.append(generate_random_ask())
    return asks


def generate_balance():
    return random.uniform(2, 1000)


def load_all_test_things():
    things = {}

    dict_of_users = {}

    first_user = User("FIRST_USER", "firstuser@email.com", "password")
    first_user.user_id = create_identifier()

    dict_of_users["FIRST_USER"] = first_user

    user_with_wallet = User(
        "USER_WITH_WALLET", "userwithwallet@email.com", "other_password"
    )
    user_with_wallet.wallet = Wallet(
        "USER_WITH_WALLET_WALLET",
        "not_creative",
        generate_phrase(4),
        generate_address(15),
        float(100),
    )
    user_with_wallet.user_id = create_identifier()
    dict_of_users["USER_WITH_WALLET"] = user_with_wallet

    user_with_an_ask = User("USER_WITH_AN_ASK", "user@email.com", "ahhhh")
    # If a user is going to be part of the ask flow they need a wallet
    user_with_an_ask.wallet = Wallet(
        "MY_WALLET", "something", generate_phrase(4), generate_address(15), generate_balance()
    )
    user_with_an_ask.asks = generate_random_asks(1)
    # If a user is going to be part of the ask flow they need a credit card
    user_with_an_ask.credit_card = CreditCard("123", "2", "1992", "234")
    user_with_an_ask.user_id = create_identifier()
    dict_of_users["USER_WITH_AN_ASK"] = user_with_an_ask

    user_with_multiple_asks = User(
        "USER_WITH_MULTIPLE_ASKS", "other_email@email.com", "yeahhh"
    )
    # If a user is going to be part of the ask flow they need a wallet
    user_with_multiple_asks.wallet = Wallet(
        "THIS_WALLET", "party", generate_phrase(4), generate_address(15), generate_balance()
    )
    user_with_multiple_asks.user_id = create_identifier()
    user_with_multiple_asks.asks = generate_random_asks(10)
    # If a user is going to be part of the ask flow they need a credit card
    user_with_multiple_asks.credit_card = CreditCard("424", "1", "1902", "777")
    dict_of_users["USER_WITH_MULTIPLE_ASKS"] = user_with_multiple_asks

    things["user"] = dict_of_users

    return things


def load_all_things():
    things = {}

    if TESTING:
        things = load_all_test_things()
    else:
        users = {}
        for path in os.listdir(TEST_STORE_PATH):
            full_path = os.path.join(TEST_STORE_PATH, path)

            if os.path.isfile(full_path):
                if ".user" in path:
                    split = path.split(".user")
                    user_name = split[0]
                    users[user_name] = load(full_path)

        things["user"] = users
    return things


def create_identifier():
    new_identifier = 1

    while new_identifier in used_identifiers:

        new_identifier = round(random.uniform(0, 1000))

    used_identifiers.append(new_identifier)
    return new_identifier


def try_to_buy_denarii(
        asks,
        to_buy_amount,
        bid_price,
        buy_regardless_of_price,
        fail_if_full_amount_isnt_met,
):
    assert type(to_buy_amount) == float
    assert type(bid_price) == float

    asks.sort(key=lambda x: x.asking_price)

    current_bought_amount = 0
    amount_to_buy_left = to_buy_amount
    current_ask_price = bid_price
    asks_met = []
    for ask in asks:

        current_ask_price = ask.asking_price

        if not buy_regardless_of_price and current_ask_price > bid_price:
            if fail_if_full_amount_isnt_met:
                for reprocessed_ask in asks:
                    reprocessed_ask.in_escrow = False
                    reprocessed_ask.amount_bought = 0

            return False, "Asking price was higher than bid price", asks_met

        ask.in_escrow = True

        if ask.amount > amount_to_buy_left:
            ask.amount_bought = amount_to_buy_left
        else:
            ask.amount_bought = ask.amount

        current_bought_amount += ask.amount_bought
        amount_to_buy_left -= ask.amount_bought

        asks_met.append(ask)

        if current_bought_amount >= to_buy_amount:
            return True, None, asks_met

    return False, "Reached end of asks so not enough was bought", asks_met


class User:
    def __init__(self, name, email, password):
        assert name is not None
        assert email is not None
        assert password is not None
        self.name = name
        self.email = email
        self.password = password
        self.user_id = None
        self.reset_requested = False
        self.reset_id = -1
        self.wallet = None
        self.asks = []
        self.credit_card = None
        self.support_tickets = []
        self.report_id = -1
        self.verification_report_status = "never_run"
        self.identity_is_verified = False
        self.creation_time = datetime.datetime.now()
        self.updated_time = datetime.datetime.now()

    def __str__(self) -> str:
        return f"{self.user_id} {self.name} {self.email} {self.wallet} {self.credit_card} {self.asks}"


class Wallet:
    def __init__(self, name, password, seed=None, address=None, balance=0):
        assert type(balance) == float
        self.name = name
        self.password = password
        self.seed = seed
        self.address = address
        self.balance = balance
        self.creation_time = datetime.datetime.now()
        self.updated_time = datetime.datetime.now()

    def __str__(self) -> str:
        return f"{self.name} {self.seed} {self.address} {self.balance}"


class DenariiAsk:
    def __init__(self, asking_price, amount):
        self.asking_price = asking_price
        assert type(self.asking_price) == float
        self.amount = amount
        self.in_escrow = False
        self.ask_id = -1
        self.amount_bought = 0
        self.is_settled = False
        self.has_been_seen_by_seller = False
        self.creation_time = datetime.datetime.now()
        self.updated_time = datetime.datetime.now()
        self.buyer = None

    def __str__(self) -> str:
        return f"{self.ask_id}: {self.amount} {self.asking_price} {self.amount_bought}"


class CreditCard:
    def __init__(
            self, card_number, expiration_date_month, expiration_date_year, security_code
    ):
        self.card_number = card_number
        self.expiration_date_month = expiration_date_month
        self.expiration_date_year = expiration_date_year
        self.security_code = security_code
        self.balance = random.uniform(1, 100)
        assert type(self.balance) == float
        self.creation_time = datetime.datetime.now()
        self.updated_time = datetime.datetime.now()

    def __str__(self) -> str:
        return f"{self.card_number}"


class SupportTicket:
    def __init__(self, description, title, resolved) -> None:
        self.description = description
        self.title = title
        self.resolved = resolved
        self.comments = []
        self.support_ticket_id = round(random.uniform(1, 100))
        self.creation_time = datetime.datetime.now()
        self.updated_time = datetime.datetime.now()


class SupportTicketComment:
    def __init__(self, author, content) -> None:
        self.author = author
        self.content = content
        self.creation_time = datetime.datetime.now()
        self.updated_time = datetime.datetime.now()
        self.comment_id = str(random.uniform(1, 100))


class DenariiMobileClient:
    def __init__(self):
        self.things = load_all_things()

        self.user = None

    def has_remaining_asks(self, user_id):

        for _, user in self.get_users().items():
            if user.user_id == user_id:
                for ask in user.asks:
                    if ask.is_settled or ask.in_escrow:
                        return True
        return False

    def has_remaining_buys(self, user_id):
        for _, user in self.get_users().items():
            if user.user_id != user_id:
                for ask in user.asks:
                    if ask.buyer is not None and ask.buyer.user_id == user_id:
                        return True
        return False

    def get_users(self):
        return self.things.get("user", {})

    def dump_users(self):
        for _, user in self.get_users().items():
            print(f"USER DUMP {user}")

    def get_asks(self, user):
        asks = []
        for _, value in self.get_users().items():
            if value.user_id != user.user_id:
                for ask in value.asks:
                    asks.append(ask)

        return asks

    def get_user_with_ask(self, ask_id):
        for _, value in self.get_users().items():
            for ask in value.asks:
                if ask.ask_id == ask_id:
                    return value

        raise ValueError("That ask id corresponds to no user")

    def get_ask_with_id(self, user, ask_id):
        for ask in user.asks:
            if ask.ask_id == ask_id:
                return ask
        raise ValueError("There is no ask with that id for the given user")

    def get_ask_with_just_id(self, ask_id):
        for _, user in self.get_users().items():
            for ask in user.asks:
                if ask.ask_id == ask_id:
                    return ask
        raise ValueError("There is no ask with that id for any user")

    def get_support_ticket_with_id(self, user, support_ticket_id):
        for ticket in user.support_tickets:
            if ticket.support_ticket_id == support_ticket_id:
                return ticket
        raise ValueError(
            f"That support ticket id correspond to no ticket for the given user {support_ticket_id}"
        )

    def get_remaining_asks(self, asks, ask_id):
        remaining_asks = []

        for other_ask in asks:
            if other_ask.ask_id != ask_id:
                remaining_asks.append(other_ask)

        return remaining_asks

    def get_user_with_id(self, id):
        users = self.get_users()
        for _, value in users.items():
            if value.user_id == id:
                return value
        raise ValueError("No user with id")

    def check_user_is_current_user_and_get(self, user_id):
        if self.user is None:
            print("Need to set a user before doing the current action")
            return None

        user = self.get_user_with_id(user_id)

        if user.user_id != self.user.user_id:
            print("That user is not the current user")
            return None

        return user

    def get_address_for_name(self, name):
        for _, user in self.get_users().items():
            if user.wallet is None:
                continue
            if user.wallet.name == name:
                return user.wallet.address
        return ""

    def get_user_with_address(self, address):
        for _, user in self.get_users().items():

            if user.wallet is None:
                continue

            if type(address) == bytes and user.wallet.address == address.decode('utf-8'):
                return user
            elif type(address) == str and user.wallet.address == address:
                return user
            elif str(address) == user.wallet.address:
                return user
        raise ValueError("No user with wallet address")

    def get_user_id(self, username, email, password):
        users = self.get_users()
        for _, value in users.items():
            # Login if they exist
            if (
                    value.name == username
                    and value.password == password
                    and value.email == email
            ):
                self.user = value
                return True, [{"user_id": self.user.user_id}]
            # If they are a known user but their password doesnt match fail
            elif (
                    value.name == username
                    and value.email == email
                    and value.password != password
            ):
                return False, []
                # If they are a known user but their email doesnt match fail
            elif value.name == username and value.email != email:
                return False, []
        # If all else fails create the user (register)
        self.user = User(username, email, password)
        self.user.user_id = create_identifier()
        users[username] = self.user
        store_user(self.user)
        return True, [{"user_id": self.user.user_id}]

    def reset_password(self, username, email, password):
        users = self.get_users()

        if len(users) == 0:
            print("There are no users to reset the password of")
            return False

        for key, value in users.items():
            if key == username:
                if value.email == email:
                    value.password = password
                    store_user(value)
                    return True
        return False

    def request_reset(self, username_or_email):
        users = self.get_users()

        if len(users) == 0:
            print("There are no users to request a reset of their password")
            return False

        for _, value in users.items():
            if value.name == username_or_email or value.email == username_or_email:
                value.reset_requested = True
                # We need a static reset identifier for testing
                if TESTING:
                    value.reset_id = 4
                else:
                    value.reset_id = create_identifier()
                store_user(value)
                return True
        return False

    def verify_reset(self, username_or_email, reset_id):
        users = self.get_users()

        if len(users) == 0:
            return False

        for _, value in users.items():
            if value.name == username_or_email or value.email == username_or_email:
                if value.reset_requested and value.reset_id == int(reset_id):
                    value.reset_requested = False
                    value.reset_id = -1
                    store_user(value)
                    return True
        return False

    def create_wallet(self, user_id, wallet_name, password):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        if user.wallet is not None:
            print(f"Tried to create a user wallet and it was not None {user.name} {user.wallet.name}")
            return False, []

        user.wallet = Wallet(wallet_name, password, balance=generate_balance())
        user.wallet.seed = generate_phrase(4)
        user.wallet.address = generate_address(15)
        store_user(user)

        return True, [{"seed": user.wallet.seed, "wallet_address": user.wallet.address}]

    def restore_wallet(self, user_id, wallet_name, password, seed):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        if user.wallet is None:
            return False, []

        if (
                user.wallet.name == wallet_name
                and user.wallet.password == password
                and user.wallet.seed == seed
        ):
            return True, [{"wallet_address": user.wallet.address}]

        return False, []

    def open_wallet(self, user_id, wallet_name, password):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        if user.wallet is None:
            return False, []

        if user.wallet.name == wallet_name and user.wallet.password == password:
            return True, [
                {"wallet_address": user.wallet.address, "seed": user.wallet.seed}
            ]

        return False, []

    def get_balance(self, user_id, wallet_name):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        if user.wallet is None:
            return False, []
        return True, [{"balance": user.wallet.balance}]

    def send_denarii(self, user_id, wallet_name, address, amount):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        if user.wallet.name == wallet_name:
            if user.wallet.balance >= float(amount):
                user.wallet.balance -= float(amount)
                receiving_user = self.get_user_with_address(address)
                receiving_user.wallet.balance += float(amount)
                store_user(receiving_user)
                store_user(user)
                return True

        return False

    def get_prices(self, user_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        asks = self.get_asks(user)

        filtered_asks = []

        for ask in asks:
            filtered_asks.append(
                {
                    "ask_id": ask.ask_id,
                    "amount": ask.amount,
                    "asking_price": ask.asking_price,
                }
            )

        return True, filtered_asks

    def buy_denarii(
            self,
            user_id,
            amount,
            bid_price,
            buy_regardless_of_price,
            fail_if_full_amount_isnt_met,
    ):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        asks = self.get_asks(user)

        _, error_message, asks_met = try_to_buy_denarii(
            asks,
            float(amount),
            float(bid_price),
            buy_regardless_of_price,
            fail_if_full_amount_isnt_met,
        )

        if len(asks_met) == 0:
            return False, []

        filtered_asks = []
        for ask in asks_met:
            ask.buyer = user
            filtered_asks.append({"ask_id": ask.ask_id})

        return True, filtered_asks

    def transfer_denarii(self, user_id, ask_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        asking_user = self.get_user_with_ask(ask_id)

        ask = self.get_ask_with_id(asking_user, ask_id)

        user.wallet.balance = float(user.wallet.balance)
        asking_user.wallet.balance = float(asking_user.wallet.balance)

        if float(user.wallet.balance) < float(ask.amount_bought):
            return False, []

        asking_user.wallet.balance += float(ask.amount_bought)

        user.wallet.balance -= float(ask.amount_bought)

        amount_bought = float(ask.amount_bought)

        ask.amount -= float(ask.amount_bought)
        ask.amount_bought = 0
        ask.in_escrow = False
        ask.buyer = None
        ask.is_settled = True

        store_user(asking_user)
        store_user(user)

        return True, [{"ask_id": ask.ask_id, "amount_bought": amount_bought}]

    def make_denarii_ask(self, user_id, amount, asking_price):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        ask = DenariiAsk(float(asking_price), float(amount))
        ask.ask_id = create_identifier()

        user.asks.append(ask)

        store_user(user)

        return True, [
            {"ask_id": ask.ask_id, "amount": amount, "asking_price": asking_price}
        ]

    def poll_for_completed_transaction(self, user_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        filtered_asks = []
        for ask in user.asks:
            if ask.is_settled:
                ask.has_been_seen_by_seller = True
                filtered_asks.append(
                    {
                        "ask_id": ask.ask_id,
                        "asking_price": ask.asking_price,
                        "amount": ask.amount,
                    }
                )
        store_user(user)
        return True, filtered_asks

    def cancel_ask(self, user_id, ask_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        user.asks = self.get_remaining_asks(user.asks, ask_id)

        return True, [{"ask_id": ask_id}]

    def has_credit_card_info(self, user_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        return True, [{"has_credit_card_info": user.credit_card is not None}]

    def set_credit_card_info(
            self,
            user_id,
            card_number,
            expiration_date_month,
            expiration_date_year,
            security_code,
    ):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False

        if user.credit_card is not None:
            return False

        user.credit_card = CreditCard(
            card_number, expiration_date_month, expiration_date_year, security_code
        )

        store_user(user)

        return True

    def clear_credit_card_info(self, user_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False

        if user.credit_card is None:
            return False

        user.credit_card = None

        store_user(user)

        return True

    def get_money_from_buyer(self, user_id, amount, currency):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False

        user.credit_card.balance = float(user.credit_card.balance)

        if float(user.credit_card.balance) < float(amount):
            return False

        user.credit_card.balance -= float(amount)
        store_user(user)
        return True

    def send_money_to_seller(self, user_id, amount, currency):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False

        user.credit_card.balance += amount
        store_user(user)

        return True

    def is_transaction_settled(self, user_id, ask_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        asking_user = self.get_user_with_ask(ask_id)

        ask = self.get_ask_with_id(asking_user, ask_id)

        if not ask.is_settled or not ask.has_been_seen_by_seller:
            return True, [{"ask_id": ask_id, "transaction_was_settled": False}]

        if ask.amount == 0:
            asking_user.asks = self.get_remaining_asks(asking_user.asks, ask_id)
        else:
            ask.is_settled = False
            ask.has_been_seen_by_seller = False

        store_user(asking_user)
        return True, [{"ask_id": ask_id, "transaction_was_settled": True}]

    def delete_user(self, user_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        if self.has_remaining_asks(user_id) or self.has_remaining_buys(user_id):
            return False, []

        users = self.get_users()

        final_users = {}

        deleted_something = False
        for key, value in users.items():
            if value.user_id == user_id:
                deleted_something = True
                delete_user(value)
            else:
                final_users[key] = value

        self.things["user"] = final_users

        return deleted_something

    def get_ask_with_identifier(self, user_id, ask_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        ask = self.get_ask_with_just_id(ask_id)

        return True, [
            {
                "ask_id": ask.ask_id,
                "amount": ask.amount,
                "amount_bought": ask.amount_bought,
            }
        ]

    def transfer_denarii_back_to_seller(self, user_id, ask_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        asking_user = self.get_user_with_ask(ask_id)

        ask = self.get_ask_with_id(asking_user, ask_id)

        user.wallet.balance = float(user.wallet.balance)
        asking_user.wallet.balance = float(asking_user.wallet.balance)

        if float(asking_user.wallet.balance) < float(ask.amount_bought):
            return False, []

        user.wallet.balance += float(ask.amount_bought)

        asking_user.wallet.balance -= float(ask.amount_bought)

        ask.amount += float(ask.amount_bought)
        ask.amount_bought = 0
        ask.in_escrow = False
        ask.buyer = None
        ask.is_settled = False

        store_user(asking_user)
        store_user(user)

        return True, [{"ask_id": ask.ask_id}]

    def send_money_back_to_buyer(self, user_id, amount, currency):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False

        user.credit_card.balance += amount
        store_user(user)
        return True

    def cancel_buy_of_ask(self, user_id, ask_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False

        ask = self.get_ask_with_just_id(ask_id)

        ask.in_escrow = False
        ask.amount_bought = 0
        ask.buyer = None

        store_user(user)
        return True

    def verify_identity(
            self,
            user_id,
            first_name,
            middle_name,
            last_name,
            email,
            dob,
            ssn,
            zipcode,
            phone,
            work_locations,
    ):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        user.identity_is_verified = True
        user.verification_report_status = "complete"

        store_user(user)

        return True, [{"verification_status": "is_verified"}]

    def is_a_verified_person(self, user_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        if user.identity_is_verified:
            return True, [{"verification_status": "is_verified"}]
        elif (
                not user.identity_is_verified
                and user.verification_report_status == "complete"
        ):
            return True, [{"verification_status": "failed_verification"}]
        elif user.verification_report_status == "pending":
            return True, [{"verification_status": "verification_pending"}]
        else:
            return True, [{"verification_status": "is_not_verified"}]

    def get_all_asks(self, user_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        filtered_asks = []

        for ask in user.asks:
            filtered_asks.append(
                {
                    "ask_id": ask.ask_id,
                    "amount": ask.amount,
                    "asking_price": ask.asking_price,
                    "amount_bought": ask.amount_bought,
                }
            )

        return True, filtered_asks

    def get_all_buys(self, user_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        filtered_asks = []

        for ask in self.get_asks(user):
            if ask.in_escrow and user.user_id == ask.buyer.user_id:
                filtered_asks.append(
                    {
                        "ask_id": ask.ask_id,
                        "amount": ask.amount,
                        "asking_price": ask.asking_price,
                        "amount_bought": ask.amount_bought,
                    }
                )

        return True, filtered_asks

    def create_support_ticket(self, user_id, title, description):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        support_ticket = SupportTicket(description, title, False)

        user.support_tickets.append(support_ticket)

        return True, [
            {
                "support_ticket_id": support_ticket.support_ticket_id,
                "creation_time_body": support_ticket.creation_time.isoformat(),
            }
        ]

    def update_support_ticket(self, user_id, support_ticket_id, comment):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        comment = SupportTicketComment(user.name, comment)

        ticket = self.get_support_ticket_with_id(user, support_ticket_id)

        ticket.comments.append(comment)

        return True, [
            {
                "support_ticket_id": support_ticket_id,
                "updated_time_body": comment.updated_time.isoformat(),
                "comment_id": comment.comment_id
            }
        ]

    def delete_support_ticket(self, user_id, support_ticket_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        remaining_tickets = []

        for ticket in user.support_tickets:
            if ticket.support_ticket_id != support_ticket_id:
                remaining_tickets.append(ticket)

        user.support_tickets = remaining_tickets

        store_user(user)

        return True, [{"support_ticket_id": support_ticket_id}]

    def get_support_tickets(self, user_id, can_be_resolved):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        filtered_support_tickets = []

        for ticket in filtered_support_tickets:
            if ticket.resolved and can_be_resolved:
                filtered_support_tickets.append(
                    {
                        "support_ticket_id": ticket.support_ticket_id,
                        "author": user.name,
                        "title": ticket.title,
                        "description": ticket.description,
                        "updated_time_body": ticket.updated_time.isoformat(),
                        "creation_time_body": ticket.creation_time.isoformat(),
                        "resolved": "True",
                    }
                )
            elif not ticket.resolved:
                filtered_support_tickets.append(
                    {
                        "support_ticket_id": ticket.support_ticket_id,
                        "author": user.name,
                        "title": ticket.title,
                        "description": ticket.description,
                        "updated_time_body": ticket.updated_time.isoformat(),
                        "creation_time_body": ticket.creation_time.isoformat(),
                        "resolved": "False",
                    }
                )

        return True, filtered_support_tickets

    def get_comments_on_ticket(self, user_id, support_ticket_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        ticket = self.get_support_ticket_with_id(user, support_ticket_id)

        filtered_comments = []

        for comment in ticket.comments:
            filtered_comments.append(
                {
                    "author": comment.author,
                    "content": comment.content,
                    "updated_time_body": comment.updated_time.isoformat(),
                    "creation_time_body": comment.creation_time.isoformat(),
                }
            )

        return True, filtered_comments

    def resolve_support_ticket(self, user_id, support_ticket_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        ticket = self.get_support_ticket_with_id(user, support_ticket_id)

        ticket.resolved = True

        store_user(user)

        return True, [
            {
                "support_ticket_id": support_ticket_id,
                "updated_time_body": ticket.updated_time.isoformat(),
            }
        ]

    def poll_for_escrowed_transaction(self, user_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        filtered_asks = []
        for ask in user.asks:
            if not ask.is_settled and ask.in_escrow:
                filtered_asks.append(
                    {
                        "ask_id": ask.ask_id,
                        "asking_price": ask.asking_price,
                        "amount": ask.amount,
                        "amount_bought": ask.amount_bought,
                    }
                )
        return True, filtered_asks

    def get_support_ticket(self, user_id, support_ticket_id):
        user = self.check_user_is_current_user_and_get(user_id)

        if user is None:
            return False, []

        filtered_support_tickets = []

        for ticket in user.support_tickets:
            if ticket.support_ticket_id == support_ticket_id:
                filtered_support_tickets.append(
                    {
                        "support_ticket_id": ticket.support_ticket_id,
                        "author": user.name,
                        "title": ticket.title,
                        "description": ticket.description,
                        "updated_time_body": ticket.updated_time.isoformat(),
                        "creation_time_body": ticket.creation_time.isoformat(),
                    }
                )

        return True, filtered_support_tickets

    def logout(self, user_id):
        user = self.check_user_is_current_user_and_get(user_id)
        if user is None:
            return False, []
        else:
            self.user = None
            return True, []
