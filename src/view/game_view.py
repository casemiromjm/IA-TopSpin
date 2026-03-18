import math
import pygame

# ── Scaling ───────────────────────────────────────────────────────────────────
SCALE_FACTOR: int = 1

# ── Colors ────────────────────────────────────────────────────────────────────
BACKGROUND_COLOR: str = "antiquewhite1"
BOARD_COLOR: tuple  = (130, 135, 145)
BOARD_DEPTH_COLOR: tuple       = (60, 62, 68)
BOARD_BORDER_COLOR: tuple = (210, 215, 220)
SLOTS_COLOR: str = "gold"
SLOT_SHADOW_COLOR: tuple = (160, 115, 0)
SLOT_HIGHLIGHT_COLOR: tuple = (255, 242, 140)
ROTATE_CIRCLE_COLOR: str = "cornflowerblue"
ROTATE_SHADOW_COLOR: tuple = (50, 80, 145)
ROTATE_HIGHLIGHT_COLOR: tuple = (175, 215, 255)

# ── Board shape ───────────────────────────────────────────────────────────────
BOARD_WIDTH: int = 700          # base width in pixels (scaled by SCALE_FACTOR)
BOARD_ASPECT: float = 2.0       # width / height ratio
BOARD_CORNER_RADIUS: int = 210  # rounded-rect corner radius (capped to half-extents)
BOARD_BORDER: int = 10          # rim stroke width

# ── Board 3-D depth ───────────────────────────────────────────────────────────
# BOARD_DEPTH_Y  : how many pixels the box drops downward (vertical depth)
# BOARD_DEPTH_X  : horizontal shift of the back face (perspective lean)
# Set both equal for a 45° perspective; set BOARD_DEPTH_X=0 for straight-down.
BOARD_DEPTH_Y: int = 30         # ← change this to make the box taller/shorter
BOARD_DEPTH_X: int = 0  # ← change independently for lean

# ── Slots (balls on the track) ────────────────────────────────────────────────
TOTAL_SLOTS: int = 20
SLOTS_SIZE: int = 30            # ball radius
SLOT_TRACK_INSET: float = 50.0  # inset from board edge to slot-track center-line
SLOT_START_OFFSET: float = 0.044  # fraction along perimeter where slot 0 sits
SLOT_SHADOW_OFFSET: int = 4     # shadow drop (pixels)

# ── Rotate circle ─────────────────────────────────────────────────────────────
ROTATE_CIRCLE_RADIUS: int = 140
ROTATE_CIRCLE_OFFSET_Y: int = 130  # upward offset from screen center
ROTATE_SHADOW_OFFSET: int = 1     # shadow drop (pixels)

# ── Apply scale (do not edit below this line) ─────────────────────────────────
_BOARD_WIDTH: float  = BOARD_WIDTH          * SCALE_FACTOR
_BOARD_HEIGHT: float = _BOARD_WIDTH         / BOARD_ASPECT
_BOARD_BORDER: int   = max(1, round(BOARD_BORDER   * SCALE_FACTOR))
_BOARD_DEPTH_Y: int  = round(BOARD_DEPTH_Y  * SCALE_FACTOR)
_BOARD_DEPTH_X: int  = round(BOARD_DEPTH_X  * SCALE_FACTOR)
_SLOTS_SIZE: int     = round(SLOTS_SIZE     * SCALE_FACTOR)
_SLOT_TRACK_INSET: float = SLOT_TRACK_INSET * SCALE_FACTOR
_ROTATE_R: int       = round(ROTATE_CIRCLE_RADIUS  * SCALE_FACTOR)
_ROTATE_OFFSET_Y: int = round(ROTATE_CIRCLE_OFFSET_Y * SCALE_FACTOR)

