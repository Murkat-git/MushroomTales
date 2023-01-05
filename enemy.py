import pygame
from pygame.sprite import AbstractGroup

from entity import Entity


class Enemy(Entity):
    def __init__(self, entity_type, weapon, pos, hp, speed, *groups: AbstractGroup) -> None:
        super().__init__(entity_type, weapon, pos, hp, speed, *groups)
        self.obstacle_data = None

    def set_obstacle_data(self, obstacle_data):
        self.obstacle_data = obstacle_data

    
