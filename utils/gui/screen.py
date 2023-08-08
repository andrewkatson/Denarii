from constants import *

if TESTING:
    from denarii_testing_message_box import MessageBox
    from denarii_testing_widget import *
else:
    from message_box import MessageBox
    from widget import *


def add_additional_gui_elements(element_key, element_dict, **kwargs):
    if element_key in kwargs:
        for key, value in kwargs[element_key].items():
            element_dict[key] = value


class Screen:
    """
    A screen that has widgets in it that are displayed on the gui.
    """

    radio_button_name = "radio_buttons"
    label_name = "labels"
    push_button_name = "push_buttons"
    line_edit_name = "line_edits"

    lang_select_screen_name = "LANG_SELECT_SCREEN"
    user_info_screen_name = "USER_INFO_SCREEN"
    wallet_info_screen_name = "WALLET_INFO_SCREEN"
    create_wallet_screen_name = "CREATE_WALLET_SCREEN"
    restore_wallet_screen_name = "RESTORE_WALLET_SCREEN"
    set_wallet_screen_name = "OPEN_WALLET_SCREEN_NAME"
    wallet_screen_name = "WALLET_SCREEN_NAME"
    buy_denarii_screen_name = "BUY_DENARII_SCREEN_NAME"
    sell_denarii_screen_name = "SELL_DENARII_SCREEN_NAME"
    login_or_register_screen_name = "LOGIN_OR_REGISTER_SCREEN_NAME"
    login_screen_name = "LOGIN_SCREEN_NAME"
    register_screen_name = "REGISTER_SCREEN_NAME"
    request_reset_screen_name = "REQUEST_RESET_SCREEN_NAME"
    reset_password_screen_name = "RESET_PASSWORD_SCREEN_NAME"
    verify_reset_screen_name = "VERIFY_RESET_SCREEN_NAME"
    credit_card_info_screen_name = "CREDIT_CARD_INFO_SCREEN_NAME"
    verification_screen_name = "VERIFICATON_SCREEN_NAME"
    user_settings_screen_name = "USER_SETTINGS_SCREEN_NAME"
    support_ticket_screen_name = "SUPPORT_TICKET_SCREEN_NAME"

    suffix_of_screen_name = "suffix"

    def __init__(
        self,
        screen_name,
        main_layout,
        deletion_func,
        denarii_client,
        gui_user,
        denarii_mobile_client,
        **kwargs,
    ):
        self.screen_name = screen_name
        self.main_layout = main_layout
        self.deletion_func = deletion_func
        self.denarii_client = denarii_client
        self.denarii_mobile_client = denarii_mobile_client
        self.gui_user = gui_user

        if self.suffix_of_screen_name in kwargs:
            self.screen_name = f"{screen_name}_{kwargs[self.suffix_of_screen_name]}"

        self.first_horizontal_layout = HBoxLayout()
        self.second_horizontal_layout = HBoxLayout()
        self.third_horizontal_layout = HBoxLayout()
        self.fourth_horizontal_layout = HBoxLayout()
        self.fifth_horizontal_layout = HBoxLayout()
        self.sixth_horizontal_layout = HBoxLayout()
        self.seventh_horizontal_layout = HBoxLayout()
        self.eight_horizontal_layout = HBoxLayout()
        self.ninth_horizontal_layout = HBoxLayout()
        self.tenth_horizontal_layout = HBoxLayout()
        self.eleventh_horizontal_layout = HBoxLayout()

        self.vertical_layout = VBoxLayout()
        
        self.form_layout = FormLayout()

        self.grid_layout = GridLayout()
        self.second_grid_layout = GridLayout()

        self.radio_buttons = {}
        self.labels = {}
        self.push_buttons = {}
        self.line_edits = {}

        add_additional_gui_elements(
            self.radio_button_name, self.radio_buttons, **kwargs
        )
        add_additional_gui_elements(self.label_name, self.labels, **kwargs)
        add_additional_gui_elements(self.push_button_name, self.push_buttons, **kwargs)
        add_additional_gui_elements(self.line_edit_name, self.line_edits, **kwargs)

        self.next_button = None
        self.back_button = None

        self.status_msg = None

        self.init(**kwargs)

    def init(self, **kwargs):
        print(f"Initializing screen: {self.screen_name}")

        if NEXT_BUTTON in self.push_buttons:
            self.next_button = self.push_buttons[NEXT_BUTTON]
            print("Found next button")

        if BACK_BUTTON in self.push_buttons:
            self.back_button = self.push_buttons[BACK_BUTTON]
            print("Found back button")

    def setup(self):
        print(f"Setting up screen: {self.screen_name}")

    def teardown(self):
        print(f"Tearing down screen: {self.screen_name}")

        self.deletion_func(self.main_layout)

    def __eq__(self, other):
        return self.screen_name == other.screen_name

    def __str__(self):
        return self.screen_name

    def status_message_box(self, status):
        self.status_msg = MessageBox()
        self.status_msg.setWindowTitle("Status")
        self.status_msg.setText(status)
        self.status_msg.exec_()
