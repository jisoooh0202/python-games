"""Snake game entities: Snake, Food, and Direction."""

import random
from enum import Enum
from .constants import GRID_WIDTH, GRID_HEIGHT


class Direction(Enum):
    """Enum representing movement directions."""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Snake:
    """Represents the snake in the game."""
    
    def __init__(self, start_x, start_y):
        """Initialize snake at starting position."""
        self.body = [(start_x, start_y)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        
    def move(self):
        """Move the snake in the current direction."""
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        
    def grow(self):
        """Grow the snake (don't remove tail after moving)."""
        # Snake grows by not removing the tail in the next move
        pass
        
    def shrink(self):
        """Remove the tail segment."""
        if len(self.body) > 0:
            self.body.pop()
            
    def change_direction(self, new_direction):
        """Change snake direction if valid."""
        # Prevent snake from going directly backwards
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if new_direction != opposite_directions.get(self.direction):
            self.next_direction = new_direction
            
    def check_wall_collision(self):
        """Check if snake hit a wall."""
        head_x, head_y = self.body[0]
        return (head_x < 0 or head_x >= GRID_WIDTH or 
                head_y < 0 or head_y >= GRID_HEIGHT)
                
    def check_self_collision(self):
        """Check if snake hit itself."""
        head = self.body[0]
        return head in self.body[1:]
        
    def get_head(self):
        """Get the head position."""
        return self.body[0]


class Food:
    """Represents food in the game."""
    
    def __init__(self):
        """Initialize food at a random position."""
        self.position = self._generate_position()
        
    def _generate_position(self):
        """Generate a random position for food."""
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)
        
    def regenerate(self, snake_body):
        """Generate new food position avoiding snake body."""
        while True:
            self.position = self._generate_position()
            if self.position not in snake_body:
                break
                
    def get_position(self):
        """Get the food position."""
        return self.position
