# DO NOT MODIFY THIS FILE

import random


def play(player1, player2, num_games, verbose=False):
    p1_prev_play = ""
    p2_prev_play = ""
    results = {"p1": 0, "p2": 0, "tie": 0}

    for _ in range(num_games):
        p1_play = player1(p2_prev_play)
        p2_play = player2(p1_prev_play)

        if p1_play == p2_play:
            results["tie"] += 1
            winner = "Tie."
        elif (p1_play == "P" and p2_play == "R") or (
                p1_play == "R" and p2_play == "S") or (p1_play == "S"
                                                       and p2_play == "P"):
            results["p1"] += 1
            winner = "Player 1 wins."
        elif p2_play == "P" and p1_play == "R" or p2_play == "R" and p1_play == "S" or p2_play == "S" and p1_play == "P":
            results["p2"] += 1
            winner = "Player 2 wins."

        if verbose:
            print("Player 1:", p1_play, "| Player 2:", p2_play)
            print(winner)
            print()

        p1_prev_play = p1_play
        p2_prev_play = p2_play

    games_won = results['p2'] + results['p1']

    if games_won == 0:
        win_rate = 0
    else:
        win_rate = results['p1'] / games_won * 100

    print("Final results:", results)
    print(f"Player 1 win rate: {win_rate}%")

    return (win_rate)


def quincy(prev_play, counter=[0]):

    counter[0] += 1
    choices = ["R", "R", "P", "P", "S"]
    return choices[counter[0] % len(choices)]


def mrugesh(prev_opponent_play, opponent_history=[]):
    opponent_history.append(prev_opponent_play)
    last_ten = opponent_history[-10:]
    most_frequent = max(set(last_ten), key=last_ten.count)

    if most_frequent == '':
        most_frequent = "S"

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[most_frequent]


def kris(prev_opponent_play):
    if prev_opponent_play == '':
        prev_opponent_play = "R"
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prev_opponent_play]


def abbey(prev_opponent_play,
          opponent_history=[],
          play_order=[{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }]):

    if not prev_opponent_play:
        prev_opponent_play = 'R'
    opponent_history.append(prev_opponent_play)

    last_two = "".join(opponent_history[-2:])
    if len(last_two) == 2:
        play_order[0][last_two] += 1

    potential_plays = [
        prev_opponent_play + "R",
        prev_opponent_play + "P",
        prev_opponent_play + "S",
    ]

    sub_order = {
        k: play_order[0][k]
        for k in potential_plays if k in play_order[0]
    }

    prediction = max(sub_order, key=sub_order.get)[-1:]

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prediction]


def human(prev_opponent_play):
    play = ""
    while play not in ['R', 'P', 'S']:
        play = input("[R]ock, [P]aper, [S]cissors? ")
        print(play)
    return play


def random_player(prev_opponent_play):
    return random.choice(['R', 'P', 'S'])


import random

def player(prev_play, prob_matr = [{}], key = [""], guess = [""], counter = [0]):
    # 
    response = {"P": "S", "S": "R", "R": "P"} 

    
    if prev_play == "" or counter[0] > 70:  # configurable memory parameter (counter)
        prev_play = random.choice(["R", "P", "S"])
        guess[0] = random.choice(["R", "P", "S"])
        counter[0] = 0
        
        prob_matr[0] = {"RR": {"R": 0, "P": 0, "S": 0},
                     "RP": {"R": 0, "P": 0, "S": 0},
                     "RS": {"R": 0, "P": 0, "S": 0},
                     "PR": {"R": 0, "P": 0, "S": 0},
                     "PP": {"R": 0, "P": 0, "S": 0},
                     "PS": {"R": 0, "P": 0, "S": 0},
                     "SR": {"R": 0, "P": 0, "S": 0},
                     "SP": {"R": 0, "P": 0, "S": 0},
                     "SS": {"R": 0, "P": 0, "S": 0},       
            } # zeroing the pobability matrix
  
    
    counter[0] += 1

    if key[0] != "":
        prob_matr[0][key[0]][prev_play] += 1 # updating values of probability matrix


    key[0] = guess[0] + prev_play
    prediction = max(prob_matr[0][key[0]], key = lambda k: prob_matr[0][key[0]][k])
    guess[0] = response[prediction]

    return guess[0]



#####


def human_vs_bot(bot_strategy, num_rounds):
    results = {"human": 0, "bot": 0, "tie": 0}

    for _ in range(num_rounds):
        human_play = ""
        while human_play not in ['R', 'P', 'S']:
            human_play = input("[R]ock, [P]aper, [S]cissors? ").upper()

        bot_play = bot_strategy(human_play)
        
        print("You chose:", human_play)
        print("Bot chose:", bot_play)

        if human_play == bot_play:
            results["tie"] += 1
            print("It's a tie!")
        elif (human_play == "P" and bot_play == "R") or (
                human_play == "R" and bot_play == "S") or (human_play == "S"
                                                       and bot_play == "P"):
            results["human"] += 1
            print("You win!")
        else:
            results["bot"] += 1
            print("Bot wins!")

    print("Final results:", results)
    return results

# Example usage:
human_vs_bot(quincy, 20)  # Play 5 rounds against the 'quincy' strategy
