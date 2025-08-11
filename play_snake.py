#!/usr/bin/env python3
"""Snake game launcher.

Run this script to play the Snake game:
    python play_snake.py
"""

from games.snake.game import SnakeGame


def main():
    """Launch the Snake game."""
    print("Starting Snake Game...")
    print("Controls:")
    print("  - Arrow keys: Move snake")
    print("  - ESC: Quit game")
    print("  - SPACE: Restart (when game over)")
    print()

    game = SnakeGame()
    game.run()

    print("Thanks for playing Snake!")


if __name__ == "__main__":
    main()
