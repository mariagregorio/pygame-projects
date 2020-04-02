import pygame
import random

pygame.init()

win_width = 192
win_height = 384
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
pygame.display.set_caption("puzzle challenge")


class Block:
    def __init__(self, block_type=None):
        self.size = 32
        self.y = 0
        if block_type is None:
            self.type = random.randint(1, 4)
        if self.type == 1:
            self.color_name = "Lila"
            self.color = (152, 120, 248)
        elif self.type == 2:
            self.color_name = "Light blue"
            self.color = (0, 232, 216)
        elif self.type == 3:
            self.color_name = "Green"
            self.color = (184, 248, 24)
        elif self.type == 4:
            self.color_name = "Yellow"
            self.color = (248, 184, 0)
        else:
            self.color_name = "Empty"
            self.color = (0, 0, 0)

    # position is going to be a tuple with (line_in_grid, block_in_line)
    def draw(self, grid_surface, grid_height, position):
        self.y = grid_height - ((position[0] + 1) * self.size)
        pygame.draw.rect(grid_surface, self.color, (position[1] * self.size, self.y, self.size, self.size))


class Grid:
    def __init__(self, blocks=None):
        if blocks is None:
            blocks = []
        self.blocks = blocks
        self.x = 0
        self.y = 0
        self.height = 384
        self.width = 192
        self.grid_surface = pygame.Surface((self.width, self.height))

    def add_block(self, block):
        self.blocks.append(block)

    def display(self):
        global window
        line_pos = 0
        block_pos = 0
        for block in self.blocks:
            block.draw(self.grid_surface, self.height, (line_pos, block_pos))
            block_pos += 1
            if block_pos == 6:
                line_pos += 1
                block_pos = 0
        window.blit(self.grid_surface, (0, 0))


run = True

blocks_list = []
for x in range(16):
    blocks_list.append(Block())

game_grid = Grid(blocks_list)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((0, 0, 0))

    game_grid.display()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
