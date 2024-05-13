# RPS Predictor Bot using Markov Chains

## Introduction
This project implements a Rock Paper Scissors (RPS) predictor bot using Markov chains. The bot utilizes historical data of player moves to predict the opponent's next move based on patterns observed in previous round sequences.

## Features
- Implementation of Markov chain-based model for RPS prediction.
- Support for variable length history for pattern recognition.
- Option to consider both player and opponent moves or only player moves for model updates.
- Discounting of previous observations to adapt to changing patterns over time.
- Periodic self-clearing of model state to prevent overfitting and encourage adaptation.

## Usage
1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the `game.py` script to start the RPS predictor bot.
4. Play RPS against the bot and observe its predictions based on your moves.

## How it Works
- The bot maintains a state matrix representing the transition probabilities between different move patterns.
- Upon receiving player moves, the bot updates the state matrix based on the observed patterns.
- The bot uses the Markov chain model to predict the opponent's next move based on the current pattern of player moves.
- Predictions are made using the softmax function to convert raw output scores into probabilities.
