from typing import List
from game.tiles import Tile
from enum import Enum


class MovesEnum(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class Moves:
    moves_dict = {
        "up": MovesEnum.UP,
        "down": MovesEnum.DOWN,
        "left": MovesEnum.LEFT,
        "right": MovesEnum.RIGHT,
    }


# def move_up(self, state: List[Tile], blank_index: int) -> List[Tile]:
#     target_index = blank_index - self.width
#     state[blank_index], state[target_index] = (
#         state[target_index],
#         state[blank_index],
#     )
#     return state
