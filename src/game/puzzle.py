import math
import os
import pickle
import random
from typing import List
from game.tiles import Tile, TileMode, RepeatMode
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
        repeat_mode: RepeatMode = RepeatMode.UNIQUE,
        duplicate_count: int = None,
    ):
        self.row_count: int = size.value[0]
        self.col_count: int = size.value[1]
        self.tile_mode: TileMode = tile_mode
        self.repeat_mode: RepeatMode = repeat_mode
        self.duplicate_count: int = duplicate_count
        self.dir_path: str = None

    def start(
        self,
        to_solve_count: int,
    ):
        cumulative_start_time: time = time.time()
        now = datetime.now()
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
        )  # todo draw solved state at beginning
        solved_states_count: int = 0
        solved_states_indices: List[int] = []
        running_times = []
        for i in range(to_solve_count):
            while True:
                random_state_index = random.randint(0, len(all_states) - 1)
                if random_state_index not in solved_states_indices:
                    break
            start_state = all_states[random_state_index]
            solved_states_indices.append(random_state_index)
            solver: Solver = Solver(
                start_state,
                random_state_index,
                self,
                self.col_count,
                self.row_count,
                solved_state,
            )
            (solution, running_time) = utils.measure_time(solver.solve)
            if solution:
                solver.apply_solution_and_draw(solution)
                solved_states_count += 1
                # print("Solution found!")
                # print(solution)
            else:
                print("No solution found for:" + "\n" + utils.write_matrix(start_state))

            running_times.append(
                f"Running time for {random_state_index}: {running_time} seconds"
            )
            print(f"Processed {i + 1} puzzles out of {to_solve_count}")
        cumulative_end_time: time = time.time()
        with open(f"{self.dir_path}/run_stats.txt", "a") as file:
            file.write(
                f"All states ({len(all_states)}) generation/retrieval time: {all_states_time} seconds\n"
            )
            for running_time in running_times:
                file.write(running_time + "\n")
            file.write(
                f"{solved_states_count} from {to_solve_count} puzzles solved in {cumulative_end_time - cumulative_start_time:.2f} seconds\n"
            )

    def get_states(self) -> List[State]:
        dir_of_script = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(dir_of_script, os.pardir, os.pardir, "assets")
        all_states_file = os.path.join(
            assets_path,
            "states",
            f"all_states_{self.tile_mode.value}_{self.repeat_mode.value}.pkl",
        )
        if os.path.exists(all_states_file):
            with open(all_states_file, "rb") as file:
                all_states, solved_state = pickle.load(file)
        else:
            all_states, solved_state = State.generate_all_states(
                col_count=self.col_count,
                row_count=self.row_count,
                tile_mode=self.tile_mode,
                repeat_mode=self.repeat_mode,
                duplicates_count=self.duplicate_count,
            )
            with open(all_states_file, "wb") as file:
                pickle.dump((all_states, solved_state), file)
        return all_states, solved_state
