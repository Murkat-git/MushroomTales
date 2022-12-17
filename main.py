import pygame
from game import Game

size = width, height = 500, 500
fps = 60

screen = pygame.display.set_mode(size)
pygame.display.set_caption("RPG")
clock = pygame.time.Clock()

game = Game("data/Tiled/maps/test_map.tmx")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.update()
    game.draw(screen)

    pygame.display.flip()
    clock.tick(fps)
pygame.quit()