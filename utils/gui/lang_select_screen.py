from screen import *

if TESTING:
    from denarii_testing_font import Font
    from denarii_testing_label import Label
    from denarii_testing_push_button import PushButton
    from denarii_testing_qt import AlignRight, AlignBottom, AlignCenter
    from denarii_testing_radio_button import RadioButton
else:
    from font import *
    from label import *
    from push_button import *
    from qt import AlignRight, AlignBottom, AlignCenter
    from radio_button import *


class LangSelectScreen(Screen):
    """
    A screen that lets the user select a language
    """

    def __init__(
        self,
        main_layout,
        deletion_func,
        denarii_client,
        gui_user,
        denarii_mobile_client,
        **kwargs
    ):

        self.pick_lang_label = None
        self.english_radio_button = None
        self.submit_button = None

        super().__init__(
            self.lang_select_screen_name,
            main_layout=main_layout,
            deletion_func=deletion_func,
            denarii_client=denarii_client,
            gui_user=gui_user,
            denarii_mobile_client=denarii_mobile_client,
            **kwargs
        )

    def init(self, **kwargs):
        super().init(**kwargs)

        self.next_button.setVisible(False)
        self.back_button.setVisible(False)

        self.pick_lang_label = Label("Pick a Language")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.pick_lang_label.setFont(font)

        self.english_radio_button = RadioButton(
            "English", kwargs["parent"], self.gui_user
        )
        self.english_radio_button.toggled.connect(
            self.english_radio_button.on_lang_select_clicked
        )
        self.english_radio_button.language = "English"
        self.english_radio_button.setVisible(False)
        self.english_radio_button.setStyleSheet(
            "QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};"
        )

        self.submit_button = PushButton("Submit", kwargs["parent"])
        self.submit_button.clicked.connect(lambda: self.on_submit_clicked())
        self.submit_button.setVisible(False)
        self.submit_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

    def setup(self):
        super().setup()

        # Remove anything on the screen
        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)
        self.main_layout.addLayout(self.fourth_horizontal_layout)

        # Add some text telling the user to select a language
        self.first_horizontal_layout.addWidget(
            self.pick_lang_label, alignment=AlignCenter
        )

        self.submit_button.setVisible(True)

        # Add a radio button for the user's language
        self.english_radio_button.setVisible(True)
        self.second_horizontal_layout.addWidget(
            self.english_radio_button, alignment=AlignCenter
        )

        self.third_horizontal_layout.addWidget(
            self.submit_button, alignment=AlignCenter
        )

        # Add a button to go the next screen
        self.fourth_horizontal_layout.addWidget(
            self.next_button, alignment=(AlignRight | AlignBottom)
        )

    def teardown(self):
        super().teardown()

    def on_submit_clicked(self):
        if self.gui_user.language is not None and self.gui_user.language != "":
            self.next_button.setVisible(True)
