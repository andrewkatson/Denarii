from screen import *
from label import *
from font import *
from line_edit import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class UserInfoScreen(Screen):
    """
    A screen that allows the user to enter in their information for later usage.
    """

    def __init__(self, main_layout, deletion_func, **kwargs):
        super().__init__(self.user_info_screen_name, main_layout, deletion_func, **kwargs)

        self.user_info_label = None
        self.name_line_edit = None
        self.email_line_edit = None
        self.gui_user = kwargs['gui_user']

    def init(self, **kwargs):
        super().init(**kwargs)

        self.user_info_label = Label("Input Your Information")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.user_info_label.setFont(font)

        self.name_line_edit = LineEdit()
        self.email_line_edit = LineEdit()

    def setup(self):
        super().setup()

        # Remove anything on the screen
        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)

        self.first_horizontal_layout.addWidget(self.user_info_label, alignment=Qt.AlignCenter)
        self.second_horizontal_layout.addWidget(self.next_button, alignment=(Qt.AlignRight | Qt.AlignBottom))
        self.second_horizontal_layout.addWidget(self.back_button, alignment=(Qt.AlignLeft | Qt.AlignBottom))
        self.form_layout.addRow("Name", self.name_line_edit)
        self.form_layout.addRow("Email", self.email_line_edit)

    def teardown(self):
        super().teardown()

    def store_user_info(self):
        """
        Store the user's input information in the user proto
        """
        self.gui_user.name = self.name_line_edit.text()
        self.gui_user.email = self.email_line_edit.text()
