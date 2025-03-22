import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from src.processing import Evaluator
from src.datagen import DeckGenerator


class Plotter:
    def __init__(self, seed: int):
        self.eval = Evaluator(seed)
        self.sampleSize = len(DeckGenerator(seed).load_decks())
        self.trick_probs, self.cards_probs = self.eval.get_wins()

    def plot_trick_winning_probs(self) -> None:
        self._plot_heatmap(
            self.trick_probs,
            f"Player Win Rates By Tricks Over {self.sampleSize} Games",
        )

    def plot_cards_won_probs(self) -> None:
        self._plot_heatmap(
            self.cards_probs,
            f"Player Win Rates By Cards Over {self.sampleSize} Games",
        )

    def _plot_heatmap(self, df: pd.DataFrame, title: str) -> None:
        # change column names with 1 to R and 0 to B
        # ex: 111 -> RRR, 000 -> BBB
        df.index = df.index.str.replace("1", "R").str.replace("0", "B")


        # Create a mask for shared diagonal values
        mask = np.eye(df.shape[0], df.shape[1], dtype=bool)
        cmap = sns.diverging_palette(10, 250, as_cmap=True)

        plt.figure(figsize=(8, 6))
        ax = sns.heatmap(
            df,
            annot=True,
            cmap=cmap,
            linewidths=0.5,
            fmt=".2f",
            mask=mask,
            cbar=False,
        )

        # Adjust label spacing
        plt.xlabel("Opponent Sequences", fontsize=12, labelpad=12)
        plt.ylabel("Player Sequences", fontsize=12, labelpad=12)
        plt.title(title, fontsize=14)

    
    def plot(self) -> None:
        self.plot_trick_winning_probs()
        self.plot_cards_won_probs()
        plt.savefig('data/trick_winning_probs.png')
        plt.savefig('data/cards_won_probs.png')
        plt.show()
        
