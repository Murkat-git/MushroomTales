import pygame
import pytmx
import pyscroll
from pytmx.util_pygame import load_pygame
from generator import Generator
from entity import Entity
from weapon import Weapon


class World:
    def __init__(self, map_path):
        # self.tmx_data = load_pygame(map_path)
        gen = Generator(map_path)
        self.tmx_data = gen.generate(5)

        self.map_layer = pyscroll.BufferedRenderer(
            data=pyscroll.data.TiledMapData(self.tmx_data),
            size=(500, 500),
            clamp_camera=False,
        )

        self.map_layer.zoom = 3
        self.all_sprites = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

        self.entities = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        tile_colliders = dict()
        for gid, colliders in self.tmx_data.get_tile_colliders():
            tile_colliders[gid] = colliders[0]

        tile_size = self.tmx_data.tilewidth
        self.colliders = []
        for layer in self.tmx_data.layers:
            if type(layer) != pytmx.TiledTileLayer:
                continue
            for x, y, gid in layer:
                if gid in tile_colliders:
                    collider = tile_colliders[gid]
                    rect = pygame.Rect(collider.x, collider.y, collider.width, collider.height)
                    rect = rect.move(x * tile_size, y * tile_size)
                    self.colliders.append(rect)

        for x, y, gid in self.tmx_data.get_layer_by_name("Entities"):
            if gid == 0:
                continue
            entity_weapon = Weapon(self, "diamondSword_", "sword_projectile", 1.25, 500, 1)
            entity_type = self.tmx_data.get_tile_properties_by_gid(gid)["type"]
            Entity(self, entity_type, entity_weapon, (x * tile_size, y * tile_size), 3, 1)
            print(x, y, gid, "entity")

    def get_group(self):
        return self.all_sprites

    def draw(self, surface):
        self.all_sprites.draw(surface)

    def center(self, sprite):
        self.all_sprites.center(sprite.rect.center)

    def add(self, sprite):
        self.all_sprites.add(sprite)

    def get_prefs(self):
        return self.map_layer.get_center_offset(), self.map_layer._real_ratio_x, self.map_layer._real_ratio_y

    def get_colliders(self):
        return self.colliders
