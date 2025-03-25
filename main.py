from src.datagen import DeckGenerator
from src.visualizing import Plotter



def main():
    while True:
        print("1. Generate new decks")
        # print("X. Simulate Games")
        print("2. Plot results")
        print("Exit\n")
        choice = input("Enter your choice: ")
        
        match choice:
            case "1":
                seed = int(input("Enter seed: "))
                n_decks = int(input("Enter number of decks: "))
                generator = DeckGenerator(seed)
                generator.create_decks(n_decks)
                print(f"Successfully generated {n_decks} decks with seed {seed}\n")
            # TODO: Reimplement this feature in the future
            # case "X":
            #     seed = int(input("Enter seed: "))
            #     playerOne = input("Enter player one's choice: ")
            #     playerTwo = input("Enter player two's choice: ")
            #     evaluator = Evaluator(seed)
            #     p1Tricks, p2Tricks, p1Cards, p2Cards = evaluator.evaluate_decks(playerOne, playerTwo)
            #     print(f"Player 1 Won {p1Tricks} Game(s) Off Tricks and {p1Cards} Off of Cards")
            #     print(f"Player 2 Won {p2Tricks} Game(s) Off Tricks and {p2Cards} Off of Cards\n")
            case "2":
                seed = int(input("Enter seed: "))
                plotter = Plotter(seed)
                # plotter.plot_trick_winning_probs()
                # plotter.plot_cards_won_probs()
                plotter.plot()
            case _:
                print("Unrecognized input or \"Exit\" entered\nExiting program")
                break
                

if __name__ == "__main__":
    main()
