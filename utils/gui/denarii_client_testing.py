"""
Class that emulates a denarii_client for testing.
"""

import os
import pathlib
import pickle as pkl
import random
import requests
import string
import time

from constants import *
from stoppable_thread import StoppableThread

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
WORDS = response.content.splitlines()


def generate_phrase(num_words):
    list_of_words = random.choices(WORDS, k=num_words)
    list_of_strings = [word.decode("utf8") for word in list_of_words]
    return " ".join(list_of_strings)


def generate_address(num_letters):
    list_of_letters = random.choices(string.ascii_letters, k=num_letters)
    return "".join(list_of_letters)


def store_wallet(wallet):
    if TESTING:
        print(f"Not writing {wallet.name} to a file since this is a test")
    else:
        path = pathlib.Path(f"{TEST_STORE_PATH}/{wallet.name}.wallet")
        with open(path, "wb") as output_file:
            pkl.dump(wallet, output_file)


def load_wallet(wallet_path):
    wallet = None
    with open(wallet_path, "rb") as input_file:
        wallet = pkl.load(input_file)

    return wallet

def delete_wallet(wallet):
    if TESTING:
        print(f"Not deleting {wallet.name} file since this is a test")
    else:
        path = pathlib.Path(f"{TEST_STORE_PATH}/{wallet.name}.wallet")
        if os.path.exists(path):
            os.remove(path)


def load_all_test_wallets():
    wallets = {}

    wallets["FIRST_USER"] = TestingWallet("FIRST_USER", "PASSWORD", generate_phrase(4))
    wallets["WITH_SUB_ADDRESSES"] = TestingWallet(
        "WITH_SUB_ADDRESSES",
        "OTHER_PASSWORD",
        generate_phrase(4),
        sub_addresses=[generate_address(15), generate_address(15)],
    )

    return wallets


def load_all_wallets():
    wallets = {}

    if TESTING:
        return load_all_test_wallets()
    else:
        for path in os.listdir(TEST_STORE_PATH):
            full_path = os.path.join(TEST_STORE_PATH, path)

            if os.path.isfile(full_path):
                if ".wallet" in path:
                    split = path.split(".wallet")
                    wallet_name = split[0]
                    wallets[wallet_name] = load_wallet(full_path)

        return wallets


class TestingWallet:
    def __init__(self, name, password, seed="", sub_addresses=None):
        self.name = name
        self.password = password
        self.seed = seed
        self.address = generate_address(15)
        # We make the balance 2 so that we can transfer some money.
        self.balance = 2.0 / 0.000000000001
        if sub_addresses is None:
            sub_addresses = []
        self.sub_addresses = sub_addresses

        self.mining_thread = None
        self.keep_mining = False


class DenariiClient:
    def __init__(self, wallets=None):
        if wallets is None:
            wallets = {}
        self.wallets = wallets

        for name, wallet in load_all_wallets().items():
            self.wallets[name] = wallet

        self.opened_wallet = None
        self.mining_thread = None

    def get_address_for_name(self, name): 
        for username, wallet in self.wallets.items(): 
            if username == name:
                return wallet.address
        return ""

    def create_wallet(self, wallet):
        if wallet.name in self.wallets:
            return False


        seed = generate_phrase(4)
        self.wallets[wallet.name] = TestingWallet(
            wallet.name, wallet.password, seed=seed
        )

        wallet.phrase = seed

        store_wallet(self.wallets[wallet.name])

        self.opened_wallet = self.wallets[wallet.name]
        return True

    def restore_wallet(self, wallet):
        if wallet.name in self.wallets:
            existing_wallet = self.wallets.get(wallet.name)
            if wallet.password == existing_wallet.password:
                if wallet.phrase == existing_wallet.seed:
                    wallet.address = existing_wallet.address
                    store_wallet(existing_wallet)
                    self.opened_wallet = existing_wallet
                    return True
        return False

    def get_address(self, wallet):
        if wallet.name in self.wallets:
            wallet.address = self.wallets.get(wallet.name).address
            return True

        wallet.address = generate_address(15)
        existing_wallet = self.wallets.get(wallet.name)
        existing_wallet.address = wallet.address
        return True

    def transfer_money(self, amount, sender, receiver):
        if sender.name in self.wallets:
            existing_wallet = self.wallets.get(sender.name)
            if existing_wallet.balance >= amount:
                existing_wallet.balance -= amount
                store_wallet(existing_wallet)
                return True
            return False
        return False

    def get_balance_of_wallet(self, wallet):
        if wallet.name in self.wallets:
            return self.wallets.get(wallet.name).balance
        return 0.0

    def set_current_wallet(self, wallet):
        if wallet.name in self.wallets:
            existing_wallet = self.wallets.get(wallet.name)
            if existing_wallet.password == wallet.password:
                self.opened_wallet = existing_wallet
                store_wallet(self.opened_wallet)
                return True
            return False
        return False

    def query_seed(self, wallet):
        if wallet.name in self.wallets:
            wallet.phrase = self.wallets.get(wallet.name).seed
            return True
        return False

    def create_no_label_address(self, wallet):
        if wallet.name in self.wallets:
            new_sub_address = generate_address(15)
            wallet.sub_addresses.append(new_sub_address)

            existing_wallet = self.wallets[wallet.name]
            existing_wallet.sub_addresses.append(new_sub_address)

            store_wallet(existing_wallet)
            return True

        return False

    def start_mining(self, do_background_mining, ignore_battery, threads):
        self.mining_thread = StoppableThread(target=self.mine)
        self.mining_thread.start()
        return True

    def stop_mining(self):
        store_wallet(self.opened_wallet)
        if self.mining_thread is not None:
            self.mining_thread.stop()
            if self.mining_thread.is_alive():
                self.mining_thread.join()
        else:
            return False
        return True

    def mine(self):
        while not self.mining_thread.stopped():
            time.sleep(1)

            self.opened_wallet.balance += random.uniform(1.0, 100.0) / 0.000000000001

            store_wallet(self.opened_wallet)

    def logout(self): 
        """
        Just used by the testing application to log the user out.
        @return True
        """
        self.opened_wallet = None
        return True

    def delete_user(self):
        """
        Just used by the testing application to delete the user
        @return True
        """
        delete_wallet(self.opened_wallet)
        self.opened_wallet = None
        return True
