import pygame
import os
from pygame.sprite import AbstractGroup


class Entity(pygame.sprite.Sprite):
    def __init__(self, entity_type, pos, speed, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        image = pygame.image.load(f"data/Spritesheets/{entity_type}/idle/0.png")
        self.image = image
        self.rect = self.image.get_rect()

        self.is_flipped_x = False
        self.frames = dict()
        self.load_frames(entity_type)
        self.status = "idle"
        self.anim_counter = 0
        self.frame_id = 0

        self.rect.topleft = pos
        self.direction = pygame.Vector2()
        self.speed = speed

    def load_frames(self, entity_type):
        self.frames = dict()
        path = f"data/Spritesheets/{entity_type}"
        for status in os.listdir(path):
            if status not in self.frames:
                self.frames[status] = []
            for frame in os.listdir(f"{path}/{status}"):
                self.frames[status].append(pygame.image.load(f"{path}/{status}/{frame}"))
        print(self.frames)

    def change_status(self, new_status):
        if self.status == new_status:
            return
        self.status = new_status
        self.frame_id = 0
        self.anim_counter = 0

    def check_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.change_status("idle")
        elif self.status != "walk":
            self.change_status("walk")

    def animate(self):
        self.anim_counter += self.speed
        if self.anim_counter % 10 == 0:
            self.frame_id += 1
            self.frame_id %= len(self.frames[self.status])
            self.image = pygame.transform.flip(self.frames[self.status][self.frame_id],
                                               self.is_flipped_x, False)

    def update(self):
        self.animate()
        self.move()

    def flip_x(self):
        self.is_flipped_x = not self.is_flipped_x
        self.image = pygame.transform.flip(self.image, True, False)

    def set_velocity_x(self, val):
        self.direction.x = val
        if (self.is_flipped_x and self.direction.x > 0)\
                or (not self.is_flipped_x and self.direction.x < 0):
            self.flip_x()
        self.check_status()

    def set_velocity_y(self, val):
        self.direction.y = val
        self.check_status()

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
