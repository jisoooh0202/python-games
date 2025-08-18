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

### Pong Game

- Classic two-paddle pong gameplay
- Single player vs AI or two-player modes
- Player selection menu
- Physics-based ball bouncing with angle variation
- Pause functionality
- First to 5 points wins

### Typing Rain Game

- Educational typing game with falling words
- Progressive difficulty from letters to long words
- 10 levels with increasing speed and complexity
- Real-time accuracy tracking
- Lives system and scoring
- Perfect for improving typing skills

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

### Pong Game

```bash
# Run the Pong game
uv run play_pong.py
```

**Controls:**

**Menu:**

- 1: Single Player (vs AI)
- 2: Two Players
- ESC: Quit

**Single Player:**

- W/S: Move paddle
- P: Pause/Unpause
- ESC: Return to menu

**Two Player:**

- Player 1: W/S keys
- Player 2: ↑/↓ arrow keys
- P: Pause/Unpause
- ESC: Return to menu

**Objective:** First player to score 5 points wins! The ball bounces off paddles and changes angle based on where it hits.

### Typing Rain Game

```bash
# Run the Typing Rain game
uv run play_typing.py
```

**Controls:**

- Type letters/words as they fall
- Backspace: Clear current input
- F11: Cycle window mode (Windowed → Maximized → Fullscreen)
- Drag window edges: Resize window
- ESC: Quit game
- SPACE: Restart (when game over)

**Objective:** Type falling words before they reach the bottom! Progress through 10 levels from single letters to complex words. Don't let words fall - you lose a life for each miss!

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
