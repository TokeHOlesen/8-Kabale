class DoubleClick:
    def __init__(self, time_window=30):
        self._time_window = time_window  # How many frames max between clicks to register as double
        self._initiated = False  # Changes to true whenever a click occurs; increments timer when on
        self._timer = 0  # Increments by one every frame if self.initiated is True
        self._click_counter = 0  # Counts MOUSEBUTTONUP events

    def _reset(self):
        self._click_counter = 0
        self._timer = 0
        self._initiated = False

    def _increment_timer(self):
        self._timer += 1

    def increment_clicks(self):
        """Run this when a MOUSEBUTTONUP event registers"""
        self._initiated = True
        self._click_counter += 1

    def update(self):
        """Run this in the beginning of the game loop"""
        if self._timer > self._time_window:
            self._reset()
        if self._initiated:
            self._increment_timer()

    def double_clicked(self):
        """Returns True if a double click has been registered"""
        if self._click_counter == 2 and self._timer <= self._time_window:
            self._reset()
            return True
        return False
