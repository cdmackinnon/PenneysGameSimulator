# Penney's Game Simulator

## Description
Penney's Game is a two-player game where each player selects a sequence of "Heads" and "Tails" to determine the winner based on specific outcomes. See [Wikipedia](https://en.wikipedia.org/wiki/Penney%27s_game) for a larger overview. This program simulates a version of the game using playing cards by red or black cards. It generates decks, evaluates game outcomes, and visualizes the results in heatmaps that display winning probabilities based on different criteria (i.e. winning by a majority of tricks or a majority of cards).

## Features
- **Deck Generation**: Generate decks of card sequences based on a provided seed.
- **Game Simulation**: Evaluate the aggregate results of numerous games based on player choices and display the number of tricks and cards won by each player.
- **Visualization**: Plot heatmaps showing the winning probabilities for each player based on tricks and cards.

## How to Run
1. Clone the repository
2. Install Python (3.12.4)
3. Install the required dependencies (using [uv](https://github.com/astral-sh/uv)):
   ```bash
   uv add numpy pandas matplotlib seaborn
   ```
5. Run the main script:
   ```bash
   uv run main.py
   ```
6. Follow the on-screen prompts to generate decks, simulate games, or plot results.

## Expected Inputs
- For generating decks:
  - Seed (integer): A number to seed the random number generator.
  - Number of decks (integer): The number of decks to generate.
  - _Note: Seeds are persistent and generated decks and random states will be stored across runtimes for deterministic behavior._
  
- For simulating games:
  - Seed (integer): A number for which generated decks to use (must be consistent with one used in deck generation).
  - Player One's choice: A string representing Player One's sequence (e.g., "000").
  - Player Two's choice: A string representing Player Two's sequence (e.g., "100").
  
- For plotting results:
  - Seed (integer): A number for which generated decks to use (must be consistent with one used in deck generation).

## TODOs
- Implement user input validation to handle unexpected or incorrect inputs gracefully.
- Develop unit tests for key functionalities (e.g., deck generation, game evaluation).
- Add edge case handling, including:
  - Input validation (invalid seeds, state machine inputs, etc.)
  - Pathing Issues
  - Manage cases where no decks are generated before simulating games or plotting.
- Enhance user experience with clearer prompts and error messages.

