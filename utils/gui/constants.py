import argparse
import os

import workspace_path_finder

parser = argparse.ArgumentParser(
    prog="Denarii Desktop GUI",
    description="A GUI for users to interact with denarii wallets",
)
optional_grp = parser.add_argument_group(title="Optional")
optional_grp.add_argument(
    "--denarii_debug",
    default=True,
    type=bool,
    help="Whether you want to run in debug mode. Debug mode won't start up denariid or denarii_wallet_rpc_server and "
         "will use a testing denarii client and denarii mobile client that mock out all the calls.",
    required=False,
)
optional_grp.add_argument(
    "--denarii_testing",
    default=True,
    type=bool,
    help="Whether you want to run in test mode. Test mode does not apply to the main gui program and instead applies "
         "to the sub classes. The main thing it does is swap out the buttons and widgets for fake ones.",
    required=False,
)

args, unknown = parser.parse_known_args()

DEBUG = args.denarii_debug
TESTING = args.denarii_testing

USER_SETTINGS_PATH = str(
    workspace_path_finder.find_workspace_path() / "utils" / "gui" / "user_settings.pkl"
)

TEST_STORE_PATH = str(workspace_path_finder.find_workspace_path() / "utils" / "gui")

BACK_BUTTON = "BACK"
NEXT_BUTTON = "NEXT"

REMOTE_WALLET = "REMOTE"
LOCAL_WALLET = "LOCAL"

DENARIID_WALLET_PATH = str(workspace_path_finder.get_home() / "denarii" / "wallet")
if not os.path.exists(DENARIID_WALLET_PATH):
    os.makedirs(DENARIID_WALLET_PATH)


def print_status(text, success):
    """
    Print the status of something
    @param text the text of the something
    @param success whether that thing succeeded
    """
    if success:
        print(text + " succeeded")
    else:
        print(text + " failed")


class HTTP:
    GET = "GET"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    
class Patterns:
    password = r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=_])(?=\S+$).{8,}$"
    double = r"^\d{1,100}[.,]{0,1}\d{0,100}$"
    paragraph_of_chars = r"^[\w \n]{5,3000}$"
    alphanumeric = r"^\w{10,500}$"
    single_letter = r"^[a-zA-Z]{1}$"
    name = r"^[a-zA-Z]{3,100}$"
    currency = r"[a-zA-Z]{3,5}$"
    digits_only = r"^\d{1,100}$"
    slash_date = r"[\d+/]{3,100}$"
    seed = r"^[\w ]{10,1000}$"
    digits_and_dashes = r"^[\d-]{3,100}$"
    phone_number = r"^(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
    alphanumeric_with_spaces = r"^[\w ]{5,100}$"
    email = r"^[^@]+@[^@]+\.[^@]+$"
    uuid4 = r"^[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}\Z$"
    boolean = r"^(?i)(true|false)$"
    json_dict_of_upper_and_lower_case_chars = r"^[\]\[{}:\"\\, a-zA-Z]{2,5000}$"
    reset_id = r"^\d{6}$"


class Params:
    username = "USERNAME"
    email = "EMAIL"
    password = "PASSWORD"
    confirm_password = "CONFIRM_PASSWORD"
    username_or_email = f"{username}_OR_{email}"
    wallet_name = "WALLET_NAME"
    user_id = "USER_ID"
    address = "ADDRESS"
    amount = "AMOUNT"
    bid_price = "BID_PRICE"
    buy_regardless_of_price = "BUY_REGARDLESS_OF_PRICE"
    fail_if_full_amount_isnt_met = "FAIL_IF_FULL_AMOUNT_ISNT_MET"
    ask_id = "ASK_ID"
    asking_price = "ASK_PRICE"
    card_number = "CARD_NUMBER"
    expiration_date_month = "EXPIRATION_DATE_MONTH"
    expiration_date_year = "EXPIRATION_DATE_YEAR"
    security_code = "SECURITY_CODE"
    currency = "CURRENCY"
    first_name = "FIRST_NAME"
    middle_name = "MIDDLE_INITIAL"
    last_name = "LAST_NAME"
    dob = "DATE_OF_BIRTH"
    ssn = "SOCIAL_SECURITY_NUMBER"
    zipcode = "ZIPCODE"
    phone = "PHONE"
    work_locations = "WORK_LOCATIONS"
    title = "TITLE"
    description = "DESCRIPTION"
    support_ticket_id = "SUPPORT_TICKET_ID"
    comment = "COMMENT"
    can_be_resolved = "CAN_BE_RESOLVED"
    seed = "SEED"
    reset_id = "RESET_ID"
