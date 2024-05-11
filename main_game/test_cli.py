import back_end as be
from pseudo_random__tester import prng
import pandas as pd
from tqdm import tqdm
import gc

choice = ["Rock", "Paper", "Scissor"]

back_end = be.BackEnd("Test", "1", False, 5)
for _ in (range(5000)):

    player_choice = input("\n\nRock Paper Scissor Shoot!!!").strip()
    if not player_choice.isdigit():
        break
    player_choice = int(player_choice)%3
    print(f"Your choice: {choice[player_choice]}")
    # prng_object = prng.MT()
    # player_choice = prng_object.random()
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

data = pd.read_csv("Test1.csv").get("winner").to_list()
winner_count = data.count("Computer")
loser_count = data.count("Player")

print(f"Winner_Count: {winner_count}")
print(f"Loser_Count: {loser_count}")
print(f"Ratio: {winner_count / (winner_count + loser_count)}")
