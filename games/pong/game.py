"""Main Pong game implementation."""

import pygame
from shared.base_game import BaseGame
from .constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    WINNING_SCORE,
    PADDLE_MARGIN,
    BACKGROUND_COLOR,
    PADDLE_COLOR,
    BALL_COLOR,
    TEXT_COLOR,
    NET_COLOR,
    SCORE_FONT_SIZE,
    MENU_FONT_SIZE,
    INSTRUCTION_FONT_SIZE,
)
from .entities import Paddle, Ball


class PongGame(BaseGame):
    """Main Pong game class."""

    def __init__(self):
        """Initialize the Pong game."""
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Pong")
        self.score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
        self.menu_font = pygame.font.Font(None, MENU_FONT_SIZE)
        self.instruction_font = pygame.font.Font(None, INSTRUCTION_FONT_SIZE)

        # Game modes
        self.game_state = "menu"  # "menu", "playing", "game_over"
        self.two_player_mode = False

        self.reset_game()

    def reset_game(self):
        """Reset the game to initial state."""
        # Initialize paddles
        left_paddle_x = PADDLE_MARGIN
        right_paddle_x = WINDOW_WIDTH - PADDLE_MARGIN - 15  # 15 is paddle width
        paddle_y = WINDOW_HEIGHT // 2 - 45  # 45 is half paddle height

        self.left_paddle = Paddle(left_paddle_x, paddle_y, is_ai=False)
        # Right paddle is AI only in single player mode
        self.right_paddle = Paddle(right_paddle_x, paddle_y, is_ai=not self.two_player_mode)

        # Initialize ball
        self.ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Game state
        self.left_score = 0
        self.right_score = 0
        self.game_over = False
        self.winner = None
        self.paused = False

    def handle_input(self):
        """Handle input events."""
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.game_state == "menu":
                    if event.key == pygame.K_1:
                        self.two_player_mode = False
                        self.game_state = "playing"
                        self.reset_game()
                    elif event.key == pygame.K_2:
                        self.two_player_mode = True
                        self.game_state = "playing"
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False

                elif self.game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "menu"
                    elif event.key == pygame.K_ESCAPE:
                        return False

                elif self.game_state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "menu"
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused

        # Handle continuous input during gameplay
        if self.game_state == "playing" and not self.paused:
            # Left paddle controls (W/S)
            if keys[pygame.K_w]:
                self.left_paddle.move_up()
            if keys[pygame.K_s]:
                self.left_paddle.move_down()

            # Right paddle controls (Up/Down arrows) - only in two-player mode
            if self.two_player_mode:
                if keys[pygame.K_UP]:
                    self.right_paddle.move_up()
                if keys[pygame.K_DOWN]:
                    self.right_paddle.move_down()

        return True

    def update(self):
        """Update game state."""
        if self.game_state != "playing" or self.paused:
            return

        # Update AI paddle only in single-player mode
        if not self.two_player_mode:
            self.right_paddle.ai_update(self.ball)

        # Update ball
        self.ball.update()

        # Check paddle collisions
        if self.ball.get_rect().colliderect(self.left_paddle.get_rect()) and self.ball.speed_x < 0:
            self.ball.bounce_off_paddle(self.left_paddle)

        if self.ball.get_rect().colliderect(self.right_paddle.get_rect()) and self.ball.speed_x > 0:
            self.ball.bounce_off_paddle(self.right_paddle)

        # Check scoring
        if self.ball.is_out_of_bounds_left():
            self.right_score += 1
            self.ball.reset_ball()

        if self.ball.is_out_of_bounds_right():
            self.left_score += 1
            self.ball.reset_ball()

        # Check win condition
        if self.left_score >= WINNING_SCORE:
            self.game_state = "game_over"
            self.winner = "Player 1" if self.two_player_mode else "Player"
        elif self.right_score >= WINNING_SCORE:
            self.game_state = "game_over"
            self.winner = "Player 2" if self.two_player_mode else "AI"

    def draw_net(self):
        """Draw the center net."""
        net_width = 5
        net_height = 15
        net_gap = 15
        net_x = WINDOW_WIDTH // 2 - net_width // 2

        y = 0
        while y < WINDOW_HEIGHT:
            pygame.draw.rect(self.screen, NET_COLOR, (net_x, y, net_width, net_height))
            y += net_height + net_gap

    def draw(self):
        """Draw the game."""
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)

        if self.game_state == "menu":
            # Draw menu screen
            title_text = self.menu_font.render("PONG", True, TEXT_COLOR)
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
            self.screen.blit(title_text, title_rect)

            select_text = self.instruction_font.render("Select Number of Players:", True, TEXT_COLOR)
            select_rect = select_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(select_text, select_rect)

            player1_text = self.instruction_font.render("Press 1 for Single Player (vs AI)", True, TEXT_COLOR)
            player1_rect = player1_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(player1_text, player1_rect)

            player2_text = self.instruction_font.render("Press 2 for Two Players", True, TEXT_COLOR)
            player2_rect = player2_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            self.screen.blit(player2_text, player2_rect)

            quit_text = self.instruction_font.render("Press ESC to Quit", True, TEXT_COLOR)
            quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            self.screen.blit(quit_text, quit_rect)

        elif self.game_state == "playing":
            # Draw net
            self.draw_net()

            # Draw paddles
            pygame.draw.rect(self.screen, PADDLE_COLOR, self.left_paddle.get_rect())
            pygame.draw.rect(self.screen, PADDLE_COLOR, self.right_paddle.get_rect())

            # Draw ball
            pygame.draw.rect(self.screen, BALL_COLOR, self.ball.get_rect())

            # Draw scores
            left_score_text = self.score_font.render(str(self.left_score), True, TEXT_COLOR)
            right_score_text = self.score_font.render(str(self.right_score), True, TEXT_COLOR)

            # Position scores
            left_score_rect = left_score_text.get_rect()
            right_score_rect = right_score_text.get_rect()

            left_score_rect.centerx = WINDOW_WIDTH // 4
            left_score_rect.y = 50
            right_score_rect.centerx = 3 * WINDOW_WIDTH // 4
            right_score_rect.y = 50

            self.screen.blit(left_score_text, left_score_rect)
            self.screen.blit(right_score_text, right_score_rect)

            # Draw controls based on mode
            if self.two_player_mode:
                controls_text = self.instruction_font.render("P1: W/S, P2: ↑/↓, P: Pause, ESC: Menu", True, TEXT_COLOR)
            else:
                controls_text = self.instruction_font.render("W/S: Move Paddle, P: Pause, ESC: Menu", True, TEXT_COLOR)

            controls_rect = controls_text.get_rect()
            controls_rect.centerx = WINDOW_WIDTH // 2
            controls_rect.y = WINDOW_HEIGHT - 30
            self.screen.blit(controls_text, controls_rect)

            # Draw pause message if paused
            if self.paused:
                pause_text = self.menu_font.render("PAUSED", True, TEXT_COLOR)
                pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                self.screen.blit(pause_text, pause_rect)

        elif self.game_state == "game_over":
            # Draw net
            self.draw_net()

            # Game over screen
            winner_text = self.menu_font.render(f"{self.winner} Wins!", True, TEXT_COLOR)
            score_text = self.instruction_font.render(
                f"Final Score: {self.left_score} - {self.right_score}", True, TEXT_COLOR
            )
            restart_text = self.instruction_font.render("Press SPACE to return to menu, ESC to quit", True, TEXT_COLOR)

            # Center the text
            winner_rect = winner_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

            self.screen.blit(winner_text, winner_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        """Main game loop with custom timing."""
        while self.running:
            self.running = self.handle_input()
            if self.running:
                self.update()
                self.draw()
                self.clock.tick(FPS)

        pygame.quit()
