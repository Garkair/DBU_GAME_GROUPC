# ─────────────────────────────────────────────────────────────
#  screens.py
# ─────────────────────────────────────────────────────────────
import pygame, math
from .constants import *
from .sprites import make_player_sprite, make_access_chip


def _centered(surface, text_surf, y):
    x = SCREEN_WIDTH // 2 - text_surf.get_width() // 2
    surface.blit(text_surf, (x, y))


def draw_title_screen(surface, tick):
    """Animated title screen."""
    surface.fill(C_BG_FINAL)

    # Animated starfield
    for i in range(60):
        bri = int(80 + 80 * math.sin(tick * 0.03 + i * 0.5))
        pygame.draw.circle(surface, (bri, bri, bri + 40),
                           ((i * 137 + 50) % SCREEN_WIDTH, (i * 97 + 30) % (SCREEN_HEIGHT - HUD_HEIGHT) + HUD_HEIGHT),
                           1 + (i % 2))

    font_title = pygame.font.SysFont("Impact", 64)
    font_sub   = pygame.font.SysFont("Arial",  22, bold=True)
    font_hint  = pygame.font.SysFont("Arial",  16)

    # Glow effect on title
    for offset in range(4, 0, -1):
        glow = font_title.render("OPERATION DBU", True,
                                 (0, int(80 + 40 * math.sin(tick * 0.05)), int(180 + 40 * math.sin(tick * 0.05))))
        _centered(surface, glow, 130 + offset)

    title = font_title.render("OPERATION DBU", True, C_WHITE)
    _centered(surface, title, 130)

    sub = font_sub.render("R E L O A D E D", True, C_ACCENT)
    _centered(surface, sub, 200)

    # Animated player icon
    pframe = (tick // 10) % 4
    player_img = pygame.transform.scale(make_player_sprite(pframe), (56, 80))
    surface.blit(player_img, (SCREEN_WIDTH // 2 - 28, 270))

    # Chip icons floating
    for i in range(3):
        chip = pygame.transform.scale(make_access_chip((tick + i * 15) % 40), (26, 26))
        x = SCREEN_WIDTH // 2 - 80 + i * 80
        y = 290 + int(8 * math.sin(tick * 0.06 + i * 1.0))
        surface.blit(chip, (x, y))

    blink = (tick // 30) % 2
    if blink:
        hint = font_hint.render("PRESS  ENTER  TO  START", True, C_TOKEN)
        _centered(surface, hint, 380)

    ctrl = font_hint.render("Arrow / WASD to move  |  Space / W to jump  |  ESC to quit", True, C_WHITE)
    _centered(surface, ctrl, 420)

    dbu = font_sub.render("Dallas Baptist University", True, C_PATRIOT_BLUE)
    _centered(surface, dbu, 460)


def draw_mission_briefing(surface, mission_text, level_name, tick):
    """Full-screen mission briefing shown at level start."""
    surface.fill(C_BG_FINAL)
    font_title = pygame.font.SysFont("Arial", 28, bold=True)
    font_body  = pygame.font.SysFont("Arial", 18)
    font_hint  = pygame.font.SysFont("Arial", 14)

    # Scanline effect
    for y in range(0, SCREEN_HEIGHT, 4):
        pygame.draw.line(surface, (0, 0, 0, 30), (0, y), (SCREEN_WIDTH, y))

    # Level badge
    badge = pygame.Surface((SCREEN_WIDTH - 200, 50), pygame.SRCALPHA)
    badge.fill((0, 80, 160, 180))
    surface.blit(badge, (100, 90))
    title_txt = font_title.render(level_name, True, C_WHITE)
    surface.blit(title_txt, (SCREEN_WIDTH // 2 - title_txt.get_width() // 2, 100))

    # Mission text
    lines = mission_text.split('\n')
    for i, line in enumerate(lines):
        t = font_body.render(line, True, C_CHIP)
        surface.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, 180 + i * 34))

    blink = (tick // 20) % 2
    if blink:
        hint = font_hint.render("Press ENTER to begin mission", True, C_TOKEN)
        surface.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 340))


def draw_game_over(surface, score, tick):
    surface.fill((20, 0, 0))
    font_big  = pygame.font.SysFont("Impact", 72)
    font_sub  = pygame.font.SysFont("Arial",  22, bold=True)
    font_hint = pygame.font.SysFont("Arial",  16)

    pulse = int(30 * abs(math.sin(tick * 0.05)))
    go = font_big.render("GAME  OVER", True, (200 + pulse, 0, 0))
    _centered(surface, go, 140)

    sc = font_sub.render(f"Final Score: {score:,}", True, C_TOKEN)
    _centered(surface, sc, 240)

    blink = (tick // 30) % 2
    if blink:
        r = font_hint.render("Press ENTER to try again  |  ESC to quit", True, C_WHITE)
        _centered(surface, r, 340)


def draw_victory(surface, score, tick):
    surface.fill(C_BG_FINAL)

    # Particle confetti
    for i in range(80):
        hue_r = (i * 53 + tick * 3) % 256
        hue_g = (i * 97 + tick * 5) % 256
        cx = (i * 137 + tick * 2) % SCREEN_WIDTH
        cy = (i * 73 + tick)       % SCREEN_HEIGHT
        pygame.draw.circle(surface, (hue_r, hue_g, 200), (cx, cy), 3)

    font_big  = pygame.font.SysFont("Impact", 52)
    font_sub  = pygame.font.SysFont("Arial",  26, bold=True)
    font_msg  = pygame.font.SysFont("Arial",  18)
    font_hint = pygame.font.SysFont("Arial",  16)

    pulse = int(20 * abs(math.sin(tick * 0.05)))
    mc = font_big.render("MISSION COMPLETE", True, (0, 220 + pulse, 100))
    _centered(surface, mc, 110)

    cr = font_sub.render("Campus Restored !", True, C_TOKEN)
    _centered(surface, cr, 180)

    sc = font_msg.render(f"Final Score: {score:,}", True, C_WHITE)
    _centered(surface, sc, 240)

    msg = font_msg.render("Agent Patriot – DBU is safe once more.", True, C_CHIP)
    _centered(surface, msg, 290)

    blink = (tick // 30) % 2
    if blink:
        r = font_hint.render("Press ENTER to play again  |  ESC to quit", True, C_TOKEN)
        _centered(surface, r, 380)


def draw_level_complete(surface, level_name, score, chips, tick):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 20, 60, 200))
    surface.blit(overlay, (0, 0))

    font_big  = pygame.font.SysFont("Arial", 40, bold=True)
    font_sub  = pygame.font.SysFont("Arial", 20)
    font_hint = pygame.font.SysFont("Arial", 16)

    ok = font_big.render("LEVEL COMPLETE!", True, C_GREEN)
    _centered(surface, ok, 160)

    sc = font_sub.render(f"Score: {score:,}   Chips: {chips}", True, C_TOKEN)
    _centered(surface, sc, 230)

    blink = (tick // 20) % 2
    if blink:
        r = font_hint.render("Press ENTER to continue", True, C_WHITE)
        _centered(surface, r, 310)


def draw_background(surface, level_data, camera_x, tick):
    """Draw the scrolling background for the current level.

    Uses level_data["bg_type"] (a plain string) for branching so that
    changing the RGB values of C_BG_* in constants.py never breaks these
    comparisons.
    """
    surface.fill(level_data["bg_color"])

    bg_type = level_data.get("bg_type", "sky")

    if bg_type == "sky":
        # Clouds
        for i in range(8):
            cx = (i * 280 - camera_x // 4 + tick) % (SCREEN_WIDTH + 200) - 100
            cy = 80 + (i % 3) * 40
            pygame.draw.ellipse(surface, C_WHITE, (cx, cy, 120, 45))
            pygame.draw.ellipse(surface, C_WHITE, (cx + 20, cy - 20, 80, 45))
        # Sun
        pygame.draw.circle(surface, C_YELLOW, (820, 80), 45)
        pygame.draw.circle(surface, (255, 255, 200), (820, 80), 40)

    elif bg_type == "indoor":
        # Windows
        for i in range(6):
            wx = 80 + i * 150 - (camera_x // 8) % 150
            pygame.draw.rect(surface, (50, 100, 200, 80), (wx, 60, 60, 80))
            pygame.draw.rect(surface, C_ACCENT, (wx, 60, 60, 80), 2)

    elif bg_type == "final":
        # Circuit-board lines
        for i in range(10):
            x = (i * 120 - camera_x // 6) % SCREEN_WIDTH
            pygame.draw.line(surface, (0, 40, 80), (x, HUD_HEIGHT), (x, SCREEN_HEIGHT), 1)
        for j in range(6):
            y = 80 + j * 80
            pygame.draw.line(surface, (0, 40, 80), (0, y), (SCREEN_WIDTH, y), 1)
