"""Visualizacao com pygame das solucoes do problema das N-rainhas.

Solucoes obtidas a partir de QueensState (aigyminsper), definida em n_queens_aigym.py.

Controles:
  SETA DIREITA / ESPACO : proxima solucao
  SETA ESQUERDA         : solucao anterior
  N                      : proximo tamanho de tabuleiro (4, 5, 6, 7, 8)
  ESC / fechar janela    : sair
"""

import sys
from pathlib import Path

import pygame

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n_queens_aigym import solve_all

BOARD_SIZES = (4, 5, 6, 7, 8)
CELL_SIZE = 72
HEADER_HEIGHT = 92
FOOTER_HEIGHT = 56
SIDE_MARGIN = 48
BOARD_TOP_GAP = 18
BOARD_BOTTOM_GAP = 22

COLOR_WINDOW_BG = (19, 21, 27)
COLOR_HEADER_BG = (26, 29, 38)
COLOR_FOOTER_BG = (26, 29, 38)
COLOR_DIVIDER = (42, 46, 58)
COLOR_BOARD_LIGHT = (238, 233, 216)
COLOR_BOARD_DARK = (94, 122, 86)
COLOR_BOARD_BORDER = (12, 13, 17)
COLOR_QUEEN = (196, 48, 58)
COLOR_QUEEN_OUTLINE = (60, 10, 14)
COLOR_TEXT_PRIMARY = (240, 241, 245)
COLOR_TEXT_SECONDARY = (146, 151, 168)
COLOR_ACCENT = (223, 176, 74)
COLOR_DOT_OFF = (60, 64, 78)


def build_fonts():
    return {
        "title": pygame.font.SysFont("segoeui", 26, bold=True),
        "subtitle": pygame.font.SysFont("segoeui", 17),
        "hint": pygame.font.SysFont("consolas", 15),
        "hint_key": pygame.font.SysFont("consolas", 15, bold=True),
    }


def draw_header(screen, fonts, window_width, n, size_index, solution_index, total_solutions):
    header_rect = pygame.Rect(0, 0, window_width, HEADER_HEIGHT)
    pygame.draw.rect(screen, COLOR_HEADER_BG, header_rect)
    pygame.draw.line(screen, COLOR_DIVIDER, (0, HEADER_HEIGHT), (window_width, HEADER_HEIGHT), 2)

    title_surface = fonts["title"].render(f"{n} Rainhas", True, COLOR_TEXT_PRIMARY)
    screen.blit(title_surface, (SIDE_MARGIN, 16))

    subtitle_surface = fonts["subtitle"].render(
        f"Solucao {solution_index + 1} de {total_solutions}", True, COLOR_TEXT_SECONDARY
    )
    screen.blit(subtitle_surface, (SIDE_MARGIN, 50))

    # Indicador de tamanhos de tabuleiro (pontos), alinhado a direita
    dot_radius = 6
    dot_gap = 22
    total_width = dot_gap * (len(BOARD_SIZES) - 1)
    start_x = window_width - SIDE_MARGIN - total_width
    dot_y = 30
    for index, size in enumerate(BOARD_SIZES):
        center = (start_x + index * dot_gap, dot_y)
        if index == size_index:
            pygame.draw.circle(screen, COLOR_ACCENT, center, dot_radius + 2)
        else:
            pygame.draw.circle(screen, COLOR_DOT_OFF, center, dot_radius)
        label = fonts["hint"].render(str(size), True, COLOR_TEXT_SECONDARY)
        screen.blit(label, (center[0] - label.get_width() // 2, dot_y + 12))


def draw_footer(screen, fonts, window_width, window_height):
    footer_rect = pygame.Rect(0, window_height - FOOTER_HEIGHT, window_width, FOOTER_HEIGHT)
    pygame.draw.rect(screen, COLOR_FOOTER_BG, footer_rect)
    pygame.draw.line(
        screen, COLOR_DIVIDER, (0, footer_rect.top), (window_width, footer_rect.top), 2
    )

    controls = [("<- ->/ESPACO", "soluções"), ("N", "tabuleiro"), ("ESC", "sair")]
    x = SIDE_MARGIN
    y = footer_rect.top + (FOOTER_HEIGHT - fonts["hint"].get_height()) // 2
    for key_label, description in controls:
        key_surface = fonts["hint_key"].render(key_label, True, COLOR_ACCENT)
        screen.blit(key_surface, (x, y))
        x += key_surface.get_width() + 6
        desc_surface = fonts["hint"].render(description, True, COLOR_TEXT_SECONDARY)
        screen.blit(desc_surface, (x, y))
        x += desc_surface.get_width() + 28


def draw_board(screen, fonts, n, solution, size_index, solution_index, total_solutions, window_width, window_height):
    screen.fill(COLOR_WINDOW_BG)

    board_pixels = n * CELL_SIZE
    origin_x = (window_width - board_pixels) // 2
    origin_y = HEADER_HEIGHT + BOARD_TOP_GAP

    border_rect = pygame.Rect(origin_x - 4, origin_y - 4, board_pixels + 8, board_pixels + 8)
    pygame.draw.rect(screen, COLOR_BOARD_BORDER, border_rect, border_radius=6)

    for row in range(n):
        for col in range(n):
            color = COLOR_BOARD_LIGHT if (row + col) % 2 == 0 else COLOR_BOARD_DARK
            rect = pygame.Rect(origin_x + col * CELL_SIZE, origin_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)

    queen_radius = int(CELL_SIZE * 0.32)
    for row, col in enumerate(solution):
        center = (origin_x + col * CELL_SIZE + CELL_SIZE // 2, origin_y + row * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(screen, COLOR_QUEEN, center, queen_radius)
        pygame.draw.circle(screen, COLOR_QUEEN_OUTLINE, center, queen_radius, 2)

    draw_header(screen, fonts, window_width, n, size_index, solution_index, total_solutions)
    draw_footer(screen, fonts, window_width, window_height)


def main():
    pygame.init()
    pygame.display.set_caption("N-Rainhas - Visualizacao (aigyminsper)")

    max_n = max(BOARD_SIZES)
    board_pixels = max_n * CELL_SIZE
    window_width = board_pixels + 2 * SIDE_MARGIN
    window_height = HEADER_HEIGHT + BOARD_TOP_GAP + board_pixels + BOARD_BOTTOM_GAP + FOOTER_HEIGHT
    screen = pygame.display.set_mode((window_width, window_height))
    fonts = build_fonts()
    clock = pygame.time.Clock()

    solutions_cache = {n: solve_all(n) for n in BOARD_SIZES}

    size_index = 0
    solution_index = 0

    running = True
    while running:
        n = BOARD_SIZES[size_index]
        solutions = solutions_cache[n]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_RIGHT, pygame.K_SPACE):
                    solution_index = (solution_index + 1) % len(solutions)
                elif event.key == pygame.K_LEFT:
                    solution_index = (solution_index - 1) % len(solutions)
                elif event.key == pygame.K_n:
                    size_index = (size_index + 1) % len(BOARD_SIZES)
                    solution_index = 0

        draw_board(
            screen,
            fonts,
            n,
            solutions[solution_index],
            size_index,
            solution_index,
            len(solutions),
            window_width,
            window_height,
        )
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
