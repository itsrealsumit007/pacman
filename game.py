import tkinter as tk

window = tk.Tk()
window.title("Pac-Man Game")
window.geometry("800x600")

canvas = tk.Canvas(window, width=800, height=600, bg="black")
canvas.pack()

board_width = 800
board_height = 600

rows = 20
cols = 20

cell_width = board_width // cols
cell_height = board_height // rows

for i in range(rows):
    canvas.create_line(0, i * cell_height, board_width, i * cell_height, fill="white")
for j in range(cols):
    canvas.create_line(j * cell_width, 0, j * cell_width, board_height, fill="white")

pacman = canvas.create_oval(50, 50, 100, 100, fill="yellow")

def move_pacman(event):
    if event.keysym == 'Up':
        canvas.move(pacman, 0, -cell_height)
    elif event.keysym == 'Down':
        canvas.move(pacman, 0, cell_height)
    elif event.keysym == 'Left':
        canvas.move(pacman, -cell_width, 0)
    elif event.keysym == 'Right':
        canvas.move(pacman, cell_width, 0)

window.bind_all('<KeyPress-Up>', move_pacman)
window.bind_all('<KeyPress-Down>', move_pacman)
window.bind_all('<KeyPress-Left>', move_pacman)
window.bind_all('<KeyPress-Right>', move_pacman)

window.mainloop()
