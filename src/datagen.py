import os
import json
from typing import Tuple
import numpy as np
from src.helpers import PATH_DATA


HALF_DECK_SIZE = 26


class DeckGenerator:
    """
    Class for generating decks for a given seed
    Generation follows a deterministic order by seed by saving random states. 
    """
    def __init__(self, seed: int, half_deck_size: int = HALF_DECK_SIZE):
        self.seed = seed
        self.half_deck_size = half_deck_size
        self.init_deck = [0] * half_deck_size + [1] * half_deck_size
        self.rng = np.random.default_rng(seed)
        # Check if state exists, if so load it, otherwise create a new save
        state = self.load_rng_state()
        if state:
            self.rng.bit_generator.state = state
        else:
            self._save_rng_state()

    def create_decks(self, n_decks: int) -> np.ndarray:
        """
        Generate and return n shuffled decks
        All generated decks and the RNG state are always saved
        """
        # Restore existing RNG state if possible
        state = self.load_rng_state()
        if state:
            self.rng.bit_generator.state = state

        # Shuffle decks
        decks = np.tile(self.init_deck, (n_decks, 1))
        self.rng.permuted(decks, axis=1, out=decks)

        # Save the decks and RNG state
        path = f"{PATH_DATA}/{self.seed}.npy"
        if os.path.exists(path):
            decks = np.vstack((self.load_decks(), decks))  # Append new decks
        np.save(path, decks)
        self._save_rng_state()

        return decks

    def _save_rng_state(self) -> None:
        """
        Save the current RNG state
        """
        with open(f"{PATH_DATA}/{self.seed}state.json", "w") as f:
            json.dump(self.rng.bit_generator.state, f)

    def load_rng_state(self) -> None:
        """
        Load the RNG state
        """
        if os.path.exists(f"{PATH_DATA}/{self.seed}state.json"):
            with open(f"{PATH_DATA}/{self.seed}state.json", "r") as f:
                state = json.load(f)
                return state
        else:
            return None

    def load_decks(self) -> np.ndarray:
        """
        Load previously stored decks from a .npy file.
        """
        return np.load(f"{PATH_DATA}/{self.seed}.npy")
