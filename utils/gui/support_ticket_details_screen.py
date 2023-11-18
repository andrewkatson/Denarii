from screen import *

if TESTING:
    from denarii_testing_font import Font
    from denarii_testing_label import Label
    from denarii_testing_line_edit import LineEdit
    from denarii_testing_message_box import MessageBox
    from denarii_testing_plain_text_edit import PlainTextEdit
    from denarii_testing_push_button import PushButton
    from denarii_testing_qt import (
        TextSelectableByMouse,
        AlignRight,
        AlignBottom,
        AlignCenter,
        AlignLeft,
        ScrollBarAlwaysOn,
        ScrollBarAlwaysOff,
    )
    from denarii_testing_radio_button import RadioButton
    from denarii_testing_widget import CommentSection, ScrollArea
else:
    from font import *
    from label import *
    from line_edit import *
    from message_box import MessageBox
    from plain_text_edit import *
    from push_button import *
    from qt import (
        TextSelectableByMouse,
        AlignRight,
        AlignBottom,
        AlignCenter,
        AlignLeft,
        ScrollBarAlwaysOn,
        ScrollBarAlwaysOff,
    )
    from radio_button import *
    from widget import CommentSection


class SupportTicketDetailsScreen(Screen):
    """
    A screen that shows details of a support ticket and allows interaction with it.
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
        self.support_ticket_details_label = None
        self.title_label = None
        self.description_label = None

        self.submit_push_button = None

        self.comment_section = None

        self.new_comment_plain_text_edit = None

        self.support_ticket_push_button = None

        self.delete_ticket_push_button = None

        self.resolve_ticket_push_button = None

        self.scroll_area = None

        self.get_current_support_ticket_id = kwargs["get_current_support_ticket_id"]

        self.on_support_ticket_screen_clicked = kwargs['on_support_ticket_screen_clicked']

        self.support_ticket_id = self.get_current_support_ticket_id()

        # We need to explicitly set the gui_user since we use it in get_support_ticket*
        self.gui_user = gui_user

        # We need to explicitly set the denarii mobile client since we call it in get_support_ticket*
        self.denarii_mobile_client = denarii_mobile_client


        self.support_ticket_details = self.get_support_ticket_details()

        self.comment_details = self.get_support_ticket_comment_details()
        
        self.comment_details_artifacts = []

        super().__init__(
            self.support_ticket_details_screen_name,
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

        self.support_ticket_details_label = Label("Support Ticket Details")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.support_ticket_details_label.setFont(font)

        self.title_label = Label(self.support_ticket_details["title"])
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.title_label.setFont(font)

        self.description_label = Label(self.support_ticket_details["description"])
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.description_label.setFont(font)

        self.submit_push_button = PushButton("Submit", kwargs["parent"])
        self.submit_push_button.clicked.connect(lambda: self.on_submit_clicked())
        self.submit_push_button.setVisible(False)
        self.submit_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.support_ticket_push_button = PushButton("Support Tickets", kwargs["parent"])
        self.support_ticket_push_button.clicked.connect(lambda: self.on_support_ticket_screen_clicked())
        self.support_ticket_push_button.setVisible(False)
        self.support_ticket_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.delete_ticket_push_button = PushButton("Delete", kwargs["parent"])
        self.delete_ticket_push_button.clicked.connect(lambda: self.on_delete_clicked())
        self.delete_ticket_push_button.setVisible(False)
        self.delete_ticket_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.resolve_ticket_push_button = PushButton("Resolve", kwargs["parent"])
        self.resolve_ticket_push_button.clicked.connect(
            lambda: self.on_resolve_clicked()
        )
        self.resolve_ticket_push_button.setVisible(False)
        self.resolve_ticket_push_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

        self.comment_section = CommentSection()

        self.populate_comment_section()

        self.new_comment_plain_text_edit = PlainTextEdit()

        self.scroll_area = ScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(ScrollBarAlwaysOff)

    def setup(self):
        super().setup()

        self.deletion_func(self.main_layout)

        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)
        self.main_layout.addLayout(self.fourth_horizontal_layout)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.fifth_horizontal_layout)
        self.main_layout.addLayout(self.sixth_horizontal_layout)
        self.main_layout.addLayout(self.seventh_horizontal_layout)
        self.main_layout.addLayout(self.eight_horizontal_layout)

        self.submit_push_button.setVisible(True)
        self.support_ticket_push_button.setVisible(True)
        self.delete_ticket_push_button.setVisible(True)
        self.resolve_ticket_push_button.setVisible(True)

        self.scroll_area.setWidget(self.comment_section)

        self.first_horizontal_layout.addWidget(
            self.support_ticket_details_label, alignment=AlignCenter
        )
        self.second_horizontal_layout.addWidget(self.title_label, alignment=AlignCenter)
        self.third_horizontal_layout.addWidget(
            self.description_label, alignment=AlignCenter
        )
        self.fourth_horizontal_layout.addWidget(self.scroll_area, alignment=AlignCenter)
        self.form_layout.addRow("New Comment", self.new_comment_plain_text_edit)
        self.fifth_horizontal_layout.addWidget(
            self.submit_push_button, alignment=AlignCenter
        )
        self.sixth_horizontal_layout.addWidget(
            self.resolve_ticket_push_button, alignment=AlignCenter
        )
        self.seventh_horizontal_layout.addWidget(
            self.delete_ticket_push_button, alignment=AlignCenter
        )
        self.eight_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )
        self.eight_horizontal_layout.addWidget(
            self.support_ticket_push_button, alignment=AlignCenter
        )
    def teardown(self):
        super().teardown()

    def on_submit_clicked(self):
        try:
            success, _ = self.denarii_mobile_client.update_support_ticket(
                self.gui_user.user_id,
                self.support_ticket_id,
                self.new_comment_plain_text_edit.toPlainText(),
            )

            if success:
                self.status_message_box("Created comment successfully")
            else:
                self.status_message_box("Failed to create a comment")

            self.comment_details = self.get_support_ticket_comment_details()
            self.populate_comment_section()
        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

    def on_delete_clicked(self):
        try:
            success, _ = self.denarii_mobile_client.delete_support_ticket(
                self.gui_user.user_id, self.support_ticket_id
            )

            if success:
                self.status_message_box("Deleted ticket successfully")
                self.on_support_ticket_screen_clicked()
            else:
                self.status_message_box("Failed to delete ticket")

        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

    def on_resolve_clicked(self):
        try:
            success, _ = self.denarii_mobile_client.resolve_support_ticket(
                self.gui_user.user_id, self.support_ticket_id
            )

            if success:
                self.status_message_box("Resolved ticket successfully")
            else:
                self.status_message_box("Failed to resolve the ticket")

        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

    def get_support_ticket_details(self):
        try:
            success, res = self.denarii_mobile_client.get_support_ticket(
                self.gui_user.user_id, self.support_ticket_id
            )

            if success:
                return res[0]
            else:
                return {"title": "", "description": ""}

        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

        return {"title": "", "description": ""}

    def get_support_ticket_comment_details(self):
        try:
            success, res = self.denarii_mobile_client.get_comments_on_ticket(
                self.gui_user.user_id, self.support_ticket_id
            )
            if success:
                return res
            else:
                return []
        except Exception as e:
            print(e)
            self.status_message_box("Failed: unknown error")

        return []

    def populate_comment_section(self):
        
        self.depopulate_comment_section()
        for comment in self.comment_details:
            self.comment_section.addComment(
                comment["author"], comment["content"], comment["updated_time_body"]
            )
            
    def depopulate_comment_section(self):
        self.comment_section.clearComments()
