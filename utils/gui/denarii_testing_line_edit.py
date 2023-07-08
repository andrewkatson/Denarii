class LineEdit:
    def __init__(self) -> None:
        self.echo_mode = None
        self.text_inner = ""

    def Password(self):
        pass

    def setEchoMode(self, echo_mode):
        self.echo_mode = echo_mode

    def text(self):
        return self.text_inner
