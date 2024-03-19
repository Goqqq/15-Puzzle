import math
import os
import pickle
import random
from typing import List
from game.tiles import Tile
from game.state import State
from game.solver import Solver
from game import utils
import os
from datetime import datetime


class Puzzle:
    def __init__(self, size: int):
        self.size = size
        self.side_length = int(math.sqrt(size))
        self.dir_path: str = None

    def start(self, solve_count: int):
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
        all_states: List[State] = utils.measure_time(self.get_states)
        for i in range(solve_count):
            random_state_index: int = random.randint(0, len(all_states) - 1)
            start_state = all_states[random_state_index]
            utils.measure_time(utils.log_matrix, start_state)
            solver: Solver = utils.measure_time(
                Solver, start_state, random_state_index, self
            )
            solution: str = utils.measure_time(solver.solve)
            if solution:
                print("Solution found!")
                print(solution)
                utils.measure_time(solver.apply_solution_and_draw, solution)
            else:
                print("No solution found.")

    def get_states(self) -> List[State]:
        dir_of_script = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(dir_of_script, os.pardir, os.pardir, "assets")
        all_states_file = os.path.join(assets_path, "states", "all_states.pkl")
        if os.path.exists(all_states_file):
            with open(all_states_file, "rb") as file:
                all_states: List[State] = pickle.load(file)
        else:
            all_states = State.generate_all_states(self.size)
            with open(all_states_file, "wb") as file:
                pickle.dump(all_states, file)
        return all_states
