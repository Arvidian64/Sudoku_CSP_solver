import pygame

board_size = 400
padding = 40
cell_size = board_size // 9
width = (board_size * 2) + (padding * 3)
height = 800

white = (255, 255, 255)
light_grey = (220, 220, 220)
dark_grey = (50, 50, 50)
black = (0, 0, 0)
blue = (0, 0, 255)
pink = (255, 182, 0)
red = (255, 0, 0)

class sudoku_visualizer:
    def __init__(self, puzzle_pairs):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sudoku CSP Solver")
        self.font = pygame.font.SysFont("Helvetica", 18)
        self.clock = pygame.time.Clock()

        self.total_height = len(puzzle_pairs) * (board_size + padding) + padding
        self.canvas = pygame.Surface((width, self.total_height))
        self.canvas.fill(light_grey)

        self.scroll_y = 0
        self.render_all_to_canvas(puzzle_pairs)

    def draw_single_board(self, surface, x_off, y_off, domains, title):
        label = self.font.render(title, True, dark_grey)
        surface.blit(label, (x_off, y_off - 20))

        for i in range(10):
            thick = 3 if i % 3 == 0 else 1

            pygame.draw.line(surface, (0, 0, 0), (x_off, y_off + i * cell_size),
                             (x_off + board_size, y_off + i * cell_size), thick)

            pygame.draw.line(surface, (0, 0, 0), (x_off + i * cell_size, y_off),
                             (x_off + i * cell_size, y_off + board_size), thick)

        for (r, c), vals in domains.items():
            if len(vals) == 1:
                color = blue if title == "Solved" else (0, 0, 0)
                txt = self.font.render(str(vals[0]), True, color)
                # Centrerar
                rect = txt.get_rect(center=(x_off + c * cell_size + cell_size // 2, y_off + r * cell_size + cell_size // 2))
                surface.blit(txt, rect)

    def render_all_to_canvas(self, puzzle_pairs):
        for i, (original, solved) in enumerate(puzzle_pairs):
            y_pos = padding + i * (board_size + padding)
            self.draw_single_board(self.canvas, padding, y_pos, original, f"Puzzle {i + 1}: Original")
            self.draw_single_board(self.canvas, board_size + padding * 2, y_pos, solved, "Solved")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle Scrolling
                if event.type == pygame.MOUSEWHEEL:
                    self.scroll_y -= event.y * 30  # Multiplier for speed
                    # Constraints so we don't scroll into the void
                    self.scroll_y = max(0, min(self.scroll_y, self.total_height - height))

            self.screen.fill((255, 255, 255))
            # Blit the canvas with the negative offset
            self.screen.blit(self.canvas, (0, -self.scroll_y))

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()