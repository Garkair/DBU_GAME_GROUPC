# ─────────────────────────────────────────────────────────────
#  levels.py  –  tile maps + object placement for all 5 levels
# ─────────────────────────────────────────────────────────────
import pygame
from .constants import *
from .sprites import get_tile_surf

T = TILE_SIZE
H = T // 2  # half-tile for thin platforms

# ── Tile types ────────────────────────────────────────────────
# G = grass/dirt   S = stone   B = bookshelf   M = metal   P = thin platform

# Each level is a dict:
#   bg_color, tiles, chips, tokens, slow_students, fast_students, drones, exit
#   Positions are in pixels (x, y).
#   Patrol ranges for enemies: (patrol_left, patrol_right)
#   Drone patrol:  (patrol_top, patrol_bottom)


def _make_tile_strip(x, y, count, tile_type):
    """Return list of (tile_type, rect) for a horizontal strip."""
    return [(tile_type, pygame.Rect(x + i * T, y, T, T)) for i in range(count)]


def _make_tile_column(x, y, count, tile_type):
    return [(tile_type, pygame.Rect(x, y + i * T, T, T)) for i in range(count)]


# ═══════════════════════════════════════════════════════════════
#  LEVEL DEFINITIONS
# ═══════════════════════════════════════════════════════════════

