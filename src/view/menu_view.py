"""Menu screen for Top Spin"""

from __future__ import annotations

import pygame
import pygame.freetype

from src.premade import count
from src.algorithms.informed import HEURISTIC_NAMES

SIZES = [10, 20]
DIFFICULTIES = ["Random", "Easy", "Medium", "Hard"]
UNINFORMED_ALGOS = ["BFS", "DFS", "IDS"]
INFORMED_ALGOS = ["Greedy", "A*", "Weighted A*"]
INFORMED_ALGOS_SOON = ["Pattern DB"]
HEURISTICS = ["Adjacency", "Min Misplaced"]
WEIGHTS = [1, 2, 3, 5]

BG_COLOR = "antiquewhite1"
TITLE_COLOR = (45, 95, 180)
SUBTITLE_COLOR = (100, 100, 110)
LABEL_COLOR = (60, 60, 65)
BTN_COLOR = (210, 215, 220)
BTN_HOVER_COLOR = (180, 195, 220)
BTN_SEL_COLOR = (55, 108, 192)
BTN_TEXT_COLOR = (50, 50, 55)
BTN_TEXT_SEL = (255, 255, 255)
START_COLOR = (60, 160, 80)
START_HOVER = (50, 190, 75)
START_TEXT = (255, 255, 255)
SOON_COLOR = (210, 175, 50)
SOON_TEXT_COLOR = (90, 70, 10)

BTN_W = 110
BTN_H = 42
BTN_GAP = 40
BTN_RADIUS = 10
START_W = 200
START_H = 52
ROW_GAP = 90

_fonts: dict = {}


def _font(name: str, size: int, bold: bool = False) -> pygame.freetype.Font:
    if not pygame.freetype.get_init():
        pygame.freetype.init()
    key = f"{name}:{size}:{bold}"
    if key not in _fonts:
        _fonts[key] = pygame.freetype.SysFont(name, size, bold=bold)
    return _fonts[key]


class MenuState:
    def __init__(self):
        self.size: int = 1  # index into SIZES (default: 20)
        self.difficulty: int = 0  # index into DIFFICULTIES
        self.board_num: int = 0  # 0-based within difficulty

        # Search configuration
        self.search_type: int = 0  # 0=Human, 1=Uninformed, 2=Informed
        self.uninformed_algo: int = 0  # index into UNINFORMED_ALGOS
        self.informed_algo: int = 0  # index into INFORMED_ALGOS
        self.heuristic: int = 0  # index into HEURISTICS (default: Adjacency)
        self.weight: int = 1  # index into WEIGHTS (default: 2)

    @property
    def selected_size(self) -> int:
        return SIZES[self.size]

    @property
    def selected_difficulty(self) -> str:
        return DIFFICULTIES[self.difficulty]

    @property
    def selected_algo(self) -> str:
        if self.search_type == 0:
            return "Human"
        elif self.search_type == 1:
            return UNINFORMED_ALGOS[self.uninformed_algo]
        else:
            return INFORMED_ALGOS[self.informed_algo]

    @property
    def selected_heuristic(self) -> str:
        """Returns lowercase name for use with get_heuristic()."""
        return HEURISTIC_NAMES[self.heuristic]

    @property
    def selected_weight(self) -> int:
        return WEIGHTS[self.weight]

    @property
    def num_boards(self) -> int:
        if self.difficulty == 0:
            return 0
        return count(self.selected_size, self.selected_difficulty)


def _button_row(screen, cx, y, labels, selected, mouse, btn_w=BTN_W, disabled=None):
    """Draw a horizontal row of buttons.

    disabled: set of indices rendered in yellow — visually distinct, not selectable.
    """
    if disabled is None:
        disabled = set()
    n = len(labels)
    total = n * btn_w + (n - 1) * BTN_GAP
    x0 = cx - total // 2
    rects = []
    for i, lbl in enumerate(labels):
        r = pygame.Rect(x0 + i * (btn_w + BTN_GAP), y, btn_w, BTN_H)
        rects.append(r)
        if i in disabled:
            bg = SOON_COLOR
            fg = SOON_TEXT_COLOR
        else:
            sel = i == selected
            hov = r.collidepoint(mouse) and not sel
            bg = BTN_SEL_COLOR if sel else (BTN_HOVER_COLOR if hov else BTN_COLOR)
            fg = BTN_TEXT_SEL if sel else BTN_TEXT_COLOR
        pygame.draw.rect(screen, bg, r, border_radius=BTN_RADIUS)
        txt, _ = _font("Arial", 15, bold=(i not in disabled and i == selected)).render(
            lbl, fg
        )
        screen.blit(txt, txt.get_rect(center=r.center))
    return rects


