"""Main Typing game implementation."""

import pygame
import random
from shared.base_game import BaseGame
from .constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    WORD_FONT_SIZE,
    UI_FONT_SIZE,
    TITLE_FONT_SIZE,
    BACKGROUND_COLOR,
    WORD_COLOR,
    UI_COLOR,
    MISSED_COLOR,
)
from .entities import FallingWord, GameState


class TypingGame(BaseGame):
    """Main Typing game class."""

    def __init__(self):
        """Initialize the Typing game."""
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Typing Rain")
        self.word_font = pygame.font.Font(None, WORD_FONT_SIZE)
        self.ui_font = pygame.font.Font(None, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)

        self.game_state = GameState()
        self.falling_words = []
        self.spawn_timer = 0
        self.game_over = False
        self.current_input = ""

    def reset_game(self):
        """Reset the game to initial state."""
        self.game_state.reset()
        self.falling_words = []
        self.spawn_timer = 0
        self.game_over = False
        self.current_input = ""

    def spawn_word(self):
        """Spawn a new falling word."""
        word_list = self.game_state.get_word_list()
        word = random.choice(word_list)

        # Random x position with some margin
        word_surface = self.word_font.render(word, True, WORD_COLOR)
        word_width = word_surface.get_width()
        max_x = WINDOW_WIDTH - word_width - 20
        x = random.randint(20, max(20, max_x))

        fall_speed = self.game_state.get_fall_speed()
        falling_word = FallingWord(word, x, -50, fall_speed, self.word_font)
        self.falling_words.append(falling_word)

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
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_BACKSPACE:
                        # Clear current input
                        self.current_input = ""
                    else:
                        # Handle character input
                        char = event.unicode
                        if char.isalpha() or char.isspace():
                            self.handle_char_input(char)

        return True

    def handle_char_input(self, char):
        """Handle character input for typing."""
        char = char.lower()

        # Try to match character with falling words
        for word in self.falling_words:
            if not word.completed and word.type_char(char):
                if word.completed:
                    # Word completed!
                    self.game_state.add_score(len(word.text))
                    self.falling_words.remove(word)

                    # Check for level up
                    if self.game_state.should_level_up():
                        self.game_state.level_up()
                break

    def update(self):
        """Update game state."""
        if self.game_over:
            return

        # Check for game over
        if self.game_state.is_game_over():
            self.game_over = True
            return

        # Spawn new words
        self.spawn_timer += 1
        if self.spawn_timer >= self.game_state.get_spawn_rate():
            self.spawn_word()
            self.spawn_timer = 0

        # Update falling words
        for word in self.falling_words[:]:
            word.update()

            # Remove words that fell off screen
            if word.is_off_screen():
                if not word.completed:
                    self.game_state.miss_word()
                self.falling_words.remove(word)

    def draw_ui(self):
        """Draw the user interface."""
        # Draw level
        level_text = self.ui_font.render(f"Level: {self.game_state.level}", True, UI_COLOR)
        self.screen.blit(level_text, (10, 10))

        # Draw score
        score_text = self.ui_font.render(f"Score: {self.game_state.score}", True, UI_COLOR)
        self.screen.blit(score_text, (10, 40))

        # Draw lives
        lives_text = self.ui_font.render(f"Lives: {self.game_state.lives}", True, UI_COLOR)
        self.screen.blit(lives_text, (10, 70))

        # Draw accuracy
        accuracy_text = self.ui_font.render(f"Accuracy: {self.game_state.accuracy:.1f}%", True, UI_COLOR)
        self.screen.blit(accuracy_text, (10, 100))

        # Draw words typed
        words_text = self.ui_font.render(f"Words: {self.game_state.words_typed}", True, UI_COLOR)
        self.screen.blit(words_text, (10, 130))

        # Draw controls
        controls_text = self.ui_font.render("Type the falling words! ESC: Quit, Backspace: Clear", True, UI_COLOR)
        self.screen.blit(controls_text, (10, WINDOW_HEIGHT - 30))

        # Draw level progress
        from .constants import LEVEL_UP_SCORE

        next_level_score = self.game_state.level * LEVEL_UP_SCORE
        progress = min(self.game_state.score / next_level_score, 1.0) if self.game_state.level < 10 else 1.0

        # Progress bar
        bar_width = 200
        bar_height = 10
        bar_x = WINDOW_WIDTH - bar_width - 10
        bar_y = 10

        # Background
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        # Progress
        pygame.draw.rect(self.screen, UI_COLOR, (bar_x, bar_y, int(bar_width * progress), bar_height))

        # Progress text
        if self.game_state.level < 10:
            progress_text = self.ui_font.render(
                f"Next Level: {self.game_state.score}/{next_level_score}", True, UI_COLOR
            )
        else:
            progress_text = self.ui_font.render("MAX LEVEL!", True, UI_COLOR)
        self.screen.blit(progress_text, (bar_x, bar_y + 15))

    def draw(self):
        """Draw the game."""
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)

        if not self.game_over:
            # Draw falling words
            for word in self.falling_words:
                word.draw(self.screen)

            # Draw UI
            self.draw_ui()

        else:
            # Game over screen
            game_over_text = self.title_font.render("GAME OVER", True, MISSED_COLOR)
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
            self.screen.blit(game_over_text, game_over_rect)

            # Final stats
            final_score_text = self.ui_font.render(f"Final Score: {self.game_state.score}", True, UI_COLOR)
            final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(final_score_text, final_score_rect)

            level_text = self.ui_font.render(f"Level Reached: {self.game_state.level}", True, UI_COLOR)
            level_rect = level_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            self.screen.blit(level_text, level_rect)

            accuracy_text = self.ui_font.render(f"Accuracy: {self.game_state.accuracy:.1f}%", True, UI_COLOR)
            accuracy_rect = accuracy_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            self.screen.blit(accuracy_text, accuracy_rect)

            words_text = self.ui_font.render(f"Words Typed: {self.game_state.words_typed}", True, UI_COLOR)
            words_rect = words_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            self.screen.blit(words_text, words_rect)

            restart_text = self.ui_font.render("Press SPACE to play again, ESC to quit", True, UI_COLOR)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        """Main game loop with custom timing."""
        while self.running:
            self.running = self.handle_input()
            if self.running:
                self.update()
                self.draw()
                self.clock.tick(FPS)

        pygame.quit()
