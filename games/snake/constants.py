"""Constants specific to the Snake game."""

from shared.constants import BLACK, WHITE, GREEN, RED

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Grid settings
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Game settings
GAME_SPEED = 3  # Lower number = slower snake (FPS)

# Colors
SNAKE_HEAD_COLOR = GREEN
SNAKE_BODY_COLOR = (0, 155, 0)  # DARK_GREEN
FOOD_COLOR = RED
BACKGROUND_COLOR = BLACK
TEXT_COLOR = WHITE
