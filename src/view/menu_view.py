"""Menu screen for Top Spin — two-page layout"""

from __future__ import annotations

import pygame
import pygame.freetype

from src.premade import count
from src.algorithms.informed import HEURISTIC_NAMES

SIZES = [10, 20]
DIFFICULTIES = ["Random", "Easy", "Medium", "Hard"]
UNINFORMED_ALGOS = ["BFS", "DFS", "IDS"]
INFORMED_ALGOS = ["Greedy", "A*"]
INFORMED_ALGOS_SOON = ["Weighted A*", "Pattern DB"]   # displayed but not yet usable
HEURISTICS = ["Adjacency", "Min Misplaced"]

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
BACK_COLOR = (160, 165, 170)
BACK_HOVER_COLOR = (130, 140, 150)
NEXT_COLOR = (55, 108, 192)
NEXT_HOVER_COLOR = (40, 85, 160)
SOON_COLOR = (210, 175, 50)       # golden yellow — coming-soon buttons
SOON_TEXT_COLOR = (90, 70, 10)    # dark brown text on yellow

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
        self.page: int = 0  # 0 = puzzle setup, 1 = algorithm config

        # Search configuration
        self.search_type: int = 0  # 0=Human, 1=Uninformed, 2=Informed
        self.uninformed_algo: int = 0  # index into UNINFORMED_ALGOS
        self.informed_algo: int = 0  # index into INFORMED_ALGOS
        self.heuristic: int = 0  # index into HEURISTICS (default: Adjacency)

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
    def num_boards(self) -> int:
        if self.difficulty == 0:
            return 0
        return count(self.selected_size, self.selected_difficulty)


