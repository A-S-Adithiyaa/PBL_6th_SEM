import tkinter as tk
import subprocess
import sys
import tkinter as tk
import logging
from enum import Enum, auto

import matplotlib.pyplot as plt
import numpy as np

import models
from environment.maze import Maze, Render

import pickle

logging.basicConfig(format="%(levelname)-8s: %(asctime)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)  # Only show messages *equal to or above* this level

filename="sarsa_model.sav"



input_rows = int(sys.argv[1])
input_cols = int(sys.argv[2])

def set_color(color):
    global sel_color
    sel_color = color

def color_the_block(row, col):
    curr_color = grid[row][col].cget('bg')

    if curr_color == 'white':
        if sel_color == 'black':
            new_color = 'black'
            maze[row][col] = 1
        elif sel_color == 'green':
            remove_previous_color('green')
            new_color = 'green'
            red_block_coords.append((row, col))
    else:
        new_color = 'white'
        maze[row][col] = 0

    grid[row][col].configure(bg=new_color)

def remove_previous_color(color):
    if color == 'green':
        for r, c in red_block_coords:
            grid[r][c].configure(bg='white')
        red_block_coords.clear()

def train_maze():
    maze1=np.array(maze)
    # print(red_block_coords)
    game = Maze(maze1, exit_cell=red_block_coords[0][::-1])

    game.render(Render.TRAINING)  # shows all moves and the q table; nice but slow.
    model = models.SarsaTableTraceModel(game)
    h, w, _, _ = model.train(discount=0.90, exploration_rate=0.10, learning_rate=0.10, episodes=200,
                                stop_at_convergence=True)
    print("Saving the model to", filename, "...")
    pickle.dump(model, open(filename, 'wb'))
    print("Saved the model")

    try:
        h  # force a NameError exception if h does not exist, and thus don't try to show win rate and cumulative reward
        fig, (ax1, ax2) = plt.subplots(2, 1, tight_layout=True)
        fig.canvas.manager.set_window_title(model.name)
        ax1.plot(*zip(*w))
        ax1.set_xlabel("episode")
        ax1.set_ylabel("win rate")
        ax2.plot(h)
        ax2.set_xlabel("episode")
        ax2.set_ylabel("cumulative reward")
        plt.show()
    except NameError:
        pass

    # print("Generator", str(maze))
    root.destroy()
    subprocess.call(['python', 'maze_trace.py', str(maze), str(red_block_coords)])


root = tk.Tk()
root.title("Maze")

# root.geometry("900x500")  # Set the initial size of the window

# wx=800
# wy=500
bx=50//input_cols
by=30//input_rows

grid = []
maze = [[0] * input_cols for _ in range(input_rows)]
selected_color = 'black'
green_block_coords = []
red_block_coords = []

color_frame = tk.Frame(root)
color_frame.grid(row=0, column=input_cols, rowspan=input_rows, padx=10)

color_btns = [
    (' ', 'black'),
    (' ', 'green')
]

for btn_text, btn_color in color_btns:
    btn = tk.Button(color_frame, text=btn_text, bg=btn_color, width=10, command=lambda color=btn_color: set_color(color))
    btn.pack(pady=5)

for i in range(input_rows):
    row = []
    for j in range(input_cols):
        block = tk.Button(root, width=bx, height=by, bg='white', command=lambda r=i, c=j: color_the_block(r, c))
        block.grid(row=i, column=j, padx=5, pady=5)
        row.append(block)
    grid.append(row)

train_button=tk.Button(color_frame, width=10, text='Train Maze', height=1, command=train_maze)
train_button.pack(pady=5)

text=tk.Text(color_frame, height=3, width=31, pady=10)
text.pack()
text.insert(tk.END," Select black for the obstacles\n Select green for exit cell")

root.protocol("WM_DELETE_WINDOW", train_maze)
root.mainloop()
