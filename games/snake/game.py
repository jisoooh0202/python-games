"""Main Snake game implementation."""

import pygame
from shared.base_game import BaseGame
from shared.constants import MEDIUM_FONT
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, GAME_SPEED,
    SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR, FOOD_COLOR, 
    BACKGROUND_COLOR, TEXT_COLOR
)
from .entities import Snake, Food, Direction


class SnakeGame(BaseGame):
    """Main Snake game class."""
    
    def __init__(self):
        """Initialize the Snake game."""
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Snake Game")
        self.font = pygame.font.Font(None, MEDIUM_FONT)
        self.reset_game()
        
    def reset_game(self):
        """Reset the game to initial state."""
        # Initialize snake at center of screen
        center_x = WINDOW_WIDTH // GRID_SIZE // 2
        center_y = WINDOW_HEIGHT // GRID_SIZE // 2
        self.snake = Snake(center_x, center_y)
        
        # Initialize food
        self.food = Food()
        self.food.regenerate(self.snake.body)
        
        # Game state
        self.score = 0
        self.game_over = False
        
    def handle_input(self):
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    # Handle direction changes
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(Direction.RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        return False
                        
        return True
        
    def update(self):
        """Update game state."""
        if self.game_over:
            return
            
        # Move snake
        self.snake.move()
        
        # Check collisions
        if self.snake.check_wall_collision() or self.snake.check_self_collision():
            self.game_over = True
            return
            
        # Check food collision
        if self.snake.get_head() == self.food.get_position():
            self.score += 10
            self.snake.grow()
            self.food.regenerate(self.snake.body)
        else:
            # Remove tail if no food eaten
            self.snake.shrink()
            
    def draw(self):
        """Draw the game."""
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        if not self.game_over:
            # Draw snake
            for i, segment in enumerate(self.snake.body):
                x = segment[0] * GRID_SIZE
                y = segment[1] * GRID_SIZE
                color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
                pygame.draw.rect(self.screen, color, (x, y, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(self.screen, BACKGROUND_COLOR, (x, y, GRID_SIZE, GRID_SIZE), 1)
                
            # Draw food
            food_x, food_y = self.food.get_position()
            food_x *= GRID_SIZE
            food_y *= GRID_SIZE
            pygame.draw.rect(self.screen, FOOD_COLOR, (food_x, food_y, GRID_SIZE, GRID_SIZE))
            
            # Draw score
            score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
            self.screen.blit(score_text, (10, 10))
            
            # Draw controls
            controls_text = self.font.render("Use arrow keys to move, ESC to quit", True, TEXT_COLOR)
            self.screen.blit(controls_text, (10, WINDOW_HEIGHT - 30))
            
        else:
            # Game over screen
            game_over_text = self.font.render("GAME OVER", True, FOOD_COLOR)
            score_text = self.font.render(f"Final Score: {self.score}", True, TEXT_COLOR)
            restart_text = self.font.render("Press SPACE to play again, ESC to quit", True, TEXT_COLOR)
            
            # Center the text
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)
            
        pygame.display.flip()
        
    def run(self):
        """Main game loop with custom timing."""
        while self.running:
            self.running = self.handle_input()
            if self.running:
                self.update()
                self.draw()
                self.clock.tick(GAME_SPEED)
                
        pygame.quit()
