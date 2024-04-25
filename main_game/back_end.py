import datetime


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

    def update_value(self, computer_move, player_move, decision, model_choice=0):
        # TODO: Check decision using a function later
        # TODO: Add model functionality here later
        if decision == -1:
            self.computer_score += 1
        elif decision == 1:
            self.player_score += 1

        round_result = [self.cur_game, self.cur_round, self.computer_score, self.player_score, computer_move,
                        player_move, decision, model_choice, datetime.datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")]
        round_result = map(str, round_result)
        round_result_str = ', '.join(round_result) + '\n'
        with open(self.url, mode='a') as file:
            file.write(round_result_str)
        self.cur_round += 1

        if self.wins_required in {self.computer_score, self.player_score}:
            self._new_game()

    def _new_game(self):
        self.cur_game += 1
        self.player_score = self.computer_score = self.cur_round = 0

    def get_csv_data(self):
        with open(self.url) as file:
            data = file.readlines()
        for index in range(len(data)):
            data[index] = data[index].strip().split(',')
        return data


back_end = BackEnd("Test", "1", False, 2)
