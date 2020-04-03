import random

import pygame

pygame.init()

win_width = 500
win_height = 500
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
        self.focused = False

    def draw(self, grid_surface):
        pygame.draw.rect(grid_surface, self.color[1], (self.x, self.y, self.width, self.height))


class Grid:
    def __init__(self):
        self.blocks = []
        self.x = 0
        self.y = 0
        self.height = 384
        self.width = 192
        self.grid_surface = pygame.Surface((self.width, self.height))

    def display(self):
        global window
        window.blit(self.grid_surface, ((win_width // 2) - (self.width // 2), (win_height // 2) - (self.height // 2)))

    def generate_line(self):
        new_line = []
        colors = [(1, (152, 120, 248)), (2, (0, 232, 216)), (3, (184, 248, 24)), (4, (248, 184, 0)),
                  (5, (248, 120, 88)), (6, (0, 0, 0))]
        if len(self.blocks) < 12:
            # move all lines -32 in y
            if len(self.blocks) > 0:
                for i, i_line in enumerate(self.blocks):
                    for i_block in i_line:
                        i_block.y -= 32

            for x in range(6):
                new_line.append(Block(x * 32, self.height - 32, colors[random.randint(0, len(colors) - 2)]))
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

    def check_for_matching_blocks(self):
        for i, i_line in enumerate(self.blocks):
            for j, i_block in enumerate(i_line):
                # check left to right matching blocks
                try:
                    if self.blocks[i][j + 1].color == i_block.color and self.blocks[i][j + 2].color == i_block.color:
                        try:
                            if self.blocks[i][j + 3].color == i_block.color:
                                try:
                                    if self.blocks[i][j + 4].color == i_block.color:
                                        try:
                                            if self.blocks[i][j + 5].color == i_block.color:
                                                print("we have 6 horizontal at line {} block {}".format(i, j))
                                                continue
                                        except IndexError:
                                            pass
                                        print("we have 5 horizontal at line {} block {}".format(i, j))
                                        continue
                                except IndexError:
                                    pass
                                print("we have 4 horizontal at line {} block {}".format(i, j))
                                continue
                            else:
                                pass
                        except IndexError:
                            pass
                        print("we have 3 horizontal at line {} block {}".format(i, j))
                except IndexError:
                    continue


run = True

grid = Grid()

grid.generate_line()

grid.blocks[0][0].focused = True


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                grid.generate_line()
            if event.key == pygame.K_RIGHT:
                for i, line in enumerate(grid.blocks):
                    for j, block in enumerate(line):
                        if block.focused and j != 5:
                            block.focused = False
                            grid.blocks[i][j + 1].focused = True
                            break
            if event.key == pygame.K_LEFT:
                for i, line in enumerate(grid.blocks):
                    for j, block in enumerate(line):
                        if block.focused and j != 0:
                            block.focused = False
                            grid.blocks[i][j - 1].focused = True
                            break
            if event.key == pygame.K_DOWN:
                # i don't understand why i had to do this found thing to get out of the loop, while the others worked
                # just fine...
                found = False
                for i, line in enumerate(grid.blocks):
                    if not found:
                        for j, block in enumerate(line):
                            if block.focused and i != len(grid.blocks) - 1:
                                block.focused = False
                                grid.blocks[i + 1][j].focused = True
                                found = True
                                break
            if event.key == pygame.K_UP:
                for i, line in enumerate(grid.blocks):
                    for j, block in enumerate(line):
                        if block.focused and i != 0:
                            block.focused = False
                            grid.blocks[i - 1][j].focused = True
                            break

    window.fill((20, 20, 20))
    grid.display()
    grid.grid_surface.fill((20, 20, 20))

    for line in grid.blocks:
        for block in line:
            block.draw(grid.grid_surface)
            if block.focused:
                pygame.draw.rect(grid.grid_surface, (250, 250, 250), (block.x + 1, block.y, block.width - 3,
                                                                      block.height - 2), 4)

    grid.check_for_empty_block()
    grid.check_for_matching_blocks()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
