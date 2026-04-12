import threading

import pygame

from src.algorithms.search import (
    breadth_first_search,
    depth_first_search,
    iterative_deepening_search,
    greedy_search,
)
from src.algorithms.informed import get_heuristic
from src.board import Board
from src.premade import get as get_config
from src.view.game_view import SCALE_FACTOR, draw_frame
from src.view.menu_view import MenuState, draw_menu, handle_menu_click

_HINT_ALGO = greedy_search
_HINT_HEURISTIC = "adjacency"

WIDTH: int = 1280 * SCALE_FACTOR
HEIGHT: int = 920 * SCALE_FACTOR
FPS: float = 60.0
STEP_DELAY: float = 0.5  # seconds between animated moves


def _build_board(menu: MenuState) -> Board:
    size = menu.selected_size
    if menu.selected_difficulty == "Random":
        return Board(size=size)
    slots = get_config(size, menu.selected_difficulty, menu.board_num + 1)
    if slots is not None:
        return Board(config=list(slots))
    return Board(size=size)


def _states_to_moves(path: list) -> list[str]:
    moves = []
    for i in range(len(path) - 1):
        s, ns = path[i], path[i + 1]
        if s[1:] + (s[0],) == ns:
            moves.append("left")
        elif (s[-1],) + s[:-1] == ns:
            moves.append("right")
        else:
            moves.append("rotate")
    return moves


def _solver_worker(board: Board, algo: str, heuristic_name: str, result: dict) -> None:
    initial = board.state_key()
    if algo == "BFS":
        node = breadth_first_search(initial, board.is_goal, board.get_child_states)
    elif algo == "DFS":
        node = depth_first_search(initial, board.is_goal, board.get_child_states)
    elif algo == "IDS":
        node = iterative_deepening_search(
            initial, board.is_goal, board.get_child_states
        )
    elif algo == "Greedy":
        heuristic_func = get_heuristic(heuristic_name)
        node = greedy_search(
            initial, board.is_goal, board.get_child_states, heuristic_func
        )
    else:
        node = None

    if node is None:
        result["moves"] = None
    else:
        path = []
        cur = node
        while cur:
            path.append(cur.state)
            cur = cur.parent
        path.reverse()
        result["moves"] = _states_to_moves(path)
    result["done"] = True


def _hint_worker(board: Board, result: dict) -> None:
    initial = board.state_key()
    heuristic_func = get_heuristic(_HINT_HEURISTIC)
    node = _HINT_ALGO(initial, board.is_goal, board.get_child_states, heuristic_func)
    if node is None:
        result["move"] = None
    else:
        path = []
        cur = node
        while cur:
            path.append(cur.state)
            cur = cur.parent
        path.reverse()
        moves = _states_to_moves(path)
        result["move"] = moves[0] if moves else None
    result["done"] = True


