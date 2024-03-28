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
    """
    A class that represents a solver for a puzzle game.

    Attributes:
        start_state (State): The initial state of the puzzle.
        state_id (int): The ID of the state.
        puzzle_instance (Puzzle): The instance of the puzzle.
        col_count (int): The number of columns in the puzzle board.
        goal_state (State): The goal state of the puzzle.

    Methods:
        solve(): Solves the puzzle and returns the solution path.
        apply_solution_and_draw(solution: List[str]): Applies the solution path to the puzzle and draws the result.
    """

    def __init__(
        self,
        start_state: State,
        state_id: int,
        puzzle_instance: "Puzzle",
        col_count: int,
        goal_state: State,
    ):
        """
        Initializes a new instance of the Solver class.

        Args:
            start_state (State): The initial state of the puzzle.
            state_id (int): The ID of the state.
            puzzle_instance (Puzzle): The instance of the puzzle.
            col_count (int): The number of columns in the puzzle board.
            goal_state (State): The goal state of the puzzle.
        """
        self.start_state: State = start_state
        self.state_id: int = state_id
        self.board_width: int = col_count
        self.puzzle_instance: Puzzle = puzzle_instance
        # Get the goal state as a tuple
        self.goal_state_tuple: tuple = State.state_to_tuple(goal_state)
        self.goal_state: State = goal_state
        # Get the value of the blank tile based on the tile mode
        self.blank_tile_value: Union[int, str] = Tile.get_blank_tile_value(
            self.puzzle_instance.tile_mode
        )
        self.visited: Set[Tuple[Tuple[int, ...], ...]] = set()
        self.prev_state: str = None

    def solve(self) -> Optional[List[List[int]]]:
        """
        Solves the puzzle and returns the solution path.

        Returns:
            Optional[List[List[int]]]: The solution path as a list of moves, or None if no solution is found.
        """
        queue: Deque[Tuple[State, List[str]]] = deque(
            [(self.start_state, [])]
        )  # Initialize the queue with the start state and an empty path
        while queue:  # While the queue is not empty
            current_state, path = queue.popleft() # Get the current state and path from the queue
            state_to_compare = current_state.state_to_tuple() # Get the current state as a tuple
            # Check if the current state is the goal state
            # If it is, return the path, as the solution has been found
            if state_to_compare == self.goal_state_tuple:
                return path
            # If the current state is not the goal state, update the previous state
            self.prev_state = current_state.state_to_tuple()

            # Add the current state to the visited set
            self.visited.add(
                current_state.state_to_tuple()
            )  # Add the current state to the visited set
            # For each neighbor and move in the current state's neighbors
            for neighbor, move in current_state.get_neighbors(self.board_width):
                neighbor_tuple = neighbor.state_to_tuple()# Get the neighbor state as a tuple
                if neighbor_tuple != self.prev_state: # Check if the neighbor state is not the previous state
                    if neighbor_tuple not in self.visited: # Check if the neighbor state has not been visited
                        queue.append(  # Append the neighbor state and updated path to the queue
                            (neighbor, path + [move])
                        )
        # If no solution is found, return None
        return None

    def apply_solution_and_draw(self, solution: List[str]) -> None:
        """
        Applies the solution path to the puzzle and draws the result.

        Args:
            solution (List[str]): The solution path as a list of moves.
        """
        solved_state: State = (
            self.start_state.deep_copy()
        )  # Create a deep copy of the start state to apply the solution
        # Write the solution to a file
        with open(
            f"{self.puzzle_instance.dir_path}/solution_{self.state_id}.txt", "w"
        ) as file:
            file.write(
                "Original State" + "\n" + utils.write_matrix(self.start_state) + "\n"
            )
            file.write("Goal State" + "\n" + utils.write_matrix(self.goal_state) + "\n")
            for move in solution:  # For each move in the solution
                row, col = next(  # Get the row and column of the blank tile
                    (tile.row, tile.col)
                    for tile in solved_state.state
                    if tile.val == self.blank_tile_value
                )
                # Get the new row and column of the blank tile after the move
                new_row, new_col = (
                    row + Moves.moves_dict[move].value[0],
                    col + Moves.moves_dict[move].value[1],
                )
                blank_index: int = solved_state.get_blank_tile_index() # Get the index of the blank tile
                target_index: int = solved_state.get_target_tile_index(new_row, new_col) # Get the index of the target tile
                solved_state.update_state(blank_index, target_index, new_row, new_col) # Update the state with the new blank tile position
                # Write the move and updated state to the file
                file.write(f"Move: {move}\n")
                file.write(utils.write_matrix(solved_state) + "\n")
