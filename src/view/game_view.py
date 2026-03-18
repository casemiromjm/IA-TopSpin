import math
import pygame

SCALE_FACTOR: int = 1

BACKGROUND_COLOR: str = "antiquewhite1"
ROTATE_CIRCLE_COLOR: str = "cornflowerblue"
BOARD_COLOR: str = "cornsilk4"
SLOTS_COLOR: str = "gold"
SLOTS_SIZE: int = 30 * SCALE_FACTOR

BOARD_DEPTH_COLOR: tuple = (85, 72, 55)
BOARD_BORDER_COLOR: tuple = (140, 122, 98)
BOARD_DEPTH: int = 30 * SCALE_FACTOR
SLOT_SHADOW_COLOR: tuple = (160, 115, 0)
SLOT_HIGHLIGHT_COLOR: tuple = (255, 242, 140)
ROTATE_SHADOW_COLOR: tuple = (50, 80, 145)
ROTATE_HIGHLIGHT_COLOR: tuple = (175, 215, 255)
BOARD_BORDER: int = 4 * SCALE_FACTOR

def _rounded_rect_point(
    t: float, cx: float, cy: float, hw: float, hh: float, r: float
) -> tuple[float, float]:
    """Return a point at fraction t (0..1) along a rounded-rectangle perimeter, clockwise from top-center."""
    r = min(r, hw, hh)
    sw, sh = hw - r, hh - r  # straight half-extents
    arc = math.pi / 2 * r
    segments = [
        (2 * sw, "top"),
        (arc,    "arc_tr"),
        (2 * sh, "right"),
        (arc,    "arc_br"),
        (2 * sw, "bottom"),
        (arc,    "arc_bl"),
        (2 * sh, "left"),
        (arc,    "arc_tl"),
    ]
    total = sum(length for length, _ in segments)
    d = (t % 1.0) * total

    for length, name in segments:
        if d <= length:
            f = d / length if length else 0
            if name == "top":
                return (cx - sw + f * 2 * sw, cy - hh)
            if name == "arc_tr":
                a = -math.pi / 2 + f * math.pi / 2
                return (cx + sw + r * math.cos(a), cy - sh + r * math.sin(a))
            if name == "right":
                return (cx + hw, cy - sh + f * 2 * sh)
            if name == "arc_br":
                a = f * math.pi / 2
                return (cx + sw + r * math.cos(a), cy + sh + r * math.sin(a))
            if name == "bottom":
                return (cx + sw - f * 2 * sw, cy + hh)
            if name == "arc_bl":
                a = math.pi / 2 + f * math.pi / 2
                return (cx - sw + r * math.cos(a), cy + sh + r * math.sin(a))
            if name == "left":
                return (cx - hw, cy + sh - f * 2 * sh)
            if name == "arc_tl":
                a = math.pi + f * math.pi / 2
                return (cx - sw + r * math.cos(a), cy - sh + r * math.sin(a))
        d -= length
    return (cx - sw, cy - hh)


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
    board_rect_small_container: pygame.Rect = pygame.Rect(0, 0, rect_width - 2 * BOARD_BORDER - 4 * SLOTS_SIZE, rect_height - 2 * BOARD_BORDER - 4 * SLOTS_SIZE)
    board_rect_small_container.center = screen_center
    # board 3d box effect
    board_r: int = min(210, int(rect_width // 2), int(rect_height // 2))
    board_sw: float = rect_width / 2 - board_r  # horizontal straight half-extent

    # back face (handles curved ends)
    depth_rect = board_rect_container.move(0, BOARD_DEPTH)
    pygame.draw.rect(screen, BOARD_DEPTH_COLOR, depth_rect, border_radius=210)

    # bottom wall: explicit parallelogram for the straight bottom section
    if board_sw > 0:
        bx = float(board_rect_container.centerx)
        by = float(board_rect_container.bottom)
        pygame.draw.polygon(screen, BOARD_DEPTH_COLOR, [
            (bx - board_sw,              by),
            (bx + board_sw,              by),
            (bx + board_sw + BOARD_DEPTH, by + BOARD_DEPTH),
            (bx - board_sw + BOARD_DEPTH, by + BOARD_DEPTH),
        ])

    # top face
    pygame.draw.rect(screen, BOARD_COLOR, board_rect_container, border_radius=210)
    pygame.draw.rect(screen, BOARD_DEPTH_COLOR, depth_rect, border_radius=210)
    pygame.draw.rect(screen, BOARD_COLOR, board_rect_small_container , border_radius=210)
    # border rim
    pygame.draw.rect(screen, BOARD_BORDER_COLOR, board_rect_container, width = BOARD_BORDER, border_radius=210)

    # rotate circle
    rotate_circle_radius = 140
    rotate_circle_center: tuple[int, int] = (
        screen_center[0],
        screen_center[1] - (130 * SCALE_FACTOR),
    )
    r = rotate_circle_radius * SCALE_FACTOR
    rcx, rcy = rotate_circle_center
    pygame.draw.circle(screen, ROTATE_SHADOW_COLOR, (rcx + 5, rcy + 5), r)
    pygame.draw.circle(screen, ROTATE_CIRCLE_COLOR, rotate_circle_center, r)
    pygame.draw.circle(screen, ROTATE_HIGHLIGHT_COLOR, (rcx - r // 4, rcy - r // 4), r // 4)

    # slots
    total_slots: int = 20
    offset: float = 50 * SCALE_FACTOR
    cx, cy = board_rect_container.center
    hw: float = rect_width / 2.0 - offset
    hh: float = rect_height / 2.0 - offset
    slot_corner_r: float = 210 - offset  # inset corner radius matches the board shape
    slot_r: int = SLOTS_SIZE

    start_offset: float = 0.044 * SCALE_FACTOR  # 0.0 = top-center, 0.25 = right, 0.5 = bottom-center, 0.75 = left
    for i in range(total_slots):
        sx, sy = _rounded_rect_point(start_offset + i / total_slots, cx, cy, hw, hh, slot_corner_r)
        isx, isy = int(sx), int(sy)
        pygame.draw.circle(screen, SLOT_SHADOW_COLOR, (isx + 4, isy + 4), slot_r)
        pygame.draw.circle(screen, SLOTS_COLOR, (isx, isy), slot_r)
        pygame.draw.circle(screen, SLOT_HIGHLIGHT_COLOR, (isx - slot_r // 3, isy - slot_r // 3), slot_r // 4)
