import pygame
import math

SCALE_FACTOR : int = 1
WIDTH : int = 1280*SCALE_FACTOR
HEIGHT : int = 720*SCALE_FACTOR
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

    while running:
        # event polling
        for event in pygame.event.get():
            # press on screen X or pressing 'q'
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                running = False

        # clear screen
        screen.fill(BACKGROUND_COLOR)

        screenWidth: int = screen.get_width()
        screenHeight: int = screen.get_height()
        screenCenter: tuple[int, int] = (int(screenWidth/2), int(screenHeight/2))

        # rendering

        # board
        rectWidth: float = 700 * SCALE_FACTOR
        rectHeight: float = rectWidth / 2
        boardRectContainer: pygame.Rect = pygame.Rect(0, 0, rectWidth, rectHeight)
        boardRectContainer.center = screenCenter
        pygame.draw.rect(screen, BOARD_COLOR, boardRectContainer, border_radius=30)

        # rotate
        rotate_circle_radius = 140
        rotateCircleCenter : tuple[int, int] = (screenCenter[0], screenCenter[1] - (150*SCALE_FACTOR))
        pygame.draw.circle(screen, ROTATE_CIRCLE_COLOR, rotateCircleCenter, rotate_circle_radius*SCALE_FACTOR)

        #slots; only 3 inside the rotate circle for now, but it must be 4 and the track is not alright
        total_slots: int = 20
        # offset so that slots are drawn inside the board
        offset: float = 30*SCALE_FACTOR
        radius_x: float = rectWidth/2.0 - offset
        radius_y:float = rectHeight/2.0 - offset

        for i in range(total_slots):

            angle = i*(2*math.pi / total_slots)
            
            slots_x = boardRectContainer.center[0] + radius_x * math.cos(angle)
            slots_y = boardRectContainer.center[1] + radius_y * math.sin(angle)

            slotsCenter : tuple[int, int] = (int(slots_x), int(slots_y))
            pygame.draw.circle(screen, SLOTS_COLOR, slotsCenter, 20*SCALE_FACTOR)

        pygame.display.flip()

        # set FPS
        dt = clock.tick(FPS) / 1000

    pygame.quit()

if __name__ == "__main__":    
    main()
