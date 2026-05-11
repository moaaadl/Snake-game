import pygame

# Screen settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20

# Colors (Modern Palette)
COLOR_BG = (30, 30, 30)
COLOR_GRID = (40, 40, 40)
COLOR_SNAKE = (0, 200, 100)
COLOR_SNAKE_HEAD = (0, 255, 130)
COLOR_FOOD = (255, 50, 50)
COLOR_TEXT = (230, 230, 230)
COLOR_UI_PANEL = (50, 50, 50)

# Game settings
INITIAL_SPEED = 10
SPEED_INCREMENT = 0.5
MAX_SPEED = 25

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
