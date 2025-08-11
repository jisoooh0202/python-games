# Python Games Collection

A collection of classic games implemented in Python using Pygame.

## Available Games

### Snake Game

- Classic snake gameplay
- Score tracking
- Game over and restart functionality
- Smooth controls with arrow keys
- Visual feedback with different colors for snake head and body

### Space Combat Game

- Classic arcade-style space shooter
- Player health system
- Enemy spawning and shooting mechanics
- Explosion effects
- Score tracking and progressive difficulty

### Coming Soon

- Tetris

## Requirements

- Python 3.11+
- Pygame
- uv (for dependency management)

## Installation

This project uses `uv` for dependency management. Make sure you have `uv` installed.

```bash
# Install dependencies
uv sync
```

## How to Play

### Snake Game

```bash
# Run the Snake game
uv run play_snake.py
```

**Controls:**

- Arrow keys: Move snake
- ESC: Quit game
- SPACE: Restart (when game over)

### Space Combat Game

```bash
# Run the Space Combat game
uv run play_space_combat.py
```

**Controls:**

- WASD or Arrow keys: Move spaceship
- SPACE: Shoot
- ESC: Quit game
- SPACE: Restart (when game over)

**Objective:** Shoot down enemy ships and avoid collisions! You lose health when enemies hit you.

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
