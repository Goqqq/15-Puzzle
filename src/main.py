import random
import tkinter as tk
from game.tiles import Tile
from welcome import create_welcome_window
from game.solve_game import SolveGame
import os
from game.elements import Elements
from game.utils import log_matrix
import json
import pickle

# from src.mode_selection import create_mode_selection_window
# from src.game import start_game


def main():
    # Initialize the main application window
    # root = tk.Tk()
    # root.title("Puzzle Game")
    # root.geometry("800x600")  # Set your desired initial size
    # root.resizable(False, False)  # Prevent the window from being resized

    # # # You could set up a menu or any other components that are constant throughout your application here

    # # Start with the welcome window
    # create_welcome_window(root)

    # # Start the Tkinter event loop
    # root.mainloop()
    elements = Elements(9)
    # start_state = [
    #     [1, 2, 3],
    #     [4, 5, 6],
    #     [7, 8, 0],
    # ]
    dir_of_script = os.path.dirname(os.path.abspath(__file__))
    assets_path = os.path.join(dir_of_script, os.pardir, "assets")
    print(assets_path)
    # all_states_file = os.path.join(assets_path, "states", "all_states.json")
    all_states_file = os.path.join(assets_path, "states", "all_states.pkl")
    if os.path.exists(all_states_file):
        # with open(all_states_file, "r") as file:
        with open(all_states_file, "rb") as file:
            # all_states = json.load(file)
            all_states = pickle.load(file)
        # all_states = [[Tile.from_dict(tile) for tile in state] for state in all_states]
    else:
        all_states = elements.generate_all_states()
        # with open(all_states_file, "w") as file:
        with open(all_states_file, "wb") as file:
            # json.dump(all_states, file)
            pickle.dump(all_states, file)

    # start_state = elements.shuffle(10)
    start_state = all_states[random.randint(0, len(all_states))]
    solver = SolveGame(start_state, elements.goal_state)
    # random_state = SolveGame.shuffle(solver, 100)
    # solver.start_state = random_state
    log_matrix(start_state, 3)
    if True:
        solution = solver.solve()
        if solution:
            print("Solution found!")
            print(solution)
        else:
            print("No solution found.")
    else:
        print("The puzzle is not solvable.")


if __name__ == "__main__":
    main()
