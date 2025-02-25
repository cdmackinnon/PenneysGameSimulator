import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from src.processing import Evaluator


class Plotter:
    def __init__(self, playerInputs: list, seed: int):
        self.df_trick_winning_probs = pd.DataFrame()
        self.df_cards_won_probs = pd.DataFrame()
        self.eval = Evaluator(seed)
        self.playerInputs = playerInputs

        for playerOne in self.playerInputs:
            for playerTwo in self.playerInputs:
                results = self.eval.evaluate(playerOne, playerTwo)
                # player 1 win probability (based on tricks)
                self.df_trick_winning_probs.at[playerOne, playerTwo] = results[0] / (
                    results[0] + results[1]
                )
                # player 1 win probability (based on cards)
                self.df_cards_won_probs.at[playerOne, playerTwo] = results[2] / (
                    results[2] + results[3]
                )

    def plot_trick_winning_probs(self):
        self._plot_heatmap(
            self.df_trick_winning_probs,
            "Penney's Game Player One Wins by Tricks",
        )

    def plot_cards_won_probs(self):
        self._plot_heatmap(
            self.df_cards_won_probs, "Penney's Game Player One Wins by Cards"
        )

    def _plot_heatmap(self, df, title):
        # Create a mask for the complement values
        mask = np.triu(np.ones(df.shape, dtype=bool))
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
        plt.xlabel("Player Two Sequences", fontsize=12, labelpad=12)
        plt.ylabel("Player One Sequences", fontsize=12, labelpad=12)
        plt.title(title, fontsize=14)

        # Adjust tick labels to remove the masked first row and column
        ax.set_yticks(ax.get_yticks()[1:8], labels=df.index[1:8])
        ax.set_xticks(ax.get_xticks()[0:7], labels=df.columns[0:7])

        plt.show()
