"""Space Combat game entities: Player, Enemy, Bullet."""

import pygame
import random
from .constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    BULLET_WIDTH,
    BULLET_HEIGHT,
    ENEMY_WIDTH,
    ENEMY_HEIGHT,
    PLAYER_SPEED,
    BULLET_SPEED,
    ENEMY_SPEED,
)


class Player:
    """Player spaceship class."""

    def __init__(self, x, y):
        """Initialize player at given position."""
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100

    def move_left(self):
        """Move player left."""
        self.x = max(0, self.x - self.speed)

    def move_right(self):
        """Move player right."""
        self.x = min(WINDOW_WIDTH - self.width, self.x + self.speed)

    def move_up(self):
        """Move player up."""
        self.y = max(0, self.y - self.speed)

    def move_down(self):
        """Move player down."""
        self.y = min(WINDOW_HEIGHT - self.height, self.y + self.speed)

    def get_rect(self):
        """Get pygame rect for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def take_damage(self, damage=20):
        """Take damage and return True if still alive."""
        self.health -= damage
        return self.health > 0

    def shoot(self):
        """Create a bullet at the player's position."""
        bullet_x = self.x + self.width // 2 - BULLET_WIDTH // 2
        bullet_y = self.y
        return Bullet(bullet_x, bullet_y, -BULLET_SPEED)  # Negative for upward movement


class Enemy:
    """Enemy spaceship class."""

    def __init__(self, x, y):
        """Initialize enemy at given position."""
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.speed = ENEMY_SPEED

    def update(self):
        """Update enemy position."""
        self.y += self.speed

    def is_off_screen(self):
        """Check if enemy is off screen."""
        return self.y > WINDOW_HEIGHT

    def get_rect(self):
        """Get pygame rect for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @staticmethod
    def spawn_random():
        """Spawn enemy at random x position at top of screen."""
        x = random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH)
        return Enemy(x, -ENEMY_HEIGHT)


class Bullet:
    """Bullet class for player shots."""

    def __init__(self, x, y, speed):
        """Initialize bullet at given position with given speed."""
        self.x = x
        self.y = y
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.speed = speed

    def update(self):
        """Update bullet position."""
        self.y += self.speed

    def is_off_screen(self):
        """Check if bullet is off screen."""
        return self.y < 0 or self.y > WINDOW_HEIGHT

    def get_rect(self):
        """Get pygame rect for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Explosion:
    """Simple explosion effect."""

    def __init__(self, x, y):
        """Initialize explosion at given position."""
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 25
        self.growth_rate = 2

    def update(self):
        """Update explosion animation."""
        self.radius += self.growth_rate

    def is_finished(self):
        """Check if explosion animation is finished."""
        return self.radius >= self.max_radius
