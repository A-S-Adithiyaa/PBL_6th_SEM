import tkinter as tk
import subprocess

def create_maze():
    global rows_entry, cols_entry
    input_rows = int(rows_entry.get())
    input_cols = int(cols_entry.get())
    root.destroy()  # Close the current window

    # Run another Python script with the data as command-line argument
    subprocess.call(['python', 'maze_generator.py', str(input_rows), str(input_cols)])

root = tk.Tk()
root.title("Maze Generator")
root.geometry("600x400")  # Set the initial size of the window

# Create a frame to hold the UI elements
frame = tk.Frame(root)
frame.pack(expand=True)

# Create labels and entry boxes for number of rows and columns
rows_label = tk.Label(frame, text="Number of Rows:")
rows_label.pack(padx=10, pady=10)
rows_entry = tk.Entry(frame)
rows_entry.pack(padx=10, pady=10)

cols_label = tk.Label(frame, text="Number of Columns:")
cols_label.pack(padx=10, pady=10)
cols_entry = tk.Entry(frame)
cols_entry.pack(padx=10, pady=10)

# Create the "Create Maze" button
create_button = tk.Button(frame, text="Create Maze", command=create_maze)
create_button.pack(padx=10, pady=10)

root.mainloop()