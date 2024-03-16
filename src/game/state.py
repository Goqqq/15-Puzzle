from itertools import permutations
import math
from game.tiles import Tile
from typing import List
from game.moves import Moves


class State:
    def __init__(self, current_state: List[Tile], count: int):
        self.side_length = int(math.sqrt(count))
        self.goal_state: List[Tile] = self.generate_goal_state()
        self.moves: Moves = Moves()
        self.state
        self.blank_tile = 0  # Assuming '0' represents the blank/empty tile

    def get_blank_tile_index(self) -> int:
        return self.state.index(
            next(tile for tile in self.state if tile.val == self.blank_tile)
        )

    def get_target_tile_index(self, row: int, col: int) -> int:
        return self.state.index(
            next(tile for tile in self.state if tile.row == row and tile.col == col)
        )

    def update_state(
        self, blank_index: int, target_index: int, new_row: int, new_col: int
    ) -> None:
        (
            self.state[blank_index].row,
            self.state[blank_index].col,
            self.state[target_index].row,
            self.state[target_index].col,
        ) = (new_row, new_col, self.state[blank_index].row, self.state[blank_index].col)

        self.state[blank_index], self.state[target_index] = (
            self.state[target_index],
            self.state[blank_index],
        )

    def generate_all_states(self) -> List[List[Tile]]:
        all_states: List[List[Tile]] = []

        # Generate all permutations of the numbers 0 to 8
        for perm in permutations(range(9)):
            state = []
            state_to_check = []
            blank_row: int
            for i in range(9):
                # Calculate the row and col of the tile
                row, col = divmod(i, 3)
                # Create a new Tile and add it to the state
                state.append(Tile(perm[i], row, col))
                if perm[i] != 0:
                    state_to_check.append(perm[i])
                else:
                    blank_row = row
            # Add the state to the list of all states
            if self.state_is_solvable(state_to_check, blank_row):
                all_states.append(state)

        # return [[Tile.to_dict(tile) for tile in state] for state in all_states]
        return all_states

    def state_is_solvable(self, state: List[Tile], blank_row: int) -> bool:
        inversions: int = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] > state[j]:
                    inversions += 1

        # For odd-sized boards, the number of inversions must be even
        if self.side_length % 2 != 0:
            return inversions % 2 == 0

        # For boards with an even width, we need to also check the row of the blank tile
        else:
            blank_row_from_bottom: int = self.side_length - blank_row
            if blank_row_from_bottom % 2 == 0:  # Blank on even row from bottom
                return inversions % 2 != 0
            else:  # Blank on odd row from bottom
                return inversions % 2 == 0

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

    def generate_goal_state(self) -> List[Tile]:
        return [
            Tile(
                0 if i == j == self.side_length - 1 else self.side_length * i + j + 1,
                i,
                j,
            )
            for i in range(self.side_length)
            for j in range(self.side_length)
        ]
