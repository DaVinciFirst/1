import os

class GameStats():
    def __init__(self, aw_settings):
        self.aw_settings = aw_settings
        self.reset_stats()
        self.game_active = False
        if os.path.exists(os.path.join(os.path.dirname(__file__), 'config.cfg')):
            with open("config.cfg", "r") as conf:
                self.high_score = int(conf.read())
        else:
            with open("config.cfg", "w") as conf:
                self.high_score = 0
                conf.write("0")


    def reset_stats(self):
        self.ships_left = self.aw_settings.ship_limit
        self.score = 0
        self.level = 1