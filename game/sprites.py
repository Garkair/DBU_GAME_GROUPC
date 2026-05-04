# ─────────────────────────────────────────────────────────────
#  sprites.py  –  procedural art (no external image files needed)
# ─────────────────────────────────────────────────────────────
import pygame
from .constants import *


def _surf(w, h, alpha=True):
    s = pygame.Surface((w, h), pygame.SRCALPHA if alpha else 0)
    return s


# ── Player ────────────────────────────────────────────────────
def make_player_sprite(frame=0):
    """Returns a 28×40 surface.  frame 0/2 = idle, 1/3 = walk"""
    s = _surf(28, 40)
    # body
    pygame.draw.rect(s, C_PATRIOT_BLUE, (6, 14, 16, 18))
    # head
    pygame.draw.ellipse(s, (230, 190, 150), (7, 2, 14, 14))
    # hair
    pygame.draw.rect(s, (80, 50, 20), (7, 2, 14, 5))
    # eyes
    pygame.draw.circle(s, C_BLACK, (11, 9), 2)
    pygame.draw.circle(s, C_BLACK, (17, 9), 2)
    pygame.draw.circle(s, C_WHITE, (12, 8), 1)
    pygame.draw.circle(s, C_WHITE, (18, 8), 1)
    # legs (animated)
    if frame % 2 == 0:
        pygame.draw.rect(s, (40, 40, 80), (7, 32, 6, 8))
        pygame.draw.rect(s, (40, 40, 80), (15, 32, 6, 8))
    else:
        pygame.draw.rect(s, (40, 40, 80), (5, 30, 6, 10))
        pygame.draw.rect(s, (40, 40, 80), (17, 34, 6, 6))
    # belt / badge
    pygame.draw.rect(s, C_ACCENT, (6, 26, 16, 3))
    pygame.draw.circle(s, C_TOKEN, (14, 27), 2)
    return s


# ── Slow Student enemy ────────────────────────────────────────
def make_slow_student(frame=0):
    s = _surf(26, 38)
    # body
    pygame.draw.rect(s, (160, 50, 50), (5, 14, 16, 16))
    # backpack
    pygame.draw.rect(s, (120, 30, 30), (17, 15, 6, 12))
    # head
    pygame.draw.ellipse(s, (220, 180, 140), (6, 2, 14, 13))
    pygame.draw.rect(s, (80, 80, 200), (6, 2, 14, 5))  # hat/hair
    # eyes – angry
    pygame.draw.line(s, C_BLACK, (8, 8), (12, 7), 2)
    pygame.draw.line(s, C_BLACK, (14, 7), (18, 8), 2)
    # legs
    if frame % 2 == 0:
        pygame.draw.rect(s, (80, 40, 40), (6, 30, 5, 8))
        pygame.draw.rect(s, (80, 40, 40), (15, 30, 5, 8))
    else:
        pygame.draw.rect(s, (80, 40, 40), (4, 28, 5, 10))
        pygame.draw.rect(s, (80, 40, 40), (17, 32, 5, 6))
    return s


# ── Fast Student enemy ────────────────────────────────────────
def make_fast_student(frame=0):
    s = _surf(26, 36)
    pygame.draw.rect(s, (200, 100, 20), (5, 14, 16, 14))
    pygame.draw.ellipse(s, (220, 180, 140), (6, 2, 13, 13))
    pygame.draw.rect(s, (50, 50, 50), (6, 2, 13, 5))
    # motion lines
    for i in range(3):
        pygame.draw.line(s, (255, 180, 80, 160), (-2 + i*3, 18+i*2), (4, 18+i*2), 1)
    if frame % 2 == 0:
        pygame.draw.rect(s, (100, 60, 10), (6, 28, 5, 8))
        pygame.draw.rect(s, (100, 60, 10), (15, 28, 5, 8))
    else:
        pygame.draw.rect(s, (100, 60, 10), (3, 26, 5, 10))
        pygame.draw.rect(s, (100, 60, 10), (18, 30, 5, 6))
    return s


