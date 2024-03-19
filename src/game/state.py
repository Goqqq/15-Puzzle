from itertools import permutations
import math
import random
from game.tiles import Tile
from typing import List, Tuple
from game.moves import Moves


class State:
    def __init__(self, tiles: List[Tile]):
        self.moves: Moves = Moves()
        self.state: List[Tile] = tiles

    def get_blank_tile_index(self) -> int:
        return self.state.index(
            next(tile for tile in self.state if tile.val == Tile.blank_tile)
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

    @staticmethod
    def state_is_solvable(state: List[Tile], blank_row: int, n: int) -> bool:
        inversions: int = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] > state[j]:
                    inversions += 1

        # For odd-sized boards, the number of inversions must be even
        if n % 2 != 0:
            return inversions % 2 == 0

        # For boards with an even width, we need to also check the row of the blank tile
        else:
            blank_row_from_bottom: int = n - blank_row
            if blank_row_from_bottom % 2 == 0:  # Blank on even row from bottom
                return inversions % 2 != 0
            else:  # Blank on odd row from bottom
                return inversions % 2 == 0

    @staticmethod
    def generate_all_states(size: int) -> List[List[Tile]]:
        side_length: int = int(math.sqrt(size))
        all_states: List[State] = []
        # Generate all permutations of the numbers 0 to 8
        for perm in permutations(range(size)):
            state = []
            state_to_check = []
            blank_row: int
            for i in range(size):
                # Calculate the row and col of the tile
                row, col = divmod(i, side_length)
                # Create a new Tile and add it to the state
                state.append(Tile(perm[i], row, col))
                if perm[i] != 0:
                    state_to_check.append(perm[i])
                else:
                    blank_row = row
            # Add the state to the list of all states
            if State.state_is_solvable(state_to_check, blank_row, side_length):
                all_states.append(State(state))
        return all_states

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

    @staticmethod
    def generate_goal_state(side_length: int) -> List[Tile]:
        return [
            Tile(
                0 if i == j == side_length - 1 else side_length * i + j + 1,
                i,
                j,
            )
            for i in range(side_length)
            for j in range(side_length)
        ]

    def state_to_tuple(self) -> Tuple[Tuple[int, int, int], ...]:
        return tuple((tile.val, tile.row, tile.col) for tile in self.state)

    def deep_copy(self) -> "State":
        return State([Tile(tile.val, tile.row, tile.col) for tile in self.state])

    def get_neighbors(
        self, side_length: int
    ) -> List[Tuple[List["State"], str]]:  # todo: check if this is the correct type
        neighbors = []
        # Find the blank tile's position
        row, col = next(
            (tile.row, tile.col) for tile in self.state if tile.val == Tile.blank_tile
        )
        moves: Moves = Moves.moves_dict
        for move, move_enum in moves.items():
            dr = move_enum.value[0]
            dc = move_enum.value[1]
            new_row, new_col = row + dr, col + dc
            # Check if the move is within the bounds of the board
            if 0 <= new_row < side_length and 0 <= new_col < side_length:
                # Make the move
                new_state: State = self.deep_copy()  # Deep copy of the state
                blank_index: int = new_state.get_blank_tile_index()
                target_index: int = new_state.get_target_tile_index(new_row, new_col)
                new_state.update_state(blank_index, target_index, new_row, new_col)
                neighbors.append((new_state, move))
        return neighbors
