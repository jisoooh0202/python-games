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

    def draw(self, surface):
        """Draw player as a spaceship pointing upward."""
        cx = self.x + self.width // 2

        # Main body polygon — swept-wing arrow pointing up
        body = [
            (cx, self.y),  # nose tip
            (cx + 7, self.y + 18),  # right shoulder
            (self.x + self.width, self.y + self.height),  # right wing tip
            (cx + 5, self.y + self.height - 5),  # right wing inner notch
            (cx, self.y + self.height - 7),  # center back notch
            (cx - 5, self.y + self.height - 5),  # left wing inner notch
            (self.x, self.y + self.height),  # left wing tip
            (cx - 7, self.y + 18),  # left shoulder
        ]
        pygame.draw.polygon(surface, (0, 210, 230), body)
        pygame.draw.polygon(surface, (180, 255, 255), body, 1)

        # Engine exhaust flame
        pygame.draw.rect(surface, (255, 160, 0), (cx - 4, self.y + self.height - 5, 8, 5))
        pygame.draw.circle(surface, (255, 80, 0), (cx, self.y + self.height), 4)

        # Cockpit dome
        pygame.draw.ellipse(surface, (160, 225, 255), (cx - 5, self.y + 7, 10, 9))
        pygame.draw.ellipse(surface, (220, 245, 255), (cx - 3, self.y + 8, 6, 5))


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

    def draw(self, surface):
        """Draw enemy as an angular alien fighter pointing downward."""
        cx = self.x + self.width // 2

        # Main body — wide angular craft with swept wings pointing down
        body = [
            (cx, self.y + self.height),  # front tip (nose pointing down)
            (cx + 5, self.y + 12),  # right inner
            (self.x + self.width, self.y + 4),  # right wing outer tip
            (self.x + self.width - 4, self.y),  # right wing leading edge
            (cx + 5, self.y + 5),  # right inner top
            (cx - 5, self.y + 5),  # left inner top
            (self.x + 4, self.y),  # left wing leading edge
            (self.x, self.y + 4),  # left wing outer tip
            (cx - 5, self.y + 12),  # left inner
        ]
        pygame.draw.polygon(surface, (200, 30, 30), body)
        pygame.draw.polygon(surface, (255, 90, 90), body, 1)

        # Wing accent lines
        pygame.draw.line(surface, (255, 100, 100), (self.x + 6, self.y + 3), (cx - 2, self.y + 10), 1)
        pygame.draw.line(surface, (255, 100, 100), (self.x + self.width - 6, self.y + 3), (cx + 2, self.y + 10), 1)

        # Glowing sensor / eye
        pygame.draw.circle(surface, (255, 50, 50), (cx, self.y + 7), 4)
        pygame.draw.circle(surface, (255, 210, 210), (cx, self.y + 7), 2)


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
