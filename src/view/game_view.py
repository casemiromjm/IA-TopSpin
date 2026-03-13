import math
import pygame

SCALE_FACTOR: int = 1

BACKGROUND_COLOR: str = "antiquewhite1"
ROTATE_CIRCLE_COLOR: str = "cornflowerblue"
BOARD_COLOR: str = "cornsilk4"
SLOTS_COLOR: str = "gold"


def draw_frame(screen: pygame.Surface, screen_size: tuple[int, int]) -> None:
    """Draw a full frame of the game."""
    screen_width, screen_height = screen_size

    # clear screen
    screen.fill(BACKGROUND_COLOR)

    screen_center: tuple[int, int] = (int(screen_width / 2), int(screen_height / 2))

    # board
    rect_width: float = 700 * SCALE_FACTOR
    rect_height: float = rect_width / 2
    board_rect_container: pygame.Rect = pygame.Rect(0, 0, rect_width, rect_height)
    board_rect_container.center = screen_center
    pygame.draw.rect(screen, BOARD_COLOR, board_rect_container, border_radius=30)

    # rotate
    rotate_circle_radius = 140
    rotate_circle_center: tuple[int, int] = (
        screen_center[0],
        screen_center[1] - (150 * SCALE_FACTOR),
    )
    pygame.draw.circle(
        screen,
        ROTATE_CIRCLE_COLOR,
        rotate_circle_center,
        rotate_circle_radius * SCALE_FACTOR,
    )

    # slots; only 3 inside the rotate circle for now, but it must be 4 and the track is not alright
    total_slots: int = 20
    # offset so that slots are drawn inside the board
    offset: float = 30 * SCALE_FACTOR
    radius_x: float = rect_width / 2.0 - offset
    radius_y: float = rect_height / 2.0 - offset

    for i in range(total_slots):
        angle = i * (2 * math.pi / total_slots)

        slots_x = board_rect_container.center[0] + radius_x * math.cos(angle)
        slots_y = board_rect_container.center[1] + radius_y * math.sin(angle)

        slots_center: tuple[int, int] = (int(slots_x), int(slots_y))
        pygame.draw.circle(screen, SLOTS_COLOR, slots_center, 20 * SCALE_FACTOR)
