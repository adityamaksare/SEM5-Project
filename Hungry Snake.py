import turtle
import time
import random

# Constants for easy configuration
SCREEN_SIZE = 600
BORDER_LIMIT = SCREEN_SIZE // 2 - 10  # Adjusted for snake size
MOVE_STEP = 20
SHIELD_DURATION = 100  # Power-up shield lasts for 100 frames
SHIELD_RESPAWN_COOLDOWN = 200  # Cooldown for shield to respawn
TEXT_SAFE_ZONE = 50  # Area around the top for the score text

# Game variables
delay = 0.1
score = 0
high_score = 0
game_over = False
shield_active = False
shield_timer = 0
shield_respawn_timer = 0
current_snake_color = "white"  # Initial snake color
paused = False  # Game pause state

# Set up the window
wn = turtle.Screen()
wn.title("Snake Game By Vincent Mark and Aditya Maksare")
wn.bgcolor("black")  # Set background to black
wn.setup(width=SCREEN_SIZE, height=SCREEN_SIZE)
wn.tracer(0)

# Create the snake's head
head = turtle.Turtle()
head.shape("square")
head.color(current_snake_color)
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# Create the food
food = turtle.Turtle()
food_shape = random.choice(['square', 'triangle', 'circle'])
food_color = random.choice(['red', 'green', 'yellow', 'blue', 'pink'])  # Random food colors
food.shape(food_shape)
food.color(food_color)
food.penup()

# Create the power-up (shield)
powerup = turtle.Turtle()
powerup.shape("circle")
powerup.color("yellow")
powerup.penup()
powerup.goto(random.randint(-BORDER_LIMIT, BORDER_LIMIT), random.randint(-BORDER_LIMIT, BORDER_LIMIT))
powerup.hideturtle()  # Initially hidden

# Create the scoreboard
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)  # Position high score text higher
pen.write("Score: 0  High Score: 0", align="center", font=("candara", 24, "bold"))

# Create the game over message
game_over_pen = turtle.Turtle()
game_over_pen.speed(0)
game_over_pen.shape("square")
game_over_pen.color("red")
game_over_pen.penup()
game_over_pen.hideturtle()
game_over_pen.goto(0, 0)

# Create the shield timer display
shield_timer_pen = turtle.Turtle()
shield_timer_pen.speed(0)
shield_timer_pen.shape("square")
shield_timer_pen.color("yellow")
shield_timer_pen.penup()
shield_timer_pen.hideturtle()
shield_timer_pen.goto(0, 200)

# List for the snake body segments
segments = []

# Functions to control the snake
def change_direction(new_direction):
    if head.direction != "down" and new_direction == "up":
        head.direction = "up"
    if head.direction != "up" and new_direction == "down":
        head.direction = "down"
    if head.direction != "right" and new_direction == "left":
        head.direction = "left"
    if head.direction != "left" and new_direction == "right":
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + MOVE_STEP)
    elif head.direction == "down":
        head.sety(head.ycor() - MOVE_STEP)
    elif head.direction == "left":
        head.setx(head.xcor() - MOVE_STEP)
    elif head.direction == "right":
        head.setx(head.xcor() + MOVE_STEP)

# Key bindings for movement
wn.listen()
wn.onkeypress(lambda: change_direction("up"), "w")
wn.onkeypress(lambda: change_direction("down"), "s")
wn.onkeypress(lambda: change_direction("left"), "a")
wn.onkeypress(lambda: change_direction("right"), "d")

# Restart the game when R is pressed
def restart_game():
    global score, delay, game_over, shield_active, shield_timer, shield_respawn_timer, current_snake_color
    score = 0
    delay = 0.1
    game_over = False
    shield_active = False
    shield_timer = 0
    shield_respawn_timer = 0
    current_snake_color = "white"  # Reset to initial color
    head.color(current_snake_color)
    head.goto(0, 0)
    head.direction = "Stop"
    game_over_pen.clear()
    shield_timer_pen.clear()
    update_score()

    # Clear all segments
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()

    # Hide powerup and reposition it
    powerup.hideturtle()
    powerup.goto(random.randint(-BORDER_LIMIT, BORDER_LIMIT), random.randint(-BORDER_LIMIT, BORDER_LIMIT))

# Bind the R key to restart the game
wn.onkeypress(restart_game, "r")

# Function to reset the game when a collision occurs
def reset_game():
    global game_over
    if not shield_active:
        time.sleep(1)
        game_over = True
        head.goto(0, 0)
        head.direction = "Stop"
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        game_over_pen.write("GAME OVER\nPress 'R' to Restart", align="center", font=("candara", 36, "bold"))

