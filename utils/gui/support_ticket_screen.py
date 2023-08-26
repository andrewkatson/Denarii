import threading
import time

from screen import *
from stoppable_thread import StoppableThread

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



class SupportTicketScreen(Screen):
    """
    A screen that allows the user to create a support ticket
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

        self.user_settings_screen_push_button = None 
        
        self.support_ticket_creation_push_button = None

        self.support_ticket_label = None

        self.support_tickets = []

        self.parent = kwargs["parent"]

        self.on_support_ticket_details_screen_clicked = kwargs['on_support_ticket_details_screen_clicked']

        self.get_support_tickets_thread = StoppableThread(target=self.get_support_tickets)

        self.populate_thread = StoppableThread(target=self.populate_screen)

        self.lock = threading.Lock()

        super().__init__(
            self.support_ticket_screen_name,
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

        self.support_ticket_label = Label("Support Tickets")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.support_ticket_label.setFont(font)


        self.user_settings_screen_push_button = PushButton(
            "Identity Verification", kwargs["parent"]
        )
        self.user_settings_screen_push_button.clicked.connect(
            lambda: kwargs["on_user_settings_screen_clicked"]()
        )
        self.user_settings_screen_push_button.setVisible(False)
        self.user_settings_screen_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.support_ticket_creation_push_button = PushButton("", kwargs["parent"])
        self.support_ticket_creation_push_button.clicked.connect(lambda: kwargs['on_support_ticket_creation_screen_clicked'])
        self.support_ticket_creation_push_button.setVisible(False)
        self.support_ticket_creation_push_button.setStyleSheet("background-image : url(plus_icon.png);")
        
    def setup(self):
        super().setup()

        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.vertical_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)

        self.first_horizontal_layout.addWidget(self.support_ticket_label)
        
        self.second_horizontal_layout.addWidget(self.support_ticket_creation_push_button)       

        self.populate_thread.start()

        self.get_support_tickets_thread.start()


    def teardown(self):
        super().teardown()

        self.populate_thread.stop()
        self.get_support_tickets_thread.stop()

        if self.populate_thread.is_alive():
            self.populate_thread.join()

        if self.get_support_tickets_thread.is_alive():
            self.get_support_tickets_thread.join()

    def populate_screen(self):
        
        while not self.populate_thread.stopped():
            try: 
                self.lock.acquire()

                for support_ticket in self.support_tickets:
                    support_ticket_details_push_button = PushButton(
                        f"{support_ticket['title']}", self.parent
                    )
                    support_ticket_details_push_button.clicked.connect(
                        lambda: self.on_support_ticket_details_screen_clicked(support_ticket['support_ticket_id'])
                    )
                    support_ticket_details_push_button.setVisible(True)
                    support_ticket_details_push_button.setStyleSheet(
                        "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
                    )

            except Exception as e:
                print(e)
                self.status_message_box("Failed: unknown error")
            finally:
                self.lock.release()
            
            time.sleep(1)

    def get_support_tickets(self):
        while not self.get_support_tickets_thread.stopped():
            try: 
                self.lock.acquire()

                success, res = self.denarii_mobile_client.get_support_tickets(self.gui_user.user_id, False)

                if success: 

                    self.support_tickets = res

                else: 
                    self.status_message_box("Failed to get suppor tickets")

            except Exception as e:
                print(e)
                self.status_message_box("Failed: unknown error")
            finally:
                self.lock.release()
            
            time.sleep(5)
