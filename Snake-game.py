import tkinter as tk
import random

# constants
GAME_HEIGHT = 600
GAME_WIDTH = 600
GAME_BGCOLOR = 'black'
SNAKE_COLOR = 'green'
FOOD_COLOR = 'red'
SPACE_SIZE = 20
SPEED = 230

# globals
direction = 'right'
score = 0
game_over = False
game_paused = False

# window
wn = tk.Tk()
wn.title('snake game')
wn.resizable(False, False)

# score frame
frame = tk.Frame(wn)
frame.pack(pady=10)

label_text = tk.Label(frame, text="Score: ", font=("Arial", 25), fg="black")
label_text.pack(side="left")

label_score = tk.Label(frame, text=score, font=("Arial", 25), fg="black")
label_score.pack(side="left")

# canvas
canvas = tk.Canvas(wn, height=GAME_HEIGHT, width=GAME_WIDTH, bg=GAME_BGCOLOR)
canvas.pack()

# snake start
x, y = 100, 100
head = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
snake = [head]

def pause_game():
    global game_paused
    game_paused = not game_paused
    if game_paused:
        label_text.config(text="PAUSED", fg="blue")
        label_score.config(text="", fg="white")
    else:
        label_text.config(text="Score: ", fg="black")
        label_score.config(text=score, fg="black")
        move_snake()

after_id = None

def move_snake():
    global game_over, SPEED, score, after_id

    if game_over or game_paused:
        return

    dx, dy = 0, 0
    if direction == 'right':
        dx = SPACE_SIZE
    elif direction == 'left':
        dx = -SPACE_SIZE
    elif direction == 'up':
        dy = -SPACE_SIZE
    elif direction == 'down':
        dy = SPACE_SIZE

    coordinates = canvas.coords(head)

    # border wrap
    if coordinates[2] > GAME_WIDTH:
        canvas.coords(head, -SPACE_SIZE, coordinates[1], 0, coordinates[3])
    elif coordinates[0] < 0:
        canvas.coords(head, GAME_WIDTH, coordinates[1], GAME_WIDTH + SPACE_SIZE, coordinates[3])
    elif coordinates[3] > GAME_HEIGHT:
        canvas.coords(head, coordinates[0], -SPACE_SIZE, coordinates[2], 0)
    elif coordinates[3] <= 0:
        canvas.coords(head, coordinates[0], GAME_HEIGHT + SPACE_SIZE, coordinates[2], GAME_HEIGHT)

    # eat food
    food_coordinates = canvas.coords(food)
    if coordinates == food_coordinates:
        x, y = generate_food(coordinates)
        canvas.coords(food, x, y, x + SPACE_SIZE, y + SPACE_SIZE)
        score += 1
        label_score.config(text="+1", fg="green")
        wn.after(500, lambda: label_score.config(text=score, fg="black"))

        body_part = canvas.create_rectangle(*coordinates, fill=SNAKE_COLOR)
        snake.append(body_part)

        if score % 5 == 0 and SPEED > 50:
            SPEED -= 20

    # body follow
    for i in range(len(snake) - 1, 0, -1):
        canvas.coords(snake[i], *canvas.coords(snake[i - 1]))

    canvas.move(head, dx, dy)

    # collision with itself
    for j in range(1, len(snake)):
        if canvas.coords(head) == canvas.coords(snake[j]):
            label_text.config(text="GAME OVER", fg="red")
            label_score.config(text="", fg="white")
            game_over = True
            return

    after_id = canvas.after(SPEED, move_snake)

def change_direction(new_direction):
    global direction
    if direction == 'left' and new_direction != 'right':
        direction = new_direction
    elif direction == 'right' and new_direction != 'left':
        direction = new_direction
    elif direction == 'up' and new_direction != 'down':
        direction = new_direction
    elif direction == 'down' and new_direction != 'up':
        direction = new_direction

def generate_food(snake):
    while True:
        x_food = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y_food = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        if [x_food, y_food] != snake:
            return x_food, y_food

def reset_game():
    GAME_HEIGHT = 600
    GAME_WIDTH = 600
    GAME_BGCOLOR = 'black'
    SNAKE_COLOR = 'green'
    FOOD_COLOR = 'red'
    SPACE_SIZE = 20
    direction = 'right'
    score = 0
    x, y = [100, 100]
    return GAME_HEIGHT, GAME_WIDTH, GAME_BGCOLOR, SNAKE_COLOR, FOOD_COLOR, SPACE_SIZE, direction, score, x, y

def restart_game():
    global head, food, snake, direction, score, game_over, after_id
    
    if after_id is not None:
        canvas.after_cancel(after_id)

    SPEED = 230
    direction = "right"
    score = 0
    game_over = False

    _, _, _, _, _, _, direction, score, x, y = reset_game()

    for s in snake:
        canvas.delete(s)
    canvas.delete(head, food)

    head = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake = [head]

    food_x, food_y = generate_food([x, y])
    food = canvas.create_oval(food_x, food_y, food_x + SPACE_SIZE, food_y + SPACE_SIZE, fill=FOOD_COLOR)

    label_text.config(text="Score:", fg="black")
    label_score.config(text=score, fg="black")

    move_snake()

# controls
wn.bind("<Left>", lambda event: change_direction("left"))
wn.bind("<Right>", lambda event: change_direction("right"))
wn.bind("<Up>", lambda event: change_direction("up"))
wn.bind("<Down>", lambda event: change_direction("down"))
wn.bind("<space>", lambda event: restart_game())
wn.bind("<p>", lambda event: pause_game())
wn.bind("<q>", lambda event: wn.quit())

food_x, food_y = generate_food(canvas.coords(head))
food = canvas.create_oval(food_x, food_y, food_x + SPACE_SIZE, food_y + SPACE_SIZE, fill=FOOD_COLOR)

move_snake()
wn.mainloop()
