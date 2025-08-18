"""Test script to check if pygame window resizing works."""

import pygame


def test_resize():
    pygame.init()

    # Create a resizable window
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Resize Test - Drag the window edges!")

    clock = pygame.time.Clock()
    running = True

    print("Window created with RESIZABLE flag")
    print("Try to resize the window by dragging the edges")
    print("Press ESC to quit")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                print(f"Window resized to: {event.w}x{event.h}")
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Fill screen with color
        screen.fill((50, 50, 100))

        # Draw some text
        font = pygame.font.Font(None, 36)
        text = font.render("Try resizing this window!", True, (255, 255, 255))
        size_text = font.render(f"Size: {screen.get_width()}x{screen.get_height()}", True, (255, 255, 255))

        screen.blit(text, (10, 10))
        screen.blit(size_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    test_resize()
