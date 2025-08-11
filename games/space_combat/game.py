"""Main Space Combat game implementation."""

import pygame
from shared.base_game import BaseGame
from shared.constants import MEDIUM_FONT, LARGE_FONT
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, ENEMY_SPAWN_RATE,
    BACKGROUND_COLOR, PLAYER_COLOR, BULLET_COLOR, ENEMY_COLOR, 
    TEXT_COLOR, EXPLOSION_COLOR, ENEMY_KILL_POINTS
)
from .entities import Player, Enemy, Explosion
from .physics import check_bullet_enemy_collisions, check_player_enemy_collisions


class SpaceCombatGame(BaseGame):
    """Main Space Combat game class."""
    
    def __init__(self):
        """Initialize the Space Combat game."""
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, "Space Combat")
        self.font = pygame.font.Font(None, MEDIUM_FONT)
        self.large_font = pygame.font.Font(None, LARGE_FONT)
        self.reset_game()
        
    def reset_game(self):
        """Reset the game to initial state."""
        # Initialize player at bottom center
        player_x = WINDOW_WIDTH // 2 - 20
        player_y = WINDOW_HEIGHT - 50
        self.player = Player(player_x, player_y)
        
        # Initialize game objects
        self.bullets = []
        self.enemies = []
        self.explosions = []
        
        # Game state
        self.score = 0
        self.game_over = False
        self.enemy_spawn_timer = 0
        self.shoot_cooldown = 0
        
    def handle_input(self):
        """Handle input events."""
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_ESCAPE:
                        return False
                        
        # Handle continuous input during gameplay
        if not self.game_over:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move_right()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.move_up()
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.move_down()
            if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
                self.bullets.append(self.player.shoot())
                self.shoot_cooldown = 10  # Prevent rapid fire
                
        return True
        
    def update(self):
        """Update game state."""
        if self.game_over:
            return
            
        # Update cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= ENEMY_SPAWN_RATE:
            self.enemies.append(Enemy.spawn_random())
            self.enemy_spawn_timer = 0
            
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
                
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
                
        # Check bullet-enemy collisions
        bullet_enemy_collisions = check_bullet_enemy_collisions(self.bullets, self.enemies)
        
        # Remove collided bullets and enemies, add explosions and score
        bullets_to_remove = set()
        enemies_to_remove = set()
        
        for bullet_idx, enemy_idx in bullet_enemy_collisions:
            bullets_to_remove.add(bullet_idx)
            enemies_to_remove.add(enemy_idx)
            
            # Add explosion at enemy position
            enemy = self.enemies[enemy_idx]
            self.explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
            
            # Add score
            self.score += ENEMY_KILL_POINTS
            
        # Remove collided objects (in reverse order to maintain indices)
        for bullet_idx in sorted(bullets_to_remove, reverse=True):
            if bullet_idx < len(self.bullets):
                self.bullets.pop(bullet_idx)
        for enemy_idx in sorted(enemies_to_remove, reverse=True):
            if enemy_idx < len(self.enemies):
                self.enemies.pop(enemy_idx)
                
        # Check player-enemy collisions
        player_enemy_collisions = check_player_enemy_collisions(self.player, self.enemies)
        
        # Handle player damage
        for enemy_idx in sorted(player_enemy_collisions, reverse=True):
            enemy = self.enemies[enemy_idx]
            self.explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
            self.enemies.pop(enemy_idx)
            
            if not self.player.take_damage():
                self.game_over = True
                
    def draw(self):
        """Draw the game."""
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        if not self.game_over:
            # Draw player
            player_rect = self.player.get_rect()
            pygame.draw.rect(self.screen, PLAYER_COLOR, player_rect)
            
            # Draw bullets
            for bullet in self.bullets:
                bullet_rect = bullet.get_rect()
                pygame.draw.rect(self.screen, BULLET_COLOR, bullet_rect)
                
            # Draw enemies
            for enemy in self.enemies:
                enemy_rect = enemy.get_rect()
                pygame.draw.rect(self.screen, ENEMY_COLOR, enemy_rect)
                
            # Draw explosions
            for explosion in self.explosions:
                pygame.draw.circle(self.screen, EXPLOSION_COLOR, 
                                 (int(explosion.x), int(explosion.y)), explosion.radius)
                                 
            # Draw HUD
            score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
            self.screen.blit(score_text, (10, 10))
            
            health_text = self.font.render(f"Health: {self.player.health}", True, TEXT_COLOR)
            self.screen.blit(health_text, (10, 40))
            
            # Draw health bar
            health_bar_width = 200
            health_bar_height = 10
            health_percentage = self.player.health / self.player.max_health
            health_bar_fill = int(health_bar_width * health_percentage)
            
            # Health bar background
            pygame.draw.rect(self.screen, (100, 100, 100), 
                           (10, 70, health_bar_width, health_bar_height))
            # Health bar fill
            if health_percentage > 0.5:
                health_color = (0, 255, 0)  # Green
            elif health_percentage > 0.25:
                health_color = (255, 255, 0)  # Yellow
            else:
                health_color = (255, 0, 0)  # Red
                
            pygame.draw.rect(self.screen, health_color, 
                           (10, 70, health_bar_fill, health_bar_height))
            
            # Draw controls
            controls_text = self.font.render("WASD/Arrows: Move, SPACE: Shoot, ESC: Quit", True, TEXT_COLOR)
            self.screen.blit(controls_text, (10, WINDOW_HEIGHT - 30))
            
        else:
            # Game over screen
            game_over_text = self.large_font.render("GAME OVER", True, EXPLOSION_COLOR)
            score_text = self.font.render(f"Final Score: {self.score}", True, TEXT_COLOR)
            restart_text = self.font.render("Press SPACE to play again, ESC to quit", True, TEXT_COLOR)
            
            # Center the text
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            
            self.screen.blit(game_over_text, game_over_rect)
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
