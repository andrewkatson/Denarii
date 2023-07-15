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


class VerifyResetScreen(Screen):
    def __init__(
        self,
        main_layout,
        deletion_func,
        denarii_client,
        gui_user,
        denarii_mobile_client,
        **kwargs
    ):
        self.verify_reset_label = None 
        self.reset_id_line_edit = None 
        self.submit_button = None

        super().__init__(
            self.verify_reset_screen_name,
            main_layout,
            deletion_func,
            denarii_client,
            gui_user,
            denarii_mobile_client,
            **kwargs
        )

    def init(self, **kwargs):
        super().init(**kwargs)

        self.next_button.setVisible(False)
        self.back_button.setVisible(True)

        self.verify_reset_label = Label("verify Reset")
        font = Font()
        font.setFamily("Arial")
        font.setPixelSize(50)
        self.verify_reset_label.setFont(font)

        self.reset_id_line_edit = LineEdit()

        self.submit_button = PushButton("Submit", kwargs["parent"])
        self.submit_button.clicked.connect(lambda: self.on_submit_clicked())
        self.submit_button.setVisible(False)
        self.submit_button.setStyleSheet(
            "QPushButton{font: 30pt Helvetica MS;} QPushButton::indicator { width: 30px; height: 30px;};"
        )

    def setup(self):
        super().setup()
        
        self.main_layout.addLayout(self.first_horizontal_layout)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.second_horizontal_layout)
        self.main_layout.addLayout(self.third_horizontal_layout)

        self.submit_button.setVisible(True)

        self.first_horizontal_layout.addWidget(self.verify_reset_label, alignment=AlignCenter)
        self.form_layout.addRow("Reset Id:", self.reset_id_line_edit)
        self.second_horizontal_layout.addWidget(self.submit_button, alignment=AlignCenter)
        self.third_horizontal_layout.addWidget(
            self.back_button, alignment=(AlignLeft | AlignBottom)
        )
        self.third_horizontal_layout.addWidget(
            self.next_button, alignment=(AlignRight | AlignBottom)
        )
        
    def teardown(self):
        super().teardown()

    
    def on_submit_clicked(self):

        try: 
            name_or_email = ""
            if self.gui_user.name != "": 
                name_or_email = self.gui_user.name
            else:
                name_or_email = self.gui_user.email

            success = self.denarii_mobile_client.verify_reset(name_or_email, self.reset_id_line_edit.text())

            if success: 
                self.status_message_box("Success")
                self.next_button.setVisible(True)
            else: 
                self.status_message_box("Failed to verify reset")
                self.next_button.setVisible(False)

        except Exception as e:
            print(e)
            self.status_message_box("Failed unknown error")
            self.next_button.setVisible(False)
