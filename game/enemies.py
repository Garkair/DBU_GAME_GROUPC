# ─────────────────────────────────────────────────────────────
#  enemies.py
# ─────────────────────────────────────────────────────────────
import pygame
from .constants import *
from .sprites import make_slow_student, make_fast_student, make_drone


class WalkingEnemy(pygame.sprite.Sprite):
    """Base class for ground-patrolling enemies."""
    SPEED = SLOW_STUDENT_SPEED

    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__()
        self.patrol_left  = patrol_left
        self.patrol_right = patrol_right
        self.vel_x        = self.SPEED
        self.vel_y        = 0.0
        self.on_ground    = False
        self.frame        = 0
        self.frame_timer  = 0
        self._build_image()
        self.rect = self.image.get_rect(topleft=(x, y))

    def _build_image(self):
        raise NotImplementedError

    def update(self, platforms):
        # Patrol
        if self.rect.left <= self.patrol_left:
            self.vel_x = abs(self.SPEED)
        elif self.rect.right >= self.patrol_right:
            self.vel_x = -abs(self.SPEED)

        # Gravity
        self.vel_y = min(self.vel_y + GRAVITY, 16)

        self.rect.x += int(self.vel_x)
        self.rect.y += int(self.vel_y)

        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y >= 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                else:
                    self.rect.top = p.rect.bottom
                self.vel_y = 0

        self.frame_timer += 1
        if self.frame_timer >= 10:
            self.frame = (self.frame + 1) % 4
            self.frame_timer = 0
        self._build_image()

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))


class SlowStudent(WalkingEnemy):
    SPEED = SLOW_STUDENT_SPEED

    def _build_image(self):
        raw = make_slow_student(self.frame)
        if self.vel_x < 0:
            raw = pygame.transform.flip(raw, True, False)
        self.image = raw


class FastStudent(WalkingEnemy):
    SPEED = FAST_STUDENT_SPEED

    def _build_image(self):
        raw = make_fast_student(self.frame)
        if self.vel_x < 0:
            raw = pygame.transform.flip(raw, True, False)
        self.image = raw


class FlyingDrone(pygame.sprite.Sprite):
    """Vertical patrol drone."""
    def __init__(self, x, y, patrol_top, patrol_bottom):
        super().__init__()
        self.patrol_top    = patrol_top
        self.patrol_bottom = patrol_bottom
        self.vel_y         = DRONE_SPEED
        self.frame         = 0
        self.frame_timer   = 0
        self._build_image()
        self.rect = self.image.get_rect(topleft=(x, y))

    def _build_image(self):
        self.image = make_drone(self.frame)

    def update(self, platforms):  # platforms unused for drone
        if self.rect.top <= self.patrol_top:
            self.vel_y = abs(DRONE_SPEED)
        elif self.rect.bottom >= self.patrol_bottom:
            self.vel_y = -abs(DRONE_SPEED)

        self.rect.y += int(self.vel_y)

        self.frame_timer += 1
        if self.frame_timer >= 4:
            self.frame = (self.frame + 1) % 8
            self.frame_timer = 0
        self._build_image()

    def draw(self, surface, camera_x):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y))
