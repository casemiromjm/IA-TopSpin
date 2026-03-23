import pygame

from src.board import Board
from src.premade import get as get_config
from src.view.game_view import SCALE_FACTOR, draw_frame
from src.view.menu_view import MenuState, draw_menu, handle_menu_click

WIDTH: int = 1280 * SCALE_FACTOR
HEIGHT: int = 720 * SCALE_FACTOR
FPS: float = 60.0


def _build_board(menu: MenuState) -> Board:
    """Create a Board from menu selections."""
    size = menu.selected_size
    if menu.selected_difficulty == "Random":
        return Board(size=size)
    slots = get_config(size, menu.selected_difficulty, menu.board_num + 1)
    if slots is not None:
        return Board(config=list(slots))
    return Board(size=size)

def main() -> None:

    # pygame setup
    pygame.init()
    pygame.display.set_caption("IART - Top Spin")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    state = "menu"
    menu = MenuState()
    menu_rects: dict = {}

    board: Board | None = None
    solved_banner: bool = False

    running = True

    while running:
        # event polling
        clock.tick(FPS)
        sw, sh = screen.get_width(), screen.get_height()
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # press on screen X or pressing 'q'
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                if state == "playing":
                    state = "menu"
                    solved_banner = False
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

                            state = "playing"

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

        # ── check win ─────────────────────────────────────────────────
        if state == "playing" and board is not None and board.is_solved():
            solved_banner = True

        # ── render ────────────────────────────────────────────────────
        if state == "menu":
            menu_rects = draw_menu(screen, (sw, sh), menu, mouse)
        elif state == "playing" and board is not None:
            draw_frame(
                screen, (sw, sh),
                slots=list(board.slots),
                total_slots=len(board.slots),
                rotate_window=board.rotate_size,
            )
            # HUD: move counter + status
            hud_font = pygame.font.SysFont("Arial", 22, bold=True)
            moves_txt = hud_font.render(f"Moves: {board.moves}", True, (60, 60, 65))
            screen.blit(moves_txt, (16, 16))

            if solved_banner:
                banner_font = pygame.font.SysFont("Arial", 40, bold=True)
                banner = banner_font.render("SOLVED!", True, (60, 160, 80))
                screen.blit(banner, banner.get_rect(centerx=sw // 2, top=sh - 70))

            # back hint
            hint_font = pygame.font.SysFont("Arial", 15)
            hint = hint_font.render("Q: back to menu", True, (140, 140, 145))
            screen.blit(hint, (sw - hint.get_width() - 12, 16))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
