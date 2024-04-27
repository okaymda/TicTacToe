import pygame
import sys
import random

vec2 = pygame.math.Vector2
window_size = 600
cell_size = window_size // 3
cell_center = vec2(cell_size / 2)
inf = float('inf')


class TicTacToe:
    def __init__(self, game):
        self.game = game
        self.map_image = self.get_image(path='image/map.png', res=[window_size] * 2)
        self.X_image = self.get_image(path='image/X.png', res=[cell_size] * 2)
        self.O_image = self.get_image(path='image/0.png', res=[cell_size] * 2)

        self.map_array = [[inf, inf, inf],
                          [inf, inf, inf],
                          [inf, inf, inf]]
        self.player = random.randint(0, 1)

        self.line_win_array = [[(0, 0), (0, 1), (0, 2)],
                               [(1, 0), (1, 1), (1, 2)],
                               [(2, 0), (2, 1), (2, 2)],
                               [(0, 0), (1, 0), (2, 0)],
                               [(0, 1), (1, 1), (2, 1)],
                               [(0, 2), (1, 2), (2, 2)],
                               [(0, 0), (1, 1), (2, 2)],
                               [(0, 2), (1, 1), (2, 0)]]

        self.winner = None
        self.steps = 0

    def check_winner(self):
        for line in self.line_win_array:
            sum_line = sum([self.map_array[i][j] for i, j in line])
            if sum_line in {0, 3}:
                self.winner = 'X0'[sum_line == 0]
                self.winner_line = [vec2(line[0][::-1]) * cell_size + cell_center,
                                    vec2(line[2][::-1]) * cell_size + cell_center, ]

    def run_game_process(self):
        current_cell = vec2(pygame.mouse.get_pos()) // cell_size
        col, row = map(int, current_cell)
        left_click = pygame.mouse.get_pressed()[0]

        if left_click and self.map_array[row][col] == inf and not self.winner:
            self.map_array[row][col] = self.player
            self.player = 1 if self.player == 0 else 0
            self.steps += 1
            self.check_winner()

    def get_image(self, path, res):
        img = pygame.image.load(path)
        return pygame.transform.smoothscale(img, res)

    def draw_map(self):
        self.game.screen.blit(self.map_image, (0, 0))
        self.draw_objects()
        self.draw_win_line()

    def draw_objects(self):
        for y, row in enumerate(self.map_array):
            for x, obj in enumerate(row):
                if obj != inf:
                    if obj:
                        self.game.screen.blit(self.X_image, vec2(x, y) * cell_size)
                    else:
                        self.game.screen.blit(self.O_image, vec2(x, y) * cell_size)

    def draw_win_line(self):
        if self.winner:
            pygame.draw.line(self.game.screen, 'blue', *self.winner_line, cell_size // 8)

    def print_caption(self):
        pygame.display.set_caption(f'Ход игрока "{"0X"[self.player]}"')
        if self.winner:
            pygame.display.set_caption(f'Победил "{self.winner}"! Нажмите "Пробел" чтобы сыграть ещё раз!')
        elif self.steps == 9:
            pygame.display.set_caption(f'Игра закончилась, ничья. Нажмите "Пробел" чтобы сыграть ещё раз!')

    def run(self):
        self.print_caption()
        self.draw_map()
        self.run_game_process()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([window_size] * 2)
        self.clock = pygame.time.Clock()
        self.tic_tac_toe = TicTacToe(self)

    def new_game(self):
        self.tic_tac_toe = TicTacToe(self)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.new_game()

    def run(self):
        while True:
            self.tic_tac_toe.run()
            self.check_events()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    Game().run()
