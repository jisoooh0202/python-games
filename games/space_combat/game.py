"""Main Space Combat game implementation."""

import pygame
from shared.base_game import BaseGame
from shared.constants import MEDIUM_FONT, LARGE_FONT
from .constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    PLAYER_WIDTH,
    ENEMY_SPAWN_RATE,
    BACKGROUND_COLOR,
    PLAYER_COLOR,
    PLAYER_OUTLINE_COLOR,
    PLAYER2_COLOR,
    PLAYER2_OUTLINE_COLOR,
    BULLET_COLOR,
    PLAYER2_BULLET_COLOR,
    TEXT_COLOR,
    EXPLOSION_COLOR,
    ENEMY_KILL_POINTS,
)
from . import constants as sc_const
from .entities import Player, Enemy, Explosion
from .physics import check_bullet_enemy_collisions, check_player_enemy_collisions


class SpaceCombatGame(BaseGame):
    """Main Space Combat game class."""

    def __init__(self):
        """Initialize the Space Combat game."""
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Space Combat")
        self.font = pygame.font.Font(None, MEDIUM_FONT)
        self.large_font = pygame.font.Font(None, LARGE_FONT)
        self.num_players = 1
        self.selecting = True  # show player-select screen first
        self.reset_game(self.num_players)

    def handle_resize(self, w, h):
        """Handle window resize, updating space combat constants."""
        super().handle_resize(w, h)
        sc_const.WINDOW_WIDTH = w
        sc_const.WINDOW_HEIGHT = h

    def reset_game(self, num_players=None):
        """Reset the game to initial state."""
        if num_players is not None:
            self.num_players = num_players

        WINDOW_WIDTH = self.window_width
        WINDOW_HEIGHT = self.window_height
        player_y = WINDOW_HEIGHT - 50
        p1_x = WINDOW_WIDTH // 2 - PLAYER_WIDTH // 2 if self.num_players == 1 else WINDOW_WIDTH // 4 - PLAYER_WIDTH // 2
        self.player1 = Player(
            p1_x,
            player_y,
            body_color=PLAYER_COLOR,
            outline_color=PLAYER_OUTLINE_COLOR,
            bullet_color=BULLET_COLOR,
        )
        if self.num_players == 2:
            self.player2 = Player(
                3 * WINDOW_WIDTH // 4 - PLAYER_WIDTH // 2,
                player_y,
                body_color=PLAYER2_COLOR,
                outline_color=PLAYER2_OUTLINE_COLOR,
                bullet_color=PLAYER2_BULLET_COLOR,
            )
        else:
            self.player2 = None

        # Initialize game objects
        self.bullets1 = []
        self.bullets2 = []
        self.enemies = []
        self.explosions = []

        # Game state
        self.score1 = 0
        self.score2 = 0
        self.game_over = False
        self.enemy_spawn_timer = 0
        self.shoot_cooldown1 = 0
        self.shoot_cooldown2 = 0

    def handle_input(self):
        """Handle input events."""
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.w, event.h)

            if event.type == pygame.KEYDOWN:
                if self.selecting:
                    if event.key == pygame.K_1:
                        self.selecting = False
                        self.reset_game(1)
                    elif event.key == pygame.K_2:
                        self.selecting = False
                        self.reset_game(2)
                    elif event.key == pygame.K_ESCAPE:
                        return False
                elif self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.selecting = True
                    elif event.key == pygame.K_r and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                        self.reset_game()
                        self.game_over = False
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_r and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                        self.selecting = True
                    elif event.key == pygame.K_ESCAPE:
                        return False

        # Handle continuous input during gameplay
        if not self.selecting and not self.game_over:
            # Player 1: WASD + LCtrl
            if self.player1.health > 0:
                if keys[pygame.K_a]:
                    self.player1.move_left()
                if keys[pygame.K_d]:
                    self.player1.move_right()
                if keys[pygame.K_w]:
                    self.player1.move_up()
                if keys[pygame.K_s]:
                    self.player1.move_down()
                if keys[pygame.K_LCTRL] and self.shoot_cooldown1 <= 0:
                    self.bullets1.append(self.player1.shoot())
                    self.shoot_cooldown1 = 10
            # Player 2: Arrow keys + Right Ctrl
            if self.player2 is not None and self.player2.health > 0:
                if keys[pygame.K_LEFT]:
                    self.player2.move_left()
                if keys[pygame.K_RIGHT]:
                    self.player2.move_right()
                if keys[pygame.K_UP]:
                    self.player2.move_up()
                if keys[pygame.K_DOWN]:
                    self.player2.move_down()
                if keys[pygame.K_RCTRL] and self.shoot_cooldown2 <= 0:
                    self.bullets2.append(self.player2.shoot())
                    self.shoot_cooldown2 = 10

        return True

    def update(self):
        """Update game state."""
        if self.selecting or self.game_over:
            return

        # Update cooldowns
        if self.shoot_cooldown1 > 0:
            self.shoot_cooldown1 -= 1
        if self.shoot_cooldown2 > 0:
            self.shoot_cooldown2 -= 1

        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= ENEMY_SPAWN_RATE:
            self.enemies.append(Enemy.spawn_random())
            self.enemy_spawn_timer = 0

        # Update bullets
        for bullet in self.bullets1[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets1.remove(bullet)
        for bullet in self.bullets2[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets2.remove(bullet)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.is_off_screen():
                self.enemies.remove(enemy)

        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_finished():
                self.explosions.remove(explosion)

        # Check bullet-enemy collisions (P1 first, P2 avoids double-scoring same enemy)
        enemy_kills = set()

        bullets1_to_remove = set()
        for b_idx, e_idx in check_bullet_enemy_collisions(self.bullets1, self.enemies):
            bullets1_to_remove.add(b_idx)
            if e_idx not in enemy_kills:
                enemy_kills.add(e_idx)
                enemy = self.enemies[e_idx]
                self.explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                self.score1 += ENEMY_KILL_POINTS

        bullets2_to_remove = set()
        for b_idx, e_idx in check_bullet_enemy_collisions(self.bullets2, self.enemies):
            bullets2_to_remove.add(b_idx)
            if e_idx not in enemy_kills:
                enemy_kills.add(e_idx)
                enemy = self.enemies[e_idx]
                self.explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                self.score2 += ENEMY_KILL_POINTS

        for b_idx in sorted(bullets1_to_remove, reverse=True):
            if b_idx < len(self.bullets1):
                self.bullets1.pop(b_idx)
        for b_idx in sorted(bullets2_to_remove, reverse=True):
            if b_idx < len(self.bullets2):
                self.bullets2.pop(b_idx)
        for e_idx in sorted(enemy_kills, reverse=True):
            if e_idx < len(self.enemies):
                self.enemies.pop(e_idx)

        # Check player-enemy collisions (only for living players)
        if self.player1.health > 0:
            for e_idx in sorted(check_player_enemy_collisions(self.player1, self.enemies), reverse=True):
                enemy = self.enemies[e_idx]
                self.explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                self.enemies.pop(e_idx)
                self.player1.take_damage()

        if self.player2 is not None and self.player2.health > 0:
            for e_idx in sorted(check_player_enemy_collisions(self.player2, self.enemies), reverse=True):
                enemy = self.enemies[e_idx]
                self.explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                self.enemies.pop(e_idx)
                self.player2.take_damage()

        # Game over when all active players are dead
        p2_dead = self.player2 is None or self.player2.health <= 0
        if self.player1.health <= 0 and p2_dead:
            self.game_over = True

    def _draw_select_screen(self):
        """Draw the player-count selection screen."""
        WINDOW_WIDTH = self.window_width
        WINDOW_HEIGHT = self.window_height
        self.screen.fill(BACKGROUND_COLOR)
        title = self.large_font.render("SPACE COMBAT", True, PLAYER_COLOR)
        self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100)))
        prompt = self.font.render("Select number of players", True, TEXT_COLOR)
        self.screen.blit(prompt, prompt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)))
        opt1 = self.font.render("Press  1  —  1 Player  (WASD + LCtrl)", True, PLAYER_COLOR)
        self.screen.blit(opt1, opt1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20)))
        opt2 = self.font.render("Press  2  —  2 Players  (P2: Arrows + RCtrl)", True, PLAYER2_COLOR)
        self.screen.blit(opt2, opt2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60)))
        esc = self.font.render("ESC: Quit", True, TEXT_COLOR)
        self.screen.blit(esc, esc.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 110)))
        self.present()

    def draw(self):
        """Draw the game."""
        WINDOW_WIDTH = self.window_width
        WINDOW_HEIGHT = self.window_height
        if self.selecting:
            self._draw_select_screen()
            return

        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)

        if not self.game_over:
            # Draw players
            if self.player1.health > 0:
                self.player1.draw(self.screen)
            if self.player2 is not None and self.player2.health > 0:
                self.player2.draw(self.screen)

            # Draw bullets (color stored per bullet)
            for bullet in self.bullets1 + self.bullets2:
                pygame.draw.rect(self.screen, bullet.color, bullet.get_rect())

            # Draw enemies
            for enemy in self.enemies:
                enemy.draw(self.screen)

            # Draw explosions
            for explosion in self.explosions:
                pygame.draw.circle(self.screen, EXPLOSION_COLOR, (int(explosion.x), int(explosion.y)), explosion.radius)

            # Draw HUD
            hp_bar_w, hp_bar_h = 150, 10

            if self.num_players == 1:
                # Centered score
                score_text = self.font.render(f"Score: {self.score1}", True, TEXT_COLOR)
                self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 10))
                # P1 health bar (left)
                p1_label = self.font.render("HP", True, PLAYER_COLOR)
                self.screen.blit(p1_label, (10, 35))
            else:
                # P1 score + label (left)
                p1_label = self.font.render(f"P1  {self.score1} pts", True, PLAYER_COLOR)
                self.screen.blit(p1_label, (10, 10))
                # P2 score + label (right)
                p2_hud_x = WINDOW_WIDTH - 160
                p2_label = self.font.render(f"P2  {self.score2} pts", True, PLAYER2_COLOR)
                self.screen.blit(p2_label, (p2_hud_x, 10))

            # P1 health bar
            p1_pct = self.player1.health / self.player1.max_health
            pygame.draw.rect(self.screen, (80, 80, 80), (10, 35, hp_bar_w, hp_bar_h))
            p1_hp_color = (0, 255, 0) if p1_pct > 0.5 else (255, 255, 0) if p1_pct > 0.25 else (255, 60, 60)
            pygame.draw.rect(self.screen, p1_hp_color, (10, 35, int(hp_bar_w * p1_pct), hp_bar_h))
            if self.player1.health <= 0:
                self.screen.blit(self.font.render("DEAD", True, (255, 80, 80)), (10, 49))

            # P2 health bar (2-player mode only)
            if self.player2 is not None:
                p2_hud_x = WINDOW_WIDTH - 160
                p2_pct = self.player2.health / self.player2.max_health
                pygame.draw.rect(self.screen, (80, 80, 80), (p2_hud_x, 35, hp_bar_w, hp_bar_h))
                p2_hp_color = (0, 255, 0) if p2_pct > 0.5 else (255, 255, 0) if p2_pct > 0.25 else (255, 60, 60)
                pygame.draw.rect(self.screen, p2_hp_color, (p2_hud_x, 35, int(hp_bar_w * p2_pct), hp_bar_h))
                if self.player2.health <= 0:
                    self.screen.blit(self.font.render("DEAD", True, (255, 80, 80)), (p2_hud_x, 49))

            # Draw controls
            if self.num_players == 2:
                ctrl = "P1: WASD+LCtrl  |  P2: Arrows+RCtrl  |  Shift+R: Restart"
            else:
                ctrl = "Move: WASD  |  Shoot: LCtrl  |  Shift+R: Restart  |  ESC: Quit"
            controls_text = self.font.render(ctrl, True, TEXT_COLOR)
            self.screen.blit(controls_text, (WINDOW_WIDTH // 2 - controls_text.get_width() // 2, WINDOW_HEIGHT - 30))

        else:
            # Game over screen
            game_over_text = self.large_font.render("GAME OVER", True, EXPLOSION_COLOR)
            if self.num_players == 2:
                if self.score1 > self.score2:
                    result = f"P1 Wins!  ({self.score1} vs {self.score2})"
                    result_color = PLAYER_COLOR
                elif self.score2 > self.score1:
                    result = f"P2 Wins!  ({self.score2} vs {self.score1})"
                    result_color = PLAYER2_COLOR
                else:
                    result = f"Tie!  ({self.score1} pts each)"
                    result_color = TEXT_COLOR
                score_text = self.font.render(result, True, result_color)
            else:
                score_text = self.font.render(f"Final Score: {self.score1}", True, TEXT_COLOR)
            restart_text = self.font.render("SPACE: menu  |  Shift+R: replay  |  ESC: quit", True, TEXT_COLOR)

            # Center the text
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(restart_text, restart_rect)

        self.present()

    def run(self):
        """Main game loop with custom timing."""
        while self.running:
            self.running = self.handle_input()
            if self.running:
                self.update()
                self.draw()
                self.clock.tick(FPS)

        pygame.quit()
