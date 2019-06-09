import pygame
import random
import time

SNAKE_WIDTH = 10
BORDER = 3
PADDING = 0
HEADER = 30
BOARD_ROW = 20
BOARD_COL = 30
WINDOW_PADDING = 20
BIG_FONT = 25
SMALL_FONT = 15
SCORE_FONT = 20
FONT_TYPE = 'Ubuntu Mono'
SNAKE_SPEED = 4 # cell per second
FOOD_NUMBER = 2 # number of food generated at once
POISON_PROBABILITY = 15 # % chance of poison to generate
VEGE_PROBABILITY = 20 # % chance of vegetable to generate
SUPER_PROBABILITY = 80
POISON_LAST = 5 # how long will poison remian on board
VEGE_LAST = 2   # how long will vege remain
SUPER_LAST = 1
FPS = 60

PALLETE = {
    'fg': (255, 255, 255),
    'bg': (0, 0, 0),
    'poison': (255, 0, 0),
    'vege': (0, 255, 0)
}

SUPER_COLORS = [
    (255, 255, 255),
    (255, 127, 255),
    (255, 255, 127),
    (127, 255, 255)
]

directions = {'up':(0,-1), 'down':(0,1), 'left':(-1, 0), 'right':(1,0)}
title = pygame.image.load('snake.png')
title_x, title_y = title.get_rect().size
mag_index = SNAKE_WIDTH * BOARD_COL // title_x
title = pygame.transform.scale(title, (title_x*mag_index, title_y*mag_index))


class Clock:
    def __init__(self, ups):
        self.ups = ups
        self.prev_time = time.monotonic()
        self.paused = False

    def should_update(self):
        if self.paused:
            return False
        now = time.monotonic()
        if now - self.prev_time >= 1 / self.ups:
            self.prev_time = now
            return True
        return False

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def set_ups(self, new_ups):
        self.ups = new_ups


class PygView:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        pygame.font.init()
        self.bigfont = pygame.font.SysFont(FONT_TYPE, BIG_FONT)
        self.smallfont = pygame.font.SysFont(FONT_TYPE, SMALL_FONT)
        self.scorefont = pygame.font.SysFont(FONT_TYPE, SCORE_FONT)
        self.board_width = BOARD_COL * SNAKE_WIDTH + BORDER + 1
        self.board_height = BOARD_ROW * SNAKE_WIDTH + BORDER + 1
        self.width = self.board_width + 2*WINDOW_PADDING
        self.height = self.board_height + 2*WINDOW_PADDING + HEADER
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(PALLETE['bg'])
        self.playground = pygame.Surface((BOARD_COL*SNAKE_WIDTH, BOARD_ROW*SNAKE_WIDTH))
        self.playground.fill(PALLETE['bg'])
        self.scoreboard = pygame.Surface(((BOARD_COL*SNAKE_WIDTH - BORDER+1)//2,
                                          HEADER - BORDER))
        self.timeboard = pygame.Surface(((BOARD_COL*SNAKE_WIDTH - BORDER+1)//2,
                                          HEADER - BORDER))
        self.render_clock = Clock(FPS)
        self.snake_clock = Clock(SNAKE_SPEED)
        self.flashing_clock = Clock(5)
        self.clock = pygame.time.Clock()

        self.program_started = time.monotonic()
        self.snake_speed = SNAKE_SPEED
        self.food_num = FOOD_NUMBER


    def paint_board(self):
        pygame.draw.rect(self.background, PALLETE['fg'],
                        (WINDOW_PADDING, WINDOW_PADDING,
                        self.board_width, self.board_height+HEADER), BORDER)

        pygame.draw.line(self.background, PALLETE['fg'],
                        (WINDOW_PADDING, WINDOW_PADDING+HEADER),
                        (WINDOW_PADDING+self.board_width, WINDOW_PADDING+HEADER),
                        BORDER)

        pygame.draw.line(self.background, PALLETE['fg'],
                        (self.width//2, WINDOW_PADDING),
                        (self.width//2, WINDOW_PADDING+HEADER), BORDER)


    def update(self):
        oppo_direction = {'up':'down', 'down':'up', 'left':'right', 'right':'left'}
        event = self.event_queue[0]
        if oppo_direction[self.previous_pos] != event:
            self.event_queue = self.event_queue[1:]
            self.snake_dir = directions[event]
            self.previous_pos = event
        else:
            self.event_queue = self.event_queue[1:]
            self.snake_dir = directions[self.previous_pos]


    def add_counts(self, count_type):
        if self.poison_lst and 'poison' in count_type:
            self.poison_count += 1
        if self.vege_lst and 'vege' in count_type:
            self.vege_count += 1
        if self.super_lst and 'super' in count_type:
            self.super_count += 1

    def update_snake(self):
        dx, dy = self.snake_dir
        new_head = (self.snake[0][0] + dx, self.snake[0][1] + dy)

        if new_head in self.food_lst:
            i = self.food_lst.index(new_head)
            self.food_lst = self.food_lst[:i] + self.food_lst[i+1:]
            self.nutrition += 1
            self.generate_poison(POISON_PROBABILITY)
            self.generate_vegetable(VEGE_PROBABILITY)
            self.generate_super(SUPER_PROBABILITY)
            self.add_counts(['poison', 'vege', 'super'])

        elif new_head in self.vege_lst:
            self.vege_lst = []
            self.nutrition += 3
            self.vege_count = 0
            self.add_counts(['poison', 'super'])

        elif new_head in self.super_lst:
            self.is_super = True
            self.super_lst = []
            self.nutrition += 10
            self.super_count = 0
            self.food_lst = []
            self.poison_lst = []
            self.vege_lst = []


        if self.nutrition > 0:
            self.snake = [new_head] + self.snake
            self.nutrition -= 1

        elif new_head in self.poison_lst:
            self.poison_lst = []
            self.snake = [new_head] + self.snake[:len(self.snake)//2]
            self.poison_count = 0
            self.add_counts(['vege', 'super'])

        else:
            self.is_super = False
            self.snake = [new_head] + self.snake[:-1]


    def is_dead(self, snake):
        if len(snake) != len(set(snake)):
            return True
        if snake[0][0] < 0 or snake[0][0] >= BOARD_COL:
            return True
        if snake[0][1] < 0 or snake[0][1] >= BOARD_ROW:
            return True

        return False


    def queueing_events(self, events, event_queue):
        def what_direction(event):
            if event.key == pygame.K_UP:
                return 'up'

            elif event.key == pygame.K_DOWN:
                return 'down'

            elif event.key == pygame.K_LEFT:
                return 'left'

            elif event.key == pygame.K_RIGHT:
                return 'right'

        oppo_direction = {'up':'down', 'down':'up', 'left':'right', 'right':'left'}

        for event in events:
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                elif event.key == pygame.K_SPACE:
                    self.change_game_state()
                    return event_queue

                direction = what_direction(event)
                if direction:
                    if event_queue == []:
                        event_queue.append(direction)

                    elif event_queue and len(event_queue) <= 3:
                        if event_queue[-1] != oppo_direction[direction] and \
                           event_queue[-1] != direction:
                            event_queue.append(direction)

        return event_queue


    def blit_squares(self, snake, color):
        topleft_x = WINDOW_PADDING + BORDER - 1
        topleft_y = WINDOW_PADDING + BORDER + HEADER - 1
        if color in PALLETE:
            rgb = PALLETE[color]
        elif type(color) is tuple and len(color) == 3:
            rgb = color

        for (x, y) in snake:
            pygame.draw.rect(self.playground, rgb,
                            (SNAKE_WIDTH*x, SNAKE_WIDTH*y,
                            SNAKE_WIDTH, SNAKE_WIDTH))

        self.screen.blit(self.playground, (topleft_x, topleft_y))


    def blit_title(self, smalltext):
        topleft_x = WINDOW_PADDING + BORDER - 1
        topleft_y = WINDOW_PADDING + BORDER + HEADER - 1
        small = self.smallfont.render(smalltext, False, PALLETE['fg'])
        title_rect = title.get_rect( \
            center=(self.board_width/2, self.board_height/2 - BIG_FONT))
        small_rect = small.get_rect( \
            center=(self.board_width/2, self.board_height/2 + SMALL_FONT))

        self.playground.blit(title, title_rect)
        self.playground.blit(small, small_rect)
        self.screen.blit(self.playground, (topleft_x, topleft_y))


    def blit_text(self, bigtext, smalltext, color):
        topleft_x = WINDOW_PADDING + BORDER - 1
        topleft_y = WINDOW_PADDING + BORDER + HEADER - 1
        big = self.bigfont.render(bigtext, False, PALLETE['fg'])
        small = self.smallfont.render(smalltext, False, PALLETE['fg'])
        big_rect = big.get_rect( \
            center=(self.board_width/2, self.board_height/2 - BIG_FONT))
        small_rect = small.get_rect( \
            center=(self.board_width/2, self.board_height/2))

        self.playground.blit(big, big_rect)
        self.playground.blit(small, small_rect)
        self.screen.blit(self.playground, (topleft_x, topleft_y))


    def blit_score(self, score):
        self.scoreboard.fill(PALLETE['bg'])
        score = self.scorefont.render('Score:{}'.format(str(score)),
                                    False, PALLETE['fg'])
        score_rect = score.get_rect( \
                center=(self.scoreboard.get_width()/2,
                        self.scoreboard.get_height()/2))
        self.scoreboard.blit(score, score_rect)
        self.screen.blit(self.scoreboard,
                        (WINDOW_PADDING + BORDER - 1, WINDOW_PADDING + BORDER -1))


    def blit_time(self, time):
        self.timeboard.fill(PALLETE['bg'])
        time = self.scorefont.render('Time:{}'.format(int(time)),
                                    False, PALLETE['fg'])
        time_rect = time.get_rect( \
                center=(self.timeboard.get_width()/2,
                        self.timeboard.get_height()/2))
        self.timeboard.blit(time, time_rect)
        self.screen.blit(self.timeboard,
                        (self.width // 2 + 1, WINDOW_PADDING + BORDER -1))


    def generate_food(self):
        for _ in range(self.food_num):
            empty_space = self.generate_legal_coord()
            self.food_lst.append(empty_space)


    def generate_legal_coord(self):
        empty_space = [(a, b) for a in range(BOARD_COL)
                               for b in range(BOARD_ROW)
                               if (a, b) not in self.snake]
        n = random.randint(0, len(empty_space)-1)
        return empty_space[n]


    def is_chance(self, probability):
        random_number = random.uniform(0, 1)
        if random_number <= probability/100:
            return True
        return False


    def generate_poison(self, probability):
        if self.is_chance(probability):
            if self.poison_lst == []:
                self.poison_lst.append(self.generate_legal_coord())
                self.poison_count = 0

        if self.poison_count >= POISON_LAST:
            self.poison_lst = []
            self.poison_count = 0


    def generate_vegetable(self, probability):
        if self.is_chance(probability):
            if self.vege_lst == []:
                self.vege_lst.append(self.generate_legal_coord())
                self.vege_count = 0

        if self.vege_count >= VEGE_LAST:
            self.vege_lst = []
            self.vege_count = 0


    def generate_super(self, probability):
        if self.is_chance(probability):
            if self.super_lst == []:
                self.super_lst.append(self.generate_legal_coord())

        if self.super_count >= SUPER_LAST:
            self.super_lst = []
            self.super_count = 0


    def start_game(self):
        self.event_queue = []
        self.food_lst = []
        self.poison_lst = []
        self.vege_lst = []
        self.super_lst = []
        self.poison_count = 0
        self.vege_count = 0
        self.super_count = 0
        self.previous_pos = 'right'
        self.snake_dir = directions[self.previous_pos]
        self.snake = [(BOARD_COL//2, BOARD_ROW//2)]
        self.state = 'running'
        self.game_started = time.monotonic()
        self.time_paused = 0
        self.time_resumed = 0
        self.total_paused = 0
        self.is_super = False
        self.nutrition = 0


    def change_game_state(self):
        if self.state == 'running':
            self.state = 'paused'
            self.time_paused = time.monotonic()
            self.snake_clock.pause()

        elif self.state == 'paused':
            self.state = 'running'
            self.time_resumed = time.monotonic()
            self.total_paused += self.time_resumed - self.time_paused
            self.snake_clock.unpause()

        elif self.state == 'game over' or self.state == 'not started':
            self.state = 'running'
            self.start_game()


    def run(self):
        directions = {'up':(0,-1), 'down':(0,1), 'left':(-1, 0), 'right':(1,0)}
        self.paint_board()
        self.screen.blit(self.background, (0,0))
        self.start_game()
        self.state = 'not started'
        self.blit_title('Press space to start')
        mainloop = True
        i = 0

        while mainloop:
            self.event_queue = self.queueing_events(pygame.event.get(), self.event_queue)
            if self.event_queue is False:
                mainloop = False

            if self.snake_clock.should_update():
                if self.state == 'running':
                    if self.event_queue:
                        self.update()
                    if not self.is_super and self.food_lst == []:
                        self.generate_food()
                    self.update_snake()

                if self.is_dead(self.snake):
                    self.state = 'game over'

            if self.render_clock.should_update():
                self.playground.fill((0,0,0))
                self.clock.tick()

                if self.flashing_clock.should_update():
                    i += 1
                    i %= len(SUPER_COLORS)
                if self.state == 'running':
                    if self.is_super:
                        self.blit_squares(self.snake, SUPER_COLORS[i])
                    else:
                        self.blit_squares(self.snake, 'fg')
                    self.blit_squares(self.food_lst, 'fg')
                    self.blit_squares(self.poison_lst, 'poison')
                    self.blit_squares(self.vege_lst, 'vege')
                    self.blit_squares(self.super_lst, SUPER_COLORS[i])
                    self.blit_score(len(self.snake) - 1)
                    self.blit_time(time.monotonic() - self.game_started - self.total_paused)

                elif self.state == 'game over':
                    self.blit_text('Game over', 'press space to restart', 'fg')

                elif self.state == 'paused':
                    self.blit_text('Paused', 'press space to resume', 'fg')

                total_playtime = time.monotonic() - self.program_started
                text = 'FPS: {0:.2f}, Playtime: {1:.2f}'.format(self.clock.get_fps(), total_playtime)
                pygame.display.set_caption(text)
                pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    PygView().run()
