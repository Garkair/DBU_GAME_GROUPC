# ─────────────────────────────────────────────────────────────
#  screens.py
# ─────────────────────────────────────────────────────────────
import pygame, math
from .constants import *
from .sprites import (make_player_sprite, make_access_chip,
                      make_slow_student, make_drone, make_patriot_token,
                      get_tile_surf)
from .background_loader import get_background, BG_W, BG_H


def _centered(surface, text_surf, y):
    x = SCREEN_WIDTH // 2 - text_surf.get_width() // 2
    surface.blit(text_surf, (x, y))


# ── Title screen ──────────────────────────────────────────────
def draw_title_screen(surface, tick):
    surface.fill(C_BG_FINAL)

    for i in range(60):
        bri = int(80 + 80 * math.sin(tick * 0.03 + i * 0.5))
        pygame.draw.circle(surface, (bri, bri, bri + 40),
                           ((i * 137 + 50) % SCREEN_WIDTH,
                            (i * 97  + 30) % (SCREEN_HEIGHT - HUD_HEIGHT) + HUD_HEIGHT),
                           1 + (i % 2))

    font_title = pygame.font.SysFont("Impact", 64)
    font_sub   = pygame.font.SysFont("Arial",  22, bold=True)
    font_hint  = pygame.font.SysFont("Arial",  15)
    font_sm    = pygame.font.SysFont("Arial",  13)

    # Render title as two lines so the frame is never split across a gap
    for line, ly in [("OPERATION", 92), ("DBU", 148)]:
        for offset in range(4, 0, -1):
            glow = font_title.render(line, True,
                                     (0, int(80 + 40 * math.sin(tick * 0.05)),
                                      int(180 + 40 * math.sin(tick * 0.05))))
            _centered(surface, glow, ly + offset)
        txt = font_title.render(line, True, C_WHITE)
        _centered(surface, txt, ly)

    # Decorative frame around the two-line title
    title_w = max(
        font_title.size("OPERATION")[0],
        font_title.size("DBU")[0]
    ) + 32
    title_h = 130
    fx = SCREEN_WIDTH // 2 - title_w // 2
    fy = 86
    pygame.draw.rect(surface, C_ACCENT, (fx, fy, title_w, title_h), 2, border_radius=6)

    sub = font_sub.render("R E L O A D E D", True, C_ACCENT)
    _centered(surface, sub, 222)

    # Animated player
    pframe = (tick // 10) % 4
    player_img = pygame.transform.scale(make_player_sprite(pframe), (48, 68))
    surface.blit(player_img, (SCREEN_WIDTH // 2 - 24, 220))

    # Floating chips
    for i in range(3):
        chip = pygame.transform.scale(make_access_chip((tick + i * 15) % 40), (22, 22))
        x = SCREEN_WIDTH // 2 - 70 + i * 70
        y = 238 + int(6 * math.sin(tick * 0.06 + i * 1.0))
        surface.blit(chip, (x, y))

    # ── Menu options ──────────────────────────────────────────
    blink = (tick // 30) % 2

    options = [
        ("ENTER",   "Start Game"),
        ("T",       "Tutorial / Practice"),
        ("G",       "Select Level"),
        ("S",       "Scoreboard"),
        ("M",       "Toggle Mute"),
        ("ESC",     "Quit"),
    ]
    box_w, box_h = 340, 28
    bx = SCREEN_WIDTH // 2 - box_w // 2
    by = 305
    gap = 33

    for idx, (key, label) in enumerate(options):
        ry = by + idx * gap
        # Highlight "Start" with blink
        if idx == 0 and blink:
            hl = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            hl.fill((0, 180, 255, 40))
            surface.blit(hl, (bx, ry))
        key_txt  = font_hint.render(f"[{key}]", True, C_TOKEN)
        lab_txt  = font_hint.render(label,      True, C_WHITE)
        surface.blit(key_txt,  (bx + 8,  ry + 5))
        surface.blit(lab_txt,  (bx + 80, ry + 5))

    dbu = font_sub.render("Dallas Baptist University", True, C_PATRIOT_BLUE)
    _centered(surface, dbu, SCREEN_HEIGHT - 28)


# ── Tutorial / Practice screen ────────────────────────────────
def draw_tutorial_screen(surface, tick):
    """
    Static tutorial screen with control hints and enemy/item previews.
    Returns nothing – caller handles input.
    """
    surface.fill((20, 30, 50))

    font_title = pygame.font.SysFont("Impact", 38)
    font_head  = pygame.font.SysFont("Arial", 17, bold=True)
    font_body  = pygame.font.SysFont("Arial", 15)
    font_hint  = pygame.font.SysFont("Arial", 13)

    # Title
    t = font_title.render("HOW TO PLAY  –  TRAINING BRIEFING", True, C_ACCENT)
    _centered(surface, t, 18)
    pygame.draw.line(surface, C_ACCENT, (60, 56), (SCREEN_WIDTH-60, 56), 1)

    # ── Left column: Controls ──────────────────────────────────
    cx = 60
    cy = 70
    surface.blit(font_head.render("CONTROLS", True, C_TOKEN), (cx, cy))

    controls = [
        ("← / A",           "Move left"),
        ("→ / D",           "Move right"),
        ("SPACE / W / ↑",   "Jump"),
        ("ENTER",           "Confirm / advance"),
        ("G",               "Select level"),
        ("M",               "Mute audio"),
        ("ESC",             "Return to main menu"),
    ]
    for i, (k, v) in enumerate(controls):
        ky = cy + 28 + i * 26
        key_s = font_body.render(k, True, C_CHIP)
        val_s = font_body.render(v, True, C_WHITE)
        surface.blit(key_s, (cx,       ky))
        surface.blit(val_s, (cx + 190, ky))

    # ── Right column: Enemies ──────────────────────────────────
    rx = 520
    ry = 70
    surface.blit(font_head.render("ENEMIES", True, C_TOKEN), (rx, ry))

    anim = (tick // 10) % 4

    enemy_rows = [
        (make_slow_student(anim), (28, 38), "Slow Student",
         "Patrols platforms. Costs 1 life on contact."),
        (make_drone(anim),        (34, 28), "Flying Drone",
         "Hovers vertically. Hard to dodge on narrow paths."),
    ]
    ey = ry + 28
    for surf_fn, size, name, desc in enemy_rows:
        img = pygame.transform.scale(surf_fn, (size[0]*2, size[1]*2))
        surface.blit(img, (rx, ey))
        surface.blit(font_body.render(name, True, (220, 100, 100)), (rx + 80, ey + 2))
        desc_s = font_hint.render(desc, True, (180, 180, 200))
        surface.blit(desc_s, (rx + 80, ey + 22))
        ey += 68

    # ── Middle section: Rules ──────────────────────────────────
    my = 270
    pygame.draw.line(surface, (40, 50, 80), (60, my), (SCREEN_WIDTH-60, my), 1)
    surface.blit(font_head.render("MISSION RULES", True, C_TOKEN), (60, my + 8))

    rules = [
        (make_access_chip(tick % 40), (22,22),
         "Collect ALL Access Chips to unlock the EXIT portal."),
        (make_patriot_token(tick % 30),(20,20),
         "Patriot Tokens are bonus points – not required to exit."),
    ]
    ry2 = my + 36
    for surf_fn, size, text in rules:
        img = pygame.transform.scale(surf_fn, (size[0]*2, size[1]*2))
        surface.blit(img, (80, ry2 + 2))
        surface.blit(font_body.render(text, True, C_WHITE), (120, ry2 + 8))
        ry2 += 44

    # Extra tips
    tips = [
        "You have 3 lives. Falling off the screen costs a life too.",
        "After losing all lives the game ends – collect 1UP tokens to earn more.",
        "Chips collected carry over if you die and respawn on the same level.",
    ]
    surface.blit(font_head.render("TIPS", True, C_TOKEN), (60, ry2 + 8))
    for i, tip in enumerate(tips):
        ts = font_hint.render("• " + tip, True, (170, 200, 230))
        surface.blit(ts, (80, ry2 + 32 + i * 22))

    # ── Practice mini-map preview ──────────────────────────────
    px, py, pw, ph = 60, 400, SCREEN_WIDTH - 120, 90
    pygame.draw.rect(surface, (20, 20, 40), (px, py, pw, ph), border_radius=6)
    pygame.draw.rect(surface, (40, 60, 100),(px, py, pw, ph), 1, border_radius=6)
    label = font_hint.render("PRACTICE MAP PREVIEW", True, (100,100,150))
    surface.blit(label, (px + 8, py + 4))

    # Draw mini tile strips
    shelf = pygame.transform.scale(get_tile_surf('B'), (20, 20))
    grass = pygame.transform.scale(get_tile_surf('G'), (20, 20))
    ground_y = py + ph - 22
    for col in range(pw // 20):
        surface.blit(grass, (px + col * 20, ground_y))
    for col in range(5):
        surface.blit(shelf, (px + 60  + col*20, ground_y - 40))
    for col in range(4):
        surface.blit(shelf, (px + 220 + col*20, ground_y - 70))
    for col in range(3):
        surface.blit(shelf, (px + 380 + col*20, ground_y - 50))

    # Mini player
    mini_p = pygame.transform.scale(make_player_sprite(anim), (14, 20))
    surface.blit(mini_p, (px + 30, ground_y - 20))

    # Arrow hints on mini map
    surface.blit(font_hint.render("→ move", True, C_WHITE), (px + 8,  ground_y - 20))
    surface.blit(font_hint.render("↑ jump", True, C_WHITE), (px + 65, ground_y - 58))

    blink = (tick // 25) % 2
    if blink:
        back = font_hint.render("ENTER or ESC  →  back to main menu", True, C_TOKEN)
        _centered(surface, back, SCREEN_HEIGHT - 22)


# ── Mission briefing ──────────────────────────────────────────
def draw_mission_briefing(surface, mission_text, level_name, tick):
    surface.fill(C_BG_FINAL)
    font_title = pygame.font.SysFont("Arial", 28, bold=True)
    font_body  = pygame.font.SysFont("Arial", 18)
    font_hint  = pygame.font.SysFont("Arial", 14)

    badge = pygame.Surface((SCREEN_WIDTH - 200, 50), pygame.SRCALPHA)
    badge.fill((0, 80, 160, 180))
    surface.blit(badge, (100, 90))
    title_txt = font_title.render(level_name, True, C_WHITE)
    surface.blit(title_txt, (SCREEN_WIDTH//2 - title_txt.get_width()//2, 100))

    for i, line in enumerate(mission_text.split('\n')):
        t = font_body.render(line, True, C_CHIP)
        surface.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2, 180 + i * 34))

    blink = (tick // 20) % 2
    if blink:
        hint = font_hint.render("Press ENTER to begin mission", True, C_TOKEN)
        surface.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, 340))

    esc = font_hint.render("ESC  →  main menu", True, (120,120,160))
    surface.blit(esc, (SCREEN_WIDTH//2 - esc.get_width()//2, 370))


# ── Game over ─────────────────────────────────────────────────
def draw_game_over(surface, score, tick):
    surface.fill((20, 0, 0))
    font_big  = pygame.font.SysFont("Impact", 72)
    font_sub  = pygame.font.SysFont("Arial",  22, bold=True)
    font_hint = pygame.font.SysFont("Arial",  16)

    pulse = int(30 * abs(math.sin(tick * 0.05)))
    go = font_big.render("GAME  OVER", True, (200 + pulse, 0, 0))
    _centered(surface, go, 130)

    sc = font_sub.render(f"Final Score: {score:,}", True, C_TOKEN)
    _centered(surface, sc, 225)

    options = [
        "ENTER  →  Return to main menu",
        "ESC    →  Return to main menu",
    ]
    for i, opt in enumerate(options):
        blink = (tick // 30) % 2
        if blink:
            r = font_hint.render(opt, True, C_WHITE)
            _centered(surface, r, 310 + i * 30)


# ── Victory ───────────────────────────────────────────────────
def draw_victory(surface, score, tick):
    surface.fill(C_BG_FINAL)

    for i in range(80):
        hue_r = (i * 53 + tick * 3) % 256
        hue_g = (i * 97 + tick * 5) % 256
        cx = (i * 137 + tick * 2) % SCREEN_WIDTH
        cy = (i * 73  + tick)      % SCREEN_HEIGHT
        pygame.draw.circle(surface, (hue_r, hue_g, 200), (cx, cy), 3)

    font_big  = pygame.font.SysFont("Impact", 52)
    font_sub  = pygame.font.SysFont("Arial",  26, bold=True)
    font_msg  = pygame.font.SysFont("Arial",  18)
    font_hint = pygame.font.SysFont("Arial",  16)

    pulse = int(20 * abs(math.sin(tick * 0.05)))
    mc = font_big.render("YOU  WIN!", True, (0, 220 + pulse, 100))
    _centered(surface, mc, 100)

    cr = font_sub.render("Campus Restored!", True, C_TOKEN)
    _centered(surface, cr, 168)

    sc = font_msg.render(f"Final Score: {score:,}", True, C_WHITE)
    _centered(surface, sc, 225)

    msg = font_msg.render("Agent Patriot – DBU is safe once more.", True, C_CHIP)
    _centered(surface, msg, 262)

    blink = (tick // 30) % 2
    if blink:
        r = font_hint.render("ENTER or ESC  →  Return to main menu", True, C_TOKEN)
        _centered(surface, r, 340)


# ── Level complete overlay ────────────────────────────────────
def draw_level_complete(surface, level_name, score, chips, tick):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 20, 60, 200))
    surface.blit(overlay, (0, 0))

    font_big  = pygame.font.SysFont("Arial", 40, bold=True)
    font_sub  = pygame.font.SysFont("Arial", 20)
    font_hint = pygame.font.SysFont("Arial", 16)

    ok = font_big.render("LEVEL COMPLETE!", True, C_GREEN)
    _centered(surface, ok, 155)

    sc = font_sub.render(f"Score: {score:,}   Chips: {chips}", True, C_TOKEN)
    _centered(surface, sc, 220)

    blink = (tick // 20) % 2
    if blink:
        r = font_hint.render("ENTER  →  next level  |  ESC  →  main menu", True, C_WHITE)
        _centered(surface, r, 295)


# ── Background (procedural + optional photo) ──────────────────
def draw_background(surface, level_data, camera_x, tick):
    level_index = level_data.get("index", 0)
    photo = get_background(level_index)

    if photo is not None:
        photo = pygame.transform.scale(photo, (4100, BG_H))
        parallax_x = int(camera_x * (4100 - SCREEN_WIDTH) / 4100)
        surface.blit(photo, (-parallax_x-400, HUD_HEIGHT))
        if parallax_x > 0:
            surface.blit(photo, (-parallax_x-400, HUD_HEIGHT))
        tint = pygame.Surface((SCREEN_WIDTH, BG_H), pygame.SRCALPHA)
        tint.fill((0, 0, 0, 60))
        surface.blit(tint, (0, HUD_HEIGHT))
        return

    surface.fill(level_data["bg_color"])
    bg_type = level_data.get("bg_type", "sky")

    if bg_type == "sky":
        for i in range(8):
            cx = (i * 280 - camera_x // 4 + tick) % (SCREEN_WIDTH + 200) - 100
            cy = 80 + (i % 3) * 40
            pygame.draw.ellipse(surface, C_WHITE, (cx, cy, 120, 45))
            pygame.draw.ellipse(surface, C_WHITE, (cx + 20, cy - 20, 80, 45))
        pygame.draw.circle(surface, C_YELLOW, (820, 80), 45)
        pygame.draw.circle(surface, (255, 255, 200), (820, 80), 40)

    elif bg_type == "indoor":
        for i in range(6):
            wx = 80 + i * 150 - (camera_x // 8) % 150
            pygame.draw.rect(surface, (50, 100, 200, 80), (wx, 60, 60, 80))
            pygame.draw.rect(surface, C_ACCENT, (wx, 60, 60, 80), 2)

    elif bg_type == "final":
        for i in range(10):
            x = (i * 120 - camera_x // 6) % SCREEN_WIDTH
            pygame.draw.line(surface, (0, 40, 80),
                             (x, HUD_HEIGHT), (x, SCREEN_HEIGHT), 1)
        for j in range(6):
            y = 80 + j * 80
            pygame.draw.line(surface, (0, 40, 80), (0, y), (SCREEN_WIDTH, y), 1)
