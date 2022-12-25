import pygame
import math
from pygame.sprite import AbstractGroup
from projectile import Projectile

PATH = "data/Spritesheets/Weapons/"
STEP = -5


class Weapon(pygame.sprite.Sprite):
    def __init__(self, weapon_type, projectile_type, projectile_speed, projectile_lifetime,
                 *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.og_image = pygame.image.load(f"{PATH}{weapon_type}.png")
        self.image = self.og_image
        self.attacking = False
        self.state = None
        self.step = STEP
        # self.image = pygame.transform.scale(self.image, (6, 24))
        self.rect = self.image.get_rect()
        self.degrees = 0

        self.projectile_type = projectile_type
        self.projectile_speed = projectile_speed
        self.projectile_lifetime = projectile_lifetime

    def flip(self):
        self.step *= -1
        self.degrees *= -1

    def animate(self):
        if self.state is None:
            return
        if self.state == 1:
            self.degrees += self.step
            if abs(self.degrees) <= 90:
                self.image = pygame.transform.rotate(self.og_image, self.degrees)
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.state = 2
        elif self.state == 2:
            self.degrees -= self.step
            if abs(self.degrees) != 0:
                self.image = pygame.transform.rotate(self.og_image, self.degrees)
                self.rect = self.image.get_rect(center=self.rect.center)
            else:
                self.image = self.og_image
                self.state = None

    def update(self):
        self.animate()

    def attack(self, coords, attack_coords):
        if self.state is not None:
            return
        self.state = 1
        self.degrees = 0

        projectile = Projectile(coords, attack_coords, self.projectile_type, self.projectile_speed,
                                self.projectile_lifetime)
        projectile.add(*self.groups())

    def set_pos(self, pos):
        self.rect.midbottom = pos
