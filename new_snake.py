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
        event = event_queue[0]
        if oppo_direction[previous_pos] != event:
            return event_queue[1:], directions[event], event
        else:
            return event_queue[1:], directions[previous_pos], previous_pos


    def update_snake(self, snake, snake_dir, food_lst):
        dx, dy = snake_dir
        new_head = (snake[0][0] + dx, snake[0][1] + dy)

        if new_head in food_lst:
            i = food_lst.index(new_head)
            food_lst = food_lst[:i] + food_lst[i+1:]
            return [new_head] + snake, food_lst

        return [new_head] + snake[:-1], food_lst


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

                if event_queue == []:
                    event_queue.append(what_direction(event))

                elif event_queue and len(event_queue) <= 5:
                    direction = what_direction(event)
                    if event_queue[-1] != oppo_direction[direction] and \
                       event_queue[-1] != direction:
                        event_queue.append(direction)

        return event_queue


    def blit_squares(self, snake, color):
        topleft_x = WINDOW_PADDING + BORDER - 1
        topleft_y = WINDOW_PADDING + BORDER + HEADER - 1
        for (x, y) in snake:
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
                               if (a, b) not in snake]

        for _ in range(self.food_num):
            n = random.randint(0, len(empty_space)-1)
            food_lst += [empty_space[n]]
            empty_space = empty_space[:n] + empty_space[n+1:]

        return food_lst


    def run(self):
        directions = {'up':(0,-1), 'down':(0,1), 'left':(-1, 0), 'right':(1,0)}
        self.paint_board()
        self.screen.blit(self.background, (0,0))

        mainloop = True
        event_queue = []
        food_lst = []
        previous_pos = 'right'
        snake_dir = directions[previous_pos]
        snake = [(BOARD_COL//2, BOARD_ROW//2)]
        state = 'running'


        while mainloop:
            event_queue = self.queueing_events(pygame.event.get(), event_queue)
            if event_queue is False:
                mainloop = False

            if self.snake_clock.should_update():
                if state == 'running':
                    if event_queue:
                        event_queue, snake_dir, previous_pos = self.update(event_queue, directions, previous_pos)
                    if food_lst == []:
                        food_lst = self.generate_food(food_lst, snake)

                    snake, food_lst = self.update_snake(snake, snake_dir, food_lst)
                if self.is_dead(snake):
                    state = 'game over'

            if self.render_clock.should_update():
                self.playground.fill((0,0,0))
                self.clock.tick()
                if state == 'running':
                    self.blit_squares(snake, 'fg')
                    self.blit_squares(food_lst, 'fg')

                elif state == 'game over':
                    self.blit_text('game over', 'press space to continue', 'fg')

                playtime = time.monotonic() - self.game_started
                text = 'FPS: {0:.2f}, Playtime: {1:.2f}'.format(self.clock.get_fps(), playtime)
                pygame.display.set_caption(text)
                pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    PygView().run()
