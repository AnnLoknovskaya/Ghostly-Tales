import json
import os

SAVE_PATH = "savegame.json"

class Data:
    def __init__(self, ui):
        self.ui = ui
        self._coins = 0
        self._health = 5

        self.unlocked_level = 0
        self.current_level = 0
        self.max_level = 18

        self.load()  # Загружаем сохранение, если оно есть

        self.ui.show_coins(self._coins)
        self.ui.create_hearts(self._health)

    def save(self):
        data = {
            "coins": self._coins,
            "health": self._health,
            "unlocked_level": self.unlocked_level,
            "current_level": self.current_level
        }
        with open(SAVE_PATH, "w") as file:
            json.dump(data, file)

    def load(self):
        if os.path.exists(SAVE_PATH):
            with open(SAVE_PATH, "r") as file:
                data = json.load(file)
                self._coins = data.get("coins", 0)
                self._health = data.get("health", 5)
                self.unlocked_level = data.get("unlocked_level", 0)
                self.current_level = data.get("current_level", 0)

    def reset(self):
        self._coins = 0
        self._health = 5
        self.unlocked_level = 0
        self.current_level = 0
        self.ui.show_coins(self._coins)
        self.ui.create_hearts(self._health)
        self.save()

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, value):
        self._coins = value
        if self.coins >= 100:
            self.coins -= 100
            self.health += 1
        self.ui.show_coins(self.coins)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        self.ui.create_hearts(value)


