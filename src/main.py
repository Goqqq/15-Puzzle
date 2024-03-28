from ui.gui import Gui
from api import (
    create_puzzle,
    start_puzzle,
    PuzzleSize,
    TileMode,
    DuplicationMode,
)


def main():
    Gui.run_gui()
    
    # For testing purposes
    # puzzle = create_puzzle(PuzzleSize.SMALL, TileMode.MIXED, DuplicationMode.DUPLICATED, 4)
    # start_puzzle(puzzle, 1)


if __name__ == "__main__":
    main()
