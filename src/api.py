from game.puzzle import Puzzle, PuzzleSize
from game.tiles import TileMode, DuplicationMode


def create_puzzle(
    size: PuzzleSize,
    tile_mode: TileMode,
    repeat_mode: DuplicationMode,
    duplicates_count: int = None,
) -> Puzzle:
    """
    Create a puzzle with the given parameters.

    Args:
        size (PuzzleSize): The size of the puzzle.
        tile_mode (TileMode): The mode for selecting tiles.
        repeat_mode (DuplicationMode): The mode for duplicating tiles.
        duplicates_count (int, optional): The number of duplicates to create. Defaults to None.

    Returns:
        Puzzle: The created puzzle object.
    """
    return Puzzle(size, tile_mode, repeat_mode, duplicates_count)


def start_puzzle(puzzle: Puzzle, to_solve: int) -> bool:
    """
    Starts the puzzle solving process.

    Args:
        puzzle (Puzzle): The puzzle object to solve.
        to_solve (int): The number of puzzles to solve.

    Returns:
        bool: True if the puzzle solving process was started successfully.
    """
    puzzle.start(to_solve)
    return True
