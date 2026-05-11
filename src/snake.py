import pygame
from typing import List, Tuple
from src.constants import GRID_SIZE, COLOR_SNAKE, COLOR_SNAKE_HEAD, RIGHT, UP, DOWN, LEFT

class Snake:
    """Class representing the snake in the game."""

    def __init__(self, x: int, y: int):
        self.body: List[Tuple[int, int]] = [(x, y), (x - GRID_SIZE, y), (x - 2 * GRID_SIZE, y)]
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Tuple[int, int] = RIGHT
        self.growing: bool = False

    def handle_keys(self, keys: pygame.key.ScancodeWrapper):
        """Updates the next direction based on keyboard input."""
        if keys[pygame.K_UP] and self.direction != DOWN:
            self.next_direction = UP
        elif keys[pygame.K_DOWN] and self.direction != UP:
            self.next_direction = DOWN
        elif keys[pygame.K_LEFT] and self.direction != RIGHT:
            self.next_direction = LEFT
        elif keys[pygame.K_RIGHT] and self.direction != LEFT:
            self.next_direction = RIGHT

    def move(self):
        """Moves the snake one step forward."""
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)

        self.body.insert(0, new_head)
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def grow(self):
        """Triggers snake growth on next move."""
        self.growing = True

    def check_collision(self, width: int, height: int) -> bool:
        """Checks if the snake has collided with walls or itself."""
        head = self.body[0]

        # Wall collision
        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            return True

        # Self collision
        if head in self.body[1:]:
            return True

        return False

    def draw(self, surface: pygame.Surface):
        """Renders the snake on the given surface."""
        for i, segment in enumerate(self.body):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE
            rect = pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            # Add a small border to segments for better visibility
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)
