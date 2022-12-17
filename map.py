import pygame
import pytmx
from pygame.sprite import AbstractGroup
from pytmx.util_pygame import load_pygame


class AnimatedTile(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup) -> None:
        super().__init__(*groups)


class Map:
    def __init__(self, filename):
        self.tmx_data = load_pygame(filename)
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tilewidth

    def get_map_data(self):
        return self.tmx_data

    def draw(self, surface: pygame.Surface):
        for layer in self.tmx_data.visible_layers:
            offsetx = layer.offsetx
            offsety = layer.offsety
            for x, y, tile in layer.tiles():
                surface.blit(tile, (x * self.tile_width + offsetx, y * self.tile_height + offsety))
