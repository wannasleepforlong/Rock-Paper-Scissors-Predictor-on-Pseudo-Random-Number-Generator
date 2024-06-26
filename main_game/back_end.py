import datetime

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


def _scoring(round_decision):
    if round_decision == -1:  # Computer Win
        return -10
    elif round_decision == 0:  # Computer Draw
        return -9
    else:  # Computer Loss
        return 10


class BackEnd:
    def __init__(self, unique_username: str, unique_token: str, start_previous_session: bool, wins_required: int):
        self.wins_required = wins_required

        self.cur_game = 0
        self.cur_round = 0
        self.computer_score = 0
        self.player_score = 0
        self.models = [
            # mod.RandomModel("random_model", max_counter=20),
            mod.MarkovChain("m2_model", 2, discount_factor=1),
            mod.MarkovChain("m2.95_model", 2, discount_factor=0.95),
            mod.MarkovChain("m2.90_model", 2, discount_factor=0.90),
            mod.MarkovChain("m3_model", 3, discount_factor=1),
            mod.MarkovChain("m3.995_model", 3, discount_factor=0.995),
            mod.MarkovChain("m3.985_model", 3, discount_factor=0.985),
            mod.MarkovChain("m3.975_model", 3, discount_factor=0.975),
            mod.MarkovChain("m4_model", 4, discount_factor=1),
            mod.MarkovChain("m4.9995_model", 4, discount_factor=0.9995),
            mod.MarkovChain("m4.9985_model", 4, discount_factor=0.9985),
            mod.MarkovChain("m4.9985_model", 4, discount_factor=0.9975),
            mod.MarkovChain("m4_model", 5, discount_factor=1),
            mod.MarkovChain("m3.99.T_model", num=3, enemy_counting=True, discount_factor=0.99),
            mod.MarkovChain("m3.98.T_model", num=3, enemy_counting=True, discount_factor=0.98),
            mod.MarkovChain("m3.97.T_model", num=3, enemy_counting=True, discount_factor=0.97),
        ]
        self.url = f"{unique_username}{unique_token}.csv"  # TODO: Create your own url pattern later
        if start_previous_session:
            pass
            # TODO: get_previous_game_info
        else:
            header_string = "game_id,round,pointC,pointP,moveC,moveP,winner,model_choice,timestamp"
            for model in self.models:
                header_string += "," + model.model_name
            header_string += "\n"
            with open(self.url, mode='w') as file:
                file.write(header_string)

        self.model_choice = 0

    def update_value(self, computer_move, player_move):
        [model.add_data(player_move, computer_move) for model in self.models]
        choice_decision = decision(computer_move, player_move)
        winner_str = "Draw"
        if choice_decision == -1:
            self.computer_score += 1
            winner_str = "Computer"
        elif choice_decision == 1:
            self.player_score += 1
            winner_str = "Player"

        round_result = [self.cur_game, self.cur_round, self.computer_score, self.player_score, computer_move,
                        player_move, winner_str, self.models[self.model_choice].model_name,
                        datetime.datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")]
        round_result += [decision(model.decision(new=False), player_move) for model in self.models]
        round_result = map(str, round_result)
        round_result_str = ','.join(round_result) + '\n'
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
        data = pd.read_csv(self.url)
        return data

    def get_scores(self):
        return self.computer_score, self.player_score

    def choose_computer_move(self):
        data = self._get_csv_data()
        score_array = np.array([model.score(data) for model in self.models])
        self.model_choice = np.argmax(score_array)
        # print(f"Model_name: {self.models[self.model_choice].model_name}")
        [model.decision() for model in self.models]  # New Decisions from all models
        return self.models[self.model_choice].decision(new=False)


back_end = BackEnd("Test", "1", False, 2)
