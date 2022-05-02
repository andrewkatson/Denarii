# This is the main file for the Denarii gui.
# It assumes that https://github.com/andrewkatson/KeirosPublic is located at either
# %HOME/denarii or %HOMEDRIVE%%HOMEPATH%/Documents/Github/denarii

import multiprocessing
import pathlib
import pickle as pkl
import psutil
import os
import subprocess
import sys
import time
import workspace_path_finder

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
try:

    # Modify PATH to include the path to where we are so in production we can find all our files.
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))

    # Modify the PATH to include the path to the denarii python client
    sys.path.append(str(workspace_path_finder.find_other_workspace_path("KeirosPublic") / "Client" / "Denarii"))

    import denarii_client

    # Modify the PATH to point to where all of python protos are located that are not nearby in the filesystem
    sys.path.append(str(workspace_path_finder.get_home() / "py_proto"))

    from Security.Proto import identifier_pb2
    from Proto import wallet_pb2

    # Modify the PATH to point to where the gui_user proto is
    sys.path.append(str(workspace_path_finder.find_workspace_path() / "bazel-bin" / "utils" / "gui"))

    from Proto import gui_user_pb2

    gui_user = gui_user_pb2.GuiUser()

    USER_SETTINGS_PATH = str(workspace_path_finder.find_workspace_path() / "utils" / "gui" / "user_settings.pkl")

    MAIN_DENARII_PATH_LINUX = "denariid"

    MAIN_DENARII_PATH_WINDOWS = "denariid.exe"

    DENARIID_PATH_LINUX = str(workspace_path_finder.find_workspace_path() / "utils" / "gui" / "denariid")

    DENARIID_PATH_WINDOWS = str(workspace_path_finder.find_workspace_path() / "utils" / "gui" / "denariid.exe")

    MAIN_DENARII_WALLET_RPC_SERVER_PATH_LINUX = "denarii_wallet_rpc_server"

    MAIN_DENARII_WALLET_RPC_SERVER_PATH_WINDOWS = "denarii_wallet_rpc_server.exe"

    DENARII_WALLET_RPC_SERVER_PATH_LINUX = str(
        workspace_path_finder.find_workspace_path() / "utils" / "gui" / "denarii_wallet_rpc_server")

    DENARII_WALLET_RPC_SERVER_PATH_WINDOWS = str(
        workspace_path_finder.find_workspace_path() / "utils" / "gui" / "denarii_wallet_rpc_server.exe")

    DENARIID_WALLET_PATH = str(workspace_path_finder.get_home() / "denarii" / "wallet")
    if not os.path.exists(DENARIID_WALLET_PATH):
        os.makedirs(DENARIID_WALLET_PATH)


    def store_user():
        with open(USER_SETTINGS_PATH, "wb") as output_file:
            pkl.dump(gui_user.SerializeToString(), output_file)


    def load_user():
        global gui_user

        with open(USER_SETTINGS_PATH, "rb") as input_file:
            gui_user.ParseFromString(pkl.load(input_file))


    class Widget(QWidget):
        def __init__(self, parent):
            super().__init__(parent)

            self.denarii_client = denarii_client.DenariiClient()

            self.denariid = self.setup_denariid()
            
            if self.denariid  is not None:
                print("Denariid started up")
            else:
                print("Denariid was not started or was already active")

            self.denarii_wallet_rpc_server = self.setup_denarii_wallet_rpc_server()
            
            if self.denarii_wallet_rpc_server is not None:
                print("Wallet rpc server started up")
            else:
                print("Wallet rpc server not started up or was already active")
            

            self.next_button = QPushButton("Next Page", self)
            self.next_button.setStyleSheet("color:black")
            self.next_button.setStyleSheet("font-weight: bold")
            self.next_button.setStyleSheet("font-size: 18pt")
            self.next_button.clicked.connect(self.next_clicked)

            self.pick_lang_label = Label("Pick a Language")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.pick_lang_label.setFont(font)

            self.user_info_label = Label("Input Your Information")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.user_info_label.setFont(font)

            self.wallet_info_label = Label("Choose Wallet")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.wallet_info_label.setFont(font)

            self.create_wallet_label = Label("Create Wallet")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.create_wallet_label.setFont(font)

            self.restore_wallet_label = Label("Restore Wallet")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.restore_wallet_label.setFont(font)

            self.set_wallet_label = Label("Set Wallet")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.set_wallet_label.setFont(font)

            self.wallet_info_label = Label("Wallet")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.wallet_info_label.setFont(font)

            self.your_balance_label = Label("Your Balance:")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.your_balance_label.setFont(font)

            self.your_address_label = Label("Your Address:")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.your_address_label.setFont(font)

            self.your_sub_address_label = Label("Your Subaddresses:")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.your_sub_address_label.setFont(font)

            self.wallet_info_text_box = Label("")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.wallet_info_text_box.setFont(font)
            self.wallet_info_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

            self.wallet_save_file_text_box = Label("")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.wallet_save_file_text_box.setFont(font)
            self.wallet_save_file_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

            self.create_wallet_text_box = Label("")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.create_wallet_text_box.setFont(font)

            self.restore_wallet_text_box = Label("")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.restore_wallet_text_box.setFont(font)

            self.set_wallet_text_box = Label("")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.set_wallet_text_box.setFont(font)
            self.set_wallet_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

            self.balance_text_box = Label("")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.balance_text_box.setFont(font)

            self.address_text_box = Label("")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.address_text_box.setFont(font)
            self.address_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)

            self.wallet_info_status_text_box = Label("")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.wallet_info_status_text_box.setFont(font)

            self.wallet_transfer_status_text_box = Label("")
            font = QFont()
            font.setFamily("Arial")
            font.setPixelSize(50)
            self.wallet_transfer_status_text_box.setFont(font)

            self.sub_address_text_boxes = []

            self.english_radio_button = RadioButton("English", self)
            self.english_radio_button.toggled.connect(self.english_radio_button.on_lang_select_clicked)
            self.english_radio_button.language = "English"
            self.english_radio_button.setVisible(False)
            self.english_radio_button.setStyleSheet(
                'QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};')

            self.name_line_edit = QLineEdit()
            self.email_line_edit = QLineEdit()
            self.password_line_edit = QLineEdit()
            self.seed_line_edit = QLineEdit()
            self.address_line_edit = QLineEdit()
            self.amount_line_edit = QLineEdit()

            self.create_wallet_push_button = PushButton("Create wallet", self)
            self.create_wallet_push_button.clicked.connect(self.on_create_wallet_clicked)
            self.create_wallet_push_button.setVisible(False)
            self.create_wallet_push_button.setStyleSheet(
                'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

            self.restore_wallet_push_button = PushButton("Restore wallet", self)
            self.restore_wallet_push_button.clicked.connect(self.on_restore_wallet_pushed)
            self.restore_wallet_push_button.setVisible(False)
            self.restore_wallet_push_button.setStyleSheet(
                'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

            self.set_wallet_push_button = PushButton("Set wallet", self)
            self.set_wallet_push_button.clicked.connect(self.on_set_wallet_pushed)
            self.set_wallet_push_button.setVisible(False)
            self.set_wallet_push_button.setStyleSheet(
                'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

            self.create_wallet_submit_push_button = PushButton("Submit", self)
            self.create_wallet_submit_push_button.clicked.connect(self.on_create_wallet_submit_clicked)
            self.create_wallet_submit_push_button.setVisible(False)
            self.create_wallet_submit_push_button.setStyleSheet(
                'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

            self.restore_wallet_submit_push_button = PushButton("Submit", self)
            self.restore_wallet_submit_push_button.clicked.connect(self.on_restore_wallet_submit_clicked)
            self.restore_wallet_submit_push_button.setVisible(False)
            self.restore_wallet_submit_push_button.setStyleSheet(
                'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

            self.set_wallet_submit_push_button = PushButton("Submit", self)
            self.set_wallet_submit_push_button.clicked.connect(self.on_set_wallet_submit_clicked)
            self.set_wallet_submit_push_button.setVisible(False)
            self.set_wallet_submit_push_button.setStyleSheet(
                'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

            self.transfer_push_button = PushButton("Transfer", self)
            self.transfer_push_button.clicked.connect(self.on_transfer_clicked)
            self.transfer_push_button.setVisible(False)
            self.transfer_push_button.setStyleSheet(
                'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

            self.create_sub_address_push_button = PushButton("Create subaddress", self)
            self.create_sub_address_push_button.clicked.connect(self.on_create_sub_address_clicked)
            self.create_sub_address_push_button.setVisible(False)
            self.create_sub_address_push_button.setStyleSheet(
                'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

            self.start_mining_push_button = PushButton("Start mining", self)
            self.start_mining_push_button.clicked.connect(self.on_start_mining_clicked)
            self.start_mining_push_button.setVisible(False)
            self.start_mining_push_button.setStyleSheet(
                'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

            self.stop_mining_push_button = PushButton("Stop mining", self)
            self.stop_mining_push_button.clicked.connect(self.on_stop_mining_clicked)
            self.stop_mining_push_button.setVisible(False)
            self.stop_mining_push_button.setStyleSheet(
                'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

            self.main_layout = QVBoxLayout()
            self.setLayout(self.main_layout)

            if os.path.exists(USER_SETTINGS_PATH):
                load_user()

            # Widgets
            self.LANG_SELECT = "LangSelect"
            self.USER_INFO = "UserInfo"
            self.WALLET_INFO = "WalletInfo"
            self.CREATE_WALLET = "CreateWallet"
            self.RESTORE_WALLET = "RestoreWallet"
            self.SET_WALLET = "SetWallet"
            self.WALLET_SCENE = "WalletScene"

            # Determine what scene we are on based on what info the stored user has
            if gui_user.language == "" and gui_user.name == "" and not gui_user.HasField("wallet"):
                self.current_widget = self.LANG_SELECT
            elif gui_user.language != "" and gui_user.name == "" and not gui_user.HasField("wallet"):
                self.current_widget = self.USER_INFO
            elif gui_user.language != "" and gui_user.name != "" and not gui_user.HasField("wallet"):
                self.current_widget = self.WALLET_INFO
            else:
                self.current_widget = self.WALLET_SCENE

            self.first_horizontal_layout = QHBoxLayout()
            self.second_horizontal_layout = QHBoxLayout()
            self.third_horizontal_layout = QHBoxLayout()
            self.fourth_horizontal_layout = QHBoxLayout()
            self.fifth_horizontal_layout = QHBoxLayout()
            self.sixth_horizontal_layout = QHBoxLayout()
            self.seventh_horizontal_layout = QHBoxLayout()
            self.eight_horizontal_layout = QHBoxLayout()
            self.vertical_layout = QVBoxLayout()
            self.form_layout = QFormLayout()

            # Add some other layouts depending on the current widget
            if self.current_widget == self.LANG_SELECT:
                self.setup_lang_select_screen()
            elif self.current_widget == self.USER_INFO:
                self.setup_user_info_screen()
            elif self.current_widget == self.WALLET_INFO:
                self.setup_wallet_info_screen()
            elif self.current_widget == self.WALLET_SCENE:
                self.setup_wallet_scene_screen()

            self.parent = parent

            self.success = False

            self.wallet = wallet_pb2.Wallet()

        def already_started_denariid(self):

            for proc in psutil.process_iter():
                if proc.name() == "denariid":
                    return True
                elif proc.name() == "denariid.exe":
                    return True

            return False

        def already_started_denarii_wallet_rpc_server(self):

            for proc in psutil.process_iter():
                if proc.name() == "denarii_wallet_rpc_server":
                    return True
                elif proc.name() == "denarii_wallet_rpc_server.exe":
                    return True

            return False

        def setup_denariid(self):

            if self.already_started_denariid():
                return None

            if os.path.exists(MAIN_DENARII_PATH_LINUX):
                return subprocess.Popen("sudo " + MAIN_DENARII_PATH_LINUX + " --no-igd", shell=True)
            elif os.path.exists(MAIN_DENARII_PATH_WINDOWS):
                return subprocess.Popen("start " + MAIN_DENARII_PATH_WINDOWS + " --no-igd", shell=True)
            elif os.path.exists(DENARIID_PATH_LINUX):
                return subprocess.Popen("sudo " + DENARIID_PATH_LINUX + " --no-igd", shell=True)
            elif os.path.exists(DENARIID_PATH_WINDOWS):
                return subprocess.Popen("start " + DENARIID_PATH_WINDOWS + " --no-igd", shell=True)

            return None

        def setup_denarii_wallet_rpc_server(self):
            if self.already_started_denarii_wallet_rpc_server():
                return None

            if not os.path.exists(DENARIID_WALLET_PATH):
                os.makedirs(DENARIID_WALLET_PATH)

            if os.path.exists(MAIN_DENARII_WALLET_RPC_SERVER_PATH_LINUX):
                return subprocess.Popen(
                    [
                        "sudo " + MAIN_DENARII_WALLET_RPC_SERVER_PATH_LINUX + " --rpc-bind-port=8080" + f" --wallet-dir={DENARIID_WALLET_PATH}" + " --disable-rpc-login"],
                    shell=True)
            elif os.path.exists(MAIN_DENARII_WALLET_RPC_SERVER_PATH_WINDOWS):
                return subprocess.Popen(
                    [
                        "start " + MAIN_DENARII_WALLET_RPC_SERVER_PATH_WINDOWS + " --rpc-bind-port=8080" + f" --wallet-dir={DENARIID_WALLET_PATH}" + " --disable-rpc-login"],
                    shell=True)
            elif os.path.exists(DENARII_WALLET_RPC_SERVER_PATH_LINUX):
                return subprocess.Popen(
                    [
                        "sudo " + DENARII_WALLET_RPC_SERVER_PATH_LINUX + " --rpc-bind-port=8080" + f" --wallet-dir={DENARIID_WALLET_PATH}" + " --disable-rpc-login"],
                    shell=True)
            elif os.path.exists(DENARII_WALLET_RPC_SERVER_PATH_WINDOWS):
                return subprocess.Popen(
                    [
                        "start " + DENARII_WALLET_RPC_SERVER_PATH_WINDOWS + " --rpc-bind-port=8080" + f" --wallet-dir={DENARIID_WALLET_PATH}" + " --disable-rpc-login"],
                    shell=True)

        def shutdown_denariid(self):

            if self.denariid is None:
                return

            self.denariid.terminate()

            # Redundant method of killing
            for proc in psutil.process_iter():
                if proc.name() == "denariid":
                    proc.kill()
                elif proc.name() == "denariid.exe":
                    proc.kill()

        def shutdown_denarii_wallet_rpc_server(self):
            if self.denarii_wallet_rpc_server is None:
                return

            self.denarii_wallet_rpc_server.terminate()

            # Redundant method of killing
            for proc in psutil.process_iter():
                if proc.name() == "denarii_wallet_rpc_server":
                    proc.kill()
                elif proc.name() == "denarii_wallet_rpc_server.exe":
                    proc.kill()

        def setup_lang_select_screen(self):
            """
            Setup the language selection screen
            """
            self.main_layout.addLayout(self.first_horizontal_layout)
            self.main_layout.addLayout(self.second_horizontal_layout)
            self.main_layout.addLayout(self.third_horizontal_layout)

            # Add some text telling the user to select a language
            self.first_horizontal_layout.addWidget(self.pick_lang_label, alignment=Qt.AlignCenter)

            # Add a radio button for the user's language
            self.english_radio_button.setVisible(True)
            self.second_horizontal_layout.addWidget(self.english_radio_button, alignment=Qt.AlignCenter)

            # Add a button to go the next screen
            self.third_horizontal_layout.addWidget(self.next_button, alignment=(Qt.AlignRight | Qt.AlignBottom))

        def setup_user_info_screen(self):
            """
            Setup the user information screen
            """
            # Remove anything on the screen
            self.remove_all_widgets(self.main_layout)

            self.main_layout.addLayout(self.first_horizontal_layout)
            self.main_layout.addLayout(self.form_layout)
            self.main_layout.addLayout(self.second_horizontal_layout)

            self.first_horizontal_layout.addWidget(self.user_info_label, alignment=Qt.AlignCenter)
            self.second_horizontal_layout.addWidget(self.next_button, alignment=(Qt.AlignRight | Qt.AlignBottom))
            self.form_layout.addRow("Name", self.name_line_edit)
            self.form_layout.addRow("Email", self.email_line_edit)

        def setup_wallet_info_screen(self):
            """
            Setup the wallet information screen where the user can choose to create or restore a wallet
            """
            self.remove_all_widgets(self.main_layout)

            self.main_layout.addLayout(self.first_horizontal_layout)
            self.main_layout.addLayout(self.second_horizontal_layout)
            self.main_layout.addLayout(self.third_horizontal_layout)

            self.create_wallet_push_button.setVisible(True)
            self.restore_wallet_push_button.setVisible(True)
            self.set_wallet_push_button.setVisible(True)

            self.first_horizontal_layout.addWidget(self.wallet_info_label, alignment=Qt.AlignCenter)
            self.second_horizontal_layout.addWidget(self.create_wallet_push_button, alignment=Qt.AlignCenter)
            self.second_horizontal_layout.addWidget(self.restore_wallet_push_button, alignment=Qt.AlignCenter)
            self.second_horizontal_layout.addWidget(self.set_wallet_push_button, alignment=Qt.AlignCenter)
            self.third_horizontal_layout.addWidget(self.next_button, alignment=(Qt.AlignRight | Qt.AlignBottom))

        def setup_create_wallet_screen(self):
            """
            Setup the wallet creation screen
            """
            self.remove_all_widgets(self.main_layout)

            self.main_layout.addLayout(self.first_horizontal_layout)
            self.main_layout.addLayout(self.form_layout)
            self.main_layout.addLayout(self.second_horizontal_layout)
            self.main_layout.addLayout(self.third_horizontal_layout)
            self.main_layout.addLayout(self.fourth_horizontal_layout)
            self.main_layout.addLayout(self.fifth_horizontal_layout)
            self.main_layout.addLayout(self.sixth_horizontal_layout)

            self.create_wallet_submit_push_button.setVisible(True)

            self.first_horizontal_layout.addWidget(self.create_wallet_label, alignment=Qt.AlignCenter)
            self.form_layout.addRow("Name", self.name_line_edit)
            self.form_layout.addRow("Password", self.password_line_edit)
            self.second_horizontal_layout.addWidget(self.wallet_info_text_box, alignment=Qt.AlignCenter)
            self.third_horizontal_layout.addWidget(self.wallet_save_file_text_box, alignment=Qt.AlignCenter)
            self.fourth_horizontal_layout.addWidget(self.create_wallet_text_box, alignment=Qt.AlignCenter)
            self.fifth_horizontal_layout.addWidget(self.create_wallet_submit_push_button, alignment=Qt.AlignCenter)
            self.sixth_horizontal_layout.addWidget(self.next_button, alignment=(Qt.AlignRight | Qt.AlignBottom))

        def setup_restore_wallet_screen(self):
            """
            Setup the restore wallet screen
            """
            self.remove_all_widgets(self.main_layout)

            self.main_layout.addLayout(self.first_horizontal_layout)
            self.main_layout.addLayout(self.form_layout)
            self.main_layout.addLayout(self.second_horizontal_layout)
            self.main_layout.addLayout(self.third_horizontal_layout)
            self.main_layout.addLayout(self.fourth_horizontal_layout)
            self.main_layout.addLayout(self.fifth_horizontal_layout)

            self.restore_wallet_submit_push_button.setVisible(True)

            self.first_horizontal_layout.addWidget(self.restore_wallet_label, alignment=Qt.AlignCenter)
            self.form_layout.addRow("Name", self.name_line_edit)
            self.form_layout.addRow("Password", self.password_line_edit)
            self.form_layout.addRow("Seed", self.seed_line_edit)
            self.second_horizontal_layout.addWidget(self.wallet_save_file_text_box, alignment=Qt.AlignCenter)
            self.third_horizontal_layout.addWidget(self.restore_wallet_text_box, alignment=Qt.AlignCenter)
            self.fourth_horizontal_layout.addWidget(self.restore_wallet_submit_push_button, alignment=Qt.AlignCenter)
            self.fifth_horizontal_layout.addWidget(self.next_button, alignment=(Qt.AlignRight | Qt.AlignBottom))

        def setup_set_wallet_screen(self):
            """
            Setup the set wallet screen
            """
            self.remove_all_widgets(self.main_layout)

            self.main_layout.addLayout(self.first_horizontal_layout)
            self.main_layout.addLayout(self.form_layout)
            self.main_layout.addLayout(self.second_horizontal_layout)
            self.main_layout.addLayout(self.third_horizontal_layout)
            self.main_layout.addLayout(self.fourth_horizontal_layout)

            self.set_wallet_submit_push_button.setVisible(True)

            self.first_horizontal_layout.addWidget(self.set_wallet_label, alignment=Qt.AlignCenter)
            self.form_layout.addRow("Name", self.name_line_edit)
            self.form_layout.addRow("Password", self.password_line_edit)
            self.second_horizontal_layout.addWidget(self.set_wallet_text_box, alignment=Qt.AlignCenter)
            self.third_horizontal_layout.addWidget(self.set_wallet_submit_push_button, alignment=Qt.AlignCenter)
            self.fourth_horizontal_layout.addWidget(self.next_button, alignment=(Qt.AlignRight | Qt.AlignBottom))

        def setup_wallet_scene_screen(self):
            """
            Setup the wallet scene where the user can transfer funds and check their own funds
            """
            self.remove_all_widgets(self.main_layout)

            self.main_layout.addLayout(self.first_horizontal_layout)
            self.main_layout.addLayout(self.second_horizontal_layout)
            self.main_layout.addLayout(self.third_horizontal_layout)
            self.main_layout.addLayout(self.fourth_horizontal_layout)
            self.main_layout.addLayout(self.vertical_layout)
            self.main_layout.addLayout(self.fifth_horizontal_layout)
            self.main_layout.addLayout(self.form_layout)
            self.main_layout.addLayout(self.sixth_horizontal_layout)
            self.main_layout.addLayout(self.seventh_horizontal_layout)

            self.transfer_push_button.setVisible(True)
            self.create_sub_address_push_button.setVisible(True)
            self.start_mining_push_button.setVisible(True)
            self.stop_mining_push_button.setVisible(True)
            self.next_button.setVisible(False)

            self.first_horizontal_layout.addWidget(self.wallet_info_label, alignment=Qt.AlignCenter)
            self.second_horizontal_layout.addWidget(self.your_balance_label, alignment=Qt.AlignCenter)
            self.second_horizontal_layout.addWidget(self.balance_text_box, alignment=Qt.AlignCenter)
            self.third_horizontal_layout.addWidget(self.your_address_label, alignment=Qt.AlignCenter)
            self.third_horizontal_layout.addWidget(self.address_text_box, alignment=Qt.AlignCenter)
            self.fourth_horizontal_layout.addWidget(self.your_sub_address_label, alignment=Qt.AlignCenter)
            self.fourth_horizontal_layout.addWidget(self.create_sub_address_push_button, alignment=Qt.AlignCenter)
            self.fifth_horizontal_layout.addWidget(self.wallet_info_status_text_box, alignment=Qt.AlignCenter)
            self.form_layout.addRow("Address", self.address_line_edit)
            self.form_layout.addRow("Amount", self.amount_line_edit)
            self.sixth_horizontal_layout.addWidget(self.transfer_push_button, alignment=Qt.AlignCenter)
            self.seventh_horizontal_layout.addWidget(self.start_mining_push_button, alignment=Qt.AlignCenter)
            self.seventh_horizontal_layout.addWidget(self.stop_mining_push_button, alignment=Qt.AlignCenter)
            self.eight_horizontal_layout.addWidget(self.wallet_transfer_status_text_box, alignment=Qt.AlignCenter)

            self.populate_wallet_screen()

        def populate_wallet_screen(self):
            """
            Populate the wallet scene with user wallet information
            """

            success = False
            balance = 0
            try:
                success = self.denarii_client.get_address(self.wallet)

                balance = self.denarii_client.get_balance_of_wallet(self.wallet)
            except Exception as e:
                print(e)

            if success:
                # We need to adjust the balance because it is in picomonero
                self.balance_text_box.setText(str(balance * 0.000000000001))
                self.address_text_box.setText(str(self.wallet.address))

                # Add all the subaddresses to the vertical layout
                for sub_address in self.wallet.sub_addresses:
                    sub_address_text_box = Label(str(sub_address))
                    font = QFont()
                    font.setFamily("Arial")
                    font.setPixelSize(50)
                    sub_address_text_box.setFont(font)
                    sub_address_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
                    self.vertical_layout.addWidget(sub_address_text_box, alignment=Qt.AlignCenter)
                    self.sub_address_text_boxes.append(sub_address_text_box)

                self.wallet_info_status_text_box.setText("Success loading wallet info")
            else:
                self.wallet_info_status_text_box.setText("Failure loading wallet info")

        def remove_all_widgets(self, layout):
            """
            Remove all widgets and layouts
            """
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.remove_all_widgets(item.layout())

        def store_user_info(self):
            """
            Store the user's input information in the user proto
            """
            gui_user.name = self.name_line_edit.text()
            gui_user.email = self.email_line_edit.text()

        def create_wallet(self):
            """
            Try to create a denarii wallet
            """
            self.wallet.name = self.name_line_edit.text()
            self.wallet.password = self.password_line_edit.text()

            success = False
            try:
                success = self.denarii_client.create_wallet(self.wallet)

                success = self.denarii_client.set_current_wallet(self.wallet) and success

                success = self.denarii_client.query_seed(self.wallet) and success
            except Exception as e:
                print(e)

            if success:
                self.wallet_info_text_box.setText(self.wallet.phrase)
                self.wallet_save_file_text_box.setText("Wallet saved to: " + DENARIID_WALLET_PATH)
                self.create_wallet_text_box.setText(
                    "Success. Make sure to write down your information. It will not be saved on this device.")
            else:
                self.create_wallet_text_box.setText("Failure")

        def set_wallet(self):
            """
            Set the wallet based on the user's information
            """

            self.wallet.name = self.name_line_edit.text()
            self.wallet.password = self.password_line_edit.text()

            success = False

            try:
                success = self.denarii_client.set_current_wallet(self.wallet)
                success = self.denarii_client.query_seed(self.wallet) and success
            except Exception as e:
                print(e)

            if success:
                self.set_wallet_text_box.setText("Success. Your seed is \n" + self.wallet.phrase)
            else:
                self.set_wallet_text_box.setText("Failure")

        def restore_wallet(self):
            """
            Try to restore a denarii wallet
            """

            self.wallet.name = self.name_line_edit.text()
            self.wallet.password = self.password_line_edit.text()
            self.wallet.phrase = self.seed_line_edit.text()

            success = False
            try:
                success = self.denarii_client.restore_wallet(self.wallet)
            except Exception as e:
                print(e)

            if success:
                self.wallet_save_file_text_box.setText("Wallet saved to: " + DENARIID_WALLET_PATH)
                self.restore_wallet_text_box.setText("Success")
            else:
                self.wallet_save_file_text_box.setText("Wallet already at: " + DENARIID_WALLET_PATH)
                self.restore_wallet_text_box.setText("Failure")

        def transfer_money(self):
            """
            Transfer money between two wallets.
            """
            success = False

            other_wallet = wallet_pb2.Wallet()
            other_wallet.address = bytes(self.address_line_edit.text(), 'utf-8')

            try:
                success = self.denarii_client.transfer_money(int(self.amount_line_edit.text()), self.wallet, other_wallet)
            except Exception as e:
                print(e)

            if success:
                self.wallet_transfer_status_text_box.setText("Success transferring money")
            else:
                self.wallet_transfer_status_text_box.setText("Failure transferring money")

        def create_sub_address(self):
            """
            Create a sub address
            """

            success = False

            try:
                success = self.denarii_client.create_no_label_address(self.wallet)
            except Exception as e:
                print(e)

            if success:
                sub_address_text_box = Label(str(self.wallet.sub_addresses[len(self.wallet.sub_addresses) - 1]))
                font = QFont()
                font.setFamily("Arial")
                font.setPixelSize(50)
                sub_address_text_box.setFont(font)
                sub_address_text_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
                self.vertical_layout.addWidget(sub_address_text_box, alignment=Qt.AlignCenter)
                self.sub_address_text_boxes.append(sub_address_text_box)
                self.wallet_info_status_text_box.setText("Success creating sub address. Use this to send to other people.")
            else:
                self.wallet_info_status_text_box.setText("Failure creating sub address.")

        def start_mining(self):
            """
            Start mining
            """

            success = False

            try:
                success = self.denarii_client.start_mining(True, False, multiprocessing.cpu_count() - 2)
            except Exception as e:
                print(e)

            if success:
                self.wallet_info_status_text_box.setText("Started mining")
            else:
                self.wallet_info_status_text_box.setText("Failed to start mining")

        def stop_mining(self):
            """
            Stop mining
            """

            success = False

            try:
                success = self.denarii_client.stop_mining()
            except Exception as e:
                print(e)

            if success:
                self.wallet_info_status_text_box.setText("Stopped mining")
            else:
                self.wallet_info_status_text_box.setText("Failed to stop mining")

        @pyqtSlot()
        def next_clicked(self):
            """
            What to do when the next page button is clicked depending on the current screen
            """
            if self.current_widget == self.LANG_SELECT:
                self.current_widget = self.USER_INFO
            elif self.current_widget == self.USER_INFO:
                self.current_widget = self.WALLET_INFO
                self.store_user_info()
            elif self.current_widget == self.WALLET_INFO:
                self.current_widget = self.WALLET_SCENE
            elif self.current_widget == self.CREATE_WALLET:
                self.current_widget = self.WALLET_SCENE
            elif self.current_widget == self.RESTORE_WALLET:
                self.current_widget = self.WALLET_SCENE
            elif self.current_widget == self.SET_WALLET:
                self.current_widget = self.WALLET_SCENE

            if self.current_widget == self.USER_INFO:
                self.setup_user_info_screen()
            elif self.current_widget == self.WALLET_INFO:
                self.setup_wallet_info_screen()
            elif self.current_widget == self.WALLET_SCENE:
                self.setup_wallet_scene_screen()

            store_user()

        @pyqtSlot()
        def on_create_wallet_clicked(self):
            """
            Setup the wallet creation screen when the user decides to create one
            """
            self.current_widget = self.CREATE_WALLET
            self.setup_create_wallet_screen()

        @pyqtSlot()
        def on_restore_wallet_pushed(self):
            """
            Setup the restore wallet screen when the user decides to restore one
            """
            self.current_widget = self.RESTORE_WALLET
            self.setup_restore_wallet_screen()

        @pyqtSlot()
        def on_set_wallet_pushed(self):
            """
            Setup the set wallet to set one saved to disk
            """
            self.current_widget = self.SET_WALLET
            self.setup_set_wallet_screen()

        @pyqtSlot()
        def on_create_wallet_submit_clicked(self):
            """
            Create the wallet based on the user's input information
            """
            self.create_wallet()

        @pyqtSlot()
        def on_restore_wallet_submit_clicked(self):
            """
            Restore a wallet based on the user's input information
            """
            self.restore_wallet()

        @pyqtSlot()
        def on_set_wallet_submit_clicked(self):
            """
            Set a wallet based on the user's input information
            """
            self.set_wallet()

        @pyqtSlot()
        def on_transfer_clicked(self):
            """
            Transfer money to another person's wallet
            """
            self.transfer_money()

        @pyqtSlot()
        def on_create_sub_address_clicked(self):
            """
            Create a subaddress
            """
            self.create_sub_address()

        @pyqtSlot()
        def on_start_mining_clicked(self):
            """
            Start mining
            """
            self.start_mining()

        @pyqtSlot()
        def on_stop_mining_clicked(self):
            """
            Stop mining
            """
            self.stop_mining()


    class RadioButton(QRadioButton):

        @pyqtSlot()
        def on_lang_select_clicked(self):
            """
            Set the user's language when they choose one
            """
            button = self.sender()

            gui_user.language = button.language

            store_user()


    class PushButton(QPushButton):
        pass


    class Label(QLabel):

        def __init__(self, name):
            super().__init__()
            self.setText(name)


    def get_main_window():
        """
        Get the main window of the program and set its style
        """
        window = QMainWindow()

        stylesheet = """
                    #mainwindow{
                        border: 0px;
                        background-color: #222;
                    }
                """

        window.setGeometry(QApplication.desktop().availableGeometry())
        window.setWindowTitle("Denarii Wallet")
        window.setStyleSheet(stylesheet)

        return window


    def create_central_widget(window):
        """
        Create the central widget for the main window
        """
        window.setCentralWidget(Widget(window))
        central_widget = window.centralWidget()
        central_widget.setGeometry(QRect(0, 0, 4000, 4000))


    def main():
        app = QApplication(sys.argv)

        window = get_main_window()

        create_central_widget(window)

        window.show()

        app.exec_()

        window.centralWidget().shutdown_denariid()
        window.centralWidget().shutdown_denarii_wallet_rpc_server()
        app.exit(0)
        sys.exit()

    if __name__ == "__main__":
        main()

except Exception as e:
    print(e)
    time.sleep(10)