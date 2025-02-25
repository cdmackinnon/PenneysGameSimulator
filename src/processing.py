from src.helpers import PATH_DATA
from src.datagen import DeckGenerator
from typing import Tuple


class Evaluator:
    def __init__(self, seed: int):
        self.seed = seed

    def evaluate(self, playerOne: str, playerTwo: str) -> Tuple[int, int, int, int]:
        """
        Evaluate the winner in each previously saved deck for a seed.

        Returns p1Tricks, p2Tricks, p1Cards, p2Cards
        """
        decks = DeckGenerator(self.seed).load_decks()
        p1Tricks, p2Tricks = 0, 0
        p1Cards, p2Cards = 0, 0
        for deck in decks:
            deck_str = "".join(deck.astype(str))
            index = 0

            while index < len(deck_str):
                p1 = deck_str.find(playerOne, index)
                p2 = deck_str.find(playerTwo, index)
                # neither pattern is found
                if p1 == -1 and p2 == -1:
                    break
                # p1 win
                if p2 == -1 or (p1 != -1 and p1 < p2):
                    p1Tricks += 1
                    p1Cards += p1 - index + len(playerOne)
                    index = p1 + len(playerOne)
                # p2 win
                else:
                    p2Tricks += 1
                    p2Cards += p2 - index + len(playerTwo)
                    index = p2 + len(playerTwo)
        return p1Tricks, p2Tricks, p1Cards, p2Cards
