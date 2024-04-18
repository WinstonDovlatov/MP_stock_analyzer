from matrix_profile.analyzer import get_last_day_score
import time


class Informant:
    def __init__(self, update_freq=3600):
        self.day = None
        self.score = None
        self.update_freq = update_freq
        self.update()

    def update(self):
        day, score = get_last_day_score()
        self.day = day
        self.score = score
        time.sleep(self.update_freq)
