#!/usr/bin/env python3
"""Color Puzzle game launcher.

Run this script to play the terminal Color Puzzle game:
    uv run play_color_puzzle.py
"""

from games.color_puzzle.game import ColorPuzzleGame


def main():
    """Launch Color Puzzle."""
    print("Starting ColorPuzzleGame...")
    print("Controls:")
    print("  - Left/Right arrows or H/L: Move between tubes")
    print("  - Enter or Space: Pick a tube, then pour into another tube")
    print("  - 1-9: Quick-select tubes")
    print("  - U: Undo last move")
    print("  - - / +: Change level")
    print("  - N: New puzzle")
    print("  - Q or ESC: Quit")
    print()

    game = ColorPuzzleGame()
    game.run()

    print("Thanks for playing ColorPuzzleGame!")


if __name__ == "__main__":
    main()
