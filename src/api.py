from game.puzzle import Puzzle, PuzzleSize
from game.tiles import TileMode, DuplicationMode


def create_puzzle(
    size: PuzzleSize,
    tile_mode: TileMode,
    repeat_mode: DuplicationMode,
    duplicates_count: int = None,
) -> Puzzle:
    return Puzzle(size, tile_mode, repeat_mode, duplicates_count)


def start_puzzle(puzzle: Puzzle, to_solve: int) -> bool:
    puzzle.start(to_solve)
    return True
