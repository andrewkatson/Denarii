import time

from stoppable_thread import StoppableThread


class ShowText:
    def __init__(self, text_box, text_to_show, time_seconds=2) -> None:
        self.text_box = text_box
        self.text_to_show = text_to_show
        self.time_seconds = time_seconds

        self.thread_to_show = StoppableThread(target=self.show_text)
        self.thread_to_show.start()

    def show_text(self):
        self.text_box.setVisible(True)
        self.text_box.setText(self.text_to_show)

        time.sleep(self.time_seconds)

        self.text_box.setText("")
        self.text_box.setVisible(False)
