import pygame

from src.view.game_view import SCALE_FACTOR, draw_frame

WIDTH: int = 1280 * SCALE_FACTOR
HEIGHT: int = 720 * SCALE_FACTOR
FPS: float = 60.0


def main() -> None:

    # pygame setup
    pygame.init()
    pygame.display.set_caption("IART - Top Spin")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True

    while running:
        # event polling
        for event in pygame.event.get():
            # press on screen X or pressing 'q'
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_q
            ):
                running = False

        screenWidth: int = screen.get_width()
        screenHeight: int = screen.get_height()

        # rendering
        draw_frame(screen, (screenWidth, screenHeight))

        pygame.display.flip()

        # set FPS
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
