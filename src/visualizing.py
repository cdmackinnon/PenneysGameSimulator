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
            f"Player Win Percents By Tricks Over {self.sampleSize} Games",
        )

    def plot_cards_won_probs(self) -> None:
        self._plot_heatmap(
            self.cards_probs,
            f"Player Win Percents By Cards Over {self.sampleSize} Games",
        )

    def _plot_heatmap(self, df: pd.DataFrame, title: str) -> None:
        # Change column names with 1 to R and 0 to B (e.g., 111 -> RRR, 000 -> BBB)
        df.index = df.index.str.replace("1", "R").str.replace("0", "B")
        df.columns = df.columns.str.replace("1", "R").str.replace("0", "B")

        # Extract win and tie probabilities as percentages
        win_probs = df.map(lambda x: float(x.split(" ")[0]) * 100)
        tie_probs = df.map(lambda x: float(x.split(" ")[1]) * 100)

        # Format the annotation win(tie) percentages
        annotations = win_probs.map(lambda win: f"{int(win)}") + tie_probs.map(lambda tie: f"({int(tie)})")

        # Create a mask for shared diagonal values
        mask = np.eye(df.shape[0], df.shape[1], dtype=bool)
        cmap = sns.diverging_palette(10, 250, as_cmap=True)

        plt.figure(figsize=(8, 6))
        ax = sns.heatmap(
            win_probs,
            annot=annotations,
            cmap=cmap,
            linewidths=0.5,
            fmt="",
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
        
