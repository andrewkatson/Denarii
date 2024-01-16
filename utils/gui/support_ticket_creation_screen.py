from screen import *

if TESTING:
    from denarii_testing_font import Font
    from denarii_testing_icon import Icon
    from denarii_testing_label import Label
    from denarii_testing_line_edit import LineEdit
    from denarii_testing_message_box import MessageBox
    from denarii_testing_pixmap import Pixmap
    from denarii_testing_plain_text_edit import PlainTextEdit
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
    from icon import Icon
    from label import *
    from line_edit import *
    from message_box import MessageBox
    from pixmap import Pixmap
    from plain_text_edit import PlainTextEdit
    from push_button import *
    from qt import (
        TextSelectableByMouse,
        AlignRight,
        AlignBottom,
        AlignCenter,
        AlignLeft,
    )
    from radio_button import *



class SupportTicketCreationScreen(Screen):
    """
    A screen to create a support ticket
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

        self.create_support_ticket_label = None 
        
        self.title_line_edit = None 
        self.description_text_edit = None

        self.submit_push_button = None 
        self.support_ticket_push_button = None

        self.on_support_ticket_details_clicked = kwargs['on_support_ticket_details_screen_clicked']

        super().__init__(
            self.support_ticket_creation_screen_name,
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

        self.create_support_ticket_label = Label("Create Support Ticket")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.create_support_ticket_label.setFont(font)

        self.support_ticket_push_button = PushButton("Support Tickets", kwargs["parent"])
        self.support_ticket_push_button.clicked.connect(
            lambda: kwargs["on_support_ticket_screen_clicked"]()
        )
        self.support_ticket_push_button.setVisible(False)
        self.support_ticket_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.submit_push_button = PushButton("Submit", kwargs["parent"])
        self.submit_push_button.clicked.connect(lambda: self.on_submit_clicked())
        self.submit_push_button.setVisible(False)
        self.submit_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.title_line_edit = LineEdit()
        self.description_text_edit = PlainTextEdit()


    def setup(self):
        super().setup()

        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)

        self.submit_push_button.setVisible(True)
        self.support_ticket_push_button.setVisible(True)

        self.first_horizontal_layout.addWidget(self.create_support_ticket_label, alignment=AlignCenter)

        self.form_layout.addRow("Title", self.title_line_edit)
        self.form_layout.addRow("Description", self.description_text_edit)

        self.second_horizontal_layout.addWidget(self.submit_push_button, alignment=AlignCenter)

        self.third_horizontal_layout.addWidget(self.back_button, alignment=(AlignLeft | AlignBottom))
        self.fourth_horizontal_layout.addWidget(self.support_ticket_push_button, alignment=AlignCenter)

    def teardown(self):
        super().teardown()

    def on_submit_clicked(self):
        
        invalid_fields = []
        
        if not is_valid_pattern(self.title_line_edit.text(), Patterns.alphanumeric_with_spaces):
            invalid_fields.append(Params.title)
        
        if not is_valid_pattern(self.description_text_edit.toPlainText(), Patterns.paragraph_of_chars): 
            invalid_fields.append(Params.description)
            
        if len(invalid_fields) > 0:
            self.status_message_box(f"Failed: Invalid Fields {invalid_fields}")
            return
        
        try: 
            success, res = self.denarii_mobile_client.create_support_ticket(self.gui_user.user_id, self.title_line_edit.text(), self.description_text_edit.toPlainText())

            if success:
                self.status_message_box("Created support ticket")

                self.on_support_ticket_details_clicked(res[0]['support_ticket_id'])
            else: 
                self.status_message_box("Failed to create support ticket")
        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")
