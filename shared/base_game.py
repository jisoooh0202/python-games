"""Base game class that all games can inherit from."""

import pygame
from abc import ABC, abstractmethod


class BaseGame(ABC):
    """Abstract base class for all games."""

    def __init__(self, window_width, window_height, title):
        """Initialize the base game.

        Args:
            window_width: Width of the game window
            window_height: Height of the game window
            title: Title of the game window
        """
        pygame.init()
        self.window_width = window_width
        self.window_height = window_height
        self.screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True

    def present(self):
        """Display the current frame."""
        pygame.display.flip()

    def handle_resize(self, w, h):
        """Handle window resize. Override to add game-specific updates."""
        self.window_width = w
        self.window_height = h
        self.screen = pygame.display.get_surface()

    @abstractmethod
    def handle_input(self):
        """Handle input events. Should return False to quit the game."""
        pass

    @abstractmethod
    def update(self):
        """Update game state."""
        pass

    @abstractmethod
    def draw(self):
        """Draw the game."""
        pass

    def run(self):
        """Main game loop."""
        while self.running:
            self.running = self.handle_input()
            if self.running:
                self.update()
                self.draw()

        pygame.quit()

    def quit_game(self):
        """Quit the game."""
        self.running = False
