import os
from tkinter import messagebox, ttk
import tkinter as tk
from api import (
    create_puzzle,
    start_puzzle,
    Puzzle,
    PuzzleSize,
    TileMode,
    DuplicationMode,
)


class Gui:

    def run_gui():
        # Create the main window
        root = tk.Tk()

        # Configure the main window
        root.geometry("600x500")
        root.resizable(False, False)
        dir_of_script = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(
            dir_of_script, os.pardir, os.pardir, "assets", "images"
        )

        # Load the welcome image
        welcome_image = os.path.join(assets_path, "Welcome_15_cropped.png")
        bg_image = tk.PhotoImage(file=welcome_image)
        bg_label = tk.Label(root, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Create a label style
        label_style = ttk.Style()
        label_style.configure("TLabel", background="lightgrey", font=("Helvetica", 10))

        # Declare global variables
        global solution_count_var
        solution_count_var = tk.StringVar()
        # Add a trace to the solution count variable
        # solution_count_var.trace_add("write")

        global size_var
        size_var = tk.StringVar()
        # Add a trace to the puzzle size variable
        # size_var.trace_add("write")

        global tile_var
        tile_var = tk.StringVar()
        # Add a trace to the tile mode variable
        # tile_var.trace_add("write")

        global dup_var
        dup_var = tk.StringVar()
        # Add a trace to the duplication mode variable
        dup_var.trace_add("write", Gui.show_duplicate_count_field)

        global dup_count_var
        dup_count_var = tk.StringVar()
        # Add a trace to the duplicate count variable
        # dup_count_var.trace_add("write")
        global dup_count_entry
        global dup_count_label
        global submit_button

        # Create a label for the puzzle size
        size_label = ttk.Label(root, text="Select Puzzle Size:", style="TLabel")
        size_label.place(relx=0.382, rely=0.34, anchor="e")

        # Create a combobox for the puzzle size
        size_options = ttk.Combobox(root, textvariable=size_var)
        # Set the values for the combobox
        # Currently, only the SMALL size is enabled. Other sizes take too long to generate all states
        size_options["values"] = (
            PuzzleSize.SMALL.name,
            # PuzzleSize.MEDIUM.name,
            # PuzzleSize.LARGE.name,
        )
        size_options.place(relx=0.4, rely=0.4, anchor="e")

        # Create a label for the solution count
        solution_count_label = ttk.Label(
            root, text="Enter Solution Count:", style="TLabel"
        )
        solution_count_label.place(relx=0.38, rely=0.54, anchor="e")

        # Create an entry for the solution count
        solution_count_entry = ttk.Entry(root, textvariable=solution_count_var)
        solution_count_entry.place(relx=0.38, rely=0.6, anchor="e")

        # Create a label for the tile mode
        tile_label = ttk.Label(root, text="Select Tile Mode:", style="TLabel")
        tile_label.place(relx=0.83, rely=0.34, anchor="e")

        # Create a combobox for the tile mode
        tile_options = ttk.Combobox(
            root,
            textvariable=tile_var,
        )
        # Set the values for the combobox
        tile_options["values"] = (
            TileMode.LETTERS.name,
            TileMode.NUMBERS.name,
            TileMode.MIXED.name,
        )
        tile_options.place(relx=0.86, rely=0.4, anchor="e")

        # Create a label for the duplication mode
        dup_label = ttk.Label(
            root,
            text="Select Duplication Mode:",
            background="lightgrey",
            style="TLabel",
        )
        dup_label.place(relx=0.87, rely=0.54, anchor="e")

        # Create a combobox for the duplication mode
        dup_options = ttk.Combobox(root, textvariable=dup_var)
        # Set the values for the combobox
        dup_options["values"] = (
            DuplicationMode.DUPLICATED.name,
            DuplicationMode.UNIQUE.name,
        )
        dup_options.place(relx=0.86, rely=0.6, anchor="e")

        # Create a label and entry for the duplicate count and hide them
        dup_count_label = ttk.Label(root, text="Enter Duplicate Count:", style="TLabel")
        dup_count_label.place_forget()
        dup_count_entry = ttk.Entry(root, textvariable=dup_count_var)
        dup_count_entry.place_forget()

        # Create a style for the submit button
        button_style = ttk.Style()
        button_style.configure(
            "TButton",
            foreground="black",
            background="lightblue",
            font=("Helvetica", 10),
        )
        # Create a submit button
        submit_button = ttk.Button(
            root, text="Submit", command=Gui.submit, style="TButton"
        )
        submit_button.place(relx=0.5, rely=0.88, anchor="center")

        # Run the main loop
        root.mainloop()

    def validate_entries():
        """
        Validates the entries before submitting the puzzle configuration.
        This function checks if the puzzle size, tile mode, duplication mode,
        duplicates count, and solution count are valid. If any of the entries
        are invalid, it shows an error message and returns False. Otherwise,
        it returns True.
        Returns:
            bool: True if all entries are valid, False otherwise.
        """
        # Validate the puzzle size
        if not Gui.validate_puzzle_size():
            messagebox.showerror("Error", "Invalid puzzle size.")
            return False
        # Validate the tile mode
        if not Gui.validate_tile_mode():
            messagebox.showerror("Error", "Invalid tile mode.")
            return False
        # Validate the duplication mode
        if not Gui.validate_duplication_mode():
            messagebox.showerror("Error", "Invalid duplication mode.")
            return False
        # Validate the duplicate count
        if not Gui.validate_duplicate_count():
            messagebox.showerror("Error", "Invalid duplicate count.")
            return False
        # Validate the solution count
        if not Gui.validate_solution_count():
            messagebox.showerror("Error", "Invalid solution count.")
            return False
        return True

    def submit():
        """
        Submits the puzzle configuration and starts solving the puzzles.

        This function retrieves the selected puzzle size, tile mode, duplication mode,
        duplicates count, and solution count from the respective variables. It then
        creates a puzzle object using the selected configuration and starts solving
        the puzzles. If the puzzles are solved successfully, a success message is shown.

        Returns:
            None
        """
        # Validate the entries before submitting the puzzle configuration
        if not Gui.validate_entries():
            return

        # Disable the submit button to prevent multiple submissions
        submit_button.config(state="disabled")
        # Get the selected puzzle size, tile mode, duplication mode, duplicates count, and solution count
        puzzle_size = size_var.get()
        tile_mode = tile_var.get()
        duplication_mode = dup_var.get()
        duplicates_count = dup_count_var.get()
        solution_count = solution_count_var.get()
        print(
            f"Puzzle Size: {puzzle_size}, Tile Mode: {tile_mode}, Duplication Mode: {duplication_mode}, Solution Count: {solution_count}, Duplicate Count: {duplicates_count}"
        )
        # Create a puzzle object based on the selected configuration
        puzzle: Puzzle = create_puzzle(
            PuzzleSize[puzzle_size],
            TileMode[tile_mode],
            DuplicationMode[duplication_mode],
            int(duplicates_count) if duplicates_count else None,
        )
        # Start solving the puzzles
        solved = start_puzzle(puzzle, int(solution_count))

        # Show a success message if the puzzles are solved successfully
        if solved:
            messagebox.showinfo(
                "Success", f"{solution_count} puzzles have been solved successfully!"
            )
        # Show an error message if an error occurred while solving the puzzles
        else:
            messagebox.showerror(
                "Error", "An error occurred while solving the puzzles."
            )

        # Enable the submit button
        submit_button.config(state="normal")

    def validate_solution_count(*args):
        """
        Validates the solution count entered by the user.

        Args:
            *args: Variable length argument list.

        Returns:
            None

        Raises:
            None
        """
        try:
            # Try to convert the value to an integer
            value = int(solution_count_var.get())

            # If the value is more than 181440, set it to an empty string
            if value > 181440 or value <= 0:
                return False
        except ValueError:
            return False
        return True

    def validate_puzzle_size(*args):
        """
        Validates the selected puzzle size.
        Returns:
            True if the puzzle size is valid, False otherwise.
        """
        puzzle_size = size_var.get()
        if puzzle_size not in [
            PuzzleSize.SMALL.name,
            PuzzleSize.MEDIUM.name,
            PuzzleSize.LARGE.name,
        ]:
            return False
        return True

    def validate_tile_mode(*args):
        """
        Validates the selected tile mode.
        Returns:
            True if the tile mode is valid, False otherwise.
        """
        tile_mode = tile_var.get()
        if tile_mode not in [
            TileMode.LETTERS.name,
            TileMode.NUMBERS.name,
            TileMode.MIXED.name,
        ]:
            return False
        return True

    def validate_duplication_mode(*args):
        """
        Validates the selected duplication mode.
        Returns:
            True if the duplication mode is valid, False otherwise.
        """
        duplication_mode = dup_var.get()
        if duplication_mode not in [
            DuplicationMode.DUPLICATED.name,
            DuplicationMode.UNIQUE.name,
        ]:
            return False
        return True

    def validate_duplicate_count(*args):
        """
        Validates the duplicate count entered by the user.
        Returns:
            True if the duplicate count is valid, False otherwise.
        """
        try:
            duplicate_mode = dup_var.get()
            duplicate_count = dup_count_var.get()
            if duplicate_mode == DuplicationMode.UNIQUE.name and duplicate_count == "":
                return True
            duplicate_count = int(dup_count_var.get())
            if (
                duplicate_count <= 0 or duplicate_count > 4
            ) and duplicate_mode == DuplicationMode.DUPLICATED.name:
                return False
        except ValueError:
            return False
        return True

    def show_duplicate_count_field(*args):
        """
        Shows or hides the duplicate count field based on the selected duplication mode.

        Args:
            *args: Variable number of arguments.

        Returns:
            None
        """
        # If the selected duplication mode is DUPLICATED, show the duplicate count field
        if dup_var.get() == DuplicationMode.DUPLICATED.name:
            # Define the duplicate count label and entry positions
            dup_count_label.place(relx=0.85, rely=0.7, anchor="e")
            dup_count_entry.place(relx=0.84, rely=0.76, anchor="e")
        else:
            # Hide the duplicate count label and entry if the duplication mode is UNIQUE
            dup_count_label.place_forget()
            dup_count_entry.place_forget()
