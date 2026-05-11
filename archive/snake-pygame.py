import pygame
import random

# 1. Initialize Pygame
pygame.init()
conf = {"width": 600, "height": 400, "cell": 20}
screen = pygame.display.set_mode((conf["width"], conf["height"]))
clock = pygame.time.Clock()

# 2. Game Variables (Keep logic similar to your Tkinter version)
snake = [[100, 50], [90, 50], [80, 50]]
direction = "RIGHT"

# 3. New Pygame Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Draw logic replacing Tkinter Canvas
    screen.fill((0, 0, 0)) # Black background
    for pos in snake:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], 20, 20))
    
    pygame.display.flip()
    clock.tick(10) # Control speed

pygame.quit()
