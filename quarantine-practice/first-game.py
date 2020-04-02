import pygame

pygame.init()
win_width = 500
win_height = 300
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()

pygame.display.set_caption("red block")

walk_right = [pygame.image.load('assets/R1.png'), pygame.image.load('assets/R2.png'),
              pygame.image.load('assets/R3.png'), pygame.image.load('assets/R4.png'),
              pygame.image.load('assets/R5.png'), pygame.image.load('assets/R6.png'),
              pygame.image.load('assets/R7.png'), pygame.image.load('assets/R8.png'),
              pygame.image.load('assets/R9.png')]
walk_left = [pygame.image.load('assets/L1.png'), pygame.image.load('assets/L2.png'), pygame.image.load('assets/L3.png'),
             pygame.image.load('assets/L4.png'), pygame.image.load('assets/L5.png'), pygame.image.load('assets/L6.png'),
             pygame.image.load('assets/L7.png'), pygame.image.load('assets/L8.png'), pygame.image.load('assets/L9.png')]
bg_layer1 = pygame.transform.scale(pygame.image.load('assets/land1.png'), (win_width, win_height))
bg_layer2 = pygame.transform.scale(pygame.image.load('assets/land2.png'), (win_width, win_height))

score = 0

bullet_sound = pygame.mixer.Sound('assets/bullet.wav')
hit_sound = pygame.mixer.Sound('assets/hit.wav')
music = pygame.mixer.music.load('assets/Parabola.mp3')

pygame.mixer.music.play(-1)


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.walk_count = 0
        self.is_jump = False
        self.jump_size = 8
        self.jump_count = self.jump_size
        self.direction = 1
        self.hitbox = (self.x + 20, self.y + 10, 24, 50)

    def draw(self, d_window):
        if self.walk_count + 1 >= 27:  # because we have 9 sprites and we're changing them every 3 frames
            self.walk_count = 0

        if self.left:
            # using int division (//) by 3 to exclude decimals
            d_window.blit(walk_left[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        elif self.right:
            d_window.blit(walk_right[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        else:
            if self.direction == -1:
                d_window.blit(walk_left[0], (self.x, self.y))
            elif self.direction == 1:
                d_window.blit(walk_right[0], (self.x, self.y))
        self.hitbox = (self.x + 20, self.y + 10, 24, 50)
        # pygame.draw.rect(d_window, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        pass


class Projectile:
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = 8 * direction  # for negative/positive multiply by direction

    def draw(self, d_window):
        pygame.draw.circle(d_window, self.color, (self.x, self.y), self.radius)


class Enemy:
    e_walk_left = [pygame.image.load('assets/L1E.png'), pygame.image.load('assets/L2E.png'),
                   pygame.image.load('assets/L3E.png'), pygame.image.load('assets/L4E.png'),
                   pygame.image.load('assets/L5E.png'), pygame.image.load('assets/L6E.png'),
                   pygame.image.load('assets/L7E.png'), pygame.image.load('assets/L8E.png'),
                   pygame.image.load('assets/L9E.png'), pygame.image.load('assets/L10E.png'),
                   pygame.image.load('assets/L11E.png')]
    e_walk_right = [pygame.image.load('assets/R1E.png'), pygame.image.load('assets/R2E.png'),
                    pygame.image.load('assets/R3E.png'), pygame.image.load('assets/R4E.png'),
                    pygame.image.load('assets/R5E.png'), pygame.image.load('assets/R6E.png'),
                    pygame.image.load('assets/R7E.png'), pygame.image.load('assets/R8E.png'),
                    pygame.image.load('assets/R9E.png'), pygame.image.load('assets/R10E.png'),
                    pygame.image.load('assets/R11E.png')]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walk_count = 0
        self.vel = 3
        self.direction = 1
        self.hitbox = (self.x + 20, self.y + 5, 35, 55)
        self.health = 3
        self.dead = False

    def draw(self, d_window):
        if not self.dead:
            if self.walk_count + 1 >= 33:
                self.walk_count = 0

            if self.direction == 1:
                d_window.blit(self.e_walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            elif self.direction == -1:
                d_window.blit(self.e_walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
            self.hitbox = (self.x + 20, self.y + 5, 35, 55)

            # health bar
            if self.health == 3:
                pygame.draw.rect(d_window, (0, 255, 0), (self.x + (self.width // 2) - 25, self.y - 10, 50, 10))
            elif self.health == 2:
                pygame.draw.rect(d_window, (255, 255, 0), (self.x + (self.width // 2) - 25, self.y - 10, 50, 10))
            elif self.health == 1:
                pygame.draw.rect(d_window, (255, 0, 0), (self.x + (self.width // 2) - 25, self.y - 10, 50, 10))
            pygame.draw.rect(d_window, (200, 200, 200), (self.x + (self.width // 2) - 25, self.y - 10, 50, 10), 1)
            # pygame.draw.rect(d_window, (255, 0, 0), self.hitbox, 2)
        else:
            # TODO find a better way
            # reset hitbox to avoid hitting it with bullets
            self.hitbox = (win_width, win_height, 0, 0)

    def move(self):
        if self.x <= 0:
            self.direction = 1
        if self.x >= win_width - self.width:
            self.direction = -1

        self.x += self.vel * self.direction

    def hit(self):
        self.health -= 1
        hit_sound.play()
        if self.health == 0:
            self.dead = True


run = True

player = Player(20, 220, 64, 64)
enemy_1 = Enemy(300, 225, 64, 64)
bullets = []
font = pygame.font.SysFont('Ubuntu Mono', 30)


def redraw_game_window():
    window.fill((0, 0, 0))
    window.blit(bg_layer1, (0, 0))
    window.blit(bg_layer2, (0, 0))
    text = font.render("Score " + str(score), 1, (200, 200, 200))
    window.blit(text, (win_width - text.get_width() - 30, 30))
    player.draw(window)
    enemy_1.draw(window)
    enemy_1.move()
    for d_bullet in bullets:
        d_bullet.draw(window)
    pygame.display.update()


# main loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and len(bullets) < 5:
                bullets.append(Projectile(int(player.x + (player.width / 2)), int(player.y + (player.height / 2)), 5,
                                          (150, 50, 255), player.direction))
                bullet_sound.play()

    keys = pygame.key.get_pressed()

    # player movement
    if keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
        player.left = True
        player.right = False
        player.direction = -1
    elif keys[pygame.K_RIGHT] and player.x < win_width - player.width:
        player.x += player.vel
        player.left = False
        player.right = True
        player.direction = 1
    else:
        player.left = False
        player.right = False
        walk_count = 0
    if not player.is_jump:
        if keys[pygame.K_SPACE]:
            player.is_jump = True
            player.left = False
            player.right = False
    else:
        if player.jump_count >= -player.jump_size:
            neg = 1
            if player.jump_count < 0:
                neg = -1
            player.y -= (player.jump_count ** 2) * 0.5 * neg
            player.jump_count -= 1
        else:
            player.is_jump = False
            player.jump_count = player.jump_size

    # bullets
    for bullet in bullets:
        # check for collision with enemy
        if enemy_1.hitbox[0] < (bullet.x - bullet.radius) < (enemy_1.hitbox[0] + enemy_1.hitbox[2]) and \
                enemy_1.hitbox[1] < (bullet.y - bullet.radius) < (enemy_1.hitbox[1] + enemy_1.hitbox[3]):
            enemy_1.hit()
            score += 100
            bullets.remove(bullet)
        # move bullet
        if win_width > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.remove(bullet)

    redraw_game_window()

    clock.tick(27)

pygame.quit()
