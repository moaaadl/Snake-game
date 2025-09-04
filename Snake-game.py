import tkinter as tk
import random


# constants 
GAME_HIGHT = 600
GAME_WIDTH = 600
GAME_BGCOLOR = 'black'
SNAKE_COLOR = 'green'
FOOD_COLOR = 'red'
SPACE_SIZE = 20
direction = 'down'
score = 0

wn = tk.Tk() # window
wn.title('snake game') # title

wn.resizable(False, False) # for not change the width and height

# label for info of game
label = tk.Label(
    wn, 
    text=f"Score: {score}",     
    font=("Arial", 25),  
    fg="black",          
)
label.pack(pady=10)

# the body of the game
canvas = tk.Canvas(wn, height=GAME_HIGHT, width=GAME_WIDTH,bg=GAME_BGCOLOR)
canvas.pack()

x, y = [100, 100]
head = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)

def move_snake():
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


    canvas.move(head, dx, dy)
    canvas.after(230, move_snake)


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
        
        if x_food or y_food not in snake:
            return x_food, y_food


food_x, food_y = generate_food(snake_cordinate)
food = canvas.create_oval(food_x, food_y, food_x+SPACE_SIZE, food_y+SPACE_SIZE, fill=FOOD_COLOR)

move_snake()

# end the game.
wn.bind('<q>', lambda event: wn.quit())

wn.mainloop()
