# ─────────────────────────────────────────────────────────────
#  collectibles.py
# ─────────────────────────────────────────────────────────────
import pygame
from .constants import *
from .sprites import make_access_chip, make_patriot_token, make_exit


class AccessChip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frame       = 0
        self.frame_timer = 0
        self.image = make_access_chip(self.frame)
        self.rect  = self.image.get_rect(center=(x, y))
        self.collected = False

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= 2:
            self.frame = (self.frame + 1) % 40
            self.frame_timer = 0
        self.image = make_access_chip(self.frame)

    def draw(self, surface, camera_x):
        if not self.collected:
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))


class PatriotToken(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frame       = 0
        self.frame_timer = 0
        self.image = make_patriot_token(self.frame)
        self.rect  = self.image.get_rect(center=(x, y))
        self.collected = False

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= 2:
            self.frame = (self.frame + 1) % 30
            self.frame_timer = 0
        self.image = make_patriot_token(self.frame)

    def draw(self, surface, camera_x):
        if not self.collected:
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))


class ExitPortal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frame       = 0
        self.frame_timer = 0
        self.active      = False   # only opens when all chips collected
        self.image = make_exit(self.frame)
        self.rect  = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= 3:
            self.frame = (self.frame + 1) % 60
            self.frame_timer = 0
        self.image = make_exit(self.frame)

    def draw(self, surface, camera_x):
        col = C_EXIT if self.active else (80, 80, 80)
        # dim overlay when inactive
        img = self.image.copy()
        if not self.active:
            overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            img.blit(overlay, (0, 0))
        surface.blit(img, (self.rect.x - camera_x, self.rect.y))
        # label
        font = pygame.font.SysFont("Arial", 11, bold=True)
        label = font.render("EXIT" if self.active else "LOCKED", True, C_WHITE)
        surface.blit(label, (self.rect.x - camera_x + 20, self.rect.y - 16))
