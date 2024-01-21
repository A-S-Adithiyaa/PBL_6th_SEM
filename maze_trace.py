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

maze=sys.argv[1]
red_coord=sys.argv[2]

print(maze, red_coord)

x=int(red_coord[2])
y=int(red_coord[5])
red_coord=(x, y)
s=maze[1:-1]
maze=[]
stack=[]
li=[]
for i in s:
    if i=='[':
        stack.append(i)
    elif i==']' and stack[-1]=='[':
        maze.append(li)
        li=[]
    elif i==',' or i==' ':
        continue
    else:
        li.append(int(i))

print("Trace", maze, red_coord)

# import tkinter as tk

root = tk.Tk()
root.title("Maze")

# root.geometry("900x500")  # Set the initial size of the window

# wx=800
# wy=500
bx=50//len(maze[0])
by=30//len(maze)

grid = []
frame = tk.Frame(root)
frame.grid(row=0, column=len(maze[0]), rowspan=len(maze), padx=10)


selected_button = None  
green_coordinates=None
def start_button_click():
    global selected_button
    if selected_button is not None:
        selected_button.config(bg='white')  
    selected_button = None
    green_coordinates=None

def button_click(i, j):
    global selected_button, green_coordinates
    if selected_button is not None:
        if maze[i][j] == 0:
            selected_button.config(bg='white')  
        selected_button = None
    if maze[i][j] == 0:
        selected_button = grid[i][j]
        selected_button.config(bg='red')
        green_coordinates=(i, j)

def trace():
    maze1 = np.array(maze)  # 0 = free, 1 = occupied

    print("Inside trace: ", green_coordinates, red_coord)
    game = Maze(maze1, start_cell=green_coordinates[::-1], exit_cell=red_coord[::-1], train=False)

    model = pickle.load(open(filename, 'rb'))
    game.render(Render.MOVES)
    game.play(model, start_cell=green_coordinates[::-1])

    plt.show() 

# print(maze, type(maze))
for i in range(len(maze)):
    row = []
    for j in range(len(maze[0])):
        if i == x and j == y:
            block = tk.Button(root, width=bx, height=by, bg='green')
        elif maze[i][j] == 0:
            block = tk.Button(root,  width=bx, height=by, bg='white')
        elif maze[i][j] == 1:
            block = tk.Button(root,  width=bx, height=by, bg='black')

        block.config(command=lambda i=i, j=j: button_click(i, j))

        block.grid(row=i, column=j, padx=5, pady=5)
        row.append(block)
    grid.append(row)

start_button = tk.Button(frame, width=20, text='Select start button', height=1, command=start_button_click)
start_button.pack(pady=5)

trace_button = tk.Button(frame, width=10, text='Trace Maze', height=1, command=trace)
trace_button.pack(pady=5)



root.protocol("WM_DELETE_WINDOW")
root.mainloop()