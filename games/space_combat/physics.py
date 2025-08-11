"""Physics and collision utilities for Space Combat game."""


def check_collision(rect1, rect2):
    """Check if two rectangles collide."""
    return rect1.colliderect(rect2)


def check_bullet_enemy_collisions(bullets, enemies):
    """Check collisions between bullets and enemies.

    Returns:
        List of (bullet_index, enemy_index) tuples for collisions
    """
    collisions = []
    for bullet_idx, bullet in enumerate(bullets):
        for enemy_idx, enemy in enumerate(enemies):
            if check_collision(bullet.get_rect(), enemy.get_rect()):
                collisions.append((bullet_idx, enemy_idx))
    return collisions


def check_player_enemy_collisions(player, enemies):
    """Check collisions between player and enemies.

    Returns:
        List of enemy indices that collided with player
    """
    collisions = []
    player_rect = player.get_rect()
    for enemy_idx, enemy in enumerate(enemies):
        if check_collision(player_rect, enemy.get_rect()):
            collisions.append(enemy_idx)
    return collisions
