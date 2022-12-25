import pygame
import os
from pygame.sprite import AbstractGroup

PATH = "data/Spritesheets/Entities/"
WEAPON_OFFSET = -5


class Entity(pygame.sprite.Sprite):
    def __init__(self, entity_type, weapon, pos, hp, speed, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        image = pygame.image.load(f"{PATH}{entity_type}/idle/0.png")
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(pos)

        self.is_flipped_x = False
        self.frames = dict()
        self.load_frames(entity_type)
        self.status = "idle"
        self.anim_counter = 0
        self.frame_id = 0

        self.direction = pygame.Vector2()
        self.speed = speed

        self.weapon = weapon
        self.looking = "right"
        self.hp = hp

    def add(self, *groups: AbstractGroup) -> None:
        super().add(*groups)
        self.weapon.add(*groups)

    def load_frames(self, entity_type):
        self.frames = dict()
        path = f"{PATH}{entity_type}"
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
        num_frames = len(self.frames[self.status])
        self.anim_counter += self.speed
        if self.anim_counter >= 10:
            self.anim_counter = 0
            self.frame_id += 1
            self.frame_id %= num_frames
            self.image = pygame.transform.flip(self.frames[self.status][self.frame_id],
                                               self.is_flipped_x, False)

    def update(self):
        self.animate()
        self.move()
        self.display_weapon()

    def flip_x(self):
        self.is_flipped_x = not self.is_flipped_x
        self.weapon.flip()
        self.image = pygame.transform.flip(self.image, True, False)

    def set_velocity_x(self, val):
        self.direction.x = val
        if (self.is_flipped_x and self.direction.x > 0) \
                or (not self.is_flipped_x and self.direction.x < 0):
            self.flip_x()
        if val < 0:
            self.looking = "left"
        elif val > 0:
            self.looking = "right"
        self.check_status()

    def set_velocity_y(self, val):
        self.direction.y = val
        self.check_status()

    def move(self):
        # self.rect.x += self.direction.x * self.speed
        # self.rect.y += self.direction.y * self.speed
        self.pos += self.direction * self.speed
        self.rect.topleft = round(self.pos.x), round(self.pos.y)

    def display_weapon(self):
        x, y = self.rect.midbottom
        if self.looking == "left":
            self.weapon.set_pos((x - WEAPON_OFFSET, y))
        elif self.looking == "right":
            self.weapon.set_pos((x + WEAPON_OFFSET, y))

    def attack(self, coord):
        self.weapon.attack(self.rect.center, coord)

    def hurt(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()
