import pygame

class PygView(object):

    def __init__(self, width=400, height=300, fps=5):               
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0,0,0))
        self.clock = pygame.time.Clock()
        self.fps = 5
        self.playtime = 0.0

    def paint(self):
        pygame.draw.rect(self.background, (255,255,255), (20, 20, 20, 20), 3)
        myball = Ball()
        myball.blit(self.background)


    def run(self):
        self.paint()
        mainloop = True
        while mainloop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False

            milliseconds = self.clock.tick(self.fps)
            self.playtime += milliseconds / 1000.0
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0)) 

            text = 'FPS: {0:.2f}, Playtime: {1:.2f}'.format(self.clock.get_fps(), self.playtime)
            pygame.display.set_caption(text)
            pygame.display.flip()
        pygame.quit()


class Ball(object):
    def __init__(self, radius = 50, color=(0,0,255), x=320, y=240):
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        self.surface = pygame.Surface((2*self.radius,2*self.radius))    
        
        pygame.draw.circle(self.surface, color, (radius, radius), radius)
        self.surface = self.surface.convert() 
        
    def blit(self, background):
        background.blit(self.surface, (self.x, self.y))


if __name__ == '__main__':
    PygView().run()