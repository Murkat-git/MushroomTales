import pygame
from entity import Entity


class Player(Entity):
    def get_controls(self):
        keys = pygame.key.get_pressed()
        vel_x = 0
        vel_y = 0
        if keys[pygame.K_UP]:
            vel_y = -1
        if keys[pygame.K_DOWN]:
            vel_y = 1
        if keys[pygame.K_LEFT]:
            vel_x = -1
        if keys[pygame.K_RIGHT]:
            vel_x = 1
        self.set_velocity_x(vel_x)
        self.set_velocity_y(vel_y)

    def update(self):
        self.get_controls()
        super().update()

