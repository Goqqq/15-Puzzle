from collections import deque
import copy
from itertools import chain
import math
import random
from typing import List, Tuple, Optional, Set, Deque
from game import utils
from game.tiles import Tile
from game.state import State
from game.moves import Moves
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.puzzle import Puzzle


class Solver:
    def __init__(self, start_state: State, state_id: int, puzzle_instance: "Puzzle"):
        self.start_state: State = start_state
        self.state_id: int = state_id
        self.board_size: int = int(math.sqrt(len(start_state.state)))
        self.goal_state: State = State.state_to_tuple(
            State(State.generate_goal_state(self.board_size))
        )
        self.puzzle_instance: Puzzle = puzzle_instance
        self.blank_tile: int = 0  # Assuming '0' represents the blank/empty tile
        self.visited: Set[Tuple[Tuple[int, ...], ...]] = set()
        self.__moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        self.prev_state: str = None

    def is_solvable(self) -> bool:
        # Flatten the list and remove the blank tile
        # flat_puzzle: List[int] = list(chain(*self.start_state))
        # flat_puzzle.remove(self.blank_tile)
        flat_puzzle = [tile.val for tile in self.start_state.state if tile.val != 0]

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

    def solve(self) -> Optional[List[List[int]]]:
        # todo: delete
        if not self.is_solvable():
            print("The puzzle is not solvable.")
            return None

        queue: Deque[Tuple[List[List[int]], List[List[int]]]] = deque(
            [(self.start_state, [])]
        )  # todo: check if this is the correct type
        while queue:
            current_state, path = queue.popleft()
            state_to_compare = current_state.state_to_tuple()
            if state_to_compare == self.goal_state:
                return path  # Found the solution

            self.prev_state = current_state.state_to_tuple()

            self.visited.add(
                current_state.state_to_tuple()
            )  # Add the current state to the visited set
            for neighbor, move in current_state.get_neighbors(self.board_size):
                neighbor_tuple = neighbor.state_to_tuple()
                if neighbor_tuple != self.prev_state:
                    if neighbor_tuple not in self.visited:
                        queue.append(
                            (neighbor, path + [move])
                        )  # Append new state with updated path
        return None

    def apply_solution_and_draw(self, solution: List[str]) -> None:
        solved_state: State = self.start_state.deep_copy()
        with open(
            f"{self.puzzle_instance.dir_path}/solution_{self.state_id}.txt", "w"
        ) as file:
            file.write(
                "Original State" + "\n" + utils.write_matrix(self.start_state) + "\n"
            )
            for move in solution:
                row, col = next(
                    (tile.row, tile.col)
                    for tile in solved_state.state
                    if tile.val == Tile.blank_tile
                )
                new_row, new_col = (
                    row + Moves.moves_dict[move].value[0],
                    col + Moves.moves_dict[move].value[1],
                )
                blank_index: int = solved_state.get_blank_tile_index()
                target_index: int = solved_state.get_target_tile_index(new_row, new_col)
                solved_state.update_state(blank_index, target_index, new_row, new_col)
                # print(f"Move: {move}")
                file.write(f"Move: {move}\n")
                # utils.log_matrix(solved_state)
                file.write(utils.write_matrix(solved_state) + "\n")
