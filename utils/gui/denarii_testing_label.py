class Label:
    def __init__(self, name) -> None:
        self.name = name
        self.font = None
        self.text_interaction_flags = []
        self.text = ""
        self.is_visible = False
        self.alignment = None
        self.pixmap = None

    def setFont(self, font):
        self.font = font

    def setTextInteractionFlags(self, new_flag):
        self.text_interaction_flags.append(new_flag)

    def setText(self, text):
        self.text = text

    def setVisible(self, visible):
        self.is_visible = visible

    def setAlignment(self, alignment):
        self.alignment = alignment

    def setPixmap(self, pixmap):
        self.pixmap = pixmap
