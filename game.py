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

pacman_position = [1, 1]
pacman = canvas.create_oval(pacman_position[0] * cell_width, pacman_position[1] * cell_height,
                            (pacman_position[0] + 1) * cell_width, (pacman_position[1] + 1) * cell_height, fill="yellow")

def move_pacman(event):
    global pacman_position
    x, y = pacman_position
    
    if event.keysym == 'Up':
        if y > 0:
            y -= 1
    elif event.keysym == 'Down':
        if y < rows - 1:
            y += 1
    elif event.keysym == 'Left':
        if x > 0:
            x -= 1
    elif event.keysym == 'Right':
        if x < cols - 1:
            x += 1
    
    pacman_position = [x, y]
    update_pacman_position()

def update_pacman_position():
    x, y = pacman_position
    canvas.coords(pacman, x * cell_width, y * cell_height, (x + 1) * cell_width, (y + 1) * cell_height)

window.bind_all('<KeyPress-Up>', move_pacman)
window.bind_all('<KeyPress-Down>', move_pacman)
window.bind_all('<KeyPress-Left>', move_pacman)
window.bind_all('<KeyPress-Right>', move_pacman)

ghost_position = [10, 10]
ghost = canvas.create_oval(ghost_position[0] * cell_width, ghost_position[1] * cell_height,
                           (ghost_position[0] + 1) * cell_width, (ghost_position[1] + 1) * cell_height, fill="red")

def move_ghost():
    global ghost_position
    px, py = pacman_position
    gx, gy = ghost_position
    
    if gx < px:
        gx += 1
    elif gx > px:
        gx -= 1
    if gy < py:
        gy += 1
    elif gy > py:
        gy -= 1
    
    ghost_position = [gx, gy]
    canvas.coords(ghost, gx * cell_width, gy * cell_height, (gx + 1) * cell_width, (gy + 1) * cell_height)
    
    window.after(500, move_ghost)

move_ghost()

score = 0
score_label = tk.Label(window, text=f"Score: {score}", font=("Helvetica", 16))
score_label.pack()

def check_game_over():
    px, py = pacman_position
    gx, gy = ghost_position
    
    if px == gx and py == gy:
        canvas.create_text(board_width/2, board_height/2, text="Game Over", font=("Helvetica", 36), fill="white")
        window.unbind_all('<KeyPress-Up>')
        window.unbind_all('<KeyPress-Down>')
        window.unbind_all('<KeyPress-Left>')
        window.unbind_all('<KeyPress-Right>')
        canvas.delete(pacman)
        canvas.delete(ghost)

window.after(1000, check_game_over)

window.mainloop()