LEVEL_DATA = [

    # ── LEVEL 1  Entrance / Mountain Creek Parkway ────────────
    {
        "index":   0,
        "name":    "Level 1 – Entrance: Mountain Creek Pkwy",
        "mission": "Agent Patriot, the campus system has been compromised.\nGain access through the main entrance.",
        "bg_color": C_BG_SKY,
        "bg_type": "sky",
        "width":   3200,
        "chips_needed": 3,
        "tiles": (
            # Ground floor
            _make_tile_strip(0,   460, 80, 'G') +
            # Hills / raised grass
            _make_tile_strip(300, 420, 5, 'G') +
            _make_tile_strip(700, 380, 6, 'G') +
            _make_tile_strip(1100,420, 5, 'G') +
            # Floating platforms
            _make_tile_strip(1400,340, 4, 'G') +
            _make_tile_strip(1700,300, 3, 'G') +
            _make_tile_strip(2000,340, 5, 'G') +
            _make_tile_strip(2400,260, 4, 'G') +
            _make_tile_strip(2700,380, 6, 'G') +
            # Walls (entrance gate pillars)
            _make_tile_column(2880, 300, 4, 'S') +
            _make_tile_column(2960, 300, 4, 'S')
        ),
        "chips":  [(500, 410), (1150, 365), (2020, 310)],
        "tokens": [(250, 410), (900, 340), (1550, 300), (1900, 280),
                   (2200, 310), (2500, 230)],
        "slow_students": [
            (400, 420, 300, 700),
            (1200, 380, 1100, 1500),
            (2000, 300, 1800, 2300),
        ],
        "fast_students": [],
        "drones": [],
        "exit":  (3000, 300),
    },

    # ── LEVEL 2  Collins Learning Center ─────────────────────
    {
        "index":   1,
        "name":    "Level 2 – Collins Learning Center",
        "mission": "Agent Patriot, recover the data files inside\nthe Learning Center to restore system access.",
        "bg_color": C_BG_INDOOR,
        "bg_type": "indoor",
        "width":   3200,
        "chips_needed": 3,
        "tiles": (
            # Floor
            _make_tile_strip(0,   460, 80, 'S') +
            # Bookshelf platforms – ascending staircase style
            _make_tile_strip(200, 380, 6, 'B') +
            _make_tile_strip(500, 300, 5, 'B') +
            _make_tile_strip(800, 220, 5, 'B') +
            _make_tile_strip(1100,300, 4, 'B') +
            _make_tile_strip(1400,380, 4, 'B') +
            _make_tile_strip(1700,260, 5, 'B') +
            _make_tile_strip(2000,180, 4, 'B') +
            _make_tile_strip(2300,260, 5, 'B') +
            _make_tile_strip(2600,340, 5, 'B') +
            # Walls
            _make_tile_column(0,    0, 12, 'S') +
            _make_tile_column(3160, 0, 12, 'S')
        ),
        "chips":  [(220, 350), (820, 190), (2020, 150)],
        "tokens": [(350, 350), (600, 265), (1000, 185), (1720, 225),
                   (2100, 145), (2400, 225)],
        "slow_students": [
            (300,  380, 200,  700),
            (1200, 380, 1100, 1600),
        ],
        "fast_students": [],
        "drones": [
            (1800, 200, 140, 360),
            (2500, 240, 140, 400),
        ],
        "exit":  (2900, 300),
    },

    # ── LEVEL 3  Mahler Student Center ───────────────────────
    {
        "index":   2,
        "name":    "Level 3 – Mahler Student Center",
        "mission": "Agent Patriot, stabilize the system nodes in\nthe Student Center before the network collapses.",
        "bg_color": C_BG_INDOOR,
        "bg_type": "indoor",
        "width":   3600,
        "chips_needed": 3,
        "tiles": (
            _make_tile_strip(0,   460, 90, 'S') +
            # Tables (wide flat platforms)
            _make_tile_strip(200, 400, 6, 'S') +
            _make_tile_strip(500, 360, 5, 'S') +
            _make_tile_strip(900, 320, 6, 'S') +
            _make_tile_strip(1300,280, 4, 'S') +
            _make_tile_strip(1700,320, 5, 'S') +
            _make_tile_strip(2100,260, 5, 'S') +
            _make_tile_strip(2300,260, 1, 'S') +
            _make_tile_strip(2500,200, 5, 'S') +
            _make_tile_strip(2900,260, 6, 'S') +
            _make_tile_strip(3200,320, 5, 'S')
        ),
        "chips":  [(250, 370), (1320, 250), (2520, 170)],
        "tokens": [(400, 370), (700, 330), (1000, 290), (1500, 290),
                   (1900, 230), (2300, 230), (2700, 165), (3000, 225)],
        "slow_students": [
            (300,  400,  200, 700),
            (1000, 280,  900, 1400),
            (2200, 220, 2100, 2600),
        ],
        "fast_students": [
            (600,  360, 500, 1000),
            (1800, 280, 1700, 2200),
            (3000, 220, 2900, 3400),
        ],
        "drones": [
            (1400, 180, 140, 340),
            (2600, 100, 80, 300),
        ],
        "exit":  (3400, 260),
    },

    # ── LEVEL 4  Dorm Zone ────────────────────────────────────
    {
        "index":   3,
        "name":    "Level 4 – Dorm Zone",
        "mission": "Agent Patriot, navigate the residential zone\nand secure the remaining access points.",
        "bg_color": C_BG_DORM,
        "bg_type": "sky",
        "width":   4000,
        "chips_needed": 3,
        "tiles": (
            _make_tile_strip(0,   460, 100, 'G') +
            # Narrow platform challenge
            _make_tile_strip(200, 380, 2, 'G') +
            _make_tile_strip(340, 340, 2, 'G') +
            _make_tile_strip(480, 300, 2, 'G') +
            _make_tile_strip(620, 260, 2, 'G') +
            _make_tile_strip(760, 220, 2, 'G') +
            _make_tile_strip(900, 260, 2, 'G') +
            _make_tile_strip(1040,300, 2, 'G') +
            # Break — gap
            _make_tile_strip(1200,360, 3, 'S') +
            _make_tile_strip(1440,300, 2, 'S') +
            _make_tile_strip(1620,240, 2, 'S') +
            _make_tile_strip(1800,300, 3, 'S') +
            _make_tile_strip(2000,360, 3, 'S') +
            # Dorm buildings (wide platforms at varied heights)
            _make_tile_strip(2200,300, 5, 'G') +
            _make_tile_strip(2500,240, 4, 'G') +
            _make_tile_strip(2800,180, 4, 'G') +
            _make_tile_strip(3100,240, 4, 'G') +
            _make_tile_strip(3400,300, 6, 'G')
        ),
        "chips":  [(640, 230), (1640, 210), (2820, 150)],
        "tokens": [(300, 350), (480, 270), (760, 190), (1200, 330),
                   (1800, 270), (2220, 270), (2700, 210), (3000, 210)],
        "slow_students": [
            (250,  380, 200, 500),
            (1250, 330, 1200, 1500),
            (2250, 270, 2200, 2600),
        ],
        "fast_students": [
            (900,  220, 800, 1100),
            (1800, 270, 1700, 2100),
            (2900, 150, 2800, 3200),
            (3450, 270, 3400, 3900),
        ],
        "drones": [
            (1460, 200, 120, 360),
            (2520, 140, 80, 300),
            (3150, 160, 100, 300),
        ],
        "exit":  (3700, 260),
    },

    # ── LEVEL 5  Control Center (Final) ──────────────────────
    {
        "index":   4,
        "name":    "Level 5 – Final Mission: Control Center",
        "mission": "Agent Patriot, this is the final system core.\nRestore control and save the campus!",
        "bg_color": C_BG_FINAL,
        "bg_type": "final",
        "width":   4800,
        "chips_needed": 5,
        "tiles": (
            _make_tile_strip(0,   460, 120, 'M') +
            # Multi-layered metal platforms
            _make_tile_strip(200, 380, 3, 'M') +
            _make_tile_strip(400, 320, 3, 'M') +
            _make_tile_strip(600, 260, 3, 'M') +
            _make_tile_strip(800, 200, 3, 'M') +
            _make_tile_strip(1000,260, 3, 'M') +
            _make_tile_strip(1200,320, 3, 'M') +
            _make_tile_strip(1400,260, 3, 'M') +
            _make_tile_strip(1600,200, 3, 'M') +
            _make_tile_strip(1800,140, 3, 'M') +
            _make_tile_strip(2000,200, 3, 'M') +
            _make_tile_strip(2200,260, 3, 'M') +
            _make_tile_strip(2400,200, 3, 'M') +
            _make_tile_strip(2600,140, 3, 'M') +
            _make_tile_strip(2800, 80, 3, 'M') +
            _make_tile_strip(3000,140, 3, 'M') +
            _make_tile_strip(3200,200, 3, 'M') +
            _make_tile_strip(3400,140, 3, 'M') +
            _make_tile_strip(3600, 80, 3, 'M') +
            _make_tile_strip(3800,140, 3, 'M') +
            _make_tile_strip(4000,200, 3, 'M') +
            _make_tile_strip(4200,260, 4, 'M') +
            _make_tile_strip(4400,320, 5, 'M')
        ),
        "chips":  [(620, 230), (1020, 170), (1820, 110), (2820, 50), (3820, 110)],
        "tokens": [(300, 350), (500, 290), (700, 230), (900, 170),
                   (1200, 230), (1600, 170), (2000, 170), (2400, 170),
                   (2600, 110), (3000, 110), (3400, 110), (3800,  50)],
        "slow_students": [
            (300,  380, 200, 500),
            (1100, 230, 1000, 1300),
            (2300, 230, 2200, 2500),
            (4250, 230, 4200, 4600),
        ],
        "fast_students": [
            (600,  230, 500, 900),
            (1400, 230, 1300, 1700),
            (2000, 170, 1900, 2300),
            (2600, 110, 2500, 2900),
            (3200, 170, 3100, 3500),
            (3600,  50, 3500, 3900),
        ],
        "drones": [
            (850,  120, 80,  300),
            (1650,  60, 40,  260),
            (2450,  40, 40,  200),
            (3050,  80, 40,  220),
            (3650,  20, 20,  180),
            (4050, 100, 60,  260),
        ],
        "exit":  (4600, 260),
    },
]


# ── Tile sprite class ─────────────────────────────────────────
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, rect):
        super().__init__()
        self.tile_type = tile_type
        self.image = pygame.transform.scale(
            get_tile_surf(tile_type), (rect.width, rect.height)
        )
        self.rect = rect


def build_tiles(level_index):
    """Return a list of Tile sprites for the given level."""
    data  = LEVEL_DATA[level_index]
    tiles = []
    for (t, rect) in data["tiles"]:
        tiles.append(Tile(t, rect))
    return tiles
