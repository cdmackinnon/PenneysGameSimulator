"""
Module for calculating and retrieving player win percentages
"""

import json
import os
from typing import Tuple
import numpy as np
import pandas as pd
from src.helpers import PATH_DATA
from src.datagen import DeckGenerator


HANDS = ["000", "001", "010", "011", "100", "101", "110", "111"]


class Evaluator:
    """
    Class supporting win calculations for a given seed.
    Stores statistics and how many decks they're for in a json file.
    """

    def __init__(self, seed: int):
        self.seed = seed
        self.results_path = f"{PATH_DATA}/{self.seed}_results.json"
        self.results = self._load_results()

    def _load_results(self) -> dict:
        """
        Load existing statistics from a json file
        If the file does not exist, return a default template
        """
        if os.path.exists(self.results_path):
            with open(self.results_path, "r") as f:
                return json.load(f)
        return {"num_decks": 0, "results": {}}

    def _save_results(self) -> None:
        """
        Save the result statistics to a json file
        """
        with open(self.results_path, "w") as f:
            json.dump(self.results, f)

    def _evaluate_decks(
        self, playerOne: str, playerTwo: str, decks: np.ndarray
    ) -> Tuple[int, int, int, int]:
        """
        Evaluate multiple decks to determine trick and card wins for both players.

        Return pattern is p1TrickWins, p2TrickWins, p1CardWins, p2CardWins
        """
        # TODO Casting arrays into strings and using string.find is expensive
        # consider keeping the elements in the array or using regex on the string

        # Initialize counts for tricks and cards won by each player
        p1TrickWins, p2TrickWins = 0, 0
        p1CardWins, p2CardWins = 0, 0

        for deck in decks:
            deck_str = "".join(deck.astype(str))
            p1Tricks, p2Tricks = 0, 0  # Reset counts for the current deck
            p1Cards, p2Cards = 0, 0  # Reset counts for the current deck
            index = 0

            while index < len(deck_str):
                p1 = deck_str.find(playerOne, index)
                p2 = deck_str.find(playerTwo, index)
                # neither pattern is found
                if p1 == -1 and p2 == -1:
                    break
                # same pattern is found for both players
                if p1 == p2:
                    p1Tricks += 1
                    p2Tricks += 1
                    cards_won = p1 - index + len(playerOne)
                    p1Cards += cards_won
                    p2Cards += cards_won
                    index = p1 + len(playerOne)
                # p1 win
                elif p2 == -1 or (p1 != -1 and p1 < p2):
                    p1Tricks += 1
                    p1Cards += p1 - index + len(playerOne)
                    index = p1 + len(playerOne)
                # p2 win
                else:
                    p2Tricks += 1
                    p2Cards += p2 - index + len(playerTwo)
                    index = p2 + len(playerTwo)

            # After evaluating the current deck, update the total counts
            # If tricks or cards are equal, we consider it a win for both players
            if p1Tricks >= p2Tricks:
                p1TrickWins += 1
            if p2Tricks >= p1Tricks:
                p2TrickWins += 1
            if p1Cards >= p2Cards:
                p1CardWins += 1
            if p2Cards >= p1Cards:
                p2CardWins += 1

        return p1TrickWins, p2TrickWins, p1CardWins, p2CardWins

    def _get_new_decks(self) -> np.ndarray:
        """
        Retreive new decks
        """
        decks = DeckGenerator(self.seed).load_decks()
        total_decks = len(decks)
        prev_decks = self.results.get("num_decks", 0)
        return decks[prev_decks:total_decks]

    def update_wins(self) -> None:
        """
        Update the results with newly generated decks since the last evaluation.
        Save the results to a json file.
        """
        new_decks = self._get_new_decks()

        # If there are no new decks, return
        if new_decks.size == 0:
            return

        for playerOne in HANDS:
            for playerTwo in HANDS:
                key = f"{playerOne}_{playerTwo}"
                if key not in self.results["results"]:
                    self.results["results"][key] = [0, 0, 0, 0]

                results = self._evaluate_decks(playerOne, playerTwo, new_decks)
                self.results["results"][key] = [
                    self.results["results"][key][i] + results[i] for i in range(4)
                ]

        self.results["num_decks"] += len(new_decks)
        self._save_results()

    def get_wins(self) -> pd.DataFrame:
        """
        Return a DataFrame with the win probabilities for each player
        """
        self.update_wins()
        # Initialize DataFrames for trick and card probabilities
        trick_probs = pd.DataFrame(index=HANDS, columns=HANDS)
        card_probs = pd.DataFrame(index=HANDS, columns=HANDS)

        # Populate DataFrames with results
        for key, value in self.results["results"].items():
            playerOne, playerTwo = key.split("_")
            p1Tricks, p2Tricks, p1Cards, p2Cards = value
            trick_probs.at[playerOne, playerTwo] = p1Tricks / (p1Tricks + p2Tricks)
            card_probs.at[playerOne, playerTwo] = p1Cards / (p1Cards + p2Cards)

        trick_probs = trick_probs.apply(pd.to_numeric, errors="coerce")
        card_probs = card_probs.apply(pd.to_numeric, errors="coerce")
        return trick_probs, card_probs
