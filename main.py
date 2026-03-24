import threading

import pygame

from src.algorithms.search import (
    breadth_first_search,
    depth_first_search,
    iterative_deepening_search,
)
from src.board import Board
from src.premade import get as get_config
from src.view.game_view import SCALE_FACTOR, draw_frame
from src.view.menu_view import MenuState, draw_menu, handle_menu_click

WIDTH: int = 1280 * SCALE_FACTOR
HEIGHT: int = 720 * SCALE_FACTOR
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


def _solver_worker(board: Board, algo: str, result: dict) -> None:
    initial = board.state_key()
    if algo == "BFS":
        node = breadth_first_search(initial, board.is_goal, board.get_child_states)
    elif algo == "DFS":
        node = depth_first_search(initial, board.is_goal, board.get_child_states)
    else:  # IDS
        node = iterative_deepening_search(
            initial, board.is_goal, board.get_child_states
        )

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
                                    args=(board, menu.selected_algo, _solve_result),
                                    daemon=True,
                                ).start()

            # ── game events (human) ───────────────────────────────────
            elif state == "playing":
                if event.type == pygame.KEYDOWN and board is not None:
                    if event.key == pygame.K_LEFT:
                        board.move_left()
                        solved_banner = False
                    elif event.key == pygame.K_RIGHT:
                        board.move_right()
                        solved_banner = False
                    elif event.key in (pygame.K_UP, pygame.K_r):
                        board.rotate()
                        solved_banner = False

        # ── state transitions ─────────────────────────────────────────
        if state == "playing" and board is not None and board.is_solved():
            solved_banner = True

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

            hint_font = pygame.font.SysFont("Arial", 15)
            hint = hint_font.render("Q: back to menu", True, (140, 140, 145))
            screen.blit(hint, (sw - hint.get_width() - 12, 16))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
