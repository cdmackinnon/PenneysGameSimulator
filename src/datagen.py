import glob
import os
import json
import uuid
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
        # Github file limit is 100mb
        # To avoid reaching this limit decks are contained in multiple files
        # 200k decks is about 80mb, so we divide generation into 200k batches
        if n_decks > 200_000:
            self.create_decks(n_decks - 200_000)
            n_decks = 200_000

        # Restore existing RNG state if possible
        state = self.load_rng_state()
        if state:
            self.rng.bit_generator.state = state

        # Shuffle decks
        decks = np.tile(self.init_deck, (n_decks, 1))
        self.rng.permuted(decks, axis=1, out=decks)

        # Generates a uuid to differentiate npy files for the same seed
        unique_id = uuid.uuid4()

        # Save the decks and RNG state
        path = f"{PATH_DATA}/{self.seed}_{unique_id}.npy"

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
        # TODO add any error handling whatsoever...
        # Beware file not found, corrupted file, empty file

        # retreive every file corresponding to the seed
        file_list = glob.glob(f"{PATH_DATA}/{self.seed}_*.npy")
        # Combine all of the files of decks into one list
        decks = [np.load(file_path) for file_path in file_list]
        # Combine the decks into one array
        combined_decks = np.concatenate(decks, axis=0)
        return combined_decks

