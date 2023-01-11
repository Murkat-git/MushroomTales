import pygame
import pytmx
import pyscroll
from pytmx.util_pygame import load_pygame
from generator import Generator
from enemy import Enemy
from player import Player
from weapon import Weapon
from stats import ENEMY_STATS, WEAPONS_STATS, PLAYER_STATS

DEBUG = False


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
            entity_type = self.tmx_data.get_tile_properties_by_gid(gid)["type"]
            if entity_type == "player_":
                player_hp = PLAYER_STATS["hp"]
                player_speed = PLAYER_STATS["speed"]
                player_weapon_type = PLAYER_STATS["weapon"]
                projectile_type = WEAPONS_STATS[player_weapon_type]["projectile_type"]
                projectile_speed = WEAPONS_STATS[player_weapon_type]["projectile_speed"]
                projectile_lifetime = WEAPONS_STATS[player_weapon_type]["projectile_lifetime"]
                weapon_dmg = WEAPONS_STATS[player_weapon_type]["dmg"]
                entity_weapon = Weapon(self, player_weapon_type, projectile_type, projectile_speed, projectile_lifetime, weapon_dmg)
                self.player = Player(self, entity_weapon, (x * tile_size, y * tile_size), player_hp, player_speed)
            else:
                enemy_hp = ENEMY_STATS[entity_type]['hp']
                enemy_speed = ENEMY_STATS[entity_type]['speed']
                enemy_weapon_type = ENEMY_STATS[entity_type]['weapon']
                projectile_type = WEAPONS_STATS[enemy_weapon_type]["projectile_type"]
                projectile_speed = WEAPONS_STATS[enemy_weapon_type]["projectile_speed"]
                projectile_lifetime = WEAPONS_STATS[enemy_weapon_type]["projectile_lifetime"]
                weapon_dmg = WEAPONS_STATS[enemy_weapon_type]["dmg"]
                entity_weapon = Weapon(self, enemy_weapon_type, projectile_type, projectile_speed, projectile_lifetime, weapon_dmg)
                Enemy(self, entity_type, entity_weapon, (x * tile_size, y * tile_size), enemy_hp, enemy_speed)
            print(x, y, gid, "entity")


    def get_group(self):
        return self.all_sprites

    def draw(self, surface):
        self.all_sprites.draw(surface)
        if DEBUG:
            for i in self.entities.sprites() + self.projectiles.sprites():
                x, y = self.map_layer.translate_point((i.rect.topleft))
                surface.blit(
                    i.mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)),
                    (x, y))

    def center(self, sprite):
        self.all_sprites.center(sprite.rect.center)

    def add(self, sprite):
        self.all_sprites.add(sprite)

    def get_prefs(self):
        return self.map_layer.get_center_offset(), self.map_layer._real_ratio_x, self.map_layer._real_ratio_y

    def get_colliders(self):
        return self.colliders
