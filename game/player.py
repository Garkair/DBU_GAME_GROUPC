# ─────────────────────────────────────────────────────────────
#  player.py
# ─────────────────────────────────────────────────────────────
import pygame
from .constants import *
from .sprites import make_player_sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frame          = 0
        self.frame_timer    = 0
        self.facing_right   = True
        self._rebuild_image()
        self.rect           = self.image.get_rect(topleft=(x, y))
        self.vel_x          = 0.0
        self.vel_y          = 0.0
        self.on_ground      = False
        self.lives          = PLAYER_MAX_LIVES
        self.score          = 0
        self.invincible     = 0          # countdown frames
        self.dead           = False
        self.chips_collected = 0

    # ── image ──────────────────────────────────────────────
    def _rebuild_image(self):
        raw = make_player_sprite(self.frame)
        if not self.facing_right:
            raw = pygame.transform.flip(raw, True, False)
        self.image = raw

    def _animate(self, moving):
        self.frame_timer += 1
        if moving and self.frame_timer >= 8:
            self.frame = (self.frame + 1) % 4
            self.frame_timer = 0
        elif not moving:
            self.frame = 0

    # ── update ─────────────────────────────────────────────
    def update(self, platforms):
        keys = pygame.key.get_pressed()

        # Horizontal
        self.vel_x = 0
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x      = -PLAYER_SPEED
            self.facing_right = False
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x      = PLAYER_SPEED
            self.facing_right = True
            moving = True

        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y  = JUMP_FORCE
            self.on_ground = False

        # Gravity
        self.vel_y = min(self.vel_y + GRAVITY, 16)

        # Move X + collide
        self.rect.x += int(self.vel_x)
        self._collide_x(platforms)

        # Move Y + collide
        self.rect.y += int(self.vel_y)
        self.on_ground = False
        self._collide_y(platforms)

        # Animate
        self._animate(moving)
        self._rebuild_image()
        # keep image rect synced
        old_topleft = self.rect.topleft
        self.image = self.image  # already set in _rebuild_image
        self.rect.topleft = old_topleft

        # Invincibility countdown
        if self.invincible > 0:
            self.invincible -= 1

    # ── collision helpers ──────────────────────────────────
    def _collide_x(self, platforms):
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                elif self.vel_x < 0:
                    self.rect.left = p.rect.right
                self.vel_x = 0

    def _collide_y(self, platforms):
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground   = True
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom
                self.vel_y = 0

    # ── take hit ───────────────────────────────────────────
    def hit(self):
        if self.invincible > 0:
            return
        self.lives -= 1
        self.invincible = INVINCIBILITY_FRAMES
        if self.lives <= 0:
            self.dead = True

    # ── draw (with flicker when invincible) ───────────────
    def draw(self, surface, camera_x):
        if self.invincible > 0 and (self.invincible // 6) % 2 == 0:
            return  # flicker
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))
