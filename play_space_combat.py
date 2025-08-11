#!/usr/bin/env python3
"""Space Combat game launcher.

Run this script to play the Space Combat game:
    uv run play_space_combat.py
"""

from games.space_combat.game import SpaceCombatGame


def main():
    """Launch the Space Combat game."""
    print("Starting Space Combat Game...")
    print("Controls:")
    print("  - WASD or Arrow keys: Move spaceship")
    print("  - SPACE: Shoot")
    print("  - ESC: Quit game")
    print("  - SPACE: Restart (when game over)")
    print()
    print("Objective: Shoot down enemy ships and avoid collisions!")
    print("You lose health when enemies hit you.")
    print()
    
    game = SpaceCombatGame()
    game.run()
    
    print("Thanks for playing Space Combat!")


if __name__ == "__main__":
    main()