def draw_menu(screen, screen_size, state: MenuState, mouse):
    sw, sh = screen_size
    cx = sw // 2
    screen.fill(BG_COLOR)

    # title
    title, _ = _font("Arial", 54, bold=True).render("TOP SPIN", TITLE_COLOR)
    screen.blit(title, title.get_rect(centerx=cx, top=sh // 8))
    sub, _ = _font("Arial", 20).render("A Puzzle Game", SUBTITLE_COLOR)
    screen.blit(sub, sub.get_rect(centerx=cx, top=sh // 8 + 64))

    lbl_font = _font("Arial", 20, bold=True)

    # count visible rows so the gap scales to always fit the start button
    is_weighted = (
        state.search_type == 2 and INFORMED_ALGOS[state.informed_algo] == "Weighted A*"
    )
    num_rows = 3  # size, difficulty, search-type always shown
    if state.search_type != 0:
        num_rows += 1  # algorithm row
    if state.search_type == 2:
        num_rows += 1  # heuristic row
    if is_weighted:
        num_rows += 1  # weight row
    if state.difficulty != 0:
        num_rows += 1  # board row

    y_start = sh // 3 - 36
    available = sh - y_start - 120
    row_gap = max(68, min(ROW_GAP, available // num_rows))
    y = y_start

    # size
    _s, _ = lbl_font.render("Size", LABEL_COLOR)
    screen.blit(_s, _s.get_rect(centerx=cx, top=y - 28))
    size_rects = _button_row(screen, cx, y, [str(s) for s in SIZES], state.size, mouse)
    y += row_gap

    # difficulty
    _d, _ = lbl_font.render("Difficulty", LABEL_COLOR)
    screen.blit(_d, _d.get_rect(centerx=cx, top=y - 28))
    diff_rects = _button_row(screen, cx, y, DIFFICULTIES, state.difficulty, mouse)
    y += row_gap

    # search type
    _st, _ = lbl_font.render("Search Type", LABEL_COLOR)
    screen.blit(_st, _st.get_rect(centerx=cx, top=y - 28))
    search_type_rects = _button_row(
        screen, cx, y, ["Human", "Uninformed", "Informed"], state.search_type, mouse
    )
    y += row_gap

    # algorithm row
    algo_rects = []
    if state.search_type == 1:
        _a, _ = lbl_font.render("Algorithm", LABEL_COLOR)
        screen.blit(_a, _a.get_rect(centerx=cx, top=y - 28))
        algo_rects = _button_row(
            screen, cx, y, UNINFORMED_ALGOS, state.uninformed_algo, mouse
        )
        y += row_gap
    elif state.search_type == 2:
        _a, _ = lbl_font.render("Algorithm", LABEL_COLOR)
        screen.blit(_a, _a.get_rect(centerx=cx, top=y - 28))
        all_informed = INFORMED_ALGOS + INFORMED_ALGOS_SOON
        soon_idx = set(range(len(INFORMED_ALGOS), len(all_informed)))
        algo_rects = _button_row(
            screen,
            cx,
            y,
            all_informed,
            state.informed_algo,
            mouse,
            btn_w=115,
            disabled=soon_idx,
        )
        y += row_gap

    # heuristic — only for Informed
    heuristic_rects = []
    if state.search_type == 2:
        _h, _ = lbl_font.render("Heuristic", LABEL_COLOR)
        screen.blit(_h, _h.get_rect(centerx=cx, top=y - 28))
        heuristic_rects = _button_row(screen, cx, y, HEURISTICS, state.heuristic, mouse)
        y += row_gap

    # weight — only when Weighted A* is selected
    weight_rects = []
    if is_weighted:
        _w, _ = lbl_font.render("Weight", LABEL_COLOR)
        screen.blit(_w, _w.get_rect(centerx=cx, top=y - 28))
        weight_rects = _button_row(
            screen, cx, y, [str(w) for w in WEIGHTS], state.weight, mouse, btn_w=70
        )
        y += row_gap

    # board — only when non-Random difficulty
    board_rects = []
    if state.difficulty != 0:
        n = state.num_boards
        labels = [f"#{i}" for i in range(1, n + 1)]
        _b, _ = lbl_font.render("Board", LABEL_COLOR)
        screen.blit(_b, _b.get_rect(centerx=cx, top=y - 28))
        board_rects = _button_row(
            screen, cx, y, labels, state.board_num, mouse, btn_w=70
        )
        y += row_gap

    # start button
    start_r = pygame.Rect(cx - START_W // 2, y + 10, START_W, START_H)
    pygame.draw.rect(
        screen,
        START_HOVER if start_r.collidepoint(mouse) else START_COLOR,
        start_r,
        border_radius=14,
    )
    stxt, _ = _font("Arial", 26, bold=True).render("START", START_TEXT)
    screen.blit(stxt, stxt.get_rect(center=start_r.center))

    hint, _ = _font("Arial", 15).render(
        "← → shift    ↑ / R rotate    Q quit", SUBTITLE_COLOR
    )
    screen.blit(hint, hint.get_rect(centerx=cx, top=start_r.bottom + 24))

    return {
        "size": size_rects,
        "diff": diff_rects,
        "search_type": search_type_rects,
        "algo": algo_rects,
        "heuristic": heuristic_rects,
        "weight": weight_rects,
        "board": board_rects,
        "start": start_r,
    }


def handle_menu_click(pos, rects, state: MenuState) -> bool:
    for i, r in enumerate(rects.get("size", [])):
        if r.collidepoint(pos):
            if state.size != i:
                state.size = i
                state.difficulty = 0
                state.board_num = 0
            return False
    for i, r in enumerate(rects.get("diff", [])):
        if r.collidepoint(pos):
            if state.difficulty != i:
                state.difficulty = i
                state.board_num = 0
            return False
    for i, r in enumerate(rects.get("search_type", [])):
        if r.collidepoint(pos):
            state.search_type = i
            return False
    for i, r in enumerate(rects.get("algo", [])):
        if r.collidepoint(pos):
            if state.search_type == 1:
                state.uninformed_algo = i
            elif state.search_type == 2 and i < len(INFORMED_ALGOS):
                state.informed_algo = i
            return False
    for i, r in enumerate(rects.get("heuristic", [])):
        if r.collidepoint(pos):
            state.heuristic = i
            return False
    for i, r in enumerate(rects.get("weight", [])):
        if r.collidepoint(pos):
            state.weight = i
            return False
    for i, r in enumerate(rects.get("board", [])):
        if r.collidepoint(pos):
            state.board_num = i
            return False
    if isinstance(rects["start"], pygame.Rect) and rects["start"].collidepoint(pos):
        return True
    return False
