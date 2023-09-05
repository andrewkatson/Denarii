import json
import requests


class DenariiMobileClient:
    def __init__(self):
        self.denarii_mobile_users_endpoint = "https://denariimobilebackend.com"

    def send_denarii_mobile_request(self, method, params):
        return self.send_request(
            self.denarii_mobile_users_endpoint, "10003", method, params
        )

    def send_request(self, ip, port, method, params):
        """
        Send a command to the specified ip address and port
        @param ip The ip to send to
        @param port The port to use
        @param method The rpc method to call
        @param params The params to pass the rpc method
        @return The json representing the response
        """
        # Empty json if there is no result
        res = json.dumps({})
        ok = False
        try:
            inputs = {
                "params": params,
                "jsonrpc": "2.0",
                "id": 0,
            }
            print("Sending " + str(inputs))
            res = requests.post(
                f"{ip}:{port}/users/{method}/",
                data=json.dumps(inputs),
                headers={"content-type": "application/json"},
            )
            ok = res.ok
        except Exception as e:
            print("Ran into problem sending request " + str(e))

        try:
            print("Received " + str(res))
            res = res.json()
            print(str(res))
        except Exception as e:
            print("Ran into problem with the response " + str(e))

        return res, ok

    def get_user_id(self, username, email, password):
        """
        @return a list of special response objects that have a single field
        'user_identifier' and whether the request succeeded
        """
        params = {"username": username, "email": email, "password": password}

        res, ok = self.send_denarii_mobile_request("get_user_id", params)

        if not ok:
            return False, []
        else:
            return True, res

    def reset_password(self, username, email, password):
        """
        @return whether the request succeeded or not
        """
        params = {"username": username, "email": email, "password": password}

        _, ok = self.send_denarii_mobile_request("reset_password", params)

        return ok

    def request_reset(self, username_or_email):
        """
        @return whether the request succeeded or not
        """
        params = {"username_or_email": username_or_email}

        _, ok = self.send_denarii_mobile_request("request_reset", params)

        return ok

    def verify_reset(self, username_or_email, reset_id):
        """
        @return whether the request succeeded or not
        """
        params = {"username_or_email": username_or_email, "reset_id": reset_id}

        _, ok = self.send_denarii_mobile_request("verify_reset", params)

        return ok

    def create_wallet(self, user_id, wallet_name, password):
        """
        @return a list of special response objects that have the fields 'seed' and 'wallet_address'
        """
        params = {"user_id": user_id, "wallet_name": wallet_name, "password": password}

        res, ok = self.send_denarii_mobile_request("create_wallet", params)

        if not ok:
            return False, []
        else:
            return True, res

    def restore_wallet(self, user_id, wallet_name, password, seed):
        """
        @return a list of special response objects that have a single field 'wallet_address'
        """
        params = {
            "user_id": user_id,
            "wallet_name": wallet_name,
            "password": password,
            "seed": seed,
        }

        res, ok = self.send_denarii_mobile_request("restore_wallet", params)

        if not ok:
            return False, []
        else:
            return True, res

    def open_wallet(self, user_id, wallet_name, password):
        """
        @return a list of special response objects that have a single field 'user_identifier'
        """
        params = {"user_id": user_id, "wallet_name": wallet_name, "password": password}

        res, ok = self.send_denarii_mobile_request("open_wallet", params)

        if not ok:
            return False, []
        else:
            return True, res

    def get_balance(self, user_id, wallet_name):
        """
        @return a list of special response objects that have a single field 'balance'
        """
        params = {"user_id": user_id, "wallet_name": wallet_name}

        res, ok = self.send_denarii_mobile_request("get_balance", params)

        if not ok:
            return False, []
        else:
            return True, res

    def send_denarii(self, user_id, wallet_name, address, amount):
        """
        @return whether the request succeeded or not
        """
        params = {
            "user_id": user_id,
            "wallet_name": wallet_name,
            "address": address,
            "amount": amount,
        }

        _, ok = self.send_denarii_mobile_request("send_denarii", params)

        if not ok:
            return False
        else:
            return True

    def get_prices(self, user_id):
        """
        @return a list of special response objects that have the fields 'ask_id', 'asking_price', and 'amount'
        """
        params = {"user_id": user_id}

        res, ok = self.send_denarii_mobile_request("get_prices", params)

        if not ok:
            return False, []
        else:
            return True, res

    def buy_denarii(
        self,
        user_id,
        amount,
        bid_price,
        buy_regardless_of_price,
        fail_if_full_amount_isnt_met,
    ):
        """
        @return a list of special response objects that have a single field 'ask_id'
        """

        params = {
            "user_id": user_id,
            "amount": amount,
            "bid_price": bid_price,
            "buy_regardless_of_price": buy_regardless_of_price,
            "fail_if_full_amount_isnt_met": fail_if_full_amount_isnt_met,
        }

        res, ok = self.send_denarii_mobile_request("buy_denarii", params)

        if not ok:
            return False, []
        else:
            return True, res

    def transfer_denarii(self, user_id, ask_id):
        """
        @return a list of special response objects that have the fields 'ask_id', and 'amount_bought'
        """

        params = {"user_id": user_id, "ask_id": ask_id}

        res, ok = self.send_denarii_mobile_request("transfer_denarii", params)

        if not ok:
            return False, []
        else:
            return True, res

    def make_denarii_ask(self, user_id, amount, asking_price):
        """
        @return a list of special response objects that have the fields 'ask_id', 'asking_price', and 'amount'
        """

        params = {"user_id": user_id, "amount": amount, "asking_price": asking_price}

        res, ok = self.send_denarii_mobile_request("make_denarii_ask", params)

        if not ok:
            return False, []
        else:
            return True, res

    def poll_for_completed_transaction(self, user_id):
        """
        @return a list of special response objects that have the fields 'ask_id', 'asking_price', and 'amount'
        """

        params = {"user_id": user_id}

        res, ok = self.send_denarii_mobile_request(
            "poll_for_completed_transaction", params
        )

        if not ok:
            return False, []
        else:
            return True, res

    def cancel_ask(self, user_id, ask_id):
        """
        @return a list of special response objects that have a single field 'ask_id'
        """

        params = {"user_id": user_id, "ask_id": ask_id}

        res, ok = self.send_denarii_mobile_request("cancel_ask", params)

        if not ok:
            return False, []
        else:
            return True, res

    def has_credit_card_info(self, user_id):
        """
        @return a list of special response objects that have a single field 'has_credit_card_info'
        """

        params = {
            "user_id": user_id,
        }

        res, ok = self.send_denarii_mobile_request("has_credit_card_info", params)

        if not ok:
            return False, []
        else:
            return True, res

    def set_credit_card_info(
        self,
        user_id,
        card_number,
        expiration_date_month,
        expiration_date_year,
        security_code,
    ):
        """
        @return whether the request succeeded or not
        """

        params = {
            "user_id": user_id,
            "card_number": card_number,
            "expiration_date_month": expiration_date_month,
            "expiration_date_year": expiration_date_year,
            "security_code": security_code,
        }

        _, ok = self.send_denarii_mobile_request("set_credit_card_info", params)

        return ok

    def clear_credit_card_info(self, user_id):
        """
        @return whether the request succeeded or not
        """

        params = {"user_id": user_id}

        _, ok = self.send_denarii_mobile_request("clear_credit_card_info", params)

        return ok

    def get_money_from_buyer(self, user_id, amount, currency):
        """
        @return whether the request succeeded or not
        """

        params = {"user_id": user_id, "amount": amount, "currency": currency}

        _, ok = self.send_denarii_mobile_request("get_money_from_buyer", params)

        return ok

    def send_money_to_seller(self, user_id, amount, currency):
        """
        @return whether the request succeeded or not
        """
        params = {"user_id": user_id, "amount": amount, "currency": currency}

        _, ok = self.send_denarii_mobile_request("send_money_to_seller", params)

        return ok

    def is_transaction_settled(self, user_id, ask_id):
        """
        @return a list of special response objects that have the fields 'transaction_was_settled' and 'ask_id'
        """

        params = {"user_id": user_id, "ask_id": ask_id}

        res, ok = self.send_denarii_mobile_request("is_transaction_settled", params)

        if not ok:
            return False, []
        else:
            return True, res

    def delete_user(self, user_id):
        """
        @return whether the request succeeded or not
        """

        params = {"user_id": user_id}

        _, ok = self.send_denarii_mobile_request("delete_user", params)

        return ok

    def get_ask_with_identifier(self, user_id, ask_id):
        """
        @return a list of special response objects that have the fields 'ask_id', 'amount', and 'amount_bought'
        """

        params = {"user_id": user_id, "ask_id": ask_id}

        res, ok = self.send_denarii_mobile_request("get_ask_with_identifier", params)

        if not ok:
            return False, []
        else:
            return True, res

    def transfer_denarii_back_to_seller(self, user_id, ask_id):
        """
        @return a list of response objects that have the field 'ask_id'
        """

        params = {"user_id": user_id, "ask_id": ask_id}

        res, ok = self.send_denarii_mobile_request(
            "transfer_denarii_back_to_seller", params
        )

        if not ok:
            return False, []
        else:
            return True, res

    def send_money_back_to_buyer(self, user_id, amount, currency):
        """
        @return  whethe the request succeeded or not
        """

        params = {"user_id": user_id, "amount": amount, "currency": currency}

        _, ok = self.send_denarii_mobile_request("send_money_back_to_buyer", params)

        return ok

    def cancel_buy_of_ask(self, user_id, ask_id):
        """
        @return whether the request succeeded or not
        """

        params = {"user_id": user_id, "ask_id": ask_id}

        _, ok = self.send_denarii_mobile_request("cancel_buy_of_ask", params)

        return ok

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
        """
        @return a list of response objects that have the field 'verification_status'
        """

        params = {
            "user_id": user_id,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "email": email,
            "dob": dob,
            "ssn": ssn,
            "zipcode": zipcode,
            "phone": phone,
            "work_locations": work_locations,
        }

        res, ok = self.send_denarii_mobile_request("verify_identity", params)

        if not ok:
            return False, []
        else:
            return True, res

    def is_a_verified_person(self, user_id):
        """
        @return a list of response objects that have the field 'verification_status'
        """

        params = {"user_id": user_id}

        res, ok = self.send_denarii_mobile_request("is_a_verified_person", params)

        if not ok:
            return False, []
        else:
            return True, res

    def get_all_asks(self, user_id):
        """
        @return a list of response objects that have the fields 'ask_id', 'amount', 'asking_price', amount_bought'
        """

        params = {
            "user_id": user_id,
        }

        res, ok = self.send_denarii_mobile_request("get_all_asks", params)

        if not ok:
            return False, []
        else:
            return True, res
        
    def get_all_buys(self, user_id):
        """
        @return a list of response objects that have the fields 'ask_id', 'amount', 'asking_price', amount_bought'
        """

        params = {
            "user_id": user_id,
        }

        res, ok = self.send_denarii_mobile_request("get_all_buys", params)

        if not ok:
            return False, []
        else:
            return True, res

    def create_support_ticket(self, user_id):
        """
        @return a list of response objects that have the fields 'support_ticket_id' and 'creation_time_body'
        """

        params = {"user_id": user_id}

        res, ok = self.send_denarii_mobile_request("create_support_ticket", params)

        if not ok:
            return False, []
        else:
            return True, res

    def update_support_ticket(self, user_id, support_ticket_id, comment):
        """
        @return a list of response objects that have the fields 'support_ticket_id', 'updated_time_body'
        """

        params = {
            "user_id": user_id,
            "support_ticket_id": support_ticket_id,
            "comment": comment,
        }

        res, ok = self.send_denarii_mobile_request("update_support_ticket", params)

        if not ok:
            return False, []
        else:
            return True, res

    def delete_support_ticket(self, user_id, support_ticket_id):
        """
        @return a list of response objects that have the field 'support_ticket_id'
        """

        params = {"user_id": user_id, "support_ticket_id": support_ticket_id}

        res, ok = self.send_denarii_mobile_request("delete_support_ticket", params)

        if not ok:
            return False, []
        else:
            return True, res

    def get_support_tickets(self, user_id, can_be_resolved):
        """
        @return a list of response objects that have the fields 'support_ticket_id', 'author', 'title', 'description', 'updated_time_body', 'creation_time_body', 'resolved'
        """

        params = {"user_id": user_id, "can_be_resolved": can_be_resolved}

        res, ok = self.send_denarii_mobile_request("get_support_tickets", params)

        if not ok:
            return False, []
        else:
            return True, res

    def get_comments_on_ticket(self, user_id, support_ticket_id):
        """
        @return a list of response objects that have the fields 'author', 'content', 'updated_time_body', 'creation_time_body'
        """

        params = {"user_id": user_id, "support_ticket_id": support_ticket_id}

        res, ok = self.send_denarii_mobile_request("get_comments_on_ticket", params)

        if not ok:
            return False, []
        else:
            return True, res

    def resolve_support_tickets(self, user_id, support_ticket_id):
        """
        @return a list of response objects that have the fields 'support_ticket_id', and 'updated_time_body'
        """

        params = {"user_id": user_id, "support_ticket_id": support_ticket_id}

        res, ok = self.send_denarii_mobile_request("resolve_support_ticket", params)

        if not ok:
            return False, []
        else:
            return True, res

    def poll_for_escrowed_transaction(self, user_id):
        """
        @return a list of response objects that have the fields 'ask_id', 'amount', 'asking_price', and 'amount_bought'
        """

        params = {"user_id": user_id}

        res, ok = self.send_denarii_mobile_request("poll_for_escrowed_transaction", params)

        if not ok: 
            return False, []
        else: 
            return True, res

    def get_support_ticket(self, user_id, support_ticket_id):
        """
        @return a list of response objects that have the fields 'support_ticket_id', 'author', 'title', 'description', 'updated_time_body', 'creation_time_body', 'resolved'
        """


        params = {"user_id": user_id, "support_ticket_id": support_ticket_id}

        res, ok = self.send_denarii_mobile_request("get_support_ticket", params)

        if not ok:
            return False, []
        else:
            return True, res
