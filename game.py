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

        print(self.world.colliders)

        weapon = Weapon(self.world, "diamondSword_", "sword_projectile", 1.25, 500, 1)
        self.player = Player(self.world, "fungant_", weapon, (150, 100), 5, 1)

    def update(self):
        self.world.all_sprites.update()
        # for entity in self.world.entities:
        #     if entity == self.player:
        #         continue
        #     entity.attack(self.player.pos)
        self.player.set_cam_prefs(*self.world.get_prefs())

    def draw(self, surface: pygame.Surface):
        # surface.fill(pygame.Color("black"))
        # self.map.draw(surface)
        # self.all_sprites.draw(surface)
        self.world.center(self.player)
        self.world.draw(surface)
