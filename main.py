import pygame

WIDTH : int = 900
HEIGHT : int = 600
FPS : float = 60.0

# uses a name pygame color
BACKGROUND_COLOR : str = "antiquewhite1"

ROTATE_CIRCLE_COLOR : str = "cornflowerblue"
BOARD_COLOR : str = "cornsilk4"

SLOTS_COLOR : str = "gold"

def main() -> None:

    # pygame setup
    pygame.init()
    pygame.display.set_caption("IART - Top Spin")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True

    screenWidth : int = screen.get_width()
    screenHeight : int = screen.get_height()
    screenCenter : tuple[int, int] = (int(screenWidth/2), int(screenHeight/2))

    dt = 0

    while running:
        # event polling
        for event in pygame.event.get():
            # press on screen X or pressing 'q'
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                running = False

        # clear screen
        screen.fill(BACKGROUND_COLOR)

        # rendering

        # board
        ellipsisWidth : float = 700
        ellipsisHeight : float = ellipsisWidth / 2
        boardRectContainer : pygame.Rect = pygame.Rect(0, 0, ellipsisWidth, ellipsisHeight)
        boardRectContainer.center = screenCenter
        pygame.draw.ellipse(screen, BOARD_COLOR, boardRectContainer)

        #rotate
        rotateCircleCenter : tuple[int, int] = (screenCenter[0], screenCenter[1] - 150)
        pygame.draw.circle(screen, ROTATE_CIRCLE_COLOR, rotateCircleCenter, 120)

        #slots; broken for now!
        for i in range(20):
            slotsCenter : tuple[int, int] = (screenCenter[0] + i*20, screenCenter[1]+20*i)
            pygame.draw.circle(screen, SLOTS_COLOR, slotsCenter, 20)

        pygame.display.flip()

        # set FPS
        dt = clock.tick(FPS) / 1000

    pygame.quit()

if __name__ == "__main__":    
    main()
