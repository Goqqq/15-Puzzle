import random
import tkinter as tk
from typing import List
from game.tiles import Tile
from welcome import create_welcome_window
from game.puzzle import Puzzle, PuzzleSize
import os
from game.elements import Elements
from game.utils import log_matrix
import json
import pickle
from game.state import State
from game.tiles import TileMode, RepeatMode
from collections import Counter


def main():

    # puzzle: Puzzle = Puzzle(PuzzleSize.SMALL, TileMode.LETTERS, RepeatMode.REPEATED, 2)
    # puzzle: Puzzle = Puzzle(PuzzleSize.SMALL, TileMode.LETTERS, RepeatMode.UNIQUE)
    puzzle: Puzzle = Puzzle(PuzzleSize.MEDIUM, TileMode.NUMBERS, RepeatMode.REPEATED, 4)
    # puzzle: Puzzle = Puzzle(PuzzleSize.MEDIUM, TileMode.NUMBERS, RepeatMode.UNIQUE)
    # puzzle: Puzzle = Puzzle(PuzzleSize.SMALL, TileMode.MIXED, RepeatMode.UNIQUE)
    puzzle.start(1)


if __name__ == "__main__":
    main()
