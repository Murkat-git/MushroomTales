import pygame
from pygame.sprite import AbstractGroup
from entity import Entity


def convert_screen2world(coords, x_offset, y_offset, real_x_ratio, real_y_ratio):
    x, y = coords
    return x // real_x_ratio - x_offset, y // real_y_ratio - y_offset


PLAYER_ENTITY_TYPE = "fungant_"


class Player(Entity):
    def __init__(self, world, weapon, pos, hp, speed, *groups: AbstractGroup) -> None:
        super().__init__(world, PLAYER_ENTITY_TYPE, weapon, pos, hp, speed, *groups)
        self.x_offset, self.y_offset = 0, 0
        self.real_ratio_x, self.real_ratio_y = 1, 1

    def get_controls(self):
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = convert_screen2world(mouse_pos, self.x_offset, self.y_offset, self.real_ratio_x,
                                         self.real_ratio_y)
        if mouse[0]:
            self.attack(mouse_pos)

        keys = pygame.key.get_pressed()
        vel_x = 0
        vel_y = 0
        if keys[pygame.K_w]:
            vel_y = -1
        if keys[pygame.K_s]:
            vel_y = 1
        if keys[pygame.K_a]:
            vel_x = -1
        if keys[pygame.K_d]:
            vel_x = 1
        self.set_velocity_x(vel_x)
        self.set_velocity_y(vel_y)

    def set_cam_prefs(self, offset, real_ratio_x, real_ratio_y):
        self.x_offset, self.y_offset = offset
        self.real_ratio_x = real_ratio_x
        self.real_ratio_y = real_ratio_y

    def update(self):
        self.get_controls()
        super().update()
