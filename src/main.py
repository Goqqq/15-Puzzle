import random
import tkinter as tk
from typing import List
from game.tiles import Tile
from welcome import create_welcome_window
from game.puzzle import Puzzle
import os
from game.elements import Elements
from game.utils import log_matrix
import json
import pickle
from game.state import State

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

    puzzle: Puzzle = Puzzle(9)
    puzzle.start(3)


if __name__ == "__main__":
    main()
