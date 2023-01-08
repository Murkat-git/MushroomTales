import pygame


class Menu:
    def __init__(self):
        self.active = True
        self.img = pygame.image.load("data/menu2.png")

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.img.get_rect())

    def handle_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.active = False

    def is_active(self):
        return self.active
