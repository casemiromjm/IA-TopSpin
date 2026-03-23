import math
import pygame
import pygame.freetype

# ── Scaling ───────────────────────────────────────────────────────────────────
SCALE_FACTOR: int = 1

# ── Colors ────────────────────────────────────────────────────────────────────
BACKGROUND_COLOR: str = "antiquewhite1"

BOARD_COLOR: tuple        = (130, 135, 145)
BOARD_DEPTH_COLOR: tuple  = (60, 62, 68)
BOARD_BORDER_COLOR: tuple = (210, 215, 220)

SLOTS_COLOR: tuple          = (255, 210, 50)
SLOT_SHADOW_COLOR: tuple    = (150, 110, 0)
SLOT_HIGHLIGHT_COLOR: tuple = (255, 245, 160)
SLOT_TEXT_COLOR: tuple      = (70, 40, 0)

ROTATE_CIRCLE_COLOR: tuple    = (55, 108, 192)
ROTATE_SHADOW_COLOR: tuple    = (20, 40, 80)
ROTATE_HIGHLIGHT_COLOR: tuple = (130, 180, 245)
ROTATE_CUT_COLOR: tuple       = (22, 48, 92)    # deep pit (top cut)
ROTATE_CUT_HIGHLIGHT: tuple   = (85, 140, 220)  # light catching a cut edge
ROTATE_CUT_SHADOW: tuple      = (10, 25, 52)    # deeper pit (bottom cut)

ROTATE_WINDOW_COLOR: tuple = (255, 100, 80)     # tint for rotate-zone slots

# ── Board shape ───────────────────────────────────────────────────────────────
BOARD_WIDTH: int        = 700    # base width in pixels (scaled by SCALE_FACTOR)
BOARD_ASPECT: float     = 2.0    # width / height ratio
BOARD_CORNER_RADIUS: int = 210   # rounded-rect corner radius (capped to half-extents)
BOARD_BORDER: int       = 10     # rim stroke width

# ── Board 3-D depth ──────────────────────────────────────────────────────────
BOARD_DEPTH_Y: int = 30
BOARD_DEPTH_X: int = 0

# ── Slots (balls on the track) ───────────────────────────────────────────────
TOTAL_SLOTS: int         = 20
SLOTS_SIZE: int          = 30     # ball radius
SLOT_TRACK_INSET: float  = 50.0   # inset from board edge to track centre-line
SLOT_START_OFFSET: float = 0.044  # fraction along perimeter where slot 0 sits
SLOT_SHADOW_OFFSET: int  = 4      # shadow drop (pixels)

# ── Rotate circle ────────────────────────────────────────────────────────────
ROTATE_SHADOW_OFFSET: int = 1     # shadow drop (pixels)

# ── Scaled values (do not edit) ──────────────────────────────────────────────
_BOARD_WIDTH: float      = BOARD_WIDTH   * SCALE_FACTOR
_BOARD_BORDER: int       = max(1, round(BOARD_BORDER * SCALE_FACTOR))
_BOARD_DEPTH_Y: int      = round(BOARD_DEPTH_Y  * SCALE_FACTOR)
_BOARD_DEPTH_X: int      = round(BOARD_DEPTH_X  * SCALE_FACTOR)
_SLOTS_SIZE: int         = round(SLOTS_SIZE      * SCALE_FACTOR)
_SLOT_TRACK_INSET: float = SLOT_TRACK_INSET      * SCALE_FACTOR

# Legacy alias
BOARD_DEPTH = _BOARD_DEPTH_Y

# ── Per-size display configuration ───────────────────────────────────────────
# aspect:       board width / height ratio  (1.0 = circle, 2.0 = wide rect)
# slot_start:   where ball-0 appears on the perimeter (0 = top-centre, CW)
# push_factor:  how far to push the circle centre along the perpendicular
#               (fraction of the half-chord between the two gap points)
# corner_mult:  extra rounding for the board corners (1.0 = default)
# gap_bias:     where the circle edge crosses the track between adjacent balls
#               (0.5 = midpoint, <0.5 = closer to the window ball)
_SIZE_DISPLAY: dict[int, dict] = {
    #              cut_fracs: [top, mid, bot] as (ircy - y) / R  (positive = above circle centre)
    10: {"aspect": 1.2, "slot_start": 0.924, "push_factor": 0.30, "corner_mult": 1.0, "gap_bias": 0.35,
         "cut_fracs": [0.20, 0.0, -0.25]},
    20: {"aspect": 2.0, "slot_start": 0.044, "push_factor": 0.15, "corner_mult": 1.0, "gap_bias": 0.35,
         "cut_fracs": [0.14, 0.0, -0.29]},
}

