import pygame
pygame.init()

screen = pygame.display.set_mode((680, 480))
background = pygame.Surface(screen.get_size())
background.fill((255,0,0))
background = background.convert()

screen.blit(background, (0, 0))
clock = pygame.time.Clock()

mainloop = True
FPS = 60
playtime = 0.0

while mainloop:
    milliseconds = clock.tick(FPS)
    playtime += milliseconds / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
    
    text = 'FPS: {0:.2f}, Playtime: {1:.2f}'.format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    pygame.display.flip()

pygame.quit()

print("This game was played for {0:.2f} seconds".format(playtime))