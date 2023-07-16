from screen import *

if TESTING:
    from denarii_testing_font import Font
    from denarii_testing_label import Label
    from denarii_testing_line_edit import LineEdit
    from denarii_testing_message_box import MessageBox
    from denarii_testing_push_button import PushButton
    from denarii_testing_qt import (
        TextSelectableByMouse,
        AlignRight,
        AlignBottom,
        AlignCenter,
        AlignLeft,
    )
    from denarii_testing_radio_button import RadioButton
else:
    from font import *
    from label import *
    from line_edit import *
    from message_box import MessageBox
    from push_button import *
    from qt import (
        TextSelectableByMouse,
        AlignRight,
        AlignBottom,
        AlignCenter,
        AlignLeft,
    )
    from radio_button import *


class CreditCardInfoScreen(Screen):
    """
    A screen that allows the user to set or clear their credit card info
    """

    def __init__(self, main_layout, deletion_func, denarii_client, gui_user, denarii_mobile_client, **kwargs):

        self.remote_wallet_screen_push_button = None
        self.sell_screen_push_button = None
        self.buy_screen_push_button = None

        super().__init__(self.credit_card_info_screen_name, main_layout, deletion_func, denarii_client, gui_user, denarii_mobile_client, **kwargs)


    def init(self, **kwargs):
         super().init(**kwargs)
    
    def setup(self):
        super().setup()
    
    def teardown(self):
        super().teardown()
