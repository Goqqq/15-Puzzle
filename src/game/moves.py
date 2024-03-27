from enum import Enum


class MovesEnum(Enum):
    """
    Enum class representing the possible moves in the game.
    Each move is associated with a tuple of (row, column) offsets.
    """

    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class Moves:
    """
    Class representing the available moves in the game.
    """

    moves_dict = {
        "up": MovesEnum.UP,
        "down": MovesEnum.DOWN,
        "left": MovesEnum.LEFT,
        "right": MovesEnum.RIGHT,
    }
