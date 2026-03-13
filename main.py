"""
import pygame

from src.view.game_view import SCALE_FACTOR, draw_frame

WIDTH: int = 1280 * SCALE_FACTOR
HEIGHT: int = 720 * SCALE_FACTOR
FPS: float = 60.0
"""

from src.algorithms.search import breadth_first_search, print_solution
from src.board import Board


def main() -> None:
    """
    # pygame setup
    pygame.init()
    pygame.display.set_caption("IART - Top Spin")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True

    while running:
        # event polling
        for event in pygame.event.get():
            # press on screen X or pressing 'q'
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_q
            ):
                running = False

        screenWidth: int = screen.get_width()
        screenHeight: int = screen.get_height()

        # rendering
        draw_frame(screen, (screenWidth, screenHeight))

        pygame.display.flip()

        # set FPS
        clock.tick(FPS)

    pygame.quit()
    """

    board = Board(size=6, spin_size=3, initial_state=(3, 2, 1, 4, 5, 6))

    print(f"Starting search from: {board.initial_state}")

    goal_node = breadth_first_search(
        board.initial_state,
        board.is_goal,
        board.get_child_states,
    )

    if goal_node:
        print_solution(goal_node)


if __name__ == "__main__":
    main()
