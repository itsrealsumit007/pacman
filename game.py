import tkinter as tk
import random

window = tk.Tk()
window.title("Pac-Man Game")
window.geometry("800x600")

canvas = tk.Canvas(window, width=800, height=600, bg="black")
canvas.pack()

board_width = 800
board_height = 600

high_scores = []

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

def load_high_scores():
    global high_scores
    try:
        with open("high_scores.txt", "r") as file:
            high_scores = [int(score.strip()) for score in file.readlines()]
    except FileNotFoundError:
        # Handle if file does not exist
        high_scores = []

# Function to save high scores to a file
def save_high_scores():
    with open("high_scores.txt", "w") as file:
        for score in high_scores:
            file.write(f"{score}\n")

# Function to update high scores and display them
def update_high_scores(score):
    global high_scores
    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:10]  # Keep only top 10 scores
    save_high_scores()

    # Display high scores
    messagebox.showinfo("High Scores", f"Top Scores:\n\n" + "\n".join(f"{i+1}. {score}" for i, score in enumerate(high_scores)))

# Modify check_game_over function to update high scores
def check_game_over():
    global high_scores, score
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
        
        # Update high scores
        update_high_scores(score)

load_high_scores()

def move_pacman(event):
    global pacman_position
    x, y = pacman_position
    
    if event.keysym == 'Up':
        if y > 0 and not check_wall_collision(x, y - 1):
            y -= 1
    elif event.keysym == 'Down':
        if y < rows - 1 and not check_wall_collision(x, y + 1):
            y += 1
    elif event.keysym == 'Left':
        if x > 0 and not check_wall_collision(x - 1, y):
            x -= 1
    elif event.keysym == 'Right':
        if x < cols - 1 and not check_wall_collision(x + 1, y):
            x += 1
    
    # Animate Pac-Man's movement
    animate_pacman_movement(x, y)

def animate_pacman_movement(x, y):
    global pacman_position
    current_x, current_y = pacman_position
    dx = (x - current_x) * cell_width
    dy = (y - current_y) * cell_height
    canvas.move(pacman, dx, dy)
    pacman_position = [x, y]

    # Check for collisions with food, power pellets, cherries, and portals
    check_food_collision()
    check_power_pellet_collision()
    check_cherries_collision()
    check_portal_collision()


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
    
    valid_moves = []
    if gx > 0 and not check_wall_collision(gx - 1, gy):
        valid_moves.append('Left')
    if gx < cols - 1 and not check_wall_collision(gx + 1, gy):
        valid_moves.append('Right')
    if gy > 0 and not check_wall_collision(gx, gy - 1):
        valid_moves.append('Up')
    if gy < rows - 1 and not check_wall_collision(gx, gy + 1):
        valid_moves.append('Down')
    
    if valid_moves:
        direction = random.choice(valid_moves)
        if direction == 'Up':
            gy -= 1
        elif direction == 'Down':
            gy += 1
        elif direction == 'Left':
            gx -= 1
        elif direction == 'Right':
            gx += 1
    
    # Animate Ghost's movement
    animate_ghost_movement(gx, gy)

def animate_ghost_movement(gx, gy):
    global ghost_position
    current_gx, current_gy = ghost_position
    dx = (gx - current_gx) * cell_width
    dy = (gy - current_gy) * cell_height
    canvas.move(ghost, dx, dy)
    ghost_position = [gx, gy]

    # Check for collisions with Pac-Man
    check_game_over()

    # Re-schedule ghost movement
    window.after(1000, move_ghost)


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

food_positions = [(5, 5), (15, 15), (5, 15), (15, 5)]
food = []

for pos in food_positions:
    x, y = pos
    food.append(canvas.create_oval(x * cell_width + cell_width // 4, y * cell_height + cell_height // 4,
                                   (x + 1) * cell_width - cell_width // 4, (y + 1) * cell_height - cell_height // 4,
                                   fill="white"))

def check_food_collision():
    global score
    px, py = pacman_position
    
    for idx, pos in enumerate(food_positions):
        fx, fy = pos
        if px == fx and py == fy:
            score += 10
            score_label.config(text=f"Score: {score}")
            canvas.delete(food[idx])
            food_positions[idx] = (-1, -1)
            
    window.after(100, check_food_collision)

check_food_collision()

power_pellets = [(3, 3), (17, 17)]
power_pellet = []

for pos in power_pellets:
    x, y = pos
    power_pellet.append(canvas.create_rectangle(x * cell_width + cell_width // 3, y * cell_height + cell_height // 3,
                                                (x + 1) * cell_width - cell_width // 3, (y + 1) * cell_height - cell_height // 3,
                                                fill="blue"))

