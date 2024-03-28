from enum import Enum
from typing import Union


class Tile:
    """
    Represents a tile in the game.

    Attributes:
        val (int): The value of the tile.
        row (int): The row position of the tile.
        col (int): The column position of the tile.
        scale_value (int): The scale value of the tile.
        id (str): The unique identifier of the tile.
        real_val (str): The real value of the tile.
        duplicated (bool): Indicates if the tile is duplicated.
    """

    @staticmethod
    def get_blank_tile_value(tile_mode: "TileMode") -> Union[int, str]:
        """
        Returns the value of a blank tile based on the given tile mode.

        Args:
            tile_mode (TileMode): The mode of the tile.

        Returns:
            Union[int, str]: The value of the blank tile.
        """
        if tile_mode == TileMode.NUMBERS or tile_mode == TileMode.MIXED:
            return 0
        elif tile_mode == TileMode.LETTERS:
            return " "

    def __init__(
        self,
        val: int,
        r: int,
        c: int,
        scale_value: int,
        duplicated: bool = False,
        real_val: str = None,
    ):
        """
        Initializes a new instance of the Tile class.

        Args:
            val (int): The value of the tile.
            r (int): The row position of the tile.
            c (int): The column position of the tile.
            scale_value (int): The scale value of the tile.
            duplicated (bool, optional): Indicates if the tile is duplicated. Defaults to False.
            real_val (str, optional): The real value of the tile. Defaults to None.
        """
        self.val = val
        self.row = r
        self.col = c
        self.scale_value = scale_value
        self.id = f"{self.row}-{self.col}"
        if real_val:
            self.real_val = real_val
            if isinstance(real_val, str) and len(real_val) > 1:
                self.duplicated = True
        else:
            self.real_val = f"{val}-{self.id}" if duplicated else val
            self.duplicated = duplicated


from enum import Enum

class TileMode(Enum):
    """
    Represents the different modes for tiles in the game.
    
    Attributes:
        NUMBERS (str): Mode for tiles with numbers.
        LETTERS (str): Mode for tiles with letters.
        MIXED (str): Mode for tiles with a mix of numbers and letters.
    """
    NUMBERS = "numbers"
    LETTERS = "letters"
    MIXED = "mixed"


from enum import Enum

class DuplicationMode(Enum):
    """
    Enumeration representing the duplication mode of a tile.

    Attributes:
        DUPLICATED (str): Represents a duplicated tile.
        UNIQUE (str): Represents a unique tile.
    """
    DUPLICATED = "duplicated"
    UNIQUE = "unique"