# ── Flying Drone enemy ────────────────────────────────────────
def make_drone(frame=0):
    s = _surf(34, 28)
    # body
    pygame.draw.ellipse(s, (60, 60, 90), (7, 9, 20, 12))
    pygame.draw.ellipse(s, (100, 100, 140), (9, 11, 16, 8))
    # eye / sensor
    col = C_RED if frame % 2 == 0 else (255, 120, 0)
    pygame.draw.circle(s, col, (17, 15), 4)
    pygame.draw.circle(s, C_WHITE, (18, 14), 2)
    # rotors
    rot_off = frame * 6
    for angle_base in [0, 90, 180, 270]:
        import math
        a = math.radians(angle_base + rot_off)
        cx, cy = 17, 15
        rx = int(cx + 12 * math.cos(a))
        ry = int(cy + 8  * math.sin(a))
        pygame.draw.line(s, (180, 180, 200), (cx, cy), (rx, ry), 2)
        pygame.draw.circle(s, (200, 200, 220), (rx, ry), 3)
    return s


# ── Access Chip collectible ───────────────────────────────────
def make_access_chip(frame=0):
    s = _surf(22, 22)
    pulse = int(40 * abs((frame % 40) / 20 - 1))
    col = (0, 200 + pulse // 2, 200 + pulse // 2)
    pygame.draw.rect(s, col, (3, 3, 16, 16), border_radius=4)
    pygame.draw.rect(s, C_WHITE, (3, 3, 16, 16), 2, border_radius=4)
    # chip pattern
    pygame.draw.line(s, C_WHITE, (7, 3), (7, 6), 1)
    pygame.draw.line(s, C_WHITE, (11, 3), (11, 6), 1)
    pygame.draw.line(s, C_WHITE, (15, 3), (15, 6), 1)
    pygame.draw.line(s, C_WHITE, (7, 16), (7, 19), 1)
    pygame.draw.line(s, C_WHITE, (11, 16), (11, 19), 1)
    pygame.draw.line(s, C_WHITE, (15, 16), (15, 19), 1)
    pygame.draw.rect(s, (0, 100, 120), (7, 7, 8, 8))
    return s


# ── Patriot Token collectible ─────────────────────────────────
def make_patriot_token(frame=0):
    s = _surf(20, 20)
    pulse = int(30 * abs((frame % 30) / 15 - 1))
    pygame.draw.circle(s, (220 + pulse // 3, 180, 0), (10, 10), 9)
    pygame.draw.circle(s, (255, 230, 80), (10, 10), 9, 2)
    # P letter
    font = None  # drawn manually
    pygame.draw.rect(s, C_WHITE, (6, 5, 3, 10))
    pygame.draw.arc(s, C_WHITE, (8, 5, 6, 5), 0, 3.14, 2)
    return s


# ── Exit portal ───────────────────────────────────────────────
def make_exit(frame=0):
    s = _surf(TILE_SIZE * 2, TILE_SIZE * 2)
    pulse = int(50 * abs((frame % 60) / 30 - 1))
    col = (0, 200 + pulse // 2, 80)
    pygame.draw.ellipse(s, col, (4, 4, 72, 72))
    pygame.draw.ellipse(s, C_WHITE, (4, 4, 72, 72), 3)
    # arrows pointing right/up
    pygame.draw.polygon(s, C_WHITE, [(30, 45), (50, 30), (50, 38), (70, 38),
                                      (70, 22), (50, 22), (50, 30)])
    return s


# ── Tile surfaces ─────────────────────────────────────────────
def make_grass_tile():
    s = _surf(TILE_SIZE, TILE_SIZE, alpha=False)
    s.fill(C_DIRT)
    pygame.draw.rect(s, C_GRASS, (0, 0, TILE_SIZE, 10))
    for i in range(0, TILE_SIZE, 6):
        h = 4 + (i % 3) * 2
        pygame.draw.line(s, (30, 120, 30), (i, 0), (i + 1, -h), 2)
    return s


def make_stone_tile():
    s = _surf(TILE_SIZE, TILE_SIZE, alpha=False)
    s.fill(C_STONE)
    pygame.draw.rect(s, (90, 90, 110), (0, 0, TILE_SIZE, TILE_SIZE), 1)
    pygame.draw.line(s, (90, 90, 110), (0, 20), (TILE_SIZE, 20), 1)
    pygame.draw.line(s, (90, 90, 110), (20, 0), (20, 20), 1)
    pygame.draw.line(s, (90, 90, 110), (0, 20), (0, TILE_SIZE), 1)
    pygame.draw.line(s, (90, 90, 110), (TILE_SIZE // 2, 20), (TILE_SIZE // 2, TILE_SIZE), 1)
    return s


def make_shelf_tile():
    """Bookshelf tile – wood frame + 4 book spines that tile seamlessly."""
    s = _surf(TILE_SIZE, TILE_SIZE, alpha=False)
    # Wood backing
    s.fill(C_SHELF)
    # Top and bottom shelf boards (solid, connect across tiles)
    pygame.draw.rect(s, (100, 65, 25), (0, 0,          TILE_SIZE, 5))   # top board
    pygame.draw.rect(s, (100, 65, 25), (0, TILE_SIZE-5, TILE_SIZE, 5))   # bottom board
    # Side edge only on left so tiles join seamlessly on the right
    pygame.draw.rect(s, (80, 50, 15), (0, 0, 3, TILE_SIZE))
    # Book spines – taller to fill between boards
    book_colors = [
        (190, 40,  40),   # red
        ( 40, 90, 190),   # blue
        ( 40, 150, 60),   # green
        (190, 150, 20),   # yellow
    ]
    bw = (TILE_SIZE - 3) // len(book_colors)
    for i, c in enumerate(book_colors):
        bx = 3 + i * bw
        pygame.draw.rect(s, c, (bx, 5, bw - 1, TILE_SIZE - 10))
        # Highlight on spine top
        pygame.draw.rect(s, tuple(min(v+60,255) for v in c), (bx, 5, bw-1, 3))
        # Dark gap between books
        pygame.draw.rect(s, (30, 20, 10), (bx + bw - 1, 5, 1, TILE_SIZE - 10))
    return s


def make_metal_tile():
    s = _surf(TILE_SIZE, TILE_SIZE, alpha=False)
    s.fill(C_METAL)
    for i in range(0, TILE_SIZE, 8):
        pygame.draw.line(s, (100, 100, 120), (i, 0), (i, TILE_SIZE), 1)
    pygame.draw.rect(s, (60, 60, 80), (0, 0, TILE_SIZE, TILE_SIZE), 1)
    return s


def make_platform_tile():
    s = _surf(TILE_SIZE, TILE_SIZE // 2, alpha=False)
    s.fill(C_PLATFORM)
    pygame.draw.rect(s, (160, 140, 100), (0, 0, TILE_SIZE, TILE_SIZE // 2), 1)
    return s


TILE_SURFS = {}


def get_tile_surf(tile_type):
    if tile_type not in TILE_SURFS:
        if tile_type == 'G':
            TILE_SURFS[tile_type] = make_grass_tile()
        elif tile_type == 'S':
            TILE_SURFS[tile_type] = make_stone_tile()
        elif tile_type == 'B':
            TILE_SURFS[tile_type] = make_shelf_tile()
        elif tile_type == 'M':
            TILE_SURFS[tile_type] = make_metal_tile()
        elif tile_type == 'P':
            TILE_SURFS[tile_type] = make_platform_tile()
    return TILE_SURFS[tile_type]
