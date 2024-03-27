from collections import deque
from typing import List, Tuple, Optional, Set, Deque, Union
from game import utils
from game.tiles import Tile
from game.state import State
from game.moves import Moves
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.puzzle import Puzzle


class Solver:
    def __init__(
        self,
        start_state: State,
        state_id: int,
        puzzle_instance: "Puzzle",
        col_count: int,
        goal_state: State,
    ):
        self.start_state: State = start_state
        self.state_id: int = state_id
        self.board_width: int = col_count
        self.puzzle_instance: Puzzle = puzzle_instance
        self.goal_state_tuple: tuple = State.state_to_tuple(goal_state)
        self.goal_state: State = goal_state
        self.blank_tile_value: Union[int, str] = Tile.get_blank_tile_value(
            self.puzzle_instance.tile_mode
        )
        self.visited: Set[Tuple[Tuple[int, ...], ...]] = set()
        self.prev_state: str = None

    def solve(self) -> Optional[List[List[int]]]:
        queue: Deque[Tuple[State, List[str]]] = deque([(self.start_state, [])])
        while queue:
            current_state, path = queue.popleft()
            state_to_compare = current_state.state_to_tuple()
            if state_to_compare == self.goal_state_tuple:
                return path  # Found the solution

            self.prev_state = current_state.state_to_tuple()

            self.visited.add(
                current_state.state_to_tuple()
            )  # Add the current state to the visited set
            for neighbor, move in current_state.get_neighbors(self.board_width):
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
            file.write("Goal State" + "\n" + utils.write_matrix(self.goal_state) + "\n")
            for move in solution:
                row, col = next(
                    (tile.row, tile.col)
                    for tile in solved_state.state
                    if tile.val == self.blank_tile_value
                )
                new_row, new_col = (
                    row + Moves.moves_dict[move].value[0],
                    col + Moves.moves_dict[move].value[1],
                )
                blank_index: int = solved_state.get_blank_tile_index()
                target_index: int = solved_state.get_target_tile_index(new_row, new_col)
                solved_state.update_state(blank_index, target_index, new_row, new_col)
                file.write(f"Move: {move}\n")
                file.write(utils.write_matrix(solved_state) + "\n")