def check_power_pellet_collision():
    global score
    px, py = pacman_position
    
    for idx, pos in enumerate(power_pellets):
        pp_x, pp_y = pos
        if px == pp_x and py == pp_y:
            score += 50
            score_label.config(text=f"Score: {score}")
            canvas.delete(power_pellet[idx])
            power_pellets[idx] = (-1, -1)
            
    window.after(100, check_power_pellet_collision)

check_power_pellet_collision()

walls = [(2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2),
         (14, 2), (15, 2), (16, 2), (17, 2), (18, 2), (19, 2), (2, 3), (19, 3), (2, 4), (19, 4), (2, 5), (19, 5),
         (2, 6), (19, 6), (2, 7), (19, 7), (2, 8), (19, 8), (2, 9), (19, 9), (2, 10), (19, 10), (2, 11), (19, 11),
         (2, 12), (19, 12), (2, 13), (19, 13), (2, 14), (19, 14), (2, 15), (19, 15), (2, 16), (19, 16), (2, 17),
         (19, 17), (2, 18), (3, 18), (4, 18), (5, 18), (6, 18), (7, 18), (8, 18), (9, 18), (10, 18), (11, 18),
         (12, 18), (13, 18), (14, 18), (15, 18), (16, 18), (17, 18), (18, 18), (19, 18)]

for pos in walls:
    x, y = pos
    canvas.create_rectangle(x * cell_width, y * cell_height, (x + 1) * cell_width, (y + 1) * cell_height, fill="blue")

def check_wall_collision(x, y):
    if (x, y) in walls:
        return True
    return False

def move_ghost():
    global ghost_position
    px, py = pacman_position
    gx, gy = ghost_position
    
    valid_moves = []
    if gx > 0 and not check_wall_collision(gx - 1, gy):
        valid_moves.append('Left')
    if gx < cols - 1 and not check_wall_collision(gx + 1, gy):
        valid_moves.append('Right')
    if gy > 0 and not check_wall_collision(gx, gy - 1):
        valid_moves.append('Up')
    if gy < rows - 1 and not check_wall_collision(gx, gy + 1):
        valid_moves.append('Down')
    
    if valid_moves:
        direction = random.choice(valid_moves)
        if direction == 'Up':
            gy -= 1
        elif direction == 'Down':
            gy += 1
        elif direction == 'Left':
            gx -= 1
        elif direction == 'Right':
            gx += 1
    
    ghost_position = [gx, gy]
    canvas.coords(ghost, gx * cell_width, gy * cell_height, (gx + 1) * cell_width, (gy + 1) * cell_height)
    
    window.after(1000, move_ghost)

move_ghost()

# Additional features:

# cherries as bonus points
cherries_positions = [(7, 7), (13, 13)]
cherries = []

for pos in cherries_positions:
    x, y = pos
    cherries.append(canvas.create_oval(x * cell_width + cell_width // 4, y * cell_height + cell_height // 4,
                                       (x + 1) * cell_width - cell_width // 4, (y + 1) * cell_height - cell_height // 4,
                                       fill="orange"))

def check_cherries_collision():
    global score
    px, py = pacman_position
    
    for idx, pos in enumerate(cherries_positions):
        cx, cy = pos
        if px == cx and py == cy:
            score += 100
            score_label.config(text=f"Score: {score}")
            canvas.delete(cherries[idx])
            cherries_positions[idx] = (-1, -1)
            
    window.after(100, check_cherries_collision)

check_cherries_collision()

# Add portals for teleportation
portals = [(1, 10), (18, 10)]
portal_colors = ["green", "purple"]
portal_pairs = []

for idx, pos in enumerate(portals):
    x, y = pos
    portal_pairs.append(canvas.create_rectangle(x * cell_width, y * cell_height, (x + 1) * cell_width, (y + 1) * cell_height, fill=portal_colors[idx]))

def check_portal_collision():
    px, py = pacman_position
    
    for idx, pos in enumerate(portals):
        portal_x, portal_y = pos
        if px == portal_x and py == portal_y:
            target_portal = portal_pairs[(idx + 1) % 2]
            x0, y0, x1, y1 = canvas.coords(target_portal)
            canvas.move(pacman, x0 - px * cell_width, y0 - py * cell_height)
            pacman_position[0] = (x0 - px * cell_width) // cell_width
            pacman_position[1] = (y0 - py * cell_height) // cell_height
            
    window.after(100, check_portal_collision)

check_portal_collision()

window.mainloop()
