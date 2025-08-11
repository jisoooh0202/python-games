#!/usr/bin/env python3
"""Pong game launcher.

Run this script to play the Pong game:
    uv run play_pong.py
"""

from games.pong.game import PongGame


def main():
    """Launch the Pong game."""
    print("Starting Pong Game...")
    print("Player Selection Menu:")
    print("  - Press 1: Single Player (vs AI)")
    print("  - Press 2: Two Players")
    print("  - ESC: Quit")
    print()
    print("Game Controls:")
    print("  Single Player:")
    print("    - W/S: Move paddle")
    print("    - P: Pause/Unpause")
    print("    - ESC: Return to menu")
    print()
    print("  Two Player:")
    print("    - Player 1: W/S keys")
    print("    - Player 2: ↑/↓ arrow keys")
    print("    - P: Pause/Unpause")
    print("    - ESC: Return to menu")
    print()
    print("Objective: First player to score 5 points wins!")
    print()

    game = PongGame()
    game.run()

    print("Thanks for playing Pong!")


if __name__ == "__main__":
    main()
