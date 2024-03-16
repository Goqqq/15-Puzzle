from collections import deque
import copy
from itertools import chain
import math
import random
from typing import List, Tuple, Optional, Set, Deque
from game import utils
from game.tiles import Tile


class SolveGame:
    def __init__(
        self, start_state: List[Tile], goal_state: List[Tile]
    ):  # The start state is a 2D list
        self.start_state: List[Tile] = start_state
        self.goal_state: List[Tile] = SolveGame.state_to_tuple(goal_state)
        self.board_size: int = math.sqrt(len(start_state))
        self.blank_tile: int = 0  # Assuming '0' represents the blank/empty tile
        self.visited: Set[Tuple[Tuple[int, ...], ...]] = set()
        self.__moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        self.prev_state: str = None

    def is_solvable(self) -> bool:
        # Flatten the list and remove the blank tile
        # flat_puzzle: List[int] = list(chain(*self.start_state))
        # flat_puzzle.remove(self.blank_tile)
        flat_puzzle = [tile.val for tile in self.start_state if tile.val != 0]

        inversions: int = 0
        for i in range(len(flat_puzzle)):
            for j in range(i + 1, len(flat_puzzle)):
                if flat_puzzle[i] > flat_puzzle[j]:
                    inversions += 1

        # For odd-sized boards, the number of inversions must be even
        if self.board_size % 2 != 0:
            return inversions % 2 == 0

        # For boards with an even width, we need to also check the row of the blank tile
        else:
            blank_row: int = next(
                row
                for row, tiles in enumerate(self.start_state)
                if self.blank_tile in tiles
            )
            blank_row_from_bottom: int = self.board_size - blank_row
            if blank_row_from_bottom % 2 == 0:  # Blank on even row from bottom
                return inversions % 2 != 0
            else:  # Blank on odd row from bottom
                return inversions % 2 == 0

    def state_to_tuple(state: List[Tile]) -> Tuple[Tuple[int, int, int], ...]:
        return tuple((tile.val, tile.row, tile.col) for tile in state)

    def solve(self) -> Optional[List[List[int]]]:
        if not self.is_solvable():
            print("The puzzle is not solvable.")
            return None
        print("The puzzle is solvable.")
        queue: Deque[Tuple[List[List[int]], List[List[int]]]] = deque(
            [(self.start_state, [])]
        )
        while queue:
            current_state, path = queue.popleft()
            state_to_compare = SolveGame.state_to_tuple(current_state)
            if state_to_compare == self.goal_state:
                return path  # Found the solution

            self.prev_state = SolveGame.state_to_tuple(current_state)

            self.visited.add(
                SolveGame.state_to_tuple(current_state)
            )  # Add the current state to the visited set
            for neighbor, move in self.get_neighbors(current_state):
                neighbor_tuple = SolveGame.state_to_tuple(neighbor)
                if neighbor_tuple != self.prev_state:
                    if neighbor_tuple not in self.visited:
                        queue.append(
                            (neighbor, path + [move])
                        )  # Append new state with updated path

                else:  # todo delete
                    print("condition not met")
        return None

    def get_neighbors(
        self, state: List[List[int]]
    ) -> List[Tuple[List[List[int]], str]]:
        neighbors = []
        # Find the blank tile's position
        row, col = next(
            (tile.row, tile.col) for tile in state if tile.val == self.blank_tile
        )

        # Potential moves: up, down, left, right
        for move, (dr, dc) in self.__moves.items():
            new_row, new_col = row + dr, col + dc
            # Check if the move is within the bounds of the board
            if 0 <= new_row < self.board_size and 0 <= new_col < self.board_size:
                # Make the move
                new_state = copy.deepcopy(state)  # Deep copy of the state
                blank_tile = next(
                    tile for tile in new_state if tile.val == self.blank_tile
                )
                target_tile = next(
                    tile
                    for tile in new_state
                    if tile.row == new_row and tile.col == new_col
                )
                blank_index: int = new_state.index(blank_tile)
                target_index: int = new_state.index(target_tile)

                (
                    new_state[blank_index].row,
                    new_state[blank_index].col,
                    new_state[target_index].row,
                    new_state[target_index].col,
                ) = (new_row, new_col, row, col)

                # Swap the blank tile with the target tile
                new_state[blank_index], new_state[target_index] = (
                    new_state[target_index],
                    new_state[blank_index],
                )
                # utils.log_matrix(new_state, 3)
                # new_state[row][col], new_state[new_row][new_col] = (
                #     new_state[new_row][new_col],
                #     new_state[row][col],
                # )
                neighbors.append((new_state, move))

        return neighbors

    def show_solution(self, path: List[str]) -> None:
        state = self.start_state
        moves = self.__moves

        for move in path:
            action = moves[move]
            state = self.apply_move(state, action)
            self.print_state(state)

    # def apply_move(self, state: List[Tile], action: callable