def main() -> None:
    pygame.init()
    pygame.display.set_caption("IART - Top Spin")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    state = "menu"
    menu = MenuState()
    menu_rects: dict = {}
    board: Board | None = None
    solved_banner: bool = False

    # solver state
    _solve_result: dict = {}
    _solution_moves: list[str] = []
    _solution_idx: int = 0
    _step_timer: float = 0.0

    # hint state
    _hint_move: str | None = None
    _hint_timer: float = 0.0
    _hint_computing: bool = False
    _hint_result: dict = {}
    _hint_btn_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
    HINT_DISPLAY_SECONDS: float = 3.0

    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        sw, sh = screen.get_width(), screen.get_height()
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if state in ("playing", "solving", "animating"):
                    state = "menu"
                    menu.page = 0
                    solved_banner = False
                    _solve_result = {}
                    _solution_moves = []
                    _solution_idx = 0
                    continue
                else:
                    running = False
                    break

            # ── menu events ───────────────────────────────────────────
            if state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if menu_rects:
                        started = handle_menu_click(event.pos, menu_rects, menu)
                        if started:
                            board = _build_board(menu)
                            solved_banner = False
                            if menu.selected_algo == "Human":
                                state = "playing"
                            else:
                                _solve_result = {}
                                _solution_moves = []
                                _solution_idx = 0
                                _step_timer = 0.0
                                state = "solving"
                                threading.Thread(
                                    target=_solver_worker,
                                    args=(
                                        board,
                                        menu.selected_algo,
                                        menu.selected_heuristic,
                                        _solve_result,
                                    ),
                                    daemon=True,
                                ).start()

            # ── game events (human) ───────────────────────────────────
            elif state == "playing":
                if event.type == pygame.KEYDOWN and board is not None:
                    if event.key == pygame.K_LEFT:
                        board.move_left()
                        solved_banner = False
                        _hint_move = None
                    elif event.key == pygame.K_RIGHT:
                        board.move_right()
                        solved_banner = False
                        _hint_move = None
                    elif event.key in (pygame.K_UP, pygame.K_r):
                        board.rotate()
                        solved_banner = False
                        _hint_move = None
                    elif event.key == pygame.K_h and not _hint_computing:
                        _hint_computing = True
                        _hint_move = None
                        _hint_result = {}
                        threading.Thread(
                            target=_hint_worker,
                            args=(board, _hint_result),
                            daemon=True,
                        ).start()
                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                    and _hint_btn_rect.collidepoint(event.pos)
                    and not _hint_computing
                    and board is not None
                ):
                    _hint_computing = True
                    _hint_move = None
                    _hint_result = {}
                    threading.Thread(
                        target=_hint_worker,
                        args=(board, _hint_result),
                        daemon=True,
                    ).start()

        # ── state transitions ─────────────────────────────────────────
        if (
            state == "playing"
            and board is not None
            and board.is_goal(board.state_key())
        ):
            solved_banner = True

        if _hint_computing and _hint_result.get("done"):
            _hint_move = _hint_result.get("move")
            _hint_timer = HINT_DISPLAY_SECONDS
            _hint_computing = False

        if _hint_move is not None:
            _hint_timer -= dt
            if _hint_timer <= 0:
                _hint_move = None

        if state == "solving" and _solve_result.get("done"):
            moves = _solve_result.get("moves")
            if not moves:
                state = "playing"
            else:
                _solution_moves = moves
                _solution_idx = 0
                _step_timer = 0.0
                state = "animating"

        if state == "animating" and board is not None:
            _step_timer += dt
            if _step_timer >= STEP_DELAY and _solution_idx < len(_solution_moves):
                move = _solution_moves[_solution_idx]
                if move == "left":
                    board.move_left()
                elif move == "right":
                    board.move_right()
                else:
                    board.rotate()
                _solution_idx += 1
                _step_timer = 0.0
            if _solution_idx >= len(_solution_moves):
                solved_banner = True
                state = "playing"

        # ── render ────────────────────────────────────────────────────
        if state == "menu":
            menu_rects = draw_menu(screen, (sw, sh), menu, mouse)

        elif board is not None:
            draw_frame(
                screen,
                (sw, sh),
                slots=list(board.slots),
                total_slots=len(board.slots),
                rotate_window=board.rotate_size,
            )

            hud_font = pygame.font.SysFont("Arial", 22, bold=True)
            moves_txt = hud_font.render(f"Moves: {board.moves}", True, (60, 60, 65))
            screen.blit(moves_txt, (16, 16))

            if state == "solving":
                spin_font = pygame.font.SysFont("Arial", 28, bold=True)
                spin = spin_font.render(
                    f"Solving with {menu.selected_algo}...", True, (55, 108, 192)
                )
                screen.blit(spin, spin.get_rect(centerx=sw // 2, top=sh * 3 // 4))

            if state == "animating":
                info_font = pygame.font.SysFont("Arial", 22, bold=True)
                info = info_font.render(
                    f"{menu.selected_algo}  step {_solution_idx}/{len(_solution_moves)}",
                    True,
                    (55, 108, 192),
                )
                screen.blit(info, info.get_rect(centerx=sw // 2, top=16))

            if solved_banner:
                banner_font = pygame.font.SysFont("Arial", 40, bold=True)
                banner = banner_font.render("SOLVED!", True, (60, 160, 80))
                screen.blit(banner, banner.get_rect(centerx=sw // 2, top=sh - 70))

            nav_font = pygame.font.SysFont("Arial", 15)
            nav = nav_font.render("Q: back to menu", True, (140, 140, 145))
            screen.blit(nav, (sw - nav.get_width() - 12, 16))

            if state == "playing":
                # hint button
                btn_font = pygame.font.SysFont("Arial", 18, bold=True)
                if _hint_computing:
                    btn_label = "Computing..."
                    btn_color = (120, 150, 200)
                else:
                    btn_label = "Get Hint"
                    btn_color = (55, 108, 192)  # updated after rect is computed below

                btn_surf = btn_font.render(btn_label, True, (255, 255, 255))
                _hint_btn_rect = btn_surf.get_rect(centerx=sw // 2, top=12)
                _hint_btn_rect.inflate_ip(28, 14)
                if not _hint_computing:
                    btn_color = (40, 85, 160) if _hint_btn_rect.collidepoint(mouse) else (55, 108, 192)
                pygame.draw.rect(screen, btn_color, _hint_btn_rect, border_radius=8)
                screen.blit(btn_surf, btn_surf.get_rect(center=_hint_btn_rect.center))

                # hint result
                if _hint_move is not None:
                    MOVE_LABELS = {
                        "left": "Shift Left ←",
                        "right": "Shift Right →",
                        "rotate": "Rotate ↑",
                    }
                    hint_label = MOVE_LABELS.get(_hint_move, _hint_move)
                    result_font = pygame.font.SysFont("Arial", 20, bold=True)
                    result_surf = result_font.render(f"Hint: {hint_label}", True, (55, 108, 192))
                    screen.blit(result_surf, result_surf.get_rect(centerx=sw // 2, top=_hint_btn_rect.bottom + 6))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
