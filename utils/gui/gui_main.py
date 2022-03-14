# This is the main file for the Denarii gui.
# It assumes that https://github.com/andrewkatson/KeirosPublic is located at either
# %HOME/denarii or %HOMEDRIVE%%HOMEPATH%/Documents/Github/denarii

import pickle as pkl
import os
import subprocess
import sys
import workspace_path_finder

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Modify the PATH to include the path to the denarii python client
sys.path.append(str(workspace_path_finder.find_other_workspace_path("KeirosPublic") / "Client" / "Denarii"))

import denarii_client

# Modify the PATH to point to where all of python protos are located that are not nearby in the filesystem
sys.path.append(str(workspace_path_finder.get_home() / "py_proto"))

from Proto import wallet_pb2

# Modify the PATH to point to where the gui_user proto is
sys.path.append(str(workspace_path_finder.find_workspace_path() / "bazel-bin" / "utils" / "gui"))

from proto import gui_user_pb2

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

DENARIID_WALLET_PATH = str(workspace_path_finder.find_workspace_path() / "utils" / "gui" / "denarii" / "wallet")

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
        if self.denariid is None:
            print("No denarii daemon. This will not work")

        self.denarii_wallet_rpc_server = self.setup_denarii_wallet_rpc_server()
        if self.denarii_wallet_rpc_server is None:
            print("No denarii wallet rpc server. This will not work")

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

        self.wallet_info_text_box = Label("")
        font = QFont()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.wallet_info_text_box.setFont(font)

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

        self.create_wallet_push_button = PushButton("Create Wallet", self)
        self.create_wallet_push_button.clicked.connect(self.on_create_wallet_clicked)
        self.create_wallet_push_button.setVisible(False)
        self.create_wallet_push_button.setStyleSheet(
            'QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};')

        self.restore_wallet_push_button = PushButton("Restore Wallet", self)
        self.restore_wallet_push_button.clicked.connect(self.on_restore_wallet_pushed)
        self.restore_wallet_push_button.setVisible(False)
        self.restore_wallet_push_button.setStyleSheet(
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

    def setup_denariid(self):
        if os.path.exists(MAIN_DENARII_PATH_LINUX):
            return subprocess.Popen("sudo " + MAIN_DENARII_PATH_LINUX, shell=True)
        elif os.path.exists(MAIN_DENARII_PATH_WINDOWS):
            return subprocess.Popen(MAIN_DENARII_PATH_WINDOWS, shell=True)
        elif os.path.exists(DENARIID_PATH_LINUX):
            return subprocess.Popen("sudo " + DENARIID_PATH_LINUX, shell=True)
        elif os.path.exists(DENARIID_PATH_WINDOWS):
            return subprocess.Popen(DENARIID_PATH_WINDOWS, shell=True)

        return None

    def setup_denarii_wallet_rpc_server(self):
        if not os.path.exists(DENARIID_WALLET_PATH):
            os.makedirs(DENARIID_WALLET_PATH)

        if os.path.exists(MAIN_DENARII_WALLET_RPC_SERVER_PATH_LINUX):
            return subprocess.Popen(
                ["sudo " + MAIN_DENARII_WALLET_RPC_SERVER_PATH_LINUX + "--rpc-bind-port=8080" + f"--wallet-dir={DENARIID_WALLET_PATH}"],
                shell=True)
        elif os.path.exists(MAIN_DENARII_WALLET_RPC_SERVER_PATH_WINDOWS):
            return subprocess.Popen(
                [MAIN_DENARII_WALLET_RPC_SERVER_PATH_WINDOWS + "--rpc-bind-port=8080" + f"--wallet-dir={DENARIID_WALLET_PATH}"],
                shell=True)
        elif os.path.exists(DENARII_WALLET_RPC_SERVER_PATH_LINUX):
            return subprocess.Popen(
                ["sudo " + DENARII_WALLET_RPC_SERVER_PATH_LINUX + "--rpc-bind-port=8080" + f"--wallet-dir={DENARIID_WALLET_PATH}"],
                shell=True)
        elif os.path.exists(DENARII_WALLET_RPC_SERVER_PATH_WINDOWS):
            return subprocess.Popen(
                [DENARII_WALLET_RPC_SERVER_PATH_WINDOWS + "--rpc-bind-port=8080" + f"--wallet-dir={DENARIID_WALLET_PATH}"],
                shell=True)

    def shutdown_denariid(self):
        self.denariid.terminate()

    def shutdown_denarii_wallet_rpc_server(self):
        self.denarii_wallet_rpc_server.terminate()

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

        self.first_horizontal_layout.addWidget(self.wallet_info_label, alignment=Qt.AlignCenter)
        self.second_horizontal_layout.addWidget(self.create_wallet_push_button, alignment=Qt.AlignCenter)
        self.second_horizontal_layout.addWidget(self.restore_wallet_push_button, alignment=Qt.AlignCenter)
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

        self.create_wallet_submit_push_button.setVisible(True)

        self.first_horizontal_layout.addWidget(self.create_wallet_label, alignment=Qt.AlignCenter)
        self.form_layout.addRow("Name", self.name_line_edit)
        self.form_layout.addRow("Password", self.password_line_edit)
        self.second_horizontal_layout.addWidget(self.wallet_info_text_box, alignment=Qt.AlignCenter)
        self.third_horizontal_layout.addWidget(self.create_wallet_text_box, alignment=Qt.AlignCenter)
        self.fourth_horizontal_layout.addWidget(self.create_wallet_submit_push_button, alignment=Qt.AlignCenter)
        self.fifth_horizontal_layout.addWidget(self.next_button, alignment=(Qt.AlignRight | Qt.AlignBottom))

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

        self.restore_wallet_submit_push_button.setVisible(True)

        self.first_horizontal_layout.addWidget(self.restore_wallet_label, alignment=Qt.AlignCenter)
        self.form_layout.addRow("Name", self.name_line_edit)
        self.form_layout.addRow("Password", self.password_line_edit)
        self.form_layout.addRow("Seed", self.seed_line_edit)
        self.second_horizontal_layout.addWidget(self.restore_wallet_text_box, alignment=Qt.AlignCenter)
        self.third_horizontal_layout.addWidget(self.restore_wallet_submit_push_button, alignment=Qt.AlignCenter)
        self.fourth_horizontal_layout.addWidget(self.next_button, alignment=(Qt.AlignRight | Qt.AlignBottom))

    def setup_wallet_scene_screen(self):
        """
        Setup the wallet scene where the user can transfer funds and check their own funds
        """
        self.remove_all_widgets(self.main_layout)

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
        wallet = wallet_pb2.Wallet()
        wallet.name = self.name_line_edit.text()
        wallet.password = self.password_line_edit.text()

        success = False
        try:
            self.denarii_client.create_wallet(wallet)

            self.denarii_client.set_current_wallet(wallet)

            success = self.denarii_client.query_seed(wallet)
        except Exception as e:
            print(e)

        if success:
            self.wallet_info_text_box.setText(gui_user.wallet.phrase)
            self.create_wallet_text_box.setText("Success")
        else:
            self.create_wallet_text_box.setText("Failure")

    def restore_wallet(self):
        """
        Try to restore a denarii wallet
        """
        wallet = wallet_pb2.Wallet()
        wallet.name = self.name_line_edit.text()
        wallet.password = self.password_line_edit.text()
        wallet.phrase = self.seed_line_edit.text()

        success = False
        try:
            success = self.denarii_client.restore_wallet(wallet)
        except Exception as e:
            print(e)

        if success:
            self.restore_wallet_text_box.setText("Success")
        else:
            self.restore_wallet_text_box.setText("Failure")

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
