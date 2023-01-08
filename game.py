import pygame
from map import Map
from entity import Entity
from player import Player
from world import World
from weapon import Weapon


class Game:
    def __init__(self, map_path):
        # self.map = Map(map_path)
        self.map_path = map_path
        self.world = World(map_path)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

    def update(self):
        if self.world.player.alive():
            self.world.all_sprites.update()
            self.world.player.set_cam_prefs(*self.world.get_prefs())

    def draw(self, surface: pygame.Surface):
        self.world.center(self.world.player)
        self.world.draw(surface)
        hp_text = self.font.render(f"Здоровье: {self.world.player.hp}", False, (255, 255, 255))
        surface.blit(hp_text, (0, 0))
        if not self.world.player.alive():
            text = self.font.render("Вы проиграли!", False, (255, 255, 255))
            text2 = self.font.render("Нажмите пробел для перезапуска.", False, (255, 255, 255))
            surface.blit(text, (0, 60))
            surface.blit(text2, (0, 90))
        elif len(self.world.entities.sprites()) == 1:
            text = self.font.render("Вы победили!", False, (255, 255, 255))
            text2 = self.font.render("Нажмите пробел для перезапуска.", False, (255, 255, 255))
            surface.blit(text, (0, 60))
            surface.blit(text2, (0, 90))
