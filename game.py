import pygame
from map import Map
from entity import Entity
from player import Player
from camera import Camera


class Game:
    def __init__(self, map_path):
        # self.map = Map(map_path)
        self.camera = Camera(map_path)
        self.all_sprites = self.camera.get_group()
        self.player = Player("fungant_", (50, 50), 1)
        self.all_sprites.add(self.player)

    def update(self):
        self.player.update()

    def draw(self, surface: pygame.Surface):
        # surface.fill(pygame.Color("black"))
        # self.map.draw(surface)
        # self.all_sprites.draw(surface)
        self.camera.center(self.player)
        self.camera.draw(surface)