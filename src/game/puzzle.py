from multiprocessing import Pool, cpu_count
import os
import pickle
import random
from typing import List
from game.tiles import TileMode, DuplicationMode
from game.state import State
from game.solver import Solver
from game import utils
import os
from datetime import datetime
import time
from enum import Enum


class PuzzleSize(Enum):
    SMALL = (3, 3)
    MEDIUM = (3, 4)
    LARGE = (4, 4)


class Puzzle:
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
        start_state, random_state_index, puzzle, col_count, solved_state = args
        solver = Solver(
            start_state, random_state_index, puzzle, col_count, solved_state
        )
        solution, running_time = utils.measure_time(solver.solve)
        if solution:
            solver.apply_solution_and_draw(solution)
            return random_state_index, running_time
        else:
            return None, running_time

    def start(
        self,
        to_solve_count: int,
    ):
        now = datetime.now()
        programm_start_time: time = time.time()
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        self.dir_path: str = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            os.pardir,
            "assets",
            "solved_states",
            timestamp_str,
        )
        os.makedirs(self.dir_path, exist_ok=True)
        all_states: List[State]
        all_states_time: str
        (all_states, solved_state), all_states_time = utils.measure_time(
            self.get_states
        )
        solved_states_indices: List[int] = []

        args_list = []
        for _ in range(to_solve_count):
            while True:
                random_state_index = random.randint(0, len(all_states) - 1)
                if random_state_index not in solved_states_indices:
                    break
            start_state = all_states[random_state_index]
            solved_states_indices.append(random_state_index)
            args_list.append(
                (
                    start_state,
                    random_state_index,
                    self,
                    self.col_count,
                    solved_state,
                )
            )
        solution_start_time: time = time.time()
        with Pool(cpu_count()) as pool:
            results = pool.map(Puzzle.solve_puzzle, args_list)
        solved_states_count: int = 0
        running_times: List[str] = []
        for result in results:
            result_index, result_time = result
            if result_index is not None:
                solved_states_count += 1
                running_times.append(
                    f"Running time for {result_index}: {result_time} seconds"
                )
        solution_end_time: time = time.time()
        # solution_start_time = datetime.fromtimestamp(solution_start_time)
        # solution_end_time = datetime.fromtimestamp(solution_end_time)
        solution_duration: str = (
            f"{float(solution_end_time) - float(solution_start_time):.2f}"
        )
        with open(f"{self.dir_path}/run_stats.txt", "a") as file:
            file.write(
                f"All states ({len(all_states)}) generation/retrieval time: {all_states_time} seconds\n"
                f"States to solve: {to_solve_count}\n"
                f"Puzzle size: {self.row_count}x{self.col_count}\n"
                f"Tile mode: {self.tile_mode.value}\n"
                f"Duplication mode: {self.duplication_mode.value}\n"
                f"--------------------------------------------------\n"
            )
            for running_time in running_times:
                file.write(running_time + "\n")
            file.write(
                f"{solved_states_count} from {to_solve_count} puzzles solved in {solution_duration} seconds\n"
            )
            file.write(
                f"Programm total running time: {(solution_end_time - programm_start_time):.2f} seconds\n"
            )

    def get_states(self) -> List[State]:
        dir_of_script = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(dir_of_script, os.pardir, os.pardir, "assets")
        file_name_extension: str = ""
        if self.duplicate_count and self.duplicate_count > 0:
            file_name_extension = f"({self.duplicate_count})"
        all_states_file = os.path.join(
            assets_path,
            "states",
            f"all_states_{self.col_count * self.row_count}_{self.tile_mode.value}_{self.duplication_mode.value}{file_name_extension}.pkl",
        )
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
            with open(all_states_file, "wb") as file:
                pickle.dump((all_states, solved_state), file)
        return all_states, solved_state
