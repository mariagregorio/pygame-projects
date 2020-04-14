import math, random, sys
import pygame


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()


w, h = 500, 500
hw, hh = w / 2, h / 2
area = w * h
pygame.init()
clock = pygame.time.Clock()
ds = pygame.display.set_mode((w, h))
pygame.display.set_caption("spritesheet")
fps = 10

dark = (20, 20, 20)


class Spritesheet:
    def __init__(self, filename, cols, rows):
        self.sheet = pygame.image.load(filename)
        self.cols = cols
        self.rows = rows
        self.total_cell_count = cols * rows
        self.rect = self.sheet.get_rect()
        sp_w = self.cell_width = self.rect.width / cols
        sp_h = self.cell_height = self.rect.height / rows
        sp_hw, sp_hh = self.cell_center = (sp_w / 2, sp_h / 2)

        # generate rect of each cell
        self.cells = list([(index % self.cols * sp_w, index // self.cols * sp_h, sp_w, sp_h) for index in
                           range(self.total_cell_count)])

        self.handle = list([
            (0, 0), (-sp_hw, 0), (-sp_w, 0), (0, -sp_hh), (-sp_hw, -sp_hh), (-sp_w, -sp_hh), (0, -sp_h),
            (-sp_hw, -sp_h), (-sp_w, -sp_h),
        ])

    def draw(self, surface, cell_index, x, y, handle):
        surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[cell_index])


s = Spritesheet('RainbowIslandsCharacter.png', 7, 4)

center_handle = 4
indexx = 0

while True:
    events()

    s.draw(ds, indexx % s.total_cell_count, hw, hh, center_handle)
    indexx += 1

    pygame.display.update()
    clock.tick(fps)
    ds.fill(dark)