from tkinter import ttk
from tkinter import *

def my_function():
    block_positions = {}
    window = Tk()
    window.title("Algoritmeja Labyrintissa")
    file_name = "data/room1.map"
    label = ttk.Label(
        window,
        text=f"column: {0}, row: {0}"
    )
    label.grid(row=0, column=0)
    """ 
    with open(file_name, 'r') as f:
        for y, line in enumerate(f):
            for x, c in enumerate(line):
                if not c.isspace():
                    block_positions[(x,y)] = c
                    label = ttk.Label(
                        window,
                        text=f"column: {y}, row: {x}"
                    )
                    label.grid(row=x, column=y)
"""
    window.mainloop()
    return block_positions




my_function()