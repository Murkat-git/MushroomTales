import pygame
import os
from pygame.sprite import AbstractGroup

PATH = "data/Spritesheets/Entities/"
WEAPON_OFFSET = -5


class Entity(pygame.sprite.Sprite):
    def __init__(self, world, entity_type, weapon, pos, hp, speed, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.world = world
        self.add(self.world.all_sprites, self.world.entities)

        self.is_flipped_x = False
        self.frames = dict()
        self.load_frames(entity_type)
        self.status = "idle"
        self.anim_counter = 0
        self.frame_id = 0
        self.frame_time = 10

        image = self.frames["idle"][0]
        self.image = image
        self.rect = self.image.get_rect()
        self.hitbox = self.image.get_bounding_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.offset = pygame.Vector2(self.rect.x - self.hitbox.x, self.rect.y - self.hitbox.y)

        self.pos = pygame.Vector2(pos)
        self.direction = pygame.Vector2()
        self.speed = speed

        self.weapon = weapon
        self.looking = "right"
        self.hp = hp

        self.hit_sound = pygame.mixer.Sound("data/sfx/hitHurt.wav")
        self.hit_sound.set_volume(0.5)
        self.death_sound = pygame.mixer.Sound("data/sfx/death.wav")
        self.death_sound.set_volume(0.3)

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
        self.frame_time = 10
        if new_status == "hurt":
            self.frame_time = 4
        elif new_status == "death":
            self.frame_time = 8

    def check_status(self):
        if self.status in ["hurt", "death"]:
            return
        if self.direction.x == 0 and self.direction.y == 0:
            self.change_status("idle")
        elif self.status != "walk":
            self.change_status("walk")

    def animate(self):
        num_frames = len(self.frames[self.status])
        self.anim_counter += self.speed
        if self.anim_counter >= self.frame_time:
            self.anim_counter = 0
            self.frame_id += 1
            if self.frame_id >= num_frames:
                if self.status == "hurt":
                    self.change_status("idle")
                elif self.status == "death":
                    self.kill()
            self.frame_id %= num_frames
            self.image = pygame.transform.flip(self.frames[self.status][self.frame_id],
                                               self.is_flipped_x, False)
            self.mask = pygame.mask.from_surface(self.image)
            # self.image.fill((255, 255, 255))

    def update(self):
        self.animate()
        self.display_weapon()
        if self.status not in ["hurt", "death"]:
            self.move()

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

        # self.pos += self.direction * self.speed
        self.pos.x += self.direction.x * self.speed
        self.hitbox.topleft = round(self.pos.x), round(self.pos.y)
        self.collide("horizontal")
        self.pos.x = self.hitbox.x

        self.pos.y += self.direction.y * self.speed
        self.hitbox.topleft = round(self.pos.x), round(self.pos.y)
        self.collide("vertical")
        self.pos.y = self.hitbox.y

        self.rect.topleft = self.pos + self.offset

    def collide(self, direction):
        ind = self.hitbox.collidelist(self.world.colliders)
        if ind == -1:
            return
        if direction == "horizontal":
            if self.direction.x > 0:
                self.hitbox.right = self.world.colliders[ind].left
            if self.direction.x < 0:
                self.hitbox.left = self.world.colliders[ind].right
        elif direction == "vertical":
            if self.direction.y > 0:
                self.hitbox.bottom = self.world.colliders[ind].top
            if self.direction.y < 0:
                self.hitbox.top = self.world.colliders[ind].bottom

    def display_weapon(self):
        x, y = self.rect.midbottom
        if self.looking == "left":
            self.weapon.set_pos((x - WEAPON_OFFSET, y))
        elif self.looking == "right":
            self.weapon.set_pos((x + WEAPON_OFFSET, y))

    def attack(self, coord):
        if self.hp > 0:
            self.weapon.attack(self.rect.center, coord, self)

    def hurt(self, dmg):
        if self.hp == 0:
            return
        self.hp -= dmg
        self.hit_sound.play()
        if self.hp <= 0:
            self.hp = 0
            self.death_sound.play()
            self.change_status("death")
        else:
            self.change_status("hurt")

    def kill(self) -> None:
        super().kill()
        self.weapon.kill()
