import pygame
from menu import Menu
from game import Game

size = width, height = 500, 500
fps = 60

pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()

menu = Menu()
pygame.mixer.music.load("data/sfx/music.wav")
pygame.mixer.music.play(-1, fade_ms=3000)
while menu.is_active():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        menu.handle_event(event)
    menu.draw(screen)
    pygame.display.flip()

path = "data/Tiled/maps/generatortest.tmx"
game = Game(path)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                game = Game(path)

    game.update()
    game.draw(screen)

    pygame.display.flip()
    clock.tick(fps)
pygame.quit()