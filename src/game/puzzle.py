from multiprocessing import Pool, cpu_count
import os
import pickle
import random
from typing import List
from game.tiles import TileMode, DuplicationMode
from game.state import State
from game.solver import Solver
from game.utils import PuzzleUtils as utils
import os
from datetime import datetime
import time
from enum import Enum


class PuzzleSize(Enum):
    SMALL = (3, 3)
    MEDIUM = (3, 4)
    LARGE = (4, 4)


class Puzzle:
    """
    Represents a puzzle game.

    Args:
        size (PuzzleSize): The size of the puzzle.
        tile_mode (TileMode, optional): The mode for generating puzzle tiles. Defaults to TileMode.NUMBERS.
        duplication_mode (DuplicationMode, optional): The mode for duplicating puzzle tiles. Defaults to DuplicationMode.UNIQUE.
        duplicate_count (int, optional): The number of times to duplicate each tile. Defaults to None.

    Attributes:
        row_count (int): The number of rows in the puzzle.
        col_count (int): The number of columns in the puzzle.
        tile_mode (TileMode): The mode for generating puzzle tiles.
        duplication_mode (DuplicationMode): The mode for duplicating puzzle tiles.
        duplicate_count (int): The number of times each tile is duplicated.
        dir_path (str): The directory path for saving solved states.

    Methods:
        solve_puzzle: Solves a puzzle using a solver.
        start: Starts the puzzle solving process.
        get_states: Retrieves or generates all possible states of the puzzle.
    """

    def __init__(
        self,
        size: PuzzleSize,
        tile_mode: TileMode = TileMode.NUMBERS,
        duplication_mode: DuplicationMode = DuplicationMode.UNIQUE,
        duplicate_count: int = None,
    ):
        self.row_count: int = size.value[0]
        self.col_count: int = size.value[1]
        self.tile_mode: TileMode = tile_mode
        self.duplication_mode: DuplicationMode = duplication_mode
        self.duplicate_count: int = duplicate_count
        self.dir_path: str = None

    @staticmethod
    def solve_puzzle(args):
        """
        Solves a puzzle using a solver.

        Args:
            args: A tuple containing the start state, random state index, puzzle, column count, and solved state.

        Returns:
            Tuple[int, float]: A tuple containing the random state index and the running time of the solver.
        """
        start_state, random_state_index, puzzle, col_count, solved_state = args
        solver = Solver(
            start_state, random_state_index, puzzle, col_count, solved_state
        )
        solution, running_time = utils.measure_time(solver.solve)
        # If a solution is found, apply the solution and draw the solved state to a file
        # and return the random state index and the running time
        if solution:
            solver.apply_solution_and_draw(solution)
            return random_state_index, running_time
        else:
            # If no solution is found, return None and the running time
            return None, running_time

    def start(
        self,
        to_solve_count: int,
    ):
        """
        Starts the puzzle solving process.

        Args:
            to_solve_count (int): The number of puzzles to solve.
        """
        now = datetime.now()  # current date and time
        programm_start_time: time = time.time()  # current time
        timestamp_str = now.strftime(
            "%Y%m%d_%H%M%S"
        )  # current date and time in string format
        # Create a directory for saving solved states
        self.dir_path: str = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            os.pardir,
            "assets",
            "solved_states",
            timestamp_str,
        )
        # Create the directory if it does not exist
        os.makedirs(self.dir_path, exist_ok=True)

        all_states: List[State]
        all_states_time: str
        # Retrieve or generate all possible states of the puzzle with given parameters
        (all_states, solved_state), all_states_time = utils.measure_time(
            self.get_states
        )
        # Keep track of the indices of the solved states
        solved_states_indices: List[int] = []

        args_list = []  # List of arguments for the solver
        for _ in range(to_solve_count):  # Loop through the number of puzzles to solve
            while True:  # Loop until a random state index that has not been solved is found
                random_state_index = random.randint(
                    0, len(all_states) - 1
                )  # Generate a random state index
                if random_state_index not in solved_states_indices:  # Check if the random state index has not been solved
                    break
            start_state = all_states[
                random_state_index
            ]  # Get the start state from all states with the random state index
            solved_states_indices.append(
                random_state_index
            )  # Add the random state index to the list of solved states
            # Add the arguments for the solver to the list of arguments
            args_list.append(
                (
                    start_state,
                    random_state_index,
                    self,
                    self.col_count,
                    solved_state,
                )
            )
        solution_start_time: time = time.time()  # Start time for solving the puzzles
        # Solve the puzzles in parallel
        with Pool(cpu_count()) as pool:  # Use the number of CPU cores available for the pool
            results = pool.map(
                Puzzle.solve_puzzle, args_list
            )  # Map the arguments to the solver function
        solved_states_count: int = 0  # Number of solved states to keep track of the number of puzzles solved
        running_times: List[str] = []  # List of running times for each puzzle
        # Loop through the results
        for result in results:
            result_index, result_time = result  # Get the index and running time from the result
            if result_index is not None:
                solved_states_count += 1  # Increment the number of solved states
                # Add the running time to the list of running times
                running_times.append(  
                    f"Running time for {result_index}: {result_time} seconds"
                )
        solution_end_time: time = time.time()
        solution_duration: str = (  # Calculate the duration of the solution process
            f"{float(solution_end_time) - float(solution_start_time):.2f}"
        )
        # Write the results to a file
        with open(f"{self.dir_path}/run_stats.txt", "a") as file:
            file.write(
                f"All states ({len(all_states)}) generation/retrieval time: {all_states_time} seconds\n"
                f"States to solve: {to_solve_count}\n"
                f"Puzzle size: {self.row_count}x{self.col_count}\n"
                f"Tile mode: {self.tile_mode.value}\n"
                f"Duplication mode: {self.duplication_mode.value}\n"
                f"--------------------------------------------------\n"
            )
            # Write the running times for each puzzle
            for running_time in running_times:
                file.write(running_time + "\n")
            file.write(
                f"{solved_states_count} from {to_solve_count} puzzles solved in {solution_duration} seconds\n"
            )
            file.write(
                f"Programm total running time: {(solution_end_time - programm_start_time):.2f} seconds\n"
            )

    def get_states(self) -> List[State]:
        """
        Retrieves or generates all possible states of the puzzle.

        Returns:
            Tuple[List[State], State]: A tuple containing the list of all states and the solved state.
        """
        # Get the directory path of the script
        dir_of_script = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(dir_of_script, os.pardir, os.pardir, "assets")
        file_name_extension: str = ""
        # Generate a file name extension if there are duplicates including the number of duplicates
        if self.duplicate_count and self.duplicate_count > 0 and self.duplication_mode.value == DuplicationMode.DUPLICATED.value:
            file_name_extension = f"({self.duplicate_count})"
        # Generate a file name for the all states file
        states_path = os.path.join(assets_path, "states")
        all_states_file = os.path.join(
            states_path,
            f"all_states_{self.col_count * self.row_count}_{self.tile_mode.value}_{self.duplication_mode.value}{file_name_extension}.pkl",
        )
        # Check if the states directory exists, if not, create it
        if not os.path.exists(states_path):
            os.makedirs(states_path)
        # Check if the all states file exists
        # If it exists, load the all states and solved state from the file
        # If it does not exist, generate all states and the solved state
        if os.path.exists(all_states_file):
            with open(all_states_file, "rb") as file:
                all_states, solved_state = pickle.load(file)
        else:
            all_states, solved_state = State.generate_all_states(
                col_count=self.col_count,
                row_count=self.row_count,
                tile_mode=self.tile_mode,
                repeat_mode=self.duplication_mode,
                duplicates_count=self.duplicate_count,
            )
            # Save the all states and solved state to a file
            with open(all_states_file, "wb") as file:
                pickle.dump((all_states, solved_state), file)
        return all_states, solved_state  # Return the all states and solved state
