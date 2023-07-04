from screen import *
from label import *
from font import *
from radio_button import *


class LangSelectScreen(Screen):
    """
    A screen that lets the user select a language
    """

    def __init__(self, main_layout, deletion_func, **kwargs):
        super().__init__(self.lang_select_screen_name, main_layout, deletion_func, **kwargs)

        self.pick_lang_label = Label("Pick a Language")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.pick_lang_label.setFont(font)

        self.english_radio_button = RadioButton("English", kwargs['parent'], kwargs['gui_user'],
                                                kwargs['store_user_func'])
        self.english_radio_button.toggled.connect(self.english_radio_button.on_lang_select_clicked)
        self.english_radio_button.language = "English"
        self.english_radio_button.setVisible(False)
        self.english_radio_button.setStyleSheet(
            'QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};')

    def setup(self):
        super().setup()
