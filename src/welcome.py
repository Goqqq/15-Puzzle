import tkinter as tk
from tkinter import PhotoImage
import os


def start_puzzle():
    print(
        "Starting the puzzle..."
    )  # This should be replaced with actual code to transition to the puzzle game


def create_welcome_window(root):
    # Load the background image
    dir_of_script = os.path.dirname(os.path.abspath(__file__))
    assets_path = os.path.join(dir_of_script, os.pardir, "assets")
    print(assets_path)
    background_path = os.path.join(
        assets_path, "images", "Welcome.png"
    )  # Replace with your background image path
    background_image = PhotoImage(file=background_path)

    # Set the background image
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create the start button
    start_button = tk.Button(
        root,
        text="Start the Puzzle",
        command=start_puzzle,
        bg="#333333",
        fg="white",
        font=("Helvetica", 16),
    )
    start_button_width = 200  # Adjust the size as needed
    start_button_height = 50  # Adjust the size as needed
    start_button_window_width = root.winfo_screenwidth()  # Get screen width
    start_button_window_height = root.winfo_screenheight()  # Get screen height
    start_button_x = (
        start_button_window_width - start_button_width
    ) // 2  # Center the button
    start_button_y = (
        start_button_window_height - start_button_height
    ) // 2  # Center the button
    start_button.place(
        width=start_button_width,
        height=start_button_height,
        x=start_button_x,
        y=start_button_y,
    )

    # Keep a reference to the background image to prevent garbage collection
    root.background_image = background_image


# This allows the module to be imported without executing the window creation code automatically
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Puzzle Game")
    create_welcome_window(root)
    root.mainloop()