# Legacy alias kept so main.py import still works
BOARD_DEPTH = _BOARD_DEPTH_Y

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

    # board rects
    board_rect_container: pygame.Rect = pygame.Rect(0, 0, _BOARD_WIDTH, _BOARD_HEIGHT)
    board_rect_container.center = screen_center
    inner_w = _BOARD_WIDTH  - 2 * (_SLOT_TRACK_INSET + _SLOTS_SIZE) - _BOARD_BORDER
    inner_h = _BOARD_HEIGHT - 2 * (_SLOT_TRACK_INSET + _SLOTS_SIZE) - _BOARD_BORDER
    board_rect_small_container: pygame.Rect = pygame.Rect(0, 0, inner_w, inner_h)
    board_rect_small_container.center = screen_center
    board_depth_small_container: pygame.Rect = pygame.Rect(0, 0, inner_w, inner_h + _BOARD_DEPTH_Y)
    board_depth_small_container.center = screen_center
    board_depth_small_container.move_ip(0, _BOARD_DEPTH_Y // 2)

    # board 3-D depth
    board_r: int = min(BOARD_CORNER_RADIUS, int(_BOARD_WIDTH // 2), int(_BOARD_HEIGHT // 2))
    board_sw: float = _BOARD_WIDTH / 2 - board_r  # horizontal straight half-extent

    # back face shifted by depth
    depth_rect = board_rect_container.move(_BOARD_DEPTH_X, _BOARD_DEPTH_Y)
    pygame.draw.rect(screen, BOARD_DEPTH_COLOR, depth_rect, border_radius=BOARD_CORNER_RADIUS)

    # bottom wall: parallelogram connecting front bottom edge to back bottom edge
    if board_sw > 0:
        bx = float(board_rect_container.centerx)
        by = float(board_rect_container.bottom)
        pygame.draw.polygon(screen, BOARD_DEPTH_COLOR, [
            (bx - board_sw,                          by),
            (bx + board_sw,                          by),
            (bx + board_sw + _BOARD_DEPTH_X, by + _BOARD_DEPTH_Y),
            (bx - board_sw + _BOARD_DEPTH_X, by + _BOARD_DEPTH_Y),
        ])

    # top face
    pygame.draw.rect(screen, BOARD_COLOR,        board_rect_container,       border_radius=BOARD_CORNER_RADIUS)
    pygame.draw.rect(screen, BOARD_DEPTH_COLOR,  depth_rect,                 border_radius=BOARD_CORNER_RADIUS)
    pygame.draw.rect(screen, BOARD_COLOR, board_depth_small_container, border_radius=BOARD_CORNER_RADIUS)
    pygame.draw.rect(screen, BOARD_BORDER_COLOR,        board_rect_small_container, border_radius=BOARD_CORNER_RADIUS)
    # border rim
    pygame.draw.rect(screen, BOARD_BORDER_COLOR, board_rect_container, width=_BOARD_BORDER, border_radius=BOARD_CORNER_RADIUS)

    # rotate circle
    rotate_circle_center: tuple[int, int] = (
        screen_center[0],
        screen_center[1] - _ROTATE_OFFSET_Y,
    )
    rcx, rcy = rotate_circle_center
    pygame.draw.circle(screen, ROTATE_SHADOW_COLOR,    (rcx + ROTATE_SHADOW_OFFSET, rcy + ROTATE_SHADOW_OFFSET), _ROTATE_R)
    pygame.draw.circle(screen, ROTATE_CIRCLE_COLOR,    rotate_circle_center,                                      _ROTATE_R)
    pygame.draw.circle(screen, ROTATE_HIGHLIGHT_COLOR, (rcx - _ROTATE_R // 4, rcy - _ROTATE_R // 4),             _ROTATE_R // 4)

    # slots
    cx, cy = board_rect_container.center
    hw: float = _BOARD_WIDTH  / 2.0 - _SLOT_TRACK_INSET
    hh: float = _BOARD_HEIGHT / 2.0 - _SLOT_TRACK_INSET
    slot_corner_r: float = BOARD_CORNER_RADIUS - _SLOT_TRACK_INSET  # inset corner radius matches board shape

    for i in range(TOTAL_SLOTS):
        sx, sy = _rounded_rect_point(SLOT_START_OFFSET + i / TOTAL_SLOTS, cx, cy, hw, hh, slot_corner_r)
        isx, isy = int(sx), int(sy)
        pygame.draw.circle(screen, SLOT_SHADOW_COLOR,    (isx + SLOT_SHADOW_OFFSET, isy + SLOT_SHADOW_OFFSET), _SLOTS_SIZE)
        pygame.draw.circle(screen, SLOTS_COLOR,          (isx, isy),                                           _SLOTS_SIZE)
        pygame.draw.circle(screen, SLOT_HIGHLIGHT_COLOR, (isx - _SLOTS_SIZE // 3, isy - _SLOTS_SIZE // 3),    _SLOTS_SIZE // 4)
