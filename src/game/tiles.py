from enum import Enum
from typing import Union


class Tile:
    @staticmethod
    def get_blank_tile_value(tile_mode: "TileMode") -> Union[int, str]:
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

    def to_dict(self):
        return {"val": self.val, "row": self.row, "col": self.col}

    @classmethod
    def from_dict(cls, data):
        return cls(data["val"], data["row"], data["col"])


class TileMode(Enum):
    NUMBERS = "numbers"
    LETTERS = "letters"
    MIXED = "mixed"


class RepeatMode(Enum):
    REPEATED = "repeated"
    UNIQUE = "unique"
