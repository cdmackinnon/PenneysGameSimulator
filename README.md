# Penney's Game Simulator

## Description
Penney's Game is a two-player game where each player selects a sequence of "Heads" and "Tails" on a coin. The coin is flipped until either sequence occurs, and whoever's first wins. [Wikipedia](https://en.wikipedia.org/wiki/Penney%27s_game) covers its key aspects and insights. This specific program simulates a version of the game using playing cards with red or black cards. This introduces a new layer of conditional probability. It generates decks and visualizes the game outcomes in heatmaps that display winning and tie probabilities based on different criteria (i.e. winning by a majority of tricks or cards).

## Features
- **Deck Generation**: Generate decks of card sequences based on a provided seed.
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
6. Follow the on-screen prompts to generate decks or calculate results and plot results.

## Expected Inputs
- For generating decks:
  - Seed (integer): A number to seed the random number generator.
  - Number of decks (integer): The number of decks to generate.
  - _Note: Seeds are persistent and generated decks and random states will be stored across runtimes for deterministic behavior._
  
- For plotting results:
  - Seed (integer): A number for which generated decks to use (must be consistent with one used in deck generation).
 
**Seed 0 contains 1M precomputed decks for which a heatmap can be instantly generated. Choose option 2 and input seed 0 to view this.**

## TODOs
- Implement user input validation to handle unexpected or incorrect inputs gracefully.
- Develop unit tests for key functionalities (e.g. deck generation).
- Add edge case handling, including:
  - Pathing Issues
  - Manage cases where no decks are generated before plotting.
- Enhance user experience with clearer prompts and error messages.

