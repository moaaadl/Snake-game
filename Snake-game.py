import tkinter as tk
import random

# constants 
GAME_HIGHT = 600
GAME_WIDTH = 600
GAME_BGCOLOR = 'black'
SNAKE_COLOR = 'green'
FOOD_COLOR = 'red'
SPACE_SIZE = 20
direction = 'right'
score = 0
SPEED = 230

wn = tk.Tk() # window
wn.title('snake game') # title

wn.resizable(False, False) # for not change the width and height

# label for info of game

frame = tk.Frame(wn)
frame.pack(pady=10)

label_text = tk.Label(frame, text="Score: ", font=("Arial", 25), fg="black")
label_text.pack(side="left")

label_score = tk.Label(frame, text=score, font=("Arial", 25), fg="black")
label_score.pack(side="left")

# the body of the game
canvas = tk.Canvas(wn, height=GAME_HIGHT, width=GAME_WIDTH,bg=GAME_BGCOLOR)
canvas.pack()

x, y = [100, 100]
head = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)

snake = [head]

game_over = False

game_paused = False

def pause_game():
    global game_paused
    game_paused = not game_paused
    if game_paused:
        label_text.config(text="PAUSED", fg="blue")
        label_score.config(text="", fg="white")
    else:
        label_text.config(text=f"Score: ", fg="black")
        label_score.config(text=score, fg="black")
        move_snake()


def move_snake(): 
    global game_over
    global game_paused
    global SPEED
    if game_over:
        return # end game
    elif game_paused:
        return
    

    dx = 0
    dy = 0
    if direction == 'right':
        dx = 20
        dy = 0
    elif direction == 'left':
        dx = -20
        dy = 0
    elif direction == 'up':
        dx = 0
        dy = -20
    elif direction == 'down':
        dx = 0
        dy = +20

    corrdinates = canvas.coords(head)
    
    # for x
    if corrdinates[2] > GAME_WIDTH: # right
        canvas.coords(head, -SPACE_SIZE, corrdinates[1], 0, corrdinates[3])
    elif corrdinates[0] < 0: # left
        canvas.coords(head, GAME_WIDTH, corrdinates[1], GAME_WIDTH+SPACE_SIZE, corrdinates[3])

    # for y
    elif corrdinates[3] > GAME_HIGHT: # up
        canvas.coords(head, corrdinates[0], -SPACE_SIZE, corrdinates[2], 0)
    elif corrdinates[3] <= 0: # down
        canvas.coords(head, corrdinates[0], GAME_HIGHT+SPACE_SIZE, corrdinates[2], GAME_HIGHT)
    
    # eat food 
    global score 
    food_cordinates = canvas.coords(food)
    if corrdinates == food_cordinates:
        x, y = generate_food(head)
        canvas.coords(food, x, y, x+SPACE_SIZE, y+SPACE_SIZE)
        score += 1
        label_score.config(text="+1", fg="green")
        wn.after(500, lambda: label_score.config(text=score, fg="black"))
        body_snake = canvas.create_rectangle(*corrdinates, fill=SNAKE_COLOR)
        snake.append(body_snake)


        if score % 5 == 0 and SPEED > 50:  
            SPEED -= 20  

    for i in range(len(snake)-1, 0, -1):
        canvas.coords(snake[i], *canvas.coords(snake[i-1])) # Move each body part to the position of the part in front of it

    canvas.move(head, dx, dy)

    for j in range(1, len(snake)):
        if canvas.coords(head) == canvas.coords(snake[j]):
            label_text.config(text="GAME_OVER", fg="red")
            label_score.config(text="", fg="white")
            game_over = True
            return
    

    canvas.after(SPEED, move_snake)


# this for the key direction 
wn.bind("<Left>", lambda event: change_direction("left"))
wn.bind("<Right>", lambda event: change_direction("right"))
wn.bind("<Up>", lambda event: change_direction("up"))
wn.bind("<Down>", lambda event: change_direction("down"))


def change_direction(new_direction):
    global direction
    if direction == 'left':
        if new_direction != 'right':
            direction = new_direction
    elif direction == 'right':
        if new_direction != 'left':
            direction = new_direction
    elif direction == 'up':
        if new_direction != 'down':
            direction = new_direction
    elif direction == 'down':
        if new_direction != 'up':
            direction = new_direction


snake_cordinate = canvas.coords(head)

def generate_food(snake):
    while True:
        x_food = random.randint(0, (GAME_WIDTH // SPACE_SIZE) -1) * SPACE_SIZE
        y_food = random.randint(0, (GAME_HIGHT // SPACE_SIZE) -1) * SPACE_SIZE
        
        if [x_food, y_food] != snake:
            return x_food, y_food


food_x, food_y = generate_food(snake_cordinate)
food = canvas.create_oval(food_x, food_y, food_x+SPACE_SIZE, food_y+SPACE_SIZE, fill=FOOD_COLOR)

move_snake()


# were here ---


def reset_game():
    GAME_HIGHT = 600
    GAME_WIDTH = 600
    GAME_BGCOLOR = 'black'
    SNAKE_COLOR = 'green'
    FOOD_COLOR = 'red'
    SPACE_SIZE = 20
    direction = 'right'
    score = 0
    SPEED = 230
    x, y = [100, 100]

def restart_game():
    reset_game()
    for s in snake:
        canvas.delete(s)
    canvas.delete(head, food)
    SPEED = 230
    direction = "right"
    score = 0

    new_head = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)
    move_snake()

# -----


    


wn.bind("<space>", lambda event: restart_game())

# pause the game.
wn.bind("<p>", lambda event: pause_game())
# end the game.
wn.bind('<q>', lambda event: wn.quit())

wn.mainloop()
