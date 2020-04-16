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
        self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)


class Melvin:
    def __init__(self):
        self.sprite = pygame.transform.scale(pygame.image.load("mel_sprite.png"), (128, 128))
        self.gravity = 4
        self.x = 0
        self.y = 50
        self.jetpackPower = 8
        self.hitbox = (self.x + 36, self.y + 10, 50, 110)
        self.isFloor = False
        self.isCeiling = False
        self.xDirection = 1
        self.yDirection = 1
        self.leftCollision = False
        self.rightCollision = False

    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))
        self.hitbox = (self.x + 36, self.y + 10, 50, 110)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def apply_gravity(self):
        if self.isFloor is False and self.hitbox[1] + self.hitbox[3] < win_height:
            self.y += self.gravity
            self.yDirection = 1

    def activate_jetpack_power(self):
        # TODO animación del fueguitoooo
        if self.hitbox[1] > 0:
            self.y -= self.jetpackPower
            self.yDirection = -1

    def check_collision_with_platforms(self, platforms):
        collided_bottom = False
        collided_top = False
        collided_left = False
        collided_right = False
        melvin_hitbox_rect = pygame.Rect(self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3])
        platform_collision_index = melvin_hitbox_rect.collidelist(platforms)
        # if theres a collision, check from which side
        if platform_collision_index != -1:
            # bottom
            for point in range(self.hitbox[0], self.hitbox[0] + self.hitbox[2]):
                if platforms[platform_collision_index].collidepoint(point, self.hitbox[1] + self.hitbox[3]):
                    collided_bottom = True
                    break
            # top
            for point in range(self.hitbox[0], self.hitbox[0] + self.hitbox[2]):
                if platforms[platform_collision_index].collidepoint(point, self.hitbox[1]):
                    collided_top = True
                    break
            # right
            for point in range(self.hitbox[1], self.hitbox[1] + self.hitbox[3]):
                if platforms[platform_collision_index].collidepoint(self.hitbox[0] + self.hitbox[2], point):
                    collided_right = True
                    break
            # left
            for point in range(self.hitbox[1], self.hitbox[1] + self.hitbox[3]):
                if platforms[platform_collision_index].collidepoint(self.hitbox[0], point):
                    collided_left = True
                    break

        # TODO when standing on platform, change sprite to standing. when walking, animate
        self.isFloor = True if collided_bottom else False
        self.isCeiling = True if collided_top else False
        self.rightCollision = True if collided_right and self.isFloor is False else False
        self.leftCollision = True if collided_left and self.isFloor is False else False


melvin = Melvin()
lvl_platforms = [Platform((50, 450, 300, 20)), Platform((300, 200, 200, 20))]
lvl_platforms_rects = [platform.rect for platform in lvl_platforms]

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if melvin.isCeiling is False:
            melvin.activate_jetpack_power()
    if keys[pygame.K_LEFT] and melvin.leftCollision is False:
        melvin.x -= 6
        melvin.xDirection = -1
    if keys[pygame.K_RIGHT] and melvin.rightCollision is False:
        melvin.x += 6
        melvin.xDirection = 1

    screen.fill(colors["almost black"])

    for platform in lvl_platforms:
        platform.draw()

    melvin.draw()
    melvin.apply_gravity()

    melvin.check_collision_with_platforms(lvl_platforms_rects)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
