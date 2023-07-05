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

        self.pick_lang_label = None
        self.english_radio_button = None

    def init(self, **kwargs):
        super().init(**kwargs)

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

        # Remove anything on the screen
        self.deletion_func(self.main_layout)

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

    def teardown(self):
        super().teardown()
