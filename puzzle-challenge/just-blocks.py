import random
import pygame

pygame.init()

win_width = 500
win_height = 500
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
pygame.display.set_caption("puzzle challenge mf")

block_id_count = 0

title_font = pygame.font.Font('videophreak.ttf', 40)
font = pygame.font.SysFont('Noto Mono', 30)
small_font = pygame.font.SysFont('Noto Mono', 15)

game_over_text = font.render("game over :(", 1, (104, 68, 252))
play_again_text = font.render("PLAY AGAIN", 1, (10, 10, 10), (250, 250, 250))
title_text = title_font.render("Puzzle Challenge MF", 1, (250, 250, 250))
start_text = font.render("START", 1, (10, 10, 10), (250, 250, 250))

play_again_rect = (0, 0, 0, 0)
start_rect = (0, 0, 0, 0)


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
        self.selected = False
        self.allowed_for_switch = False

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
        self.animation_count = 1
        self.selected_block = None
        self.score = 0
        self.latest_score = 0

    def animate_blocks(self):
        if self.animation_count < 6:
            self.animation_count += 1
        else:
            self.animation_count = 1

    def display(self):
        global window
        window.blit(self.grid_surface, ((win_width // 2) - (self.width // 2), (win_height // 2) - (self.height // 2)))

    def generate_line(self):
        new_line = []
        colors = [(1, (152, 120, 248)), (2, (0, 232, 216)), (3, (184, 248, 24)), (4, (248, 184, 0)),
                  (5, (248, 120, 88)), (6, (40, 40, 40))]

        # remove empty lines
        for i_line in self.blocks:
            empties_counter = 0
            for i_block in i_line:
                if i_block.color[0] == 6:
                    empties_counter += 1
            if empties_counter == 6:
                self.blocks.remove(i_line)

        if len(self.blocks) < 12:
            # move all lines -32 in y
            if len(self.blocks) > 0:
                for i_line in self.blocks:
                    for i_block in i_line:
                        i_block.y -= 32

            for x in range(6):
                new_line.append(Block(x * 32, self.height - 32, colors[random.randint(0, len(colors) - 2)]))
            self.blocks.append(new_line)
        else:
            global game_over
            game_over = True

    def check_for_empty_block(self):
        if len(self.blocks) > 1:
            for i, i_line in enumerate(self.blocks):
                for j, i_block in enumerate(i_line):
                    if i != len(self.blocks) - 1 and self.blocks[i][j].color[0] != 6 \
                            and self.blocks[i+1][j].color[0] == 6:
                        # make the block below the current same color as current, make current block empty
                        if self.animation_count == 6:
                            self.blocks[i+1][j].color = self.blocks[i][j].color
                            self.blocks[i][j].color = (6, (40, 40, 40))

    def check_current_focus_is_not_empty(self):
        for i, j_line in enumerate(self.blocks):
            for j, j_block in enumerate(j_line):
                if (j_block.focused or j_block.selected) and j_block.color[0] == 6:
                    # start checking closest not empty
                    j_block.focused = False
                    j_block.selected = False
                    not_empty_found = False
                    search_level = 1
                    while not_empty_found is False:
                        # search right
                        try:
                            if self.blocks[i][j + search_level].color[0] != 6:
                                self.blocks[i][j + search_level].focused = True
                                not_empty_found = True
                                break
                        except IndexError:
                            pass
                        # search left
                        try:
                            if self.blocks[i][j - search_level].color[0] != 6:
                                self.blocks[i][j - search_level].focused = True
                                not_empty_found = True
                                break
                        except IndexError:
                            pass
                        # search down
                        try:
                            if self.blocks[i + search_level][j].color[0] != 6:
                                self.blocks[i + search_level][j].focused = True
                                not_empty_found = True
                                break
                        except IndexError:
                            pass
                        # search down-right
                        try:
                            if self.blocks[i + search_level][j + search_level].color[0] != 6:
                                self.blocks[i + search_level][j + search_level].focused = True
                                not_empty_found = True
                                break
                        except IndexError:
                            pass
                        # search down-left
                        try:
                            if self.blocks[i + search_level][j - search_level].color[0] != 6:
                                self.blocks[i + search_level][j - search_level].focused = True
                                not_empty_found = True
                                break
                        except IndexError:
                            pass
                        search_level += 1
                    self.selected_block = None

# TODO set timer for single score to kinda flash for a moment and then go away and so on
    def update_score_display(self):
        score_text = small_font.render("SCORE {}".format(self.score), 1, (250, 250, 250), (20, 20, 20))
        window.blit(score_text, (360, 40))

    def update_latest_score_display(self):
        latest_score_text = small_font.render("+{}".format(self.latest_score), 1, (248, 164, 192), (20, 20, 20))
        window.blit(latest_score_text, (360, 70))

    def check_for_matching_blocks(self):
        global selected_block_animation_counter
        for i, i_line in enumerate(self.blocks):
            for j, i_block in enumerate(i_line):
                # check left to right matching blocks
                match_horizontal_num = 0
                count_score = 0
                try:
                    if self.blocks[i][j + 1].color == i_block.color and self.blocks[i][j + 2].color == i_block.color \
                            and i_block.color[0] != 6:
                        match_horizontal_num = 3
                        count_score += 100
                        if self.blocks[i][j + 3].color == i_block.color:
                            match_horizontal_num += 1
                            count_score += 100
                            if self.blocks[i][j + 4].color == i_block.color:
                                match_horizontal_num += 1
                                count_score += 300
                                if self.blocks[i][j + 5].color == i_block.color:
                                    match_horizontal_num += 1
                                    count_score += 500
                except IndexError:
                    pass
                for num in range(match_horizontal_num):
                    self.blocks[i][j + num].color = (6, (40, 40, 40))
                self.score += count_score
                if count_score != 0:
                    self.latest_score = count_score
                self.update_score_display()

                # check top to bottom matching blocks
                match_vertical_num = 0
                count_score = 0
                try:
                    if self.blocks[i + 1][j].color == i_block.color and self.blocks[i + 2][j].color == i_block.color \
                            and i_block.color[0] != 6:
                        match_vertical_num = 3
                        count_score += 100
                        if self.blocks[i + 3][j].color == i_block.color:
                            match_vertical_num += 1
                            count_score += 100
                            if self.blocks[i + 4][j].color == i_block.color:
                                match_vertical_num += 1
                                count_score += 300
                                if self.blocks[i + 5][j].color == i_block.color:
                                    match_vertical_num += 1
                                    count_score += 500
                except IndexError:
                    pass
                for num in range(match_vertical_num):
                    self.blocks[i + num][j].color = (6, (40, 40, 40))
                self.score += count_score
                if count_score != 0:
                    self.latest_score = count_score
                self.update_score_display()


run = True

grid = Grid()

grid.generate_line()

grid.blocks[0][0].focused = True

NEWLINE = pygame.USEREVENT + 1
pygame.time.set_timer(NEWLINE, 5000)

selected_block_animation_counter = 0

start_screen = True
game_over = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and game_over is True:
            if event.button == 1:
                if (play_again_rect[0] + play_again_rect[2]) > event.pos[0] > play_again_rect[0] and \
                        (play_again_rect[1] + play_again_rect[3]) > event.pos[1] > play_again_rect[1]:
                    game_over = False
                    grid = Grid()
                    grid.generate_line()
                    grid.blocks[0][0].focused = True
                    selected_block_animation_counter = 0
                    block_id_count = 0

        if event.type == pygame.MOUSEBUTTONDOWN and game_over is False and start_screen:
            if event.button == 1:
                if (start_rect[0] + start_rect[2]) > event.pos[0] > start_rect[0] and \
                        (start_rect[1] + start_rect[3]) > event.pos[1] > start_rect[1]:
                    start_screen = False

        if event.type == pygame.KEYDOWN and game_over is False:
            if event.key == pygame.K_SPACE:
                for i, line in enumerate(grid.blocks):
                    for j, block in enumerate(line):
                        if block.focused and block.selected is False and grid.selected_block is None:
                            block.selected = True
                            grid.selected_block = block.id
                            # set allowed blocks
                            if j != 0:
                                if grid.blocks[i][j - 1].color[0] != 6:
                                    grid.blocks[i][j - 1].allowed_for_switch = True
                            if j != 5:
                                if grid.blocks[i][j + 1].color[0] != 6:
                                    grid.blocks[i][j + 1].allowed_for_switch = True
                            if i != 0:
                                if grid.blocks[i - 1][j].color[0] != 6:
                                    grid.blocks[i - 1][j].allowed_for_switch = True
                            if i != len(grid.blocks) - 1:
                                grid.blocks[i + 1][j].allowed_for_switch = True
                        elif block.focused and block.selected is True:
                            block.selected = False
                            grid.selected_block = None
                        # make the switch
                        if block.focused and block.selected is False and grid.selected_block is not None:
                            for k_line in grid.blocks:
                                for l_block in k_line:
                                    if l_block.selected:
                                        focused_color = block.color
                                        selected_color = l_block.color
                                        l_block.color = focused_color
                                        block.color = selected_color
                                        l_block.selected = False
                                        grid.selected_block = None
                                        break
                        if grid.selected_block is None:
                            for k_line in grid.blocks:
                                for l_block in k_line:
                                    l_block.allowed_for_switch = False
            if event.key == pygame.K_RIGHT:
                for i, line in enumerate(grid.blocks):
                    for j, block in enumerate(line):
                        if block.focused and j != 5 and line[j + 1].color[0] != 6:
                            if grid.selected_block is not None and (block.selected is True or
                                                                    grid.blocks[i][j + 1].selected is True):
                                block.focused = False
                                grid.blocks[i][j + 1].focused = True
                            elif grid.selected_block is not None and block.id != grid.selected_block:
                                pass
                                break
                            block.focused = False
                            grid.blocks[i][j + 1].focused = True
                            break
            if event.key == pygame.K_LEFT:
                for i, line in enumerate(grid.blocks):
                    for j, block in enumerate(line):
                        if block.focused and j != 0 and line[j - 1].color[0] != 6:
                            if grid.selected_block is not None and (block.selected is True or
                                                                    grid.blocks[i][j - 1].selected is True):
                                block.focused = False
                                grid.blocks[i][j - 1].focused = True
                            elif grid.selected_block is not None and block.id != grid.selected_block:
                                pass
                                break
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
                                if grid.selected_block is not None and (block.selected is True or
                                                                        grid.blocks[i + 1][j].selected is True):
                                    block.focused = False
                                    grid.blocks[i + 1][j].focused = True
                                    found = True
                                elif grid.selected_block is not None and block.id != grid.selected_block:
                                    pass
                                    break
                                block.focused = False
                                grid.blocks[i + 1][j].focused = True
                                found = True
                                break
            if event.key == pygame.K_UP:
                for i, line in enumerate(grid.blocks):
                    for j, block in enumerate(line):
                        if block.focused and i != 0 and grid.blocks[i - 1][j].color[0] != 6:
                            if grid.selected_block is not None and (block.selected is True or
                                                                    grid.blocks[i - 1][j].selected is True):
                                block.focused = False
                                grid.blocks[i - 1][j].focused = True
                            elif grid.selected_block is not None and block.id != grid.selected_block:
                                pass
                                break
                            block.focused = False
                            grid.blocks[i - 1][j].focused = True
                            break
        if event.type == NEWLINE and game_over is False and start_screen is False:
            grid.generate_line()

    window.fill((20, 20, 20))

    if game_over:
        play_again_text_size = play_again_text.get_rect()
        game_over_text_size = game_over_text.get_rect()
        window.blit(game_over_text, ((win_width // 2) - (game_over_text_size[2] // 2), (win_height // 2) -
                                     (game_over_text_size[3] // 2) - play_again_text_size[3] - 30))
        play_again_rect = window.blit(play_again_text, ((win_width // 2) - (play_again_text_size[2] // 2),
                                      (win_height // 2) - (play_again_text_size[3] // 2)))
        final_score_text = title_font.render("final score: {}".format(grid.score), 1, (250, 250, 250))
        final_score_text_rect = final_score_text.get_rect()
        window.blit(final_score_text, ((win_width // 2) - (final_score_text_rect[2] // 2), (win_height // 2) -
                                       (final_score_text_rect[3] // 2) + 80))

    elif game_over is False and start_screen is False:
        grid.display()
        grid.grid_surface.fill((40, 40, 40))

        if selected_block_animation_counter < 10:
            selected_block_animation_counter += 1
        else:
            selected_block_animation_counter = 0

        for line in grid.blocks:
            for block in line:
                block.draw(grid.grid_surface)
                if block.focused:
                    pygame.draw.rect(grid.grid_surface, (250, 250, 250), (block.x + 1, block.y, block.width - 3,
                                                                          block.height - 2), 4)
                if block.selected:
                    if 0 <= selected_block_animation_counter < 6:
                        selected_border_color = (250, 250, 250)
                    else:
                        selected_border_color = (0, 0, 0)
                    pygame.draw.rect(grid.grid_surface, selected_border_color, (block.x + 1, block.y, block.width - 3,
                                                                                block.height - 2), 4)
                if block.allowed_for_switch and block.focused is False:
                    pygame.draw.rect(grid.grid_surface, (0, 0, 0), (block.x + 1, block.y, block.width - 3,
                                                                    block.height - 2), 4)

        grid.check_for_empty_block()
        grid.check_for_matching_blocks()
        grid.animate_blocks()
        grid.check_current_focus_is_not_empty()

    elif game_over is False and start_screen:
        title_text_size = title_text.get_rect()
        start_text_size = start_text.get_rect()
        start_rect = window.blit(start_text, ((win_width // 2) - (start_text_size[2] // 2), (win_height // 2) -
                                 (start_text_size[3] // 2) + title_text_size[3] + 40))
        window.blit(title_text, ((win_width // 2) - (title_text_size[2] // 2), (win_height // 2) -
                                 (title_text_size[3] // 2)))

    pygame.display.update()
    clock.tick(30)

pygame.quit()

# TODO music and sound effects

