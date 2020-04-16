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

FPS = 40

run = True


class Spritesheet:
    def __init__(self, filename, cols, rows):
        sheet = pygame.image.load(filename)
        self.sheet = pygame.transform.scale(sheet, (sheet.get_size()[0] * 2, sheet.get_size()[1] * 2))
        self.cols = cols
        self.rows = rows
        self.total_cell_count = cols * rows
        self.rect = self.sheet.get_rect()
        sprite_w = self.cell_width = self.rect.width / cols
        sprite_h = self.cell_height = self.rect.height / rows

        # generate rect of each cell
        self.cells = list([(index % self.cols * sprite_w, index // self.cols * sprite_h, sprite_w, sprite_h) for index
                           in range(self.total_cell_count)])

    def draw(self, surface, cell_index, x, y):
        surface.blit(self.sheet, (x, y), self.cells[cell_index])


class Platform:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)


class Melvin:
    def __init__(self):
        self.sprite = pygame.transform.scale(pygame.image.load("assets/mel_flying.png"), (128, 128))
        self.gravity = 4
        self.x = 0
        self.y = 50
        self.jetpackPower = 8
        self.jetpackOn = False
        self.hitbox = (self.x + 36, self.y + 10, 50, 110)
        self.isFloor = False
        self.isCeiling = False
        self.xDirection = 1
        self.yDirection = 1
        self.leftCollision = False
        self.rightCollision = False
        self.isWalking = False
        self.ani_walk_count = 0
        self.ani_walk_frame = 1
        self.ani_fueguito_count = 0
        self.ani_fueguito_frame = 0

    def draw(self, sp, sp_cell):
        sp.draw(screen, sp_cell, self.x, self.y)
        self.hitbox = (self.x + 36, self.y + 10, 50, 110)
        if self.jetpackOn:
            fueguito_sp = Spritesheet("assets/fueguito.png", 6, 1)
            fueguito_sp.draw(screen, self.ani_fueguito_frame, self.x - 38, self.y + 40)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def animate_fueguito(self):
        if self.ani_walk_count < 4:
            self.ani_walk_count += 1
        else:
            self.ani_walk_count = 0
            if self.ani_fueguito_frame < 5:
                self.ani_fueguito_frame += 1
            else:
                self.ani_fueguito_frame = 0

    def animate_walking(self):
        if self.ani_walk_count < 5:
            self.ani_walk_count += 1
        else:
            self.ani_walk_count = 0
            self.ani_walk_frame = 1 if self.ani_walk_frame == 2 else 2

    def apply_gravity(self):
        if self.isFloor is False and self.hitbox[1] + self.hitbox[3] < win_height:
            self.y += self.gravity
            self.yDirection = 1

    def activate_jetpack_power(self):
        if self.hitbox[1] > 0:
            self.y -= self.jetpackPower
            self.yDirection = -1
            self.jetpackOn = True

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

        self.isFloor = True if collided_bottom else False
        self.isCeiling = True if collided_top else False
        self.rightCollision = True if collided_right and self.isFloor is False else False
        self.leftCollision = True if collided_left and self.isFloor is False else False


melvin = Melvin()
mel_walking_sheet = Spritesheet("assets/mel_walking_spritesheet.png", 3, 1)
mel_walking_flipped_sheet = Spritesheet("assets/mel_walking_spritesheet_flipped.png", 3, 1)
mel_flying_sheet = Spritesheet("assets/mel_flying.png", 1, 1)

lvl_platforms = [Platform((50, 450, 300, 20)), Platform((300, 200, 200, 20))]
lvl_platforms_rects = [platform.rect for platform in lvl_platforms]

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # reset event properties
    melvin.isWalking = False
    melvin.jetpackOn = False

    if keys[pygame.K_UP]:
        if melvin.isCeiling is False:
            melvin.activate_jetpack_power()
            melvin.animate_fueguito()
    if keys[pygame.K_LEFT] and melvin.leftCollision is False:
        melvin.x -= 6
        melvin.xDirection = -1
        melvin.isWalking = True
    if keys[pygame.K_RIGHT] and melvin.rightCollision is False:
        melvin.x += 6
        melvin.xDirection = 1
        melvin.isWalking = True

    screen.fill(colors["almost black"])

    for platform in lvl_platforms:
        platform.draw()

    if melvin.isFloor and melvin.xDirection == 1 and melvin.isWalking is False:
        melvin.draw(mel_walking_sheet, 0)
    elif melvin.isFloor and melvin.xDirection == -1 and melvin.isWalking is False:
        melvin.draw(mel_walking_flipped_sheet, 0)
    elif melvin.isFloor and melvin.xDirection == 1 and melvin.isWalking:
        melvin.animate_walking()
        melvin.draw(mel_walking_sheet, melvin.ani_walk_frame)
    elif melvin.isFloor and melvin.xDirection == -1 and melvin.isWalking:
        melvin.animate_walking()
        melvin.draw(mel_walking_flipped_sheet, melvin.ani_walk_frame)
    else:
        melvin.draw(mel_flying_sheet, 0)
    melvin.apply_gravity()

    melvin.check_collision_with_platforms(lvl_platforms_rects)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
