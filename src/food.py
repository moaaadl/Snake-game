import pygame
import random
from typing import List, Tuple
from src.constants import GRID_SIZE, COLOR_FOOD

class Food:
    """Class representing the food in the game."""

    def __init__(self, width: int, height: int, snake_body: List[Tuple[int, int]]):
        self.width = width
        self.height = height
        self.position = self._generate_position(snake_body)

    def _generate_position(self, snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Generates a random position for the food that is not on the snake's body."""
        while True:
            x = random.randrange(0, self.width, GRID_SIZE)
            y = random.randrange(0, self.height, GRID_SIZE)
            if (x, y) not in snake_body:
                return (x, y)

    def respawn(self, snake_body: List[Tuple[int, int]]):
        """Respawns the food at a new location."""
        self.position = self._generate_position(snake_body)

    def draw(self, surface: pygame.Surface):
        """Renders the food on the given surface."""
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.ellipse(surface, COLOR_FOOD, rect)
