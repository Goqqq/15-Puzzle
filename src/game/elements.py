import copy
import math
import random
from typing import List
from game.tiles import Tile
from itertools import permutations


class Elements:
    def __init__(self, count: int):
        self.side_length = int(math.sqrt(count))  # ! rethink this for 3x4
        self.goal_state: List[Tile] = [
            Tile(
                0 if i == j == self.side_length - 1 else self.side_length * i + j + 1,
                i,
                j,
            )
            for i in range(self.side_length)
            for j in range(self.side_length)
        ]
        self.__moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

    def shuffle_(self, complexity: int) -> List[List[int]]:
        movesCount: int = complexity * 3
        state = self.goal_state
        row, col = self.goal_state[-1].row, self.goal_state[-1].col

        for _ in range(movesCount):
            valid_moves = []
            for name, (dr, dc) in self.__moves.items():
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.side_length and 0 <= new_col < self.side_length:
                    valid_moves.append((new_row, new_col))

            if not valid_moves:
                continue

            new_row, new_col = random.choice(valid_moves)
            # Find the tiles to swap based on their current positions
            blank_index = row * self.side_length + col
            target_index = new_row * self.side_length + new_col
            # Swap the blank tile with the target tile
            state[blank_index], state[target_index] = (
                state[target_index],
                state[blank_index],
            )
            state[blank_index].row, state[blank_index].col = row, col
            state[target_index].row, state[target_index].col = new_row, new_col

            row, col = new_row, new_col  # Update the position of the blank

        return state

    def is_goal_state(self, state: List[Tile]) -> bool:
        return all(
            tile.row == tile.val // self.side_length
            and tile.col == tile.val % self.side_length
            for tile in state
        )

    def shuffle(self, complexity: int) -> List[Tile]:
        movesCount: int = complexity * 3
        state = [
            Tile(tile.val, tile.row, tile.col) for tile in self.goal_state
        ]  # Deep copy to prevent modifying the goal_state
        blank_index = (
            self.side_length * self.side_length - 1
        )  # Assuming the last tile is the blank
        row, col = state[blank_index].row, state[blank_index].col

        while movesCount > 0 or self.is_goal_state(state):
            valid_moves = []
            for name, (dr, dc) in self.__moves.items():
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.side_length and 0 <= new_col < self.side_length:
                    valid_moves.append((new_row, new_col))

            if not valid_moves:
                continue

            new_row, new_col = random.choice(valid_moves)
            # Swap logic based on row and col, find the tiles to swap
            blank_index = [
                i for i, tile in enumerate(state) if tile.row == row and tile.col == col
            ][0]
            target_index = [
                i
                for i, tile in enumerate(state)
                if tile.row == new_row and tile.col == new_col
            ][0]

            # Update the row and col of swapped tiles
            (
                state[blank_index].row,
                state[blank_index].col,
                state[target_index].row,
                state[target_index].col,
            ) = (new_row, new_col, row, col)

            state[blank_index], state[target_index] = (
                state[target_index],
                state[blank_index],
            )

            row, col = new_row, new_col  # Update the position of the blank
            movesCount -= 1

        return state