def _button_row(screen, cx, y, labels, selected, mouse, btn_w=BTN_W, disabled=None):
    """Draw a horizontal row of buttons.

    disabled: set of indices that should appear as yellow/coming-soon and be unclickable.
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
        txt, _ = _font("Arial", 15, bold=(i not in disabled and i == selected)).render(lbl, fg)
        screen.blit(txt, txt.get_rect(center=r.center))
    return rects


def _action_button(screen, cx, y, label, base_color, hover_color, mouse, w=START_W, h=START_H):
    r = pygame.Rect(cx - w // 2, y, w, h)
    color = hover_color if r.collidepoint(mouse) else base_color
    pygame.draw.rect(screen, color, r, border_radius=14)
    txt, _ = _font("Arial", 22, bold=True).render(label, START_TEXT)
    screen.blit(txt, txt.get_rect(center=r.center))
    return r


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

    # ── PAGE 0: puzzle setup ──────────────────────────────────────────────
    if state.page == 0:
        # count rows for this page
        num_rows = 3  # size, difficulty, solver-type
        if state.difficulty != 0:
            num_rows += 1  # board row

        y_start = sh // 3 - 36
        available = sh - y_start - 120
        row_gap = max(70, min(ROW_GAP, available // num_rows))
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

        # board — only when non-Random
        board_rects = []
        if state.difficulty != 0:
            n = state.num_boards
            labels = [f"#{i}" for i in range(1, n + 1)]
            _b, _ = lbl_font.render("Board", LABEL_COLOR)
            screen.blit(_b, _b.get_rect(centerx=cx, top=y - 28))
            board_rects = _button_row(screen, cx, y, labels, state.board_num, mouse, btn_w=70)
            y += row_gap

        # solver type: Human or Algorithm
        _sv, _ = lbl_font.render("Solver", LABEL_COLOR)
        screen.blit(_sv, _sv.get_rect(centerx=cx, top=y - 28))
        solver_sel = 0 if state.search_type == 0 else 1
        solver_rects = _button_row(screen, cx, y, ["Human", "Algorithm"], solver_sel, mouse)
        y += row_gap

        # action button: START (Human) or NEXT → (Algorithm)
        if state.search_type == 0:
            start_r = _action_button(
                screen, cx, y + 10, "START", START_COLOR, START_HOVER, mouse
            )
            next_r = None
        else:
            start_r = None
            next_r = _action_button(
                screen, cx, y + 10, "Next  →", NEXT_COLOR, NEXT_HOVER_COLOR, mouse, w=START_W
            )

        # hint
        hint, _ = _font("Arial", 15).render(
            "← → shift    ↑ / R rotate    Q quit", SUBTITLE_COLOR
        )
        btn_bottom = (start_r or next_r).bottom
        screen.blit(hint, hint.get_rect(centerx=cx, top=btn_bottom + 24))

        return {
            "page": 0,
            "size": size_rects,
            "diff": diff_rects,
            "board": board_rects,
            "solver": solver_rects,
            "start": start_r,
            "next": next_r,
        }

    # ── PAGE 1: algorithm config ──────────────────────────────────────────
    # back chevron at top-left
    back_r = pygame.Rect(20, 20, 110, 40)
    back_color = BACK_HOVER_COLOR if back_r.collidepoint(mouse) else BACK_COLOR
    pygame.draw.rect(screen, back_color, back_r, border_radius=10)
    back_txt, _ = _font("Arial", 16, bold=True).render("← Back", (255, 255, 255))
    screen.blit(back_txt, back_txt.get_rect(center=back_r.center))

    # count rows for this page
    num_rows = 2  # algo-type + algorithm
    if state.search_type == 2:
        num_rows += 1  # heuristic

    y_start = sh // 3 - 36
    available = sh - y_start - 120
    row_gap = max(70, min(ROW_GAP, available // num_rows))
    y = y_start

    # algo type: Uninformed / Informed
    _at, _ = lbl_font.render("Algorithm Type", LABEL_COLOR)
    screen.blit(_at, _at.get_rect(centerx=cx, top=y - 28))
    algo_type_sel = state.search_type - 1  # 1→0, 2→1
    algo_type_rects = _button_row(
        screen, cx, y, ["Uninformed", "Informed"], algo_type_sel, mouse, btn_w=BTN_W
    )
    y += row_gap

    # specific algorithm — coming-soon entries shown in yellow
    _a, _ = lbl_font.render("Algorithm", LABEL_COLOR)
    screen.blit(_a, _a.get_rect(centerx=cx, top=y - 28))
    if state.search_type == 1:
        algo_rects = _button_row(screen, cx, y, UNINFORMED_ALGOS, state.uninformed_algo, mouse)
    else:
        all_informed = INFORMED_ALGOS + INFORMED_ALGOS_SOON
        soon_indices = set(range(len(INFORMED_ALGOS), len(all_informed)))
        algo_rects = _button_row(
            screen, cx, y, all_informed, state.informed_algo, mouse,
            btn_w=120, disabled=soon_indices,
        )
    y += row_gap

    # heuristic — only for Informed
    heuristic_rects = []
    if state.search_type == 2:
        _h, _ = lbl_font.render("Heuristic", LABEL_COLOR)
        screen.blit(_h, _h.get_rect(centerx=cx, top=y - 28))
        heuristic_rects = _button_row(screen, cx, y, HEURISTICS, state.heuristic, mouse)
        y += row_gap

    # start button
    start_r = _action_button(screen, cx, y + 10, "START", START_COLOR, START_HOVER, mouse)

    return {
        "page": 1,
        "back": back_r,
        "algo_type": algo_type_rects,
        "algo": algo_rects,
        "heuristic": heuristic_rects,
        "start": start_r,
        "next": None,
    }


def handle_menu_click(pos, rects, state: MenuState) -> bool:
    """Returns True when the game should start."""
    page = rects.get("page", 0)

    if page == 0:
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
        for i, r in enumerate(rects.get("board", [])):
            if r.collidepoint(pos):
                state.board_num = i
                return False
        for i, r in enumerate(rects.get("solver", [])):
            if r.collidepoint(pos):
                if i == 0:
                    state.search_type = 0  # Human
                else:
                    # default to Uninformed when switching to Algorithm
                    if state.search_type == 0:
                        state.search_type = 1
                return False
        # START (Human mode)
        if rects.get("start") and rects["start"].collidepoint(pos):
            return True
        # NEXT (Algorithm mode) — go to page 1
        if rects.get("next") and rects["next"].collidepoint(pos):
            state.page = 1
            return False

    else:  # page == 1
        # BACK
        if rects.get("back") and rects["back"].collidepoint(pos):
            state.page = 0
            return False
        # algo type toggle
        for i, r in enumerate(rects.get("algo_type", [])):
            if r.collidepoint(pos):
                state.search_type = i + 1  # 0→Uninformed(1), 1→Informed(2)
                return False
        # specific algorithm — ignore clicks on coming-soon (disabled) entries
        for i, r in enumerate(rects.get("algo", [])):
            if r.collidepoint(pos):
                if state.search_type == 1:
                    state.uninformed_algo = i
                else:
                    if i < len(INFORMED_ALGOS):  # only active ones
                        state.informed_algo = i
                return False
        # heuristic
        for i, r in enumerate(rects.get("heuristic", [])):
            if r.collidepoint(pos):
                state.heuristic = i
                return False
        # START
        if rects.get("start") and rects["start"].collidepoint(pos):
            return True

    return False
