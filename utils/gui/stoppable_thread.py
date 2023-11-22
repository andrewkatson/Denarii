import threading


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self._start_event = threading.Event()

    def start(self) -> None:
        if not self.is_alive() and not self._start_event.is_set():
            self._start_event.set()
            super().start()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        if self._stop_event.is_set():
            self._start_event.set()
        return self._stop_event.is_set()
