import random

import pygame
import sys
import random

window_size = 600
cell_size = window_size // 3
inf = float('inf')
vec2 = pygame.math.Vector2


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

    def run_game_process(self):
        current_cell = vec2(pygame.mouse.get_pos()) // cell_size
        col, row = map(int, current_cell)
        left_click = pygame.mouse.get_pressed()[0]

        if left_click and self.map_array[row][col] == inf:
            self.map_array[row][col] = self.player
            self.player = not self.player

    def get_image(self, path, res):
        img = pygame.image.load(path)
        return pygame.transform.smoothscale(img, res)

    def draw_map(self):
        self.game.screen.blit(self.map_image, (0, 0))
        self.draw_objects()

    def draw_objects(self):
        for y, row in enumerate(self.map_array):
            for x, obj in enumerate(row):
                if obj != inf:
                    if obj:
                        self.game.screen.blit(self.X_image, vec2(x, y) * cell_size)
                    else:
                        self.game.screen.blit(self.O_image, vec2(x, y) * cell_size)

    def print_caption(self):
        pygame.display.set_caption(f'Ход игрока "{"0X"[self.player]}"')

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

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.tic_tac_toe.run()
            self.check_events()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    Game().run()
