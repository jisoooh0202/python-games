"""Shared utility functions for all games."""

import pygame


def load_font(size=None, font_path=None):
    """Load a font with given size and optional path.
    
    Args:
        size: Font size (default: 36)
        font_path: Path to font file (default: None for system font)
        
    Returns:
        pygame.font.Font object
    """
    if size is None:
        size = 36
    return pygame.font.Font(font_path, size)


def clamp(value, min_value, max_value):
    """Clamp a value between min and max.
    
    Args:
        value: Value to clamp
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Returns:
        Clamped value
    """
    return max(min_value, min(value, max_value))


def distance(point1, point2):
    """Calculate distance between two points.
    
    Args:
        point1: (x, y) tuple
        point2: (x, y) tuple
        
    Returns:
        Distance as float
    """
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return (dx * dx + dy * dy) ** 0.5
