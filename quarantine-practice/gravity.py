import pygame

pygame.init()

win_width = 500
win_height = 300
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()

pygame.display.set_caption("gravity")

run = True


class Floor:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))


class Body:
    def __init__(self, x, y, width, height, fill_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = fill_color
        self.gravity = 1
        self.base = ((self.x, self.x + self.width), self.y + self.height)
        self.floor = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        if self.gravity > 0 and not self.floor:
            self.y += self.gravity
            self.base = ((self.x, self.x + self.width), self.y + self.height)


class Block(Body):
    def __init__(self, x, y, fill_color):
        super().__init__(x, y, 32, 32, fill_color)


block = Block(30, 20, (0, 255, 0))
floor = Floor(40, 180, 200, 20, (0, 0, 255))

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((0, 0, 0))

    floor.draw(window)
    block.draw(window)

    # check collision with floor
    if block.base[1] == floor.y:
        for block_point in range(block.base[0][0], block.base[0][1] + 1):
            for floor_point in range(floor.x, floor.width + 1):
                if block_point == floor_point:
                    block.floor = True
                    break

    pygame.display.update()
    clock.tick(30)

pygame.quit()
