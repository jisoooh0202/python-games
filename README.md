# Snake Game

A classic Snake game implemented in Python using Pygame.

## Features

- Classic snake gameplay
- Score tracking
- Game over and restart functionality
- Smooth controls with arrow keys
- Visual feedback with different colors for snake head and body

## Requirements

- Python 3.11+
- Pygame

## Installation

This project uses `uv` for dependency management. Make sure you have `uv` installed.

1. Create a virtual environment:

   ```bash
   uv venv
   ```

2. Install dependencies:
   ```bash
   uv add pygame
   ```

## How to Play

1. Run the game:

   ```bash
   uv run python main.py
   ```

2. Game Controls:

   - **Arrow Keys**: Move the snake (Up, Down, Left, Right)
   - **ESC**: Quit the game
   - **SPACE**: Restart the game (when game over)

3. Objective:
   - Control the green snake to eat the red food
   - Each food eaten increases your score by 10 points
   - Avoid hitting the walls or the snake's own body
   - The snake grows longer with each food eaten

## Game Rules

- The snake moves continuously in the direction you choose
- You cannot move directly opposite to your current direction
- The game ends if the snake hits a wall or itself
- Your score is displayed in the top-left corner

Enjoy playing!
