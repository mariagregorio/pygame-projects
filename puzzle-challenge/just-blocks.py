import random

import pygame

pygame.init()

win_width = 500
win_height = 320
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
pygame.display.set_caption("puzzle challenge mf")

block_id_count = 0


class Block:
    def __init__(self, x, y, color, width=None, height=None, gravity=3):
        global block_id_count
        self.x = x
        self.y = y
        if width is None:
            self.width = 32
        else:
            self.width = width
        if height is None:
            self.height = 32
        else:
            self.height = height
        self.gravity = gravity
        self.color = color
        self.id = block_id_count
        block_id_count += 1
        self.selected = False

    def draw(self):
        global window
        global win_height

        pygame.draw.rect(window, self.color[1], (self.x, self.y, self.width, self.height))


class Grid:
    def __init__(self):
        self.blocks = []

    def generate_line(self):
        new_line = []
        colors = [(1, (152, 120, 248)), (2, (0, 232, 216)), (3, (184, 248, 24)), (4, (248, 184, 0)),
                  (5, (248, 120, 88)), (6, (0, 0, 0))]
        if len(self.blocks) < 6:
            # move all lines -32 in y
            if len(self.blocks) > 0:
                for i, i_line in enumerate(self.blocks):
                    for i_block in i_line:
                        i_block.y -= 32

            for x in range(6):
                new_line.append(Block(x * 32, win_height - 32, colors[random.randint(0, len(colors) - 2)]))
            self.blocks.append(new_line)
        else:
            print("you lose")

    def check_for_empty_block(self):
        if len(self.blocks) > 1:
            for i, i_line in enumerate(self.blocks):
                for j, i_block in enumerate(i_line):
                    if i != len(self.blocks) - 1 and self.blocks[i][j].color[0] != 6 \
                            and self.blocks[i+1][j].color[0] == 6:
                        # make the block below the current same color as current
                        self.blocks[i+1][j].color = self.blocks[i][j].color
                        # make current block empty
                        self.blocks[i][j].color = (6, (0, 0, 0))


run = True

grid = Grid()
grid.generate_line()

grid.blocks[0][0].selected = True


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                grid.generate_line()

    window.fill((20, 20, 20))

    for line in grid.blocks:
        for block in line:
            block.draw()

    for line in grid.blocks:
        for block in line:
            if block.selected:
                pygame.draw.rect(window, (0, 0, 0), (block.x - 2, block.y - 2, block.width + 4, block.height + 4), 2)

    grid.check_for_empty_block()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
