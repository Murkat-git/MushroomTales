import pygame
from pygame.sprite import AbstractGroup

from entity import Entity

DETECTION_RADIUS = 60
STOP_RADIUS = 15
ATTACK_RADIUS = 45


class Enemy(Entity):
    def decide(self):
        player_pos = pygame.Vector2(self.world.player.hitbox.center)
        dist = pygame.Vector2(player_pos - self.pos)
        dx, dy = 0, 0
        if dist.magnitude() <= ATTACK_RADIUS:
            self.attack(player_pos)
        if dist.magnitude() <= DETECTION_RADIUS:
            dx, dy = dist.normalize()
        if dist.magnitude() < STOP_RADIUS:
            dx, dy = 0, 0
        self.set_velocity_x(dx)
        self.set_velocity_y(dy)

    def update(self):
        self.decide()
        super().update()

