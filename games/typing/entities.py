"""Typing game entities: FallingWord and GameState."""

import pygame
from .constants import (
    WINDOW_HEIGHT,
    WORD_COLOR,
    TYPED_COLOR,
    BASE_FALL_SPEED,
    SPEED_INCREASE_PER_LEVEL,
    LEVEL_WORDS,
    MAX_LEVEL,
)


class FallingWord:
    """A word that falls from the top of the screen."""

    def __init__(self, text, x, y, fall_speed, font):
        """Initialize a falling word."""
        self.text = text.lower()
        self.original_text = text.lower()
        self.x = x
        self.y = y
        self.fall_speed = fall_speed
        self.font = font
        self.typed_chars = 0  # Number of characters correctly typed
        self.completed = False
        self.missed = False

    def update(self):
        """Update word position."""
        self.y += self.fall_speed

    def is_off_screen(self):
        """Check if word has fallen off the bottom of the screen."""
        return self.y > WINDOW_HEIGHT

    def type_char(self, char):
        """Try to type a character. Returns True if correct, False if wrong."""
        if self.completed:
            return False

        expected_char = self.text[self.typed_chars] if self.typed_chars < len(self.text) else None

        if expected_char and char.lower() == expected_char:
            self.typed_chars += 1
            if self.typed_chars >= len(self.text):
                self.completed = True
            return True
        return False

    def get_remaining_text(self):
        """Get the part of the word that hasn't been typed yet."""
        return self.text[self.typed_chars :]

    def get_typed_text(self):
        """Get the part of the word that has been typed."""
        return self.text[: self.typed_chars]

    def draw(self, screen):
        """Draw the word on screen with typed portion in different color."""
        if self.completed:
            return

        # Draw typed portion in green
        if self.typed_chars > 0:
            typed_surface = self.font.render(self.get_typed_text(), True, TYPED_COLOR)
            screen.blit(typed_surface, (self.x, self.y))

            # Calculate x offset for remaining text
            typed_width = typed_surface.get_width()
        else:
            typed_width = 0

        # Draw remaining portion in white
        remaining_text = self.get_remaining_text()
        if remaining_text:
            remaining_surface = self.font.render(remaining_text, True, WORD_COLOR)
            screen.blit(remaining_surface, (self.x + typed_width, self.y))

    def get_rect(self):
        """Get pygame rect for collision detection."""
        full_text = self.font.render(self.text, True, WORD_COLOR)
        return pygame.Rect(self.x, self.y, full_text.get_width(), full_text.get_height())


class GameState:
    """Manages the overall game state including level, score, etc."""

    def __init__(self):
        """Initialize game state."""
        self.level = 1
        self.score = 0
        self.lives = 3
        self.words_typed = 0
        self.words_missed = 0
        self.accuracy = 100.0

    def add_score(self, word_length):
        """Add score for completing a word."""
        from .constants import SCORE_PER_CHAR

        points = word_length * SCORE_PER_CHAR
        self.score += points
        self.words_typed += 1
        self.update_accuracy()

    def miss_word(self):
        """Handle missing a word."""
        self.lives -= 1
        self.words_missed += 1
        self.update_accuracy()

    def update_accuracy(self):
        """Update typing accuracy percentage."""
        total_words = self.words_typed + self.words_missed
        if total_words > 0:
            self.accuracy = (self.words_typed / total_words) * 100

    def should_level_up(self):
        """Check if player should advance to next level."""
        from .constants import LEVEL_UP_SCORE

        return self.score >= self.level * LEVEL_UP_SCORE and self.level < MAX_LEVEL

    def level_up(self):
        """Advance to next level."""
        if self.level < MAX_LEVEL:
            self.level += 1

    def get_fall_speed(self):
        """Get current fall speed based on level."""
        return BASE_FALL_SPEED + (self.level - 1) * SPEED_INCREASE_PER_LEVEL

    def get_spawn_rate(self):
        """Get current spawn rate based on level."""
        from .constants import BASE_SPAWN_RATE, MIN_SPAWN_RATE

        rate = BASE_SPAWN_RATE - (self.level - 1) * 10
        return max(MIN_SPAWN_RATE, rate)

    def get_word_list(self):
        """Get word list for current level."""
        return LEVEL_WORDS.get(self.level, LEVEL_WORDS[MAX_LEVEL])

    def is_game_over(self):
        """Check if game is over."""
        return self.lives <= 0

    def reset(self):
        """Reset game state."""
        self.level = 1
        self.score = 0
        self.lives = 3
        self.words_typed = 0
        self.words_missed = 0
        self.accuracy = 100.0
