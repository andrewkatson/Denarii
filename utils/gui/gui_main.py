# This is the main file for the Denarii gui.
# It assumes that https://github.com/andrewkatson/KeirosPublic is located at either
# %HOME/denarii or %HOMEDRIVE%%HOMEPATH%/Documents/Github/denarii

import pickle as pkl
import psutil
import os
import subprocess
import sys
import threading
import time

import workspace_path_finder


try:
    # DO NOT REMOVE THESE
    # They look like they aren't used but they are when building the exe
    # We try to import google.protobuf in case we are using a built exe using pyinstaller instead of bazel run
    from PyQt5 import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *

    from constants import *
    from create_wallet_screen import *
    from font import *
    from label import *
    from lang_select_screen import *
    from line_edit import *
    from local_wallet_screen import *
    from push_button import *
    from radio_button import *
    from remote_wallet_screen import *
    from restore_wallet_screen import *
    from screen import *
    from set_wallet_screen import *
    from stoppable_thread import StoppableThread
    from user_info_screen import *
    from wallet_info_screen import *
    from wallet_screen import *

    # Modify PATH to include the path to where we are so in production we can find all our files.
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))

    # Modify the PATH to include the path to the denarii python client
    sys.path.append(
        str(
            workspace_path_finder.find_other_workspace_path("KeirosPublic")
            / "Client"
            / "Denarii"
        )
    )

    if DEBUG:
        import denarii_client_testing as denarii_client
        import denarii_mobile_client_testing as denarii_mobile_client
    else:
        import denarii_client
        import denarii_mobile_client

    # Modify the PATH to point to where all of python protos are located that are not nearby in the filesystem
    sys.path.append(str(workspace_path_finder.get_home() / "py_proto"))

    from wallet import *
    from gui_user import *

    # Modify the PATH to point to where the gui_user proto is
    sys.path.append(
        str(workspace_path_finder.find_workspace_path() / "bazel-bin" / "utils" / "gui")
    )

    gui_user = GuiUser()

    MAIN_DENARII_PATH_LINUX = "denariid"

    MAIN_DENARII_PATH_WINDOWS = "denariid.exe"

    DENARIID_PATH_LINUX = str(
        workspace_path_finder.find_workspace_path() / "utils" / "gui" / "denariid"
    )

    DENARIID_PATH_WINDOWS = str(
        workspace_path_finder.find_workspace_path() / "utils" / "gui" / "denariid.exe"
    )

    MAIN_DENARII_WALLET_RPC_SERVER_PATH_LINUX = "denarii_wallet_rpc_server"

    MAIN_DENARII_WALLET_RPC_SERVER_PATH_WINDOWS = "denarii_wallet_rpc_server.exe"

    DENARII_WALLET_RPC_SERVER_PATH_LINUX = str(
        workspace_path_finder.find_workspace_path()
        / "utils"
        / "gui"
        / "denarii_wallet_rpc_server"
    )

    DENARII_WALLET_RPC_SERVER_PATH_WINDOWS = str(
        workspace_path_finder.find_workspace_path()
        / "utils"
        / "gui"
        / "denarii_wallet_rpc_server.exe"
    )

    # Files used to tell this program that the synchronization process is already done or is starting. Both indicators
    # that the denariid is working.
    SYNCHRONIZED_OK = "synchronized_ok.txt"
    SYNCHRONIZATION_STARTED = "synchronization_started.txt"

    def store_user():
        global gui_user
        with open(USER_SETTINGS_PATH, "wb") as output_file:
            # We dont save the user identifier. 
            user_id = gui_user.user_id
            gui_user.user_id = None
            pkl.dump(gui_user, output_file)
            gui_user.user_id = user_id

    def load_user():
        global gui_user

        with open(USER_SETTINGS_PATH, "rb") as input_file:
            gui_user = pkl.load(input_file)

    class Widget(QWidget):
        def __init__(self, parent):
            super().__init__(parent)

            self.denarii_client = denarii_client.DenariiClient()
            self.denarii_mobile_client = denarii_mobile_client.DenariiMobileClient()

            if DEBUG:
                print("Debug mode so no binaries are being started up")
            else:
                self.denariid = self.run_denariid_setup()

                self.denarii_wallet_rpc_server = self.setup_denarii_wallet_rpc_server()
                if (
                    self.denarii_wallet_rpc_server is not None
                    and self.denarii_wallet_rpc_server.returncode == 0
                ):
                    print("Wallet rpc server started up")
                else:
                    print("Wallet rpc server not started up or was already active")
                    if self.denarii_wallet_rpc_server is not None:
                        print(self.denarii_wallet_rpc_server.returncode)

            # Setup threads that will monitor the server and wallet rpc and ensure they are healthy.
            if DEBUG:
                print("Debug mode so no binary threads are going to be started up")
            else:
                self.server_thread = self.setup_server_thread()
                self.wallet_thread = self.setup_wallet_thread()

                # Start the threads up.
                self.server_thread.start()
                self.wallet_thread.start()

            self.main_layout = QVBoxLayout()
            self.setLayout(self.main_layout)

            self.local_wallet = Wallet()
            self.remote_wallet = Wallet()
            self.which_wallet = None

            # Common buttons
            self.next_button = PushButton("Next Page", self)
            self.next_button.setStyleSheet("color:black")
            self.next_button.setStyleSheet("font-weight: bold")
            self.next_button.setStyleSheet("font-size: 18pt")
            self.next_button.clicked.connect(self.next_clicked)

            self.back_button = PushButton("Back", self)
            self.back_button.setStyleSheet("color:black")
            self.back_button.setStyleSheet("font-weight: bold")
            self.back_button.setStyleSheet("font-size: 18pt")
            self.back_button.clicked.connect(self.back_clicked)

            common_buttons = {
                NEXT_BUTTON: self.next_button,
                BACK_BUTTON: self.back_button,
            }

            self.kwargs = {
                "push_buttons": common_buttons,
                "gui_user": gui_user,
                "parent": self,
                "main_layout": self.main_layout,
                "deletion_func": self.remove_all_widgets,
                "denarii_client": denarii_client,
                "on_create_wallet_clicked": self.on_create_wallet_clicked,
                "on_restore_wallet_clicked": self.on_restore_wallet_pushed,
                "on_set_wallet_clicked": self.on_set_wallet_pushed,
                "remote_wallet": self.remote_wallet,
                "local_wallet": self.local_wallet,
                "set_wallet_type_callback": self.set_wallet_type,
                "denarii_mobile_client": self.denarii_mobile_client,
            }

            if os.path.exists(USER_SETTINGS_PATH):
                load_user()

            # Widgets
            self.LANG_SELECT = LangSelectScreen(
                push_buttons=common_buttons,
                gui_user=gui_user,
                parent=self,
                main_layout=self.main_layout,
                deletion_func=self.remove_all_widgets,
                denarii_mobile_client=self.denarii_mobile_client,
                denarii_client=self.denarii_client,
            )
            self.USER_INFO = UserInfoScreen(
                push_buttons=common_buttons,
                main_layout=self.main_layout,
                denarii_mobile_client=self.denarii_mobile_client,
                deletion_func=self.remove_all_widgets,
                gui_user=gui_user,
                denarii_client=self.denarii_client,
                parent=self,
            )
            self.WALLET_INFO = WalletInfoScreen(
                push_buttons=common_buttons,
                parent=self,
                denarii_mobile_client=self.denarii_mobile_client,
                on_create_wallet_clicked=self.on_create_wallet_clicked,
                on_restore_wallet_clicked=self.on_restore_wallet_pushed,
                on_set_wallet_clicked=self.on_set_wallet_pushed,
                main_layout=self.main_layout,
                deletion_func=self.remove_all_widgets,
                denarii_client=self.denarii_client,
                gui_user=gui_user,
            )
            self.CREATE_WALLET = CreateWalletScreen(
                push_buttons=common_buttons,
                parent=self,
                denarii_mobile_client=self.denarii_mobile_client,
                main_layout=self.main_layout,
                deletion_func=self.remove_all_widgets,
                denarii_client=self.denarii_client,
                remote_wallet=self.remote_wallet,
                local_wallet=self.local_wallet,
                gui_user=gui_user,
                set_wallet_type_callback=self.set_wallet_type,
            )
            self.RESTORE_WALLET = RestoreWalletScreen(
                push_buttons=common_buttons,
                parent=self,
                denarii_mobile_client=self.denarii_mobile_client,
                main_layout=self.main_layout,
                deletion_func=self.remove_all_widgets,
                denarii_client=self.denarii_client,
                remote_wallet=self.remote_wallet,
                local_wallet=self.local_wallet,
                gui_user=gui_user,
                set_wallet_type_callback=self.set_wallet_type,
            )
            self.SET_WALLET = SetWalletScreen(
                push_buttons=common_buttons,
                parent=self,
                denarii_mobile_client=self.denarii_mobile_client,
                main_layout=self.main_layout,
                deletion_func=self.remove_all_widgets,
                denarii_client=self.denarii_client,
                remote_wallet=self.remote_wallet,
                local_wallet=self.local_wallet,
                gui_user=gui_user,
                set_wallet_type_callback=self.set_wallet_type,
            )
            self.CURRENT_WALLET = None
            self.LOCAL_WALLET_SCREEN = LocalWalletScreen(
                push_buttons=common_buttons,
                denarii_mobile_client=self.denarii_mobile_client,
                main_layout=self.main_layout,
                deletion_func=self.remove_all_widgets,
                parent=self,
                denarii_client=self.denarii_client,
                local_wallet=self.local_wallet,
                gui_user=gui_user,
            )
            self.REMOTE_WALLET_SCREEN = RemoteWalletScreen(
                push_buttons=common_buttons,
                main_layout=self.main_layout,
                denarii_mobile_client=self.denarii_mobile_client,
                deletion_func=self.remove_all_widgets,
                denarii_client=self.denarii_client,
                parent=self,
                remote_wallet=self.remote_wallet,
                gui_user=gui_user,
            )

            # Determine what scene we are on based on what info the stored user has
            if (gui_user.language is None or gui_user.language == "") and (
                gui_user.name is None or gui_user.name == ""
            ):
                self.current_widget = self.LANG_SELECT
            elif (
                gui_user.language is not None
                and gui_user.language != ""
                and (gui_user.name is None or gui_user.name == "")
            ):
                self.current_widget = self.USER_INFO
            elif (
                gui_user.language is not None
                and gui_user.language != ""
                and gui_user.name is not None
                and gui_user.name != ""
            ):
                self.current_widget = self.WALLET_INFO
            else:
                self.current_widget = self.WALLET_INFO

            self.last_widget = None
            self.setup_current_widget()

            self.parent = parent

            self.success = False

        def run_denariid_setup(self):
            self.denariid = self.setup_denariid()
            if self.denariid is not None and self.denariid.returncode == 0:
                print("Denariid started up")
            else:
                print("Denariid was not started or was already active")
                if self.denariid is not None:
                    print(self.denariid.returncode)

            return self.denariid

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
                return subprocess.Popen(
                    "sudo " + MAIN_DENARII_PATH_LINUX + " --no-igd",
                    shell=True,
                    encoding="utf-8",
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                )
            elif os.path.exists(MAIN_DENARII_PATH_WINDOWS):
                return subprocess.Popen(
                    "start " + MAIN_DENARII_PATH_WINDOWS + " --no-igd",
                    shell=True,
                    encoding="utf-8",
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                )
            elif os.path.exists(DENARIID_PATH_LINUX):
                return subprocess.Popen(
                    "sudo " + DENARIID_PATH_LINUX + " --no-igd",
                    shell=True,
                    encoding="utf-8",
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                )
            elif os.path.exists(DENARIID_PATH_WINDOWS):
                return subprocess.Popen(
                    "start " + DENARIID_PATH_WINDOWS + " --no-igd",
                    shell=True,
                    encoding="utf-8",
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                )

            return None

        def setup_denarii_wallet_rpc_server(self):
            if self.already_started_denarii_wallet_rpc_server():
                return None

            if not os.path.exists(DENARIID_WALLET_PATH):
                os.makedirs(DENARIID_WALLET_PATH)

            if os.path.exists(MAIN_DENARII_WALLET_RPC_SERVER_PATH_LINUX):
                return subprocess.Popen(
                    "sudo "
                    + MAIN_DENARII_WALLET_RPC_SERVER_PATH_LINUX
                    + " --rpc-bind-port=8080"
                    + f" --wallet-dir={DENARIID_WALLET_PATH}"
                    + " --disable-rpc-login",
                    shell=True,
                    encoding="utf-8",
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                )
            elif os.path.exists(MAIN_DENARII_WALLET_RPC_SERVER_PATH_WINDOWS):
                return subprocess.Popen(
                    "start "
                    + MAIN_DENARII_WALLET_RPC_SERVER_PATH_WINDOWS
                    + " --rpc-bind-port=8080"
                    + f" --wallet-dir={DENARIID_WALLET_PATH}"
                    + " --disable-rpc-login",
                    shell=True,
                    encoding="utf-8",
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                )
            elif os.path.exists(DENARII_WALLET_RPC_SERVER_PATH_LINUX):
                return subprocess.Popen(
                    "sudo "
                    + DENARII_WALLET_RPC_SERVER_PATH_LINUX
                    + " --rpc-bind-port=8080"
                    + f" --wallet-dir={DENARIID_WALLET_PATH}"
                    + " --disable-rpc-login",
                    shell=True,
                    encoding="utf-8",
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                )
            elif os.path.exists(DENARII_WALLET_RPC_SERVER_PATH_WINDOWS):
                return subprocess.Popen(
                    "start "
                    + DENARII_WALLET_RPC_SERVER_PATH_WINDOWS
                    + " --rpc-bind-port=8080"
                    + f" --wallet-dir={DENARIID_WALLET_PATH}"
                    + " --disable-rpc-login",
                    shell=True,
                    encoding="utf-8",
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                )

            return None

        def setup_server_thread(self):
            return StoppableThread(target=self.monitor_server_thread)

        def setup_wallet_thread(self):
            return StoppableThread(target=self.monitor_wallet_thread)

        def monitor_server_thread(self):
            """
            Restart the server thread if there are any issues with it
            """

            while True:
                time.sleep(60)

                if os.path.exists(SYNCHRONIZATION_STARTED) or os.path.exists(
                    SYNCHRONIZED_OK
                ):
                    print("Synchronized")
                    if os.path.exists(SYNCHRONIZATION_STARTED):
                        os.remove(SYNCHRONIZATION_STARTED)
                    if os.path.exists(SYNCHRONIZED_OK):
                        os.remove(SYNCHRONIZED_OK)
                    return
                else:
                    print("Not synchronized")
                    self.shutdown_denariid()
                    self.denariid = self.run_denariid_setup()

        def monitor_wallet_thread(self):
            """
            Restart the wallet thread if there any issues with it
            @param wallet_rpc_server the wallet rpc server
            """
            # There are no known issues with denarii wallet rpc server so just exit.
            return

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

        def shutdown_threads(self):
            self.server_thread.join()
            self.wallet_thread.join()

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

        def shutdown_all_screens(self):
            # We should only have to turn down the current one.
            self.current_widget.teardown()

        @pyqtSlot()
        def next_clicked(self):
            """
            What to do when the next page button is clicked depending on the current screen
            """
            self.last_widget = self.current_widget
            if self.current_widget == self.LANG_SELECT:
                self.current_widget = self.USER_INFO
            elif self.current_widget == self.USER_INFO:
                self.current_widget = self.WALLET_INFO
            elif self.current_widget == self.WALLET_INFO:
                # The next button on the wallet info screen should do nothing
                self.current_widget = self.WALLET_INFO
            elif self.current_widget == self.CREATE_WALLET:
                self.current_widget = self.current_wallet_widget
            elif self.current_widget == self.RESTORE_WALLET:
                self.current_widget = self.current_wallet_widget
            elif self.current_widget == self.SET_WALLET:
                self.current_widget = self.current_wallet_widget

            self.setup_current_widget()

            store_user()

        @pyqtSlot()
        def back_clicked(self):
            """
            What to do when the back_button button is clicked depending on the current screen
            """
            self.last_widget = self.current_widget
            if self.current_widget == self.LANG_SELECT:
                # The back button on lang select should do nothing
                self.current_widget = self.LANG_SELECT
            elif self.current_widget == self.USER_INFO:
                self.current_widget = self.LANG_SELECT
            elif self.current_widget == self.WALLET_INFO:
                self.current_widget = self.USER_INFO
            elif self.current_widget == self.CREATE_WALLET:
                self.current_widget = self.WALLET_INFO
            elif self.current_widget == self.RESTORE_WALLET:
                self.current_widget = self.WALLET_INFO
            elif self.current_widget == self.SET_WALLET:
                self.current_widget = self.WALLET_INFO
            elif self.current_widget == self.current_wallet_widget:
                self.current_widget = self.WALLET_INFO

            self.setup_current_widget()

            store_user()

        @pyqtSlot()
        def on_create_wallet_clicked(self):
            """
            Setup the wallet creation screen when the user decides to create one
            """
            self.current_widget = self.CREATE_WALLET
            self.setup_current_widget()

        @pyqtSlot()
        def on_restore_wallet_pushed(self):
            """
            Setup the restore wallet screen when the user decides to restore one
            """
            self.current_widget = self.RESTORE_WALLET
            self.setup_current_widget()

        @pyqtSlot()
        def on_set_wallet_pushed(self):
            """
            Setup the set wallet to set one saved to disk
            """
            self.current_widget = self.SET_WALLET
            self.setup_current_widget()

        def setup_current_widget(self):
            if self.last_widget is not None:
                self.last_widget.teardown()

            self.current_widget.init(**self.kwargs)
            self.current_widget.setup()

        @property
        def wallet(self):
            if self.which_wallet is None:
                return self.local_wallet

            if self.which_wallet == REMOTE_WALLET:
                return self.remote_wallet
            elif self.which_wallet == LOCAL_WALLET:
                return self.local_wallet
            return self.local_wallet

        @property
        def current_wallet_widget(self):
            if self.which_wallet is None:
                return self.LOCAL_WALLET_SCREEN

            if self.which_wallet == REMOTE_WALLET:
                return self.REMOTE_WALLET_SCREEN
            elif self.which_wallet == LOCAL_WALLET:
                return self.LOCAL_WALLET_SCREEN
            return self.LOCAL_WALLET_SCREEN

        def set_wallet_type(self, type):
            if type == REMOTE_WALLET:
                self.which_wallet = REMOTE_WALLET
            else:
                self.which_wallet = LOCAL_WALLET

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
        window.setWindowTitle("Denarii Desktop GUI")
        window.setStyleSheet(stylesheet)

        return window

    def create_central_widget(window):
        """
        Create the central widget for the main window
        """
        window.setCentralWidget(Widget(window))
        central_widget = window.centralWidget()
        central_widget.setGeometry(QRect(0, 0, 4000, 4000))

    def shutdown_threads():
        for thread in threading.enumerate():
            if thread.name != "MainThread":
                thread.stop()

                while not thread.stopped():
                    time.sleep(1)

    def main():
        app = QApplication(sys.argv)

        window = get_main_window()

        create_central_widget(window)

        window.show()

        app.exec_()

        if DEBUG:
            print("Debug mode so we don't need to shut any binaries down")
        else:
            window.centralWidget().shutdown_denariid()
            window.centralWidget().shutdown_denarii_wallet_rpc_server()
            window.centralWidget().shutdown_threads()

        window.centralWidget().shutdown_all_screens()

        app.exit(0)

        shutdown_threads()

        sys.exit()

    if __name__ == "__main__":
        main()

except Exception as e:
    print(e)
    time.sleep(10)