# ── Font cache ────────────────────────────────────────────────────────────────
_font_cache: dict[int, pygame.freetype.Font] = {}


def _get_font(size: int) -> pygame.freetype.Font:
    """Return a cached bold font at the given pixel size."""
    if not pygame.freetype.get_init():
        pygame.freetype.init()
    if size not in _font_cache:
        _font_cache[size] = pygame.freetype.SysFont("Arial", size, bold=True)
    return _font_cache[size]


# ── Geometry helpers ──────────────────────────────────────────────────────────

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



# ── Main draw routine ────────────────────────────────────────────────────────

def draw_frame(
    screen: pygame.Surface,
    screen_size: tuple[int, int],
    slots: list[int] | None = None,
    total_slots: int = TOTAL_SLOTS,
    rotate_window: int = 4,
) -> None:
    """Draw one frame of the Top Spin board.

    *slots*: ordered list of slot values (e.g. [3,1,5,…]).
             If None a static demo board is drawn.
    *total_slots*: how many balls on the track.
    *rotate_window*: how many front slots the circle flips.
    """
    screen_width, screen_height = screen_size
    screen.fill(BACKGROUND_COLOR)
    screen_center = (screen_width // 2, screen_height // 2)

    # ── per-size display config ────────────────────────────────────────
    cfg = _SIZE_DISPLAY.get(total_slots, _SIZE_DISPLAY[20])
    board_aspect = cfg["aspect"]
    slot_start = cfg["slot_start"]
    _push_factor = cfg["push_factor"]
    _corner_mult = cfg.get("corner_mult", 1.0)
    _gap_bias = cfg.get("gap_bias", 0.35)
    _cut_fracs = cfg.get("cut_fracs", [0.14, 0.0, -0.29])

    # ── dynamic scaling based on slot count ────────────────────────────
    s = 0.4 + 0.6 * (total_slots / 20)
    bw = _BOARD_WIDTH * s
    bh = bw / board_aspect
    b_border = _BOARD_BORDER
    b_depth_y = int(_BOARD_DEPTH_Y * s)
    b_depth_x = int(_BOARD_DEPTH_X * s)
    b_inset = _SLOT_TRACK_INSET * s
    b_corner_r = int(BOARD_CORNER_RADIUS * s * _corner_mult)

    # ── board layout rects ────────────────────────────────────────────
    board_rect = pygame.Rect(0, 0, int(bw), int(bh))
    board_rect.center = screen_center

    inner_w = bw - 2 * (b_inset + _SLOTS_SIZE) - b_border
    inner_h = bh - 2 * (b_inset + _SLOTS_SIZE) - b_border
    inner_rect = pygame.Rect(0, 0, int(inner_w), int(inner_h))
    inner_rect.center = screen_center

    depth_inner = pygame.Rect(0, 0, int(inner_w), int(inner_h + b_depth_y))
    depth_inner.center = screen_center
    depth_inner.move_ip(0, b_depth_y // 2)

    # ── 3-D depth ─────────────────────────────────────────────────────
    board_r = min(b_corner_r, int(bw // 2), int(bh // 2))
    board_sw = bw / 2 - board_r

    depth_rect = board_rect.move(b_depth_x, b_depth_y)
    pygame.draw.rect(screen, BOARD_DEPTH_COLOR, depth_rect, border_radius=b_corner_r)

    if board_sw > 0:
        bx = float(board_rect.centerx)
        by = float(board_rect.bottom)
        pygame.draw.polygon(screen, BOARD_DEPTH_COLOR, [
            (bx - board_sw, by),
            (bx + board_sw, by),
            (bx + board_sw + b_depth_x, by + b_depth_y),
            (bx - board_sw + b_depth_x, by + b_depth_y),
        ])

    # ── top face layers ───────────────────────────────────────────────
    pygame.draw.rect(screen, BOARD_COLOR, board_rect, border_radius=b_corner_r)
    pygame.draw.rect(screen, BOARD_DEPTH_COLOR, depth_rect, border_radius=b_corner_r)
    pygame.draw.rect(screen, BOARD_COLOR, depth_inner, border_radius=b_corner_r)
    pygame.draw.rect(screen, BOARD_BORDER_COLOR, inner_rect, border_radius=b_corner_r)

    # ── slot track geometry ───────────────────────────────────────────
    cx, cy = board_rect.center
    hw = bw / 2.0 - b_inset
    hh = bh / 2.0 - b_inset
    slot_corner_r = b_corner_r - b_inset

    _r = min(slot_corner_r, int(hw), int(hh))
    _track_perimeter = 4 * (hw - _r + hh - _r) + 2 * math.pi * _r
    _ball_r = max(_SLOTS_SIZE,
                  min(int(b_inset * 0.90),
                      int(_track_perimeter * 0.40 / total_slots)))

    # ── rotate circle (all sizes) ─────────────────────────────────────
    # The circle boundary passes through two "gap" points on the track:
    # one between ball N-1 and ball 0, one between ball 3 and ball 4.
    # This guarantees that exactly the 4 window balls are inside.

    # Window ball positions (needed for centroid direction check)
    window_pts = [
        _rounded_rect_point(
            slot_start + i / total_slots, cx, cy, hw, hh, slot_corner_r,
        )
        for i in range(rotate_window)
    ]
    wcx = sum(p[0] for p in window_pts) / rotate_window
    wcy = sum(p[1] for p in window_pts) / rotate_window

    # Gap points on the track (between window and non-window balls)
    gap1 = _rounded_rect_point(
        (slot_start - _gap_bias / total_slots) % 1.0,
        cx, cy, hw, hh, slot_corner_r,
    )
    gap2 = _rounded_rect_point(
        slot_start + (rotate_window - 1 + _gap_bias) / total_slots,
        cx, cy, hw, hh, slot_corner_r,
    )

    # Chord between gap points
    gmx = (gap1[0] + gap2[0]) / 2
    gmy = (gap1[1] + gap2[1]) / 2
    gdx = gap2[0] - gap1[0]
    gdy = gap2[1] - gap1[1]
    half_chord = math.hypot(gdx, gdy) / 2

    # Perpendicular direction — oriented toward the window (outward)
    perp_x, perp_y = -gdy, gdx
    out_x, out_y = wcx - cx, wcy - cy
    if perp_x * out_x + perp_y * out_y < 0:
        perp_x, perp_y = -perp_x, -perp_y
    perp_len = math.hypot(perp_x, perp_y)
    if perp_len > 0:
        perp_x /= perp_len
        perp_y /= perp_len

    # Circle through the two gap points, centre on the perpendicular
    _d = half_chord * _push_factor
    rcx = gmx + perp_x * _d
    rcy = gmy + perp_y * _d
    R = int(math.sqrt(half_chord * half_chord + _d * _d))

    ircx, ircy = int(rcx), int(rcy)

    # ── arc-band helper: horizontal band clipped to the circle arc ────
    _N_ARC = 32

    def _arc_band(y_top: int, y_bot: int) -> list:
        dy_t = max(-R, min(R, ircy - y_top))
        dy_b = max(-R, min(R, ircy - y_bot))
        dx_t = math.sqrt(max(0.0, R * R - dy_t * dy_t))
        dx_b = math.sqrt(max(0.0, R * R - dy_b * dy_b))
        th_t = math.asin(dy_t / R)
        th_b = math.asin(dy_b / R)
        pts = [(ircx - dx_b, y_bot), (ircx + dx_b, y_bot)]
        for i in range(1, _N_ARC):
            th = th_b + (th_t - th_b) * i / _N_ARC
            pts.append((ircx + R * math.cos(th), ircy - R * math.sin(th)))
        pts += [(ircx + dx_t, y_top), (ircx - dx_t, y_top)]
        for i in range(1, _N_ARC):
            th = (math.pi - th_t) + (th_t - th_b) * i / _N_ARC
            pts.append((ircx + R * math.cos(th), ircy - R * math.sin(th)))
        return pts

    # Cut y-positions from per-size fractions of R
    cut_y1 = int(ircy - _cut_fracs[0] * R)
    cut_y2 = int(ircy - _cut_fracs[1] * R)
    cut_y3 = int(ircy - _cut_fracs[2] * R)

    # 1. drop shadow
    pygame.draw.circle(screen, ROTATE_SHADOW_COLOR,
                       (ircx + ROTATE_SHADOW_OFFSET, ircy + ROTATE_SHADOW_OFFSET), R)
    # 2. solid base
    pygame.draw.circle(screen, ROTATE_CIRCLE_COLOR, (ircx, ircy), R)
    # 3. top cut band
    pygame.draw.polygon(screen, ROTATE_CUT_COLOR,  _arc_band(cut_y1, cut_y2))
    # 4. bottom cut band
    pygame.draw.polygon(screen, ROTATE_CUT_SHADOW, _arc_band(cut_y2, cut_y3))
    # 5. divider highlight
    _dy_mid = max(-R, min(R, ircy - cut_y2))
    _dx_mid = math.sqrt(max(0.0, R * R - _dy_mid * _dy_mid))
    pygame.draw.line(screen, ROTATE_CUT_HIGHLIGHT,
                     (int(ircx - _dx_mid + 2), cut_y2),
                     (int(ircx + _dx_mid - 2), cut_y2), 1)
    # 6. specular highlight arc
    _hl_r = R - 4
    if _hl_r > 0:
        pygame.draw.arc(screen, ROTATE_HIGHLIGHT_COLOR,
                        pygame.Rect(ircx - _hl_r, ircy - _hl_r, 2 * _hl_r, 2 * _hl_r),
                        math.radians(45), math.radians(135), 2)

    # ── border arc where the circle exits the board ───────────────────
    _arc_r = R + b_border // 2
    arc_rect = pygame.Rect(
        ircx - _arc_r, ircy - _arc_r, 2 * _arc_r, 2 * _arc_r,
    )
    d_top = ircy - board_rect.top
    d_bot = board_rect.bottom - ircy
    d_left = ircx - board_rect.left
    d_right = board_rect.right - ircx
    min_d = min(d_top, d_bot, d_left, d_right)

    if min_d == d_top and d_top < _arc_r:
        ratio = max(-1.0, min(1.0, d_top / _arc_r))
        a = math.asin(ratio)
        a = max(0.0, a - math.radians(2))
        pygame.draw.arc(screen, BOARD_BORDER_COLOR, arc_rect,
                        a, math.pi - a, b_border)
    elif min_d == d_right and d_right < _arc_r:
        ratio = max(-1.0, min(1.0, d_right / _arc_r))
        a = math.acos(ratio)
        a = max(0.0, a - math.radians(2))
        pygame.draw.arc(screen, BOARD_BORDER_COLOR, arc_rect,
                        -a, a, b_border)
    elif min_d == d_bot and d_bot < _arc_r:
        ratio = max(-1.0, min(1.0, d_bot / _arc_r))
        a = math.asin(ratio)
        a = max(0.0, a - math.radians(2))
        pygame.draw.arc(screen, BOARD_BORDER_COLOR, arc_rect,
                        math.pi + a, 2 * math.pi - a, b_border)
    elif min_d == d_left and d_left < _arc_r:
        ratio = max(-1.0, min(1.0, d_left / _arc_r))
        a = math.acos(ratio)
        a = max(0.0, a - math.radians(2))
        pygame.draw.arc(screen, BOARD_BORDER_COLOR, arc_rect,
                        math.pi - a, math.pi + a, b_border)

    # ── board border rim ──────────────────────────────────────────────
    pygame.draw.rect(screen, BOARD_BORDER_COLOR, board_rect,
                     width=b_border, border_radius=b_corner_r)

    # ── draw balls ────────────────────────────────────────────────────
    font = _get_font(int(_ball_r * 1.1))

    for i in range(total_slots):
        sx, sy = _rounded_rect_point(
            slot_start + i / total_slots, cx, cy, hw, hh, slot_corner_r,
        )
        isx, isy = int(sx), int(sy)

        in_window = i < rotate_window
        ball_color = ROTATE_WINDOW_COLOR if in_window else SLOTS_COLOR
        shadow_color = (120, 50, 35) if in_window else SLOT_SHADOW_COLOR
        highlight_color = (255, 170, 155) if in_window else SLOT_HIGHLIGHT_COLOR

        # shadow → ball → specular highlight
        pygame.draw.circle(screen, shadow_color,
                           (isx + SLOT_SHADOW_OFFSET, isy + SLOT_SHADOW_OFFSET),
                           _ball_r)
        pygame.draw.circle(screen, ball_color, (isx, isy), _ball_r)
        pygame.draw.circle(screen, highlight_color,
                           (isx - _ball_r // 3, isy - _ball_r // 3),
                           _ball_r // 4)

        # number label
        if slots is not None:
            label = str(slots[i])
        else:
            label = str(i + 1)
        txt, _ = font.render(label, SLOT_TEXT_COLOR)
        txt_rect = txt.get_rect(center=(isx, isy))
        screen.blit(txt, txt_rect)
