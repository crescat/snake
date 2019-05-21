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
FPS = 5

PALLETE = {
    'fg': (255, 255, 255),
    'bg': (0, 0, 0)
}

class PygView(object):

    def __init__(self):               
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        pygame.font.init()
        self.bigfont = pygame.font.SysFont('Arial', BIG_FONT)
        self.smallfont = pygame.font.SysFont('Arial', SMALL_FONT)
        self.scorefont = pygame.font.SysFont('Arial', SCORE_FONT)
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


    def run(self):
        self.paint_board()
        self.screen.blit(self.background, (0,0))
        mainloop = True
        state = 'running'
        topleft_x = WINDOW_PADDING + BORDER - 1
        topleft_y = WINDOW_PADDING + BORDER + HEADER - 1
        snake = [(BOARD_COL//2, BOARD_ROW//2)]
        food = []
        dx = 1
        dy = 0
        while mainloop:

            milliseconds = self.clock.tick(self.fps)
            self.totalplaytime += milliseconds / 1000.0
            self.playtime += milliseconds / 1000.0

            if state == 'game over':
                dx, dy = 0, 0
                snake = []

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False
                    if state == 'running':
                        if event.key == pygame.K_UP:
                            if (dx, dy) != (0, 1):
                                dx, dy = 0, -1
                        elif event.key == pygame.K_DOWN:
                            if (dx, dy) != (0, -1):
                                dx, dy = 0, 1
                        elif event.key == pygame.K_LEFT:
                            if (dx, dy) != (1, 0):
                                dx, dy = -1, 0
                        elif event.key == pygame.K_RIGHT:
                            if (dx, dy) != (-1, 0):
                                dx, dy = 1, 0
                        elif event.key == pygame.K_SPACE:
                                previous_dxy = (dx, dy)
                                dx, dy = 0, 0
                                state = 'pause'

                    elif state == 'pause':
                        if event.key == pygame.K_SPACE:
                            dx, dy = previous_dxy
                            state = 'running'

                    elif state == 'game over':                     
                        if event.key == pygame.K_SPACE:
                            snake = [(BOARD_COL//2, BOARD_ROW//2)]
                            dx, dy = 1, 0
                            food = []
                            self.playtime = 0.0
                            state = 'running'
            

            if state == 'game over':
                
                gameover = self.bigfont.render('Game over', False, PALLETE['fg'])
                cont = self.smallfont.render('Press space to restart',
                                          False, PALLETE['fg'])
                gameover_rect = gameover.get_rect( \
                    center=(self.board_width/2, self.board_height/2 - BIG_FONT))
                cont_rect = cont.get_rect( \
                    center=(self.board_width/2, self.board_height/2))

                self.playground.blit(gameover, gameover_rect)
                self.playground.blit(cont, cont_rect)
                self.screen.blit(self.playground, (topleft_x, topleft_y))


            elif state == 'pause':
                pausetext = self.bigfont.render('Paused',
                                False, PALLETE['fg'])
                cont = self.smallfont.render('Press space to continue',
                                          False, PALLETE['fg'])

                pausetext_rect = pausetext.get_rect( \
                    center=(self.board_width/2, self.board_height/2 - BIG_FONT))
                cont_rect = cont.get_rect( \
                    center=(self.board_width/2, self.board_height/2))

                self.playground.blit(pausetext, pausetext_rect)
                self.playground.blit(cont, cont_rect)
                self.screen.blit(self.playground, (topleft_x, topleft_y))


            elif state == 'running':
                empty_space = [(a, b) for a in range(BOARD_COL)
                               for b in range(BOARD_ROW)
                               if (a, b) not in snake]
                if food == []:
                    number = random.randint(0, len(empty_space)-1)
                    food += [empty_space[number]]

                new_head = (snake[0][0] + dx, snake[0][1] + dy)

                if new_head in snake:
                    print(111)
                    state = 'game over'
                if new_head[0] < 0 or new_head[0] >= BOARD_COL:
                    state = 'game over'
                if new_head[1] < 0 or new_head[1] >= BOARD_ROW:
                    state = 'game over'   


                if new_head in food:
                    snake = [new_head] + snake
                    food = []
                else:
                    snake = [new_head] + snake[:-1]


                for x, y in food:
                    pygame.draw.rect(self.playground, PALLETE['fg'],
                                    (SNAKE_WIDTH*x, SNAKE_WIDTH*y,
                                    SNAKE_WIDTH, SNAKE_WIDTH))

                for x, y in snake:
                    pygame.draw.rect(self.playground, PALLETE['fg'],
                                    (SNAKE_WIDTH*x, SNAKE_WIDTH*y,
                                    SNAKE_WIDTH, SNAKE_WIDTH))
                self.screen.blit(self.playground, (topleft_x, topleft_y))
                self.playground.fill((0,0,0))

                score = len(snake) - 1
                self.scoreboard.fill(PALLETE['bg'])
                score = self.scorefont.render('Score:{}'.format(str(score)),
                                            False, PALLETE['fg'])
                score_rect = score.get_rect( \
                        center=(self.scoreboard.get_width()/2,
                                self.scoreboard.get_height()/2))
                self.scoreboard.blit(score, score_rect)
                self.screen.blit(self.scoreboard,
                                (topleft_x, WINDOW_PADDING + BORDER -1))

                self.timeboard.fill(PALLETE['bg'])
                time = self.scorefont.render('Time:{}'.format(int(self.playtime)),
                                            False, PALLETE['fg'])
                time_rect = time.get_rect( \
                        center=(self.timeboard.get_width()/2,
                                self.timeboard.get_height()/2))
                self.timeboard.blit(time, time_rect)
                self.screen.blit(self.timeboard,
                                (self.width // 2 + 1, WINDOW_PADDING + BORDER -1))

            text = 'FPS: {0:.2f}, Playtime: {1:.2f}'.format(self.clock.get_fps(), self.playtime)
            pygame.display.set_caption(text)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    PygView().run()