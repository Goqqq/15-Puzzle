from collections import Counter
from itertools import permutations
import random
from string import ascii_uppercase
from game.tiles import Tile, TileMode, DuplicationMode
from typing import Dict, List, Tuple, Union
from game.moves import Moves


class State:
    def __init__(
        self,
        tiles: List[Tile],
        tile_mode: TileMode = TileMode.NUMBERS,
        repeat_mode: DuplicationMode = DuplicationMode.UNIQUE,
    ):
        """
        Initializes a new State object.
        Args:
            tiles (List[Tile]): A list of Tile objects representing the initial state of the game.
            tile_mode (TileMode, optional): The mode for displaying the tiles. Defaults to TileMode.NUMBERS.
            repeat_mode (DuplicationMode, optional): The mode for handling tile duplication. Defaults to DuplicationMode.UNIQUE.
        """
        self.moves: Moves = Moves()
        self.state: List[Tile] = tiles
        self.tile_mode = tile_mode
        self.repeat_mode = repeat_mode

    def get_blank_tile_index(self) -> int:
        """
        Returns the index of the blank tile in the state.
        Returns:
            int: The index of the blank tile.
        """
        return self.state.index(
            next(
                tile
                for tile in self.state
                if tile.val == Tile.get_blank_tile_value(self.tile_mode)
            )
        )

    def get_target_tile_index(self, row: int, col: int) -> int:
        """
        Returns the index of the target tile in the state list.
        Args:
            row (int): The row of the target tile.
            col (int): The column of the target tile.
        Returns:
            int: The index of the target tile in the state list.
        """
        return self.state.index(
            next(tile for tile in self.state if tile.row == row and tile.col == col)
        )

    def update_state(
        self, blank_index: int, target_index: int, new_row: int, new_col: int
    ) -> None:
        """
        Updates the state of the game by swapping the positions of two tiles and updating their row and column values.
        Args:
            blank_index (int): The index of the blank tile.
            target_index (int): The index of the target tile.
            new_row (int): The new row value for the blank tile.
            new_col (int): The new column value for the blank tile.
        Returns:
            None
        """
        (
            self.state[blank_index].row,
            self.state[blank_index].col,
            self.state[target_index].row,
            self.state[target_index].col,
        ) = (new_row, new_col, self.state[blank_index].row, self.state[blank_index].col)
        self.state[blank_index], self.state[target_index] = (
            self.state[target_index],
            self.state[blank_index],
        )

    @staticmethod
    def state_is_solvable(state: List[Tile], blank_row: int, n: int) -> bool:
        """
        Check if a given state of the game is solvable.
        Args:
            state (List[Tile]): The current state of the game represented as a list of Tile objects.
            blank_row (int): The row index of the blank tile.
            n (int): The width of the game board.
        Returns:
            bool: True if the state is solvable, False otherwise.
        """
        inversions: int = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i].scale_value > state[j].scale_value:
                    inversions += 1
        # For odd-sized boards, the number of inversions must be even
        if n % 2 != 0:
            return inversions % 2 == 0
        # For boards with an even width, we need to also check the row of the blank tile
        else:
            blank_row_from_bottom: int = n - blank_row
            if blank_row_from_bottom % 2 == 0:  # Blank on even row from bottom
                return inversions % 2 != 0
            else:  # Blank on odd row from bottom
                return inversions % 2 == 0

    # Not in use, but can be used to generate all unique permutations of a list
    def perm_unique(elements):
        """
        Generate all unique permutations of the given elements.
        Args:
            elements (iterable): The elements to generate permutations from.
        Yields:
            list: A list containing a unique permutation of the elements.
        Returns:
            generator: A generator that yields all unique permutations of the elements.
        Example:
            >>> list(perm_unique([1, 2, 2]))
            [[1, 2, 2], [2, 1, 2], [2, 2, 1]]
        """

        def backtrack(path, counter):
            if len(path) == len(elements):
                yield list(path)
                return
            for element in counter:
                if counter[element] > 0:
                    path.append(element)
                    counter[element] -= 1
                    yield from backtrack(path, counter)
                    path.pop()
                    counter[element] += 1

        return backtrack([], Counter(elements))

    @staticmethod
    def state_to_hash(state: List[Tile]) -> str:
        """
        Converts the state of the game to a hash string.
        Args:
            state (List[Tile]): The current state of the game.
        Returns:
            str: The hash string representing the state of the game.
        """
        return "-".join(str(tile.val) for tile in state)

    @staticmethod
    def generate_all_states(
        col_count: int,
        row_count: int,
        tile_mode: TileMode,
        repeat_mode: DuplicationMode,
        duplicates_count: int = 0,
    ) -> Tuple[List["State"], "State"]:
        """
        Generates all possible states for a given puzzle configuration.

        Args:
            col_count (int): The number of columns in the puzzle.
            row_count (int): The number of rows in the puzzle.
            tile_mode (TileMode): The mode for generating tile values.
            repeat_mode (DuplicationMode): The mode for duplicating tiles.
            duplicates_count (int, optional): The number of duplicate tiles to generate. Defaults to 0.

        Returns:
            Tuple[List[State], State]: A tuple containing a list of all possible states and the solved state.

        """
        all_states: List[State] = []
        size: int = col_count * row_count
        # Get the blank tile value based on the tile mode
        blank_tile_value: Union[int, str] = Tile.get_blank_tile_value(tile_mode)
        # Prepare the tiles based on the tile mode and duplication mode
        tiles = State.prepare_tiles(
            size, tile_mode, duplicates_count, blank_tile_value, repeat_mode
        )
        # Generate the solved state
        solved_state = State.generate_solved_state(
            tiles, col_count, tile_mode, repeat_mode
        )
        # Get the real values of the tiles
        tiles = [tile.real_val for tile in solved_state.state]
        # Get the scale values of the tiles to check for solvability
        scale_values: Dict[str, int] = State.get_scale_values(solved_state.state)
        # Define a set to store the hashes of the states
        seen_hashes = set()
        # Generate all states
        for perm in permutations(tiles):
            state = []
            blank_row = None
            state_to_check = [] # To check if the state is solvable
            for i, real_value in enumerate(perm):
                row, col = divmod(i, col_count)
                # Convert the value to an integer if it is a string
                value = (
                    real_value.split("-")[0]
                    if isinstance(real_value, str)
                    else real_value
                )
                # Convert the value to an integer if it is a string and a digit
                if isinstance(value, str) and value.isdigit():
                    value = int(value)
                # Create a new tile object
                tile = Tile(
                    value,
                    row,
                    col,
                    scale_values[real_value],
                    real_val=real_value,
                )
                # Append the tile to the state and state_to_check if it is not a blank tile
                state.append(tile)
                if tile.val != blank_tile_value:
                    state_to_check.append(tile)
                # Store the row of the blank tile to check for solvability
                else:
                    blank_row = tile.row
            # Add the hash of the state to the set of seen hashes if it is not already in the set
            # Else, skip the state
            hash_value = State.state_to_hash(state)
            if hash_value in seen_hashes:
                continue
            seen_hashes.add(hash_value)
            # Check if the state is solvable and add it to the list of all states
            if State.state_is_solvable(state_to_check, blank_row, col_count):
                all_states.append(State(state, tile_mode, repeat_mode))
        # Return the list of all states and the solved state
        return all_states, solved_state

    @staticmethod
    def prepare_tiles(
        size: int,
        tile_mode: TileMode,
        duplicates_count: int,
        blank_tile_value: Union[int, str],
        repeat_mode: DuplicationMode,
    ) -> List[Union[int, str]]:
        """
        Prepare the tiles for the game state.

        Args:
            size (int): The size of the game board.
            tile_mode (TileMode): The mode for generating the tiles.
            duplicates_count (int): The number of duplicate tiles to include.
            blank_tile_value (int): The value of the blank tile.
            repeat_mode (DuplicationMode): The mode for duplicating tiles.

        Returns:
            list: The prepared tiles for the game state.
        """
        # Generate the tiles based on the tile mode
        if tile_mode == TileMode.NUMBERS:
            # Generate a list of numbers from 1 to size - 1 and add the blank tile value
            tiles = list(range(1, size)) + [blank_tile_value]
        elif tile_mode == TileMode.LETTERS:
            # Generate a list of uppercase letters from A to size - 1 and add the blank tile value
            tiles = list(ascii_uppercase)[: size - 1] + [blank_tile_value]
        else:  # tile_mode == TileMode.MIXED
            # Generate a list of numbers from 1 to size // 2, uppercase letters from A to size // 2, and the blank tile value
            tiles = (
                list(range(1, size // 2 + 1))
                + list(ascii_uppercase)[: size // 2]
                + [blank_tile_value]
            )
        # Handle tile duplication based on the duplication mode
        if repeat_mode == DuplicationMode.DUPLICATED:
            # If duplicates count is less than 1 or greater than size // 2, default to 2 duplicates
            if duplicates_count == 0 or duplicates_count > size // 2:
                print(
                    "Duplicate count must be between 1 and size // 2. Defaulting to 2 duplicates"
                )
                duplicates_count = 2
            # Pick random different tiles to duplicate
            duplicates = random.sample(
                [tile for tile in tiles if tile != blank_tile_value], duplicates_count
            )
            # Replace random tiles which are not blank or already duplicated with duplicates
            for i in range(duplicates_count):
                replace_index = random.choice(
                    [
                        i
                        for i in range(len(tiles))
                        if tiles[i] != blank_tile_value and tiles[i] not in duplicates
                    ]
                )
                # Replace the tile at the replace index with the duplicate
                tiles[replace_index] = duplicates[i]
        # Return the prepared tiles
        return tiles

    @staticmethod
    def generate_solved_state(
        tiles: List[Tile],
        col_count: int,
        tile_mode: TileMode,
        repeat_mode: DuplicationMode,
    ) -> "State":
        """
        Generate a solved state based on the given parameters.

        Args:
            tiles (List[Tile]): A list of tiles.
            col_count (int): The number of columns in the state.
            tile_mode (TileMode): The tile mode.
            repeat_mode (DuplicationMode): The duplication mode.

        Returns:
            State: The generated solved state.
        """
        solved_state = []
        appended_tiles = []
        # Iterate over the tiles and create a new Tile object for each tile
        for i, value in enumerate(tiles):
            row, col = divmod(i, col_count)
            # Set the scale value based on the index
            scale_value = i + 1
            # Check if the tile is duplicated
            duplicated: bool = value in appended_tiles
            # Append the new Tile object to the solved state
            solved_state.append(Tile(value, row, col, scale_value, duplicated))
            # Keep track of appended tiles to check for duplicates
            appended_tiles.append(value)
        # Return the solved state
        return State(solved_state, tile_mode, repeat_mode)

    @staticmethod
    def get_scale_values(tiles: List[Tile]) -> Dict[str, int]:
        """
        Returns a dictionary mapping the real values of tiles to their scale values.

        Args:
            tiles (List[Tile]): A list of Tile objects.

        Returns:
            Dict[str, int]: A dictionary mapping the real values of tiles to their scale values.
        """
        return {tile.real_val: tile.scale_value for tile in tiles}

    def state_to_tuple(
        self,
    ) -> Union[Tuple[Tuple[int, int, int], ...], Tuple[Tuple[str, int, int], ...]]:
        """
        Converts the state of the game to a tuple representation.

        Returns:
            Union[Tuple[Tuple[int, int, int], ...], Tuple[Tuple[str, int, int], ...]]: 
            A tuple representation of the game state, where each element is a tuple 
            containing the value, row, column, and scale value of a tile in the state.
        """
        return tuple(
            (tile.val, tile.row, tile.col, tile.scale_value) for tile in self.state
        )

    def deep_copy(self) -> "State":
        """
            Creates a deep copy of the current State object.

            Returns:
                A new State object that is a deep copy of the current State.
            """
        return State(
            [
                Tile(
                    tile.val,
                    tile.row,
                    tile.col,
                    tile.scale_value,
                    getattr(
                        tile, "duplicated", None
                    ),  # Returns None if 'duplicated' does not exist
                    tile.real_val,
                )
                for tile in self.state
            ],
            self.tile_mode,
            self.repeat_mode,
        )

    def get_neighbors(self, side_length: int) -> List[Tuple[List["State"], str]]:
        """
        Returns a list of neighboring states and the corresponding move.

        Args:
            side_length (int): The side length of the board.

        Returns:
            List[Tuple[List[State], str]]: A list of tuples containing the neighboring states and the corresponding move.
        """
        # Initialize the list of neighbors
        neighbors = []
        # Find the blank tile's position
        row, col = next(
            (tile.row, tile.col)
            for tile in self.state
            if tile.val == Tile.get_blank_tile_value(self.tile_mode)
        )
        # Get the possible moves
        moves: Moves = Moves.moves_dict
        # Iterate over the possible moves
        for move, move_enum in moves.items():
            # Calculate the new row and column
            dr = move_enum.value[0]
            dc = move_enum.value[1]
            # Calculate the new row and column
            new_row, new_col = row + dr, col + dc
            # Check if the move is within the bounds of the board
            if 0 <= new_row < side_length and 0 <= new_col < side_length:
                # Make the move
                new_state: State = self.deep_copy()  # Deep copy of the state
                blank_index: int = new_state.get_blank_tile_index()
                target_index: int = new_state.get_target_tile_index(new_row, new_col)
                new_state.update_state(blank_index, target_index, new_row, new_col)
                neighbors.append((new_state, move))
        # Return the list of neighbors
        return neighbors
