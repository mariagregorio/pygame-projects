import pygame

pygame.init()

win_width = 500
win_height = 300
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
pygame.display.set_caption("title")

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((0, 0, 0))

    pygame.display.update()
    clock.tick(30)

pygame.quit()