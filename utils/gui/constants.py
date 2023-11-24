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
