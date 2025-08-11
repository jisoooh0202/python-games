"""Pong game entities: Paddle and Ball."""

import pygame
import random
from .constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    BALL_SIZE,
    BALL_SPEED_X,
    BALL_SPEED_Y,
)


class Paddle:
    """Paddle class for both player and AI."""

    def __init__(self, x, y, is_ai=False):
        """Initialize paddle at given position."""
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        self.is_ai = is_ai

    def move_up(self):
        """Move paddle up."""
        self.y = max(0, self.y - self.speed)

    def move_down(self):
        """Move paddle down."""
        self.y = min(WINDOW_HEIGHT - self.height, self.y + self.speed)

    def get_rect(self):
        """Get pygame rect for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_center_y(self):
        """Get the center Y position of the paddle."""
        return self.y + self.height // 2

    def ai_update(self, ball):
        """Simple AI movement - follows the ball."""
        if not self.is_ai:
            return

        paddle_center = self.get_center_y()
        ball_center_y = ball.y + ball.size // 2

        # Add some delay/imperfection to make AI beatable
        if abs(paddle_center - ball_center_y) > 5:
            if paddle_center < ball_center_y:
                self.move_down()
            elif paddle_center > ball_center_y:
                self.move_up()


class Ball:
    """Ball class for the pong ball."""

    def __init__(self, x, y):
        """Initialize ball at given position."""
        self.x = x
        self.y = y
        self.size = BALL_SIZE
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
        self.reset_ball()

    def reset_ball(self):
        """Reset ball to center with random direction."""
        self.x = WINDOW_WIDTH // 2 - self.size // 2
        self.y = WINDOW_HEIGHT // 2 - self.size // 2

        # Random direction
        self.speed_x = BALL_SPEED_X if random.choice([True, False]) else -BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y if random.choice([True, False]) else -BALL_SPEED_Y

    def update(self):
        """Update ball position."""
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off top and bottom walls
        if self.y <= 0 or self.y >= WINDOW_HEIGHT - self.size:
            self.speed_y = -self.speed_y

    def get_rect(self):
        """Get pygame rect for collision detection."""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def bounce_off_paddle(self, paddle):
        """Handle ball bouncing off paddle with angle variation."""
        # Reverse horizontal direction
        self.speed_x = -self.speed_x

        # Add angle variation based on where ball hits paddle
        paddle_center = paddle.get_center_y()
        ball_center = self.y + self.size // 2
        hit_pos = (ball_center - paddle_center) / (paddle.height // 2)

        # Modify vertical speed based on hit position (-1 to 1)
        self.speed_y = hit_pos * 3

        # Ensure minimum horizontal speed
        if abs(self.speed_x) < 2:
            self.speed_x = 2 if self.speed_x > 0 else -2

    def is_out_of_bounds_left(self):
        """Check if ball went off left side."""
        return self.x < -self.size

    def is_out_of_bounds_right(self):
        """Check if ball went off right side."""
        return self.x > WINDOW_WIDTH
