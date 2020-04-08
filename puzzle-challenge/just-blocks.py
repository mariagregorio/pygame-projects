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
                  (5, (248, 120, 88)), (6, (20, 20, 20))]

        # TODO stop the game when you reach 12 lines, and show a "you lose" message and "start again" option
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
            print("you lose")

    def check_for_empty_block(self):
        if len(self.blocks) > 1:
            for i, i_line in enumerate(self.blocks):
                for j, i_block in enumerate(i_line):
                    if i != len(self.blocks) - 1 and self.blocks[i][j].color[0] != 6 \
                            and self.blocks[i+1][j].color[0] == 6:
                        # make the block below the current same color as current, make current block empty
                        if self.animation_count == 6:
                            self.blocks[i+1][j].color = self.blocks[i][j].color
                            self.blocks[i][j].color = (6, (20, 20, 20))

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

    # this is buggy, check vertical matches are working fine
    # UPDATE: CHECKED BUT STAY ALERT
    def check_for_matching_blocks(self):
        for i, i_line in enumerate(self.blocks):
            for j, i_block in enumerate(i_line):
                # check left to right matching blocks
                try:
                    if self.blocks[i][j + 1].color == i_block.color and self.blocks[i][j + 2].color == i_block.color \
                            and i_block.color[0] != 6:
                        self.blocks[i][j].color = (6, (20, 20, 20))
                        self.blocks[i][j + 1].color = (6, (20, 20, 20))
                        self.blocks[i][j + 2].color = (6, (20, 20, 20))
                        print("found 3 in line horizontal")
                        if self.blocks[i][j + 3].color == i_block.color:
                            self.blocks[i][j + 3].color = (6, (20, 20, 20))
                            print("found 4 in line horizontal")
                            if self.blocks[i][j + 4].color == i_block.color:
                                self.blocks[i][j + 4].color = (6, (20, 20, 20))
                                print("found 5 in line horizontal")
                                if self.blocks[i][j + 5].color == i_block.color:
                                    self.blocks[i][j + 5].color = (6, (20, 20, 20))
                                    print("found 6 in line horizontal")
                except IndexError:
                    pass
                # check top to bottom matching blocks
                try:
                    if self.blocks[i + 1][j].color == i_block.color and self.blocks[i + 2][j].color == i_block.color \
                            and i_block.color[0] != 6:
                        self.blocks[i][j].color = (6, (20, 20, 20))
                        self.blocks[i + 1][j].color = (6, (20, 20, 20))
                        self.blocks[i + 2][j].color = (6, (20, 20, 20))
                        print("found 3 in line vertical")
                        if self.blocks[i + 3][j].color == i_block.color:
                            self.blocks[i + 3][j].color = (6, (20, 20, 20))
                            print("found 4 in line vertical")
                            if self.blocks[i + 4][j].color == i_block.color:
                                self.blocks[i + 4][j].color = (6, (20, 20, 20))
                                print("found 5 in line vertical")
                                if self.blocks[i + 5][j].color == i_block.color:
                                    self.blocks[i + 5][j].color = (6, (20, 20, 20))
                                    print("found 6 in line vertical")
                except IndexError:
                    pass


run = True

grid = Grid()

grid.generate_line()

grid.blocks[0][0].focused = True

NEWLINE = pygame.USEREVENT + 1
pygame.time.set_timer(NEWLINE, 5000)

selected_block_animation_counter = 0

# TODO don't start the game right away! make a "start" button
# TODO add score functionality and display it
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for i, line in enumerate(grid.blocks):
                    for j, block in enumerate(line):
                        if block.focused and block.selected is False and grid.selected_block is None:
                            block.selected = True
                            grid.selected_block = block.id
                        elif block.focused and block.selected is True:
                            block.selected = False
                            grid.selected_block = None
                        elif block.focused and block.selected is False and grid.selected_block is not None:
                            # make the switch
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
        if event.type == NEWLINE:
            grid.generate_line()

    window.fill((20, 20, 20))
    grid.display()
    grid.grid_surface.fill((20, 20, 20))

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
            # TODO animate allowed blocks for the switch

    grid.check_for_empty_block()
    grid.check_for_matching_blocks()
    grid.animate_blocks()
    grid.check_current_focus_is_not_empty()

    pygame.display.update()
    clock.tick(30)

pygame.quit()

