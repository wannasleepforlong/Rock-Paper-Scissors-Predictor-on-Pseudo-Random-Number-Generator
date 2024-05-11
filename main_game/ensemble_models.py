import random

import numpy as np
import pandas as pd

IDEAL_RESPONSE = {'0': '1', '1': '2', '2': '0'}


class Model:
    def __init__(self, model_name):
        self.power_score = 2
        self.model_name = model_name

    def get_name(self):
        return self.model_name

    def score(self, data: pd.DataFrame):  # This code is correctly giving the required score
        winning_result = data.get(self.model_name)
        winning_score_list = [((i + 1) ** self.power_score * -j) for i, j in enumerate(winning_result)]
        winning_score = sum(winning_score_list)
        normalised_winning_score = winning_score / (sum(
            [((i + 1) ** self.power_score) for i, j in enumerate(winning_result)]) + 0.000001)
        return normalised_winning_score

    def decision(self, new=True):
        pass

    def add_data(self, player_move, computer_move):
        pass


class MarkovChain(Model):
    def __init__(self, model_name, num, enemy_counting=False, discount_factor=1):
        super().__init__(model_name)
        self.num = num
        self.state = None
        self._model_creation()
        self.enemy_counting = enemy_counting
        self.discount_factor = discount_factor
        self.player_history = num * "0"
        self.result = None

    def _model_creation(self):
        self.state = np.zeros((3 ** self.num, 3))

    def add_data(self, player_move, computer_move):
        self.state = self.state * self.discount_factor
        pattern_index = sum([int(val) * (3 ** index) for index, val in enumerate(self.player_history[::-1])])
        self.state[pattern_index, player_move] += 1
        if self.enemy_counting:
            self.player_history = self.player_history[1:] + str(player_move)
        else:
            self.player_history = self.player_history[2:] + str(player_move) + str(computer_move)
            # This will allow the computer to also calculate patters based on its moves
        # print(self.state)

    def decision(self, new=True):
        super().decision(new)
        if new:
            pattern_index = sum([int(val) * (3 ** index) for index, val in enumerate(self.player_history[::-1])])
            prediction = np.argmax(self.state[pattern_index])
            self.result = int(IDEAL_RESPONSE[str(prediction)])
        return self.result


class RandomModel(Model):
    def __init__(self, model_name, max_counter):
        super().__init__(model_name)
        self.result = None
        self.max_counter = max_counter
        self.counter = 0

    def decision(self, new=True):
        super().decision()
        if new:
            self.result = random.randint(0, 2)
        return self.result

    def increase_counter(self):
        self.counter += 1

    def score(self, data: pd.DataFrame):
        self.increase_counter()
        if self.counter == self.max_counter:
            self.counter = 0
            return 100000000
        else:
            return super().score(data)
