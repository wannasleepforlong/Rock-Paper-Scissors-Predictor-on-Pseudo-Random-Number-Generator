import random

import numpy as np


class Model:
    def __init__(self, model_name):
        self.power_score = 2
        self.model_name = model_name

    def get_name(self):
        return self.model_name

    def score(self, data: dict):  # This code is correctly giving the required score
        winning_result = data.get(self.model_name)
        winning_score_list = [((i + 1) ** self.power_score * j) for i, j in enumerate(winning_result)]
        winning_score = sum(winning_score_list)
        normalised_winning_score = winning_score / sum(
            [((i + 1) ** self.power_score) for i, j in enumerate(winning_result)])
        return normalised_winning_score

    def decision(self):
        pass


class MarkovChain(Model):
    def __init__(self, model_name, num, enemy_counting=False):
        super().__init__(model_name)
        self.num = num
        self.state = None
        self._model_creation()
        self.past_order = "0" * num

    def _model_creation(self):
        self.state = np.zeros((3 ** self.num, 3))

    def add_data(self):
        print(self.state)

    def decision(self):
        super().decision()
        pass

    def score(self, data: dict):  # Todo: Temp placeholder later just delete
        return 0


class RandomModel(Model):
    def decision(self):
        super().decision()
        return random.randint(0, 2)

    def score(self, data: dict):  # Todo: Temp placeholder for testing later just delete
        return 1000
