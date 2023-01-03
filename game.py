import pygame
from map import Map
from entity import Entity
from player import Player
from world import World
from weapon import Weapon


class Game:
    def __init__(self, map_path):
        # self.map = Map(map_path)
        self.world = World(map_path)
        self.all_sprites = self.world.get_group()
        self.entities = pygame.sprite.Group()

        weapon = Weapon("diamondSword_", "sword_projectile", 1.25, 500)
        self.player = Player("fungant_", weapon, (150, 100), 20, 1)
        entit_weapon = Weapon("woodenSword_", "attack_wave", 1, 500)
        self.entit = Entity("fungant_", entit_weapon, (150, 150), 20, 1)
        self.player.add(self.all_sprites)
        self.entit.add(self.all_sprites)

    def update(self):
        self.all_sprites.update()
        self.player.set_cam_prefs(*self.world.get_prefs())

    def draw(self, surface: pygame.Surface):
        # surface.fill(pygame.Color("black"))
        # self.map.draw(surface)
        # self.all_sprites.draw(surface)
        self.world.center(self.player)
        self.world.draw(surface)
