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
FPS = 60

PALLETE = {
    'fg': (255, 255, 255),
    'bg': (0, 0, 0),
    'poison':(255, 0, 0)
}

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
        self.clock = pygame.time.Clock()

        self.game_started = time.monotonic()
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


    def update(self, event_queue, directions, previous_pos):
        oppo_direction = {'up':'down', 'down':'up', 'left':'right', 'right':'left'}
        event = self.event_queue[0]
        if oppo_direction[self.previous_pos] != event:
            return self.event_queue[1:], directions[event], event
        else:
            return self.event_queue[1:], directions[self.previous_pos], self.previous_pos


    def update_snake(self, self.snake, self.snake_dir, food_lst):
        dx, dy = self.snake_dir
        new_head = (self.snake[0][0] + dx, self.snake[0][1] + dy)

        if new_head in self.food_lst:
            i = self.food_lst.index(new_head)
            self.food_lst = self.food_lst[:i] + self.food_lst[i+1:]
            return [new_head] + self.snake, self.food_lst

        return [new_head] + self.snake[:-1], self.food_lst


    def is_dead(self, self.snake):
        if len(self.snake) != len(set(self.snake)):
            return True
        if self.snake[0][0] < 0 or self.snake[0][0] >= BOARD_COL:
            return True
        if self.snake[0][1] < 0 or self.snake[0][1] >= BOARD_ROW:
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
                    return ['space'] + self.event_queue

                direction = what_direction(event)
                if direction:
                    if self.event_queue == []:
                        self.event_queue.append(direction)

                    elif self.event_queue and len(self.event_queue) <= 3:
                        if self.event_queue[-1] != oppo_direction[direction] and \
                        self.event_queue[-1] != direction:
                            self.event_queue.append(direction)

        return self.event_queue


    def blit_squares(self, self.snake, color):
        topleft_x = WINDOW_PADDING + BORDER - 1
        topleft_y = WINDOW_PADDING + BORDER + HEADER - 1
        for (x, y) in self.snake:
            pygame.draw.rect(self.playground, PALLETE[color],
                            (SNAKE_WIDTH*x, SNAKE_WIDTH*y,
                            SNAKE_WIDTH, SNAKE_WIDTH))

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


    def generate_food(self, food_lst, snake):
        empty_space = [(a, b) for a in range(BOARD_COL)
                               for b in range(BOARD_ROW)
                               if (a, b) not in self.snake]

        for _ in range(self.food_num):
            n = random.randint(0, len(empty_space)-1)
            self.food_lst += [empty_space[n]]
            empty_space = empty_space[:n] + empty_space[n+1:]

        return self.food_lst


    def start_game(self):
        self.event_queue = []
        self.food_lst = []
        self.previous_pos = 'right'
        self.snake_dir = directions[self.previous_pos]
        self.snake = [(BOARD_COL//2, BOARD_ROW//2)]
        self.state = 'running'


    def run(self):
        directions = {'up':(0,-1), 'down':(0,1), 'left':(-1, 0), 'right':(1,0)}
        self.paint_board()
        self.screen.blit(self.background, (0,0))

        mainloop = True



        while mainloop:
            self.event_queue = self.queueing_events(pygame.event.get(), self.event_queue)
            if self.event_queue is False:
                mainloop = False

            if self.event_queue:
                if self.event_queue[0] == 'space':
                    if self.state == 'running':
                        self.state == 'paused'
                        self.snake_clock.pause()

                    elif self.state == 'paused':
                        self.state == 'running'
                        self.snake_clock.unpause()

                    elif self.state == 'game over':
                        self.state = 'running'


            if self.snake_clock.should_update():
                if self.state == 'running':
                    if self.event_queue:
                        self.event_queue, self.snake_dir, self.previous_pos = \
                            self.update(self.event_queue, directions, self.previous_pos)
                    if self.food_lst == []:
                        self.food_lst = self.generate_food(self.food_lst, self.snake)

                    self.snake, self.food_lst = self.update_snake(self.snake, self.snake_dir, self.food_lst)
                if self.is_dead(self.snake):
                    self.state = 'game over'

            if self.render_clock.should_update():
                self.playground.fill((0,0,0))
                self.clock.tick()
                if self.state == 'running':
                    self.blit_squares(self.snake, 'fg')
                    self.blit_squares(self.food_lst, 'fg')

                elif self.state == 'game over':
                    self.blit_text('game over', 'press space to continue', 'fg')

                playtime = time.monotonic() - self.game_started
                text = 'FPS: {0:.2f}, Playtime: {1:.2f}'.format(self.clock.get_fps(), playtime)
                pygame.display.set_caption(text)
                pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    PygView().run()
