"""Test script to show system font sizes being used."""

import pygame
from games.typing.constants import WORD_FONT_SIZE, UI_FONT_SIZE, TITLE_FONT_SIZE


def show_font_info():
    pygame.init()

    print("System Font Information:")
    print(f"Default font: {pygame.font.get_default_font()}")
    print(f"Available system fonts: {len(pygame.font.get_fonts())} fonts")

    print("\nCalculated Font Sizes:")
    print(f"Word font size: {WORD_FONT_SIZE}px")
    print(f"UI font size: {UI_FONT_SIZE}px")
    print(f"Title font size: {TITLE_FONT_SIZE}px")

    # Test render to show actual sizes
    try:
        default_font = pygame.font.Font(None, 0)
        test_surface = default_font.render("Test", True, (255, 255, 255))
        print(f"\nSystem default font renders at: {test_surface.get_height()}px height")
    except Exception as e:
        print(f"Error testing default font: {e}")

    pygame.quit()


if __name__ == "__main__":
    show_font_info()
