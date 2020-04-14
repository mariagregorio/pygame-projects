import pygame

pygame.init()

colors = {
    "almost black": (20, 20, 20)
}

win_width = 800
win_height = 500
screen = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
pygame.display.set_caption("jetpac melvin")

run = True


class Platform:
    def __init__(self, rect):
        self.rect = rect

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)


class Melvin:
    def __init__(self):
        self.sprite = pygame.transform.scale(pygame.image.load("mel_sprite.png"), (128, 128))
        self.gravity = 3
        self.x = 0
        self.y = 50
        self.jetpackPower = 6
        self.hitbox = (self.x + 36, self.y + 10, 50, 110)
        self.isFloor = False
        self.isCeiling = False
        self.xDirection = 1
        self.leftCollision = False
        self.rightCollision = False

    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))
        self.hitbox = (self.x + 36, self.y + 10, 50, 110)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def apply_gravity(self):
        if self.isFloor is False and self.hitbox[1] + self.hitbox[3] < win_height:
            self.y += self.gravity

    def activate_jetpack_power(self):
        if self.hitbox[1] > 0:
            self.y -= self.jetpackPower

    def check_collision(self, platforms):
        collided_bottom = False
        collided_top = False
        collided_left = False
        collided_right = False
        for platform in platforms:
            # bottom collision
            if platform.rect[1] <= self.hitbox[1] + self.hitbox[3] <= platform.rect[1] + platform.rect[3]:
                for point in range(self.hitbox[0], self.hitbox[0] + self.hitbox[2]):
                    if platform.rect[0] < point < platform.rect[0] + platform.rect[2]:
                        collided_bottom = True
                        break
            # top collision
            if platform.rect[1] + platform.rect[3] >= self.hitbox[1] >= platform.rect[1]:
                for point in range(self.hitbox[0], self.hitbox[0] + self.hitbox[2]):
                    if platform.rect[0] < point < platform.rect[0] + platform.rect[2]:
                        collided_top = True
                        break
            # left collision
            if self.xDirection == -1 and platform.rect[0] + platform.rect[2] - 10 <= self.hitbox[0] <= \
                    platform.rect[0] + platform.rect[2]:  # the minus ten is for some offset padding
                for point in range(self.hitbox[1], self.hitbox[1] + self.hitbox[3]):
                    if platform.rect[1] < point < platform.rect[1] + platform.rect[3]:
                        collided_left = True
                        break
            # right collision
            if self.xDirection == 1 and platform.rect[0] + 10 >= self.hitbox[0] + self.hitbox[2] >= platform.rect[0]:
                # the plus ten is for some offset padding
                for point in range(self.hitbox[1], self.hitbox[1] + self.hitbox[3]):
                    if platform.rect[1] < point < platform.rect[1] + platform.rect[3]:
                        collided_right = True
                        break
        if collided_bottom:
            self.isFloor = True
        else:
            self.isFloor = False
        if collided_top:
            self.isCeiling = True
        else:
            self.isCeiling = False
        if collided_left:
            self.leftCollision = True
        else:
            self.leftCollision = False
        if collided_right:
            self.rightCollision = True
        else:
            self.rightCollision = False


melvin = Melvin()
platforms = [Platform((50, 450, 600, 10)), Platform((400, 200, 200, 10))]

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if melvin.isCeiling is False:
            melvin.activate_jetpack_power()
    if keys[pygame.K_LEFT] and melvin.leftCollision is False:
        melvin.x -= 4
        melvin.xDirection = -1
    if keys[pygame.K_RIGHT] and melvin.rightCollision is False:
        melvin.x += 4
        melvin.xDirection = 1

    screen.fill(colors["almost black"])

    for platform in platforms:
        platform.draw()

    melvin.draw()
    melvin.apply_gravity()

    melvin.check_collision(platforms)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
