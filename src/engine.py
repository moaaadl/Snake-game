import pygame
import os
from enum import Enum
from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, COLOR_BG, COLOR_GRID,
    COLOR_TEXT, INITIAL_SPEED, SPEED_INCREMENT, MAX_SPEED, COLOR_UI_PANEL
)
from src.snake import Snake
from src.food import Food

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

class GameEngine:
    """Main game engine handling logic and rendering."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pro Snake Elite")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("Arial", 64, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 32)
        self.font_small = pygame.font.SysFont("Arial", 24)

        self.high_score = self._load_high_score()
        self.reset_game()
        self.state = GameState.MENU

    def _load_high_score(self) -> int:
        """Loads the high score from a file."""
        if os.path.exists("highscore.txt"):
            try:
                with open("highscore.txt", "r") as f:
                    content = f.read().strip()
                    return int(content) if content else 0
            except (ValueError, IOError):
                return 0
        return 0

    def _save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def reset_game(self):
        self.snake = Snake(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.food = Food(WINDOW_WIDTH, WINDOW_HEIGHT, self.snake.body)
        self.score = 0
        self.speed = INITIAL_SPEED
        self.state = GameState.PLAYING

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_p:
                        self.state = GameState.PAUSED
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_p:
                        self.state = GameState.PLAYING
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()

        if self.state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            self.snake.handle_keys(keys)

        return True

    def update(self):
        if self.state != GameState.PLAYING:
            return

        self.snake.move()

        # Check food collision
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.respawn(self.snake.body)
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
                self._save_high_score()

            # Increase speed
            if self.speed < MAX_SPEED:
                self.speed += SPEED_INCREMENT

        # Check death
        if self.snake.check_collision(WINDOW_WIDTH, WINDOW_HEIGHT):
            self.state = GameState.GAME_OVER

    def _draw_grid(self):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (WINDOW_WIDTH, y))

    def _draw_ui(self):
        # Draw score panel
        score_text = self.font_small.render(f"Score: {self.score}", True, COLOR_TEXT)
        high_score_text = self.font_small.render(f"High Score: {self.high_score}", True, COLOR_TEXT)

        self.screen.blit(score_text, (20, 10))
        self.screen.blit(high_score_text, (WINDOW_WIDTH - 200, 10))

    def _draw_overlay(self, title: str, subtitle: str):
        # Darken background
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        title_surf = self.font_large.render(title, True, (255, 255, 255))
        subtitle_surf = self.font_medium.render(subtitle, True, (200, 200, 200))

        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        subtitle_rect = subtitle_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))

        self.screen.blit(title_surf, title_rect)
        self.screen.blit(subtitle_surf, subtitle_rect)

    def draw(self):
        self.screen.fill(COLOR_BG)
        self._draw_grid()

        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        self._draw_ui()

        if self.state == GameState.MENU:
            self._draw_overlay("PRO SNAKE ELITE", "Press SPACE to Start")
        elif self.state == GameState.PAUSED:
            self._draw_overlay("PAUSED", "Press P to Resume")
        elif self.state == GameState.GAME_OVER:
            self._draw_overlay("GAME OVER", f"Score: {self.score} | Press SPACE to Restart")

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.speed)

        pygame.quit()
