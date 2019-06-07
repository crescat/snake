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
        self.event_update_clock = Clock(3)
        self.snake_clock = Clock(3)
        self.clock = pygame.time.Clock()

        self.game_started = time.monotonic()
        self.program_started = time.monotonic()


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


    def update(self, event_queue):
        directions = {'up':(0,-1), 'down':(0,1), 'left':(-1, 0), 'right':(1,0)}
        event = event_queue[0]
        return event_queue[1:], directions[event]


    def update_snake(self, snake, dx, dy):
        new_head = (snake[0][0] + dx, snake[0][1] + dy)
        return [new_head] + snake[:-1]


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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if event_queue == []:
                    event_queue.append(what_direction(event))

                else:
                    direction = what_direction(event)
                    if event_queue[-1] != oppo_direction[direction] and \
                       event_queue[-1] != direction:
                        event_queue.append(direction)

        return event_queue


    def run(self):
        self.paint_board()
        self.screen.blit(self.background, (0,0))

        mainloop = True
        event_queue = []
        snake = [(BOARD_COL//2, BOARD_ROW//2)]
        topleft_x = WINDOW_PADDING + BORDER - 1
        topleft_y = WINDOW_PADDING + BORDER + HEADER - 1
        dx, dy = 1, 0
        snake_speed = 1 # cell per sec
        game_speed = 60


        while mainloop:
            event_queue = self.queueing_events(pygame.event.get(), event_queue)
            if event_queue is False:
                mainloop = False

            if self.event_update_clock.should_update() and event_queue:
                event_queue, (dx, dy) = self.update(event_queue)

            if self.snake_clock.should_update():
                snake = self.update_snake(snake, dx, dy)

            if self.render_clock.should_update():
                self.clock.tick()
                for x, y in snake:
                    pygame.draw.rect(self.playground, PALLETE['fg'],
                                    (SNAKE_WIDTH*x, SNAKE_WIDTH*y,
                                    SNAKE_WIDTH, SNAKE_WIDTH))

                self.screen.blit(self.playground, (topleft_x, topleft_y))
                self.playground.fill((0,0,0))
                playtime = time.monotonic() - self.game_started

                text = 'FPS: {0:.2f}, Playtime: {1:.2f}'.format(self.clock.get_fps(), playtime)
                pygame.display.set_caption(text)
                pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    PygView().run()
