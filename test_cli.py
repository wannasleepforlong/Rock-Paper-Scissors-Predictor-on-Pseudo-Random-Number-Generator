import back_end as be
from prng import *

back_end = be.BackEnd("Test", "1", False, 5)
choice = ["Rock", "Paper", "Scissor"]

while True:
    player_choice = int(input("\n\nRock Paper Scissor Shoot!!!"))%3
    MT = MT()
    player_choice = MT.random()
    print(f"Your choice: {choice[player_choice]}")
    computer_choice = back_end.choose_computer_move()
    print(f"Computer choice: {choice[computer_choice]}")
    decision = back_end.update_value(computer_choice, player_choice)
    if decision == 0:
        print("Draw!")
    elif decision == -1:
        print("You lose!")
    else:
        print("You win!")
    print(back_end.get_scores())
