from typing import Any

import pygame
import math
from pygame.sprite import AbstractGroup

PATH = "data/Spritesheets/Projectiles/"


class Projectile(pygame.sprite.Sprite):
    def __init__(self, world, parent, created_pos, target_pos, projectile_type, speed, lifetime,
                 dmg, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.world = world
        self.parent = parent
        self.add(self.world.all_sprites, self.world.projectiles)
        self.cx, self.cy = created_pos
        self.tx, self.ty = target_pos

        self.dmg = dmg

        rel_x, rel_y = self.cx - self.tx, self.ty - self.cy
        angle = math.degrees(math.atan2(rel_y, rel_x))
        angle += 90

        self.image = pygame.transform.rotate(pygame.image.load(f"{PATH}{projectile_type}.png"),
                                             angle)
        self.rect = self.image.get_rect()
        self.rect.center = created_pos
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.Vector2()
        self.direction.y = -speed
        self.direction.rotate_ip(-angle)

        self.created_time = pygame.time.get_ticks()
        self.lifetime = lifetime

    def update(self, *args: Any, **kwargs: Any) -> None:
        super().update(*args, **kwargs)
        self.collide()
        self.pos += self.direction
        self.rect.center = round(self.pos.x), round(self.pos.y)
        if pygame.time.get_ticks() > self.created_time + self.lifetime:
            self.kill()

    def collide(self):
        collided_entities = pygame.sprite.spritecollide(self, self.world.entities, False, pygame.sprite.collide_mask)
        for entity in collided_entities:
            if type(entity) == type(self.parent):
                return
            entity.hurt(self.dmg)
            self.kill()
