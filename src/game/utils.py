import math
from game.state import State
import time


def build_matrix_string(state: State) -> str:
    """
    Builds a matrix string representation of the game state.

    Args:
        state (State): The game state object.

    Returns:
        str: The matrix string representation of the game state.
    """
    # Calculate the board size based on the state length
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

    # Return the matrix string
    return matrix_str


def log_matrix(state: State) -> None:
    """
    Prints the matrix representation of the given state.

    Args:
        state (State): The state object to log.

    Returns:
        None
    """
    print(build_matrix_string(state))


def write_matrix(state: State) -> str:
    """
    Converts the given state into a matrix string representation.

    Args:
        state (State): The state object to convert.

    Returns:
        str: The matrix string representation of the state.
    """
    return build_matrix_string(state)


def measure_time(func, *args, **kwargs) -> tuple:
    """
    Measures the execution time of a function.

    Parameters:
    - func: The function to be measured.
    - *args: Positional arguments to be passed to the function.
    - **kwargs: Keyword arguments to be passed to the function.

    Returns:
    A tuple containing the result of the function and the time taken in seconds.
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    time_taken: str = f"{end_time - start_time:.2f}"
    return result, time_taken
