class Tile:
    blank_tile = 0

    def __init__(self, val: int, r: int, c: int):
        self.val = val
        self.row = r
        self.col = c

    def to_dict(self):
        return {"val": self.val, "row": self.row, "col": self.col}

    @classmethod
    def from_dict(cls, data):
        return cls(data["val"], data["row"], data["col"])
