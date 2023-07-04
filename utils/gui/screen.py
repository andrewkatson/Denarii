from PyQt5.QtWidgets import *


def add_additional_gui_elements(element_key, element_list, **kwargs):
    if element_key in kwargs:
        for element in kwargs[element_key]:
            element_list.append(element)


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

    suffix_of_screen_name = "suffix"

    def __init__(self, screen_name, main_layout, deletion_func, **kwargs):
        self.screen_name = screen_name
        self.main_layout = main_layout
        self.deletion_func = deletion_func

        if self.suffix_of_screen_name in kwargs:
            self.screen_name = f"{screen_name}{kwargs[self.suffix_of_screen_name]}"

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

        self.radio_buttons = []
        self.labels = []
        self.push_buttons = []
        self.line_edits = []

        add_additional_gui_elements(self.radio_button_name, self.radio_buttons, **kwargs)
        add_additional_gui_elements(self.label_name, self.labels, **kwargs)
        add_additional_gui_elements(self.push_button_name, self.push_buttons, **kwargs)
        add_additional_gui_elements(self.line_edit_name, self.line_edits, **kwargs)

    def setup(self):
        print(f"Setting up screen: {self.screen_name}")

    def __eq__(self, other):
        return self.screen_name == other.screen_name

    def __str__(self):
        return self.screen_name
