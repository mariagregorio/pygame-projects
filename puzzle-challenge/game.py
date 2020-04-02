import random
import pygame

pygame.init()

win_width = 212
win_height = 404
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
pygame.display.set_caption("puzzle challenge")


class BlockType:
    def __init__(self, block_id):
        self.block_id = block_id
        if self.block_id == 1:
            self.color_name = "Lila"
            self.color = (152, 120, 248)
        elif self.block_id == 2:
            self.color_name = "Light blue"
            self.color = (0, 232, 216)
        elif self.block_id == 3:
            self.color_name = "Green"
            self.color = (184, 248, 24)
        elif self.block_id == 4:
            self.color_name = "Yellow"
            self.color = (248, 184, 0)
        else:
            self.color_name = "Empty"
            self.color = (0, 0, 0)


class Block:
    def __init__(self, block_type):
        self.block_type = block_type  # type BlockType
        self.position = -1
        self.x = 0
        self.y = 0

    def draw(self, surface):
        self.x = self.position * 32
        pygame.draw.rect(surface, self.block_type.color, (self.x, 0, 32, 32))


class Line:
    def __init__(self, surface, blocks, grid_pos):
        self.blocks = blocks
        self.grid_pos = grid_pos
        self.surface = surface
        self.line_surface = pygame.Surface((192, 32))
        self.y = self.grid_pos * 32

    def display(self, grid_surface):
        for i, block in enumerate(self.blocks):
            block.position = i
            block.draw(self.line_surface)
        grid_surface.blit(self.line_surface, (0, self.y))


class Grid:
    def __init__(self, surface):
        self.surface = surface
        self.lines = []
        self.x = 20
        self.y = 20
        self.height = 384
        self.width = 192
        self.grid_surface = pygame.Surface((self.width, self.height))

    def add_line_bottom(self, line):
        self.lines.append(line)

    def display(self):
        for line in self.lines:
            line.display(self.grid_surface)

        self.surface.blit(self.grid_surface, (0, 0))


run = True

blocks_11 = []
blocks_10 = []

for x in range(6):
    if x == 1:
        blocks_11.append(Block(BlockType(-1)))
        blocks_10.append(Block(BlockType(-1)))
        continue
    blocks_11.append(Block(BlockType(random.randint(1, 4))))
    blocks_10.append(Block(BlockType(random.randint(1, 4))))


random_line1 = Line(window, blocks_11, 11)
random_line2 = Line(window, blocks_10, 10)

game_grid = Grid(window)
game_grid.add_line_bottom(random_line1)
game_grid.add_line_bottom(random_line2)


def apply_gravity(grid):
    global run
    for line in grid.lines:
        for block in line.blocks:
            if block.block_type.block_id == -1:
                print("theres an empty block in line {}, block {}".format(line.grid_pos, block.position))
                run = False
                # TODO redraw affected lines


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((0, 0, 0))

    game_grid.display()

    apply_gravity(game_grid)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
