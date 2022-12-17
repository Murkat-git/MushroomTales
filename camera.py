import pygame
import pytmx
import pyscroll
from pytmx.util_pygame import load_pygame


class Camera:
    def __init__(self, map_path):
        self.tmx_data = load_pygame(map_path)

        self.map_layer = pyscroll.BufferedRenderer(
            data=pyscroll.data.TiledMapData(self.tmx_data),
            size=(500, 500),
            clamp_camera=True,
        )
        self.map_layer.zoom = 2.5
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)

    def get_group(self):
        return self.group

    def draw(self, surface):
        self.group.draw(surface)

    def center(self, sprite):
        self.group.center(sprite.rect.center)

    def add(self, sprite):
        self.group.add(sprite)
