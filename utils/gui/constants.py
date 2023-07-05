import os
import workspace_path_finder


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
