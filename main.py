import pygame

WIDTH : int = 900
HEIGHT : int = 600
FPS : int = 60

BACKGROUND : str = "black"

def main() -> None:

    # pygame setup
    pygame.init()
    pygame.display.set_caption("IART - Water Sort")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    while running:
        # event polling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND)

        pygame.display.flip()

        # set FPS
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
