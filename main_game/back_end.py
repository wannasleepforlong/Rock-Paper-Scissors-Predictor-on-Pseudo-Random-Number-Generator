import datetime
import random

import numpy as np

import ensemble_models as mod
import pandas as pd


def decision(computer_move, player_move):
    if (player_move == 0 and computer_move == 2) or (player_move == 1 and computer_move == 0) or (
            player_move == 2 and computer_move == 1):
        return 1
    elif (computer_move == 0 and player_move == 2) or (computer_move == 1 and player_move == 0) or (
            computer_move == 2 and player_move == 1):
        return -1
    else:
        return 0



class BackEnd:
    def __init__(self, unique_username: str, unique_token: str, start_previous_session: bool, wins_required: int):
        self.wins_required = wins_required

        self.cur_game = 0
        self.cur_round = 0
        self.computer_score = 0
        self.player_score = 0
        self.url = f"{unique_username}{unique_token}.csv"  # TODO: Create your own url pattern later
        if start_previous_session:
            pass
            # TODO: get_previous_game_info
        else:
            with open(self.url, mode='w') as file:
                file.write("game_id, round, pointC, pointP, moveC, moveP, winner, model_choice, timestamp\n")
        self.models = [mod.RandomModel("random"), mod.MarkovChain("m2", 2), ]
        self.model_choice = 0

    def update_value(self, computer_move, player_move):
        choice_decision = decision(computer_move, player_move)
        winner_str = "Draw"
        if choice_decision == -1:
            self.computer_score += 1
            winner_str = "Computer"
        elif choice_decision == 1:
            self.player_score += 1
            winner_str = "Player"

        round_result = [self.cur_game, self.cur_round, self.computer_score, self.player_score, computer_move,
                        player_move, winner_str, self.models[self.model_choice].model_name, datetime.datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")]
        round_result = map(str, round_result)
        round_result_str = ', '.join(round_result) + '\n'
        with open(self.url, mode='a') as file:
            file.write(round_result_str)
        self.cur_round += 1

        if self.wins_required in {self.computer_score, self.player_score}:
            self._new_game()

        return choice_decision

    def _new_game(self):
        self.cur_game += 1
        self.player_score = self.computer_score = self.cur_round = 0

    def _get_csv_data(self):
        data = pd.read_csv(self.url).to_dict()
        return data

    def get_scores(self):
        return self.computer_score, self.player_score

    def choose_computer_move(self):
        data = self._get_csv_data()
        self.model_choice = np.argmax(np.array([model.score(data) for model in self.models]))
        print(f"Model_name: {self.models[self.model_choice].model_name}")
        return self.models[self.model_choice].decision()


back_end = BackEnd("Test", "1", False, 2)
