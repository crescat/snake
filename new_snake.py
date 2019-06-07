import pygame
import random

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
        self.clock = pygame.time.Clock()
        self.scoreboard = pygame.Surface(((BOARD_COL*SNAKE_WIDTH - BORDER+1)//2,
                                          HEADER - BORDER))
        self.timeboard = pygame.Surface(((BOARD_COL*SNAKE_WIDTH - BORDER+1)//2,
                                          HEADER - BORDER))
        self.fps = FPS
        self.totalplaytime = 0.0
        self.playtime = 0.0


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


    def update(self, event_queue, dx, dy):
        pass



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
        dx, dy = 1, 0

        while mainloop:

            milliseconds = self.clock.tick(self.fps)
            self.totalplaytime += milliseconds / 1000.0
            self.playtime += milliseconds / 1000.0

            event_queue = self.queueing_events(pygame.event.get(), event_queue)
            if event_queue is False:
                mainloop = False

            print(event_queue)




            text = 'FPS: {0:.2f}, Playtime: {1:.2f}'.format(self.clock.get_fps(), self.playtime)
            pygame.display.set_caption(text)
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    PygView().run()
