import math
from typing import List
from game.state import State
import time
from game.tiles import Tile


def build_matrix_string(state: State) -> str:
    board_size: int = int(math.sqrt(len(state.state)))
    # Initialize an empty 2D array to represent the matrix
    matrix = [["" for _ in range(board_size)] for _ in range(board_size)]

    # Populate the matrix with tile indices based on their row and col
    for tile in state.state:
        matrix[tile.row][tile.col] = str(tile.val)

    # Build the matrix string
    matrix_str = ""
    for row in matrix:
        matrix_str += " ".join(row) + "\n"
    matrix_str += "------------------------------\n"

    return matrix_str


def log_matrix(state: State) -> None:
    print(build_matrix_string(state))


def write_matrix(state: State) -> str:
    return build_matrix_string(state)


def measure_time(func, *args, **kwargs) -> tuple:
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    time_taken: str = f"{end_time - start_time:.2f}"
    # print(f"Time taken by {func.__name__}: {end_time - start_time:.2f} seconds")
    return result, time_taken
