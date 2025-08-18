#!/usr/bin/env python3
"""Typing game launcher.

Run this script to play the Typing Rain game:
    uv run play_typing.py
"""

from games.typing.game import TypingGame


def main():
    """Launch the Typing Rain game."""
    print("Starting Typing Rain Game...")
    print()
    print("How to Play:")
    print("  - Words will fall from the top of the screen")
    print("  - Type the letters/words to make them disappear")
    print("  - Don't let words reach the bottom!")
    print("  - You lose a life for each missed word")
    print()
    print("Level Progression:")
    print("  Level 1: Single letters (a, s, d, f...)")
    print("  Level 2-3: More letters")
    print("  Level 4+: Real words (getting longer)")
    print("  Level 10: Very long words!")
    print()
    print("Controls:")
    print("  - Type: Letters and words")
    print("  - Backspace: Clear current input")
    print("  - F11: Cycle window mode (Small → Large → Fullscreen)")
    print("  - Drag window edges: Resize window anytime")
    print("  - ESC: Quit game")
    print("  - SPACE: Restart (when game over)")
    print()
    print("The game starts with a normal resizable window!")
    print("Resize the window by dragging its edges to your preferred size.")
    print("Use F11 to toggle between different window sizes.")
    print("Get ready to improve your typing skills!")
    print()

    game = TypingGame()
    game.run()

    print("Thanks for playing Typing Rain!")


if __name__ == "__main__":
    main()
