from screen import *
from label import *
from font import *
from line_edit import *


class UserInfoScreen(Screen):
    """
    A screen that allows the user to enter in their information for later usage.
    """

    def __init__(self, main_layout, deletion_func, **kwargs):
        super().__init__(self.user_info_screen_name, main_layout, deletion_func, **kwargs)

        self.user_info_label = Label("Input Your Information")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.user_info_label.setFont(font)

        self.name_line_edit = LineEdit()
        self.email_line_edit = LineEdit()

    def setup(self):
        super().setup()
