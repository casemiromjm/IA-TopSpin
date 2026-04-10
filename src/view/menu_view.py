"""Menu screen for Top Spin"""

from __future__ import annotations

import pygame
import pygame.freetype

from src.premade import count
from src.algorithms.informed import HEURISTIC_NAMES

SIZES = [10, 20]
DIFFICULTIES = ["Random", "Easy", "Medium", "Hard"]
UNINFORMED_ALGOS = ["BFS", "DFS", "IDS"]
INFORMED_ALGOS = ["Greedy", "AStar"]
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


def _button_row(screen, cx, y, labels, selected, mouse, btn_w=BTN_W):
    n = len(labels)
    total = n * btn_w + (n - 1) * BTN_GAP
    x0 = cx - total // 2
    rects = []
    for i, lbl in enumerate(labels):
        r = pygame.Rect(x0 + i * (btn_w + BTN_GAP), y, btn_w, BTN_H)
        rects.append(r)
        sel = i == selected
        hov = r.collidepoint(mouse) and not sel
        bg = BTN_SEL_COLOR if sel else (BTN_HOVER_COLOR if hov else BTN_COLOR)
        fg = BTN_TEXT_SEL if sel else BTN_TEXT_COLOR
        pygame.draw.rect(screen, bg, r, border_radius=BTN_RADIUS)
        txt, _ = _font("Arial", 17, bold=sel).render(lbl, fg)
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
    base_y = sh // 3 - 36

    # size row
    _s, _ = lbl_font.render("Size", LABEL_COLOR)
    screen.blit(_s, _s.get_rect(centerx=cx, top=base_y - 28))
    size_rects = _button_row(
        screen, cx, base_y, [str(s) for s in SIZES], state.size, mouse
    )

    # difficulty row
    _d, _ = lbl_font.render("Difficulty", LABEL_COLOR)
    screen.blit(_d, _d.get_rect(centerx=cx, top=base_y + ROW_GAP - 28))
    diff_rects = _button_row(
        screen, cx, base_y + ROW_GAP, DIFFICULTIES, state.difficulty, mouse
    )

    # search type row
    _st, _ = lbl_font.render("Search Type", LABEL_COLOR)
    screen.blit(_st, _st.get_rect(centerx=cx, top=base_y + ROW_GAP * 2 - 28))
    search_type_rects = _button_row(
        screen,
        cx,
        base_y + ROW_GAP * 2,
        ["Human", "Uninformed", "Informed"],
        state.search_type,
        mouse,
    )

    # algorithm row (changes based on search type)
    algo_rects = []
    y_algo = base_y + ROW_GAP * 3
    if state.search_type == 1:  # Uninformed
        _a, _ = lbl_font.render("Algorithm", LABEL_COLOR)
        screen.blit(_a, _a.get_rect(centerx=cx, top=y_algo - 28))
        algo_rects = _button_row(
            screen, cx, y_algo, UNINFORMED_ALGOS, state.uninformed_algo, mouse
        )
    elif state.search_type == 2:  # Informed
        _a, _ = lbl_font.render("Algorithm", LABEL_COLOR)
        screen.blit(_a, _a.get_rect(centerx=cx, top=y_algo - 28))
        algo_rects = _button_row(
            screen, cx, y_algo, INFORMED_ALGOS, state.informed_algo, mouse
        )

    # heuristic row (only for informed search)
    heuristic_rects = []
    y_heur = base_y + ROW_GAP * 4
    if state.search_type == 2:  # Informed
        _h, _ = lbl_font.render("Heuristic", LABEL_COLOR)
        screen.blit(_h, _h.get_rect(centerx=cx, top=y_heur - 28))
        heuristic_rects = _button_row(
            screen, cx, y_heur, HEURISTICS, state.heuristic, mouse
        )

    # board number sub-row — only when a difficulty (not Random) is selected
    board_rects = []
    y_board = base_y + ROW_GAP * 5
    if state.difficulty != 0:
        n = state.num_boards
        labels = [f"#{i}" for i in range(1, n + 1)]
        _b, _ = lbl_font.render("Board", LABEL_COLOR)
        screen.blit(_b, _b.get_rect(centerx=cx, top=y_board - 28))
        board_rects = _button_row(
            screen, cx, y_board, labels, state.board_num, mouse, btn_w=70
        )
        y_board += ROW_GAP

    # start button
    start_r = pygame.Rect(cx - START_W // 2, y_board + 10, START_W, START_H)
    pygame.draw.rect(
        screen,
        START_HOVER if start_r.collidepoint(mouse) else START_COLOR,
        start_r,
        border_radius=14,
    )
    stxt, _ = _font("Arial", 26, bold=True).render("START", START_TEXT)
    screen.blit(stxt, stxt.get_rect(center=start_r.center))

    # hint
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
            if state.search_type == 1:  # Uninformed
                state.uninformed_algo = i
            elif state.search_type == 2:  # Informed
                state.informed_algo = i
            return False
    for i, r in enumerate(rects.get("heuristic", [])):
        if r.collidepoint(pos):
            state.heuristic = i
            return False
    for i, r in enumerate(rects.get("board", [])):
        if r.collidepoint(pos):
            state.board_num = i
            return False
    if isinstance(rects["start"], pygame.Rect) and rects["start"].collidepoint(pos):
        return True
    return False
