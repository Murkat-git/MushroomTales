import pygame
from pygame.sprite import AbstractGroup


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, speed, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        image = pygame.surface.Surface((24, 24))
        image.fill(pygame.Color("gray"))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.direction = pygame.Vector2()
        self.speed = speed

    def update(self):
        self.move()

    def set_velocity_x(self, val):
        self.direction.x = val

    def set_velocity_y(self, val):
        self.direction.y = val

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