def update_score():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("candara", 24, "bold"))

def activate_shield():
    global shield_active, shield_timer
    shield_active = True
    shield_timer = SHIELD_DURATION  # Set the shield timer
    shield_timer_pen.color("yellow")  # Reset timer pen color for active shield

def destroy_shield():
    global shield_active
    shield_active = False
    shield_timer_pen.clear()  # Clear the timer display
    # Optional: Display a shield destroyed message
    shield_timer_pen.color("red")
    shield_timer_pen.write("Shield Destroyed", align="center", font=("candara", 24, "bold"))
    # Start the shield respawn cooldown
    global shield_respawn_timer
    shield_respawn_timer = SHIELD_RESPAWN_COOLDOWN

# Function to spawn the food at random positions while avoiding the score text area
def spawn_food():
    while True:
        x = random.randint(-BORDER_LIMIT, BORDER_LIMIT)
        y = random.randint(-BORDER_LIMIT, BORDER_LIMIT)
        # Check if the food spawns in the safe zone
        if y < 260 - TEXT_SAFE_ZONE:  # Avoid the score area
            food.goto(x, y)
            food.showturtle()  # Show the food turtle
            break

# Spawn the initial food
spawn_food()

# Wall wrapping when shield is active
def handle_wall_collision():
    if head.xcor() > BORDER_LIMIT:
        head.setx(-BORDER_LIMIT)
    elif head.xcor() < -BORDER_LIMIT:
        head.setx(BORDER_LIMIT)
    if head.ycor() > BORDER_LIMIT:
        head.sety(-BORDER_LIMIT)
    elif head.ycor() < BORDER_LIMIT:
        head.sety(BORDER_LIMIT)

# Pause functionality
def toggle_pause():
    global paused
    paused = not paused  # Toggle the pause state
    if paused:
        # Save the current position of the pen
        pen_pos = pen.position()
        pen.goto(0, 0)
        pen.write("PAUSED", align="center", font=("candara", 36, "bold"))
        pen.goto(pen_pos)  # Restore the pen's position
    else:
        pen.clear()
        update_score()  # Refresh the score display


# Bind the P key to toggle pause
wn.onkeypress(toggle_pause, "p")

# Main game loop
while True:
    wn.update()

    if not game_over and not paused:  # Only update the game if it's not over and not paused
        # Update shield respawn cooldown
        if shield_respawn_timer > 0:
            shield_respawn_timer -= 1

        # Border collision detection with shield wrapping logic
        if abs(head.xcor()) > BORDER_LIMIT or abs(head.ycor()) > BORDER_LIMIT:
            if shield_active:
                handle_wall_collision()
            else:
                reset_game()

        # Food collision detection
        if head.distance(food) < 20:
            # Change the snake's color to the food's color
            current_snake_color = food.color()[0]  # Use the color of the eaten food
            head.color(current_snake_color)
            for segment in segments:
                segment.color(current_snake_color)

            # Spawn new food in a valid location with a new random color
            food_color = random.choice(['red', 'green', 'yellow', 'blue', 'pink'])  # New color for food
            food.shape(random.choice(['square', 'triangle', 'circle']))  # Random shape for food
            food.color(food_color)
            spawn_food()

            # Add a new segment to the snake's body
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color(current_snake_color)  # Tail color changes too
            new_segment.penup()
            segments.append(new_segment)

            # Increase the score
            score += 10
            if score > high_score:
                high_score = score

            update_score()
            delay -= 0.001  # Decrease delay to speed up game

        # Move the snake's body
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)

        move()

        # Shield logic
        if shield_active:
            shield_timer -= 1
            shield_timer_pen.clear()
            shield_timer_pen.write(f"Shield Active: {shield_timer}", align="center", font=("candara", 24, "bold"))
            if shield_timer <= 0:
                destroy_shield()

        # Respawn shield if cooldown is over
        if shield_respawn_timer == 0 and not shield_active:
            activate_shield()
            powerup.goto(random.randint(-BORDER_LIMIT, BORDER_LIMIT), random.randint(-BORDER_LIMIT, BORDER_LIMIT))
            powerup.showturtle()

        # Power-up collision detection
        if head.distance(powerup) < 20:
            activate_shield()
            powerup.hideturtle()  # Hide the power-up after collecting it

        # Self collision detection
        for segment in segments:
            if segment.distance(head) < 20:
                reset_game()

    time.sleep(delay)

wn.mainloop()