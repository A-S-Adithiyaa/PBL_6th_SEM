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
            green_block_coords.append((row, col))
        elif sel_color == 'red':
            remove_previous_color('red')
            new_color = 'red'
            red_block_coords.append((row, col))
    elif curr_color == 'green' and sel_color == 'red':
        remove_previous_color('green')
        new_color = 'red'
        red_block_coords.append((row, col))
    elif curr_color == 'red' and sel_color == 'green':
        remove_previous_color('red')
        new_color = 'green'
        green_block_coords.append((row, col))
    else:
        new_color = 'white'
        maze[row][col] = 0

    grid[row][col].configure(bg=new_color)

def remove_previous_color(color):
    if color == 'green':
        for r, c in green_block_coords:
            grid[r][c].configure(bg='white')
        green_block_coords.clear()
    elif color == 'red':
        for r, c in red_block_coords:
            grid[r][c].configure(bg='white')
        red_block_coords.clear()

def stop():
    maze1=np.array(maze)
    game = Maze(maze1)

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

    model = pickle.load(open(filename, 'rb'))
    game.render(Render.MOVES)
    game.play(model, start_cell=green_block_coords[0])

    # print(maze)
    # print("Green Block Coordinates:", green_block_coords)
    # print("Red Block Coordinates:", red_block_coords)
    root.destroy()

root = tk.Tk()
root.title("Maze")

grid = []
maze = [[0] * 6 for _ in range(6)]
selected_color = 'black'
green_block_coords = []
red_block_coords = []

color_frame = tk.Frame(root)
color_frame.grid(row=0, column=6, rowspan=6, padx=10)

color_btns = [
    ('Black', 'black'),
    ('Green', 'green'),
    ('Red', 'red')
]

for btn_text, btn_color in color_btns:
    btn = tk.Button(color_frame, text=btn_text, width=10, command=lambda color=btn_color: set_color(color))
    btn.pack(pady=5)

for i in range(6):
    row = []
    for j in range(6):
        block = tk.Button(root, width=10, height=5, bg='white',
                          command=lambda r=i, c=j: color_the_block(r, c))
        block.grid(row=i, column=j, padx=5, pady=5)
        row.append(block)
    grid.append(row)

root.protocol("WM_DELETE_WINDOW", stop)
root.mainloop()
