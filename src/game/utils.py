from typing import List

from game.tiles import Tile


def log_matrix(tiles: List[Tile], board_size: int) -> None:
    # Initialize an empty 2D array to represent the matrix
    matrix = [["" for _ in range(board_size)] for _ in range(board_size)]

    # Populate the matrix with tile indices based on their row and col
    for tile in tiles:
        matrix[tile.row][tile.col] = str(tile.val)

    # Print the matrix
    for row in matrix:
        print(" ".join(row))
    print("------------------------------")
