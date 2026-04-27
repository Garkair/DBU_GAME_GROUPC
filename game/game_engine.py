# ─────────────────────────────────────────────────────────────
#  game_engine.py  –  core state machine and game loop
# ─────────────────────────────────────────────────────────────
import pygame
from .constants import *
from .player      import Player
from .enemies     import SlowStudent, FastStudent, FlyingDrone
from .collectibles import AccessChip, PatriotToken, ExitPortal
from .levels      import LEVEL_DATA, build_tiles
from .hud         import HUD
from .background_loader import preload_all, get_status as bg_status
from .screens     import (draw_title_screen, draw_mission_briefing,
                          draw_game_over, draw_victory,
                          draw_level_complete, draw_background)

# ── Game states ───────────────────────────────────────────────
STATE_TITLE      = "title"
STATE_BRIEFING   = "briefing"
STATE_PLAYING    = "playing"
STATE_LEVEL_DONE = "level_done"
STATE_GAME_OVER  = "game_over"
STATE_VICTORY    = "victory"

SCORE_CHIP    = 500
SCORE_TOKEN   = 100
SCORE_LEVEL   = 2000


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock  = pygame.time.Clock()
        preload_all()  # scan backgrounds/ folder at startup
        self.hud    = HUD()
        self.state  = STATE_TITLE
        self.tick   = 0
        self.level_index  = 0
        self.debug_open   = False   # toggled with G
        self.debug_cursor = 0       # highlighted row in menu
        self._reset_game()

    # ── setup helpers ──────────────────────────────────────
    def _reset_game(self):
        self.level_index = 0
        self.total_score = 0
        self._load_level(self.level_index)

    def _load_level(self, index):
        data = LEVEL_DATA[index]
        self.level_data   = data
        self.level_width  = data["width"]
        self.chips_needed = data["chips_needed"]

        # Tiles
        self.tiles      = build_tiles(index)
        self.tile_group = pygame.sprite.Group(self.tiles)

        # Player – spawn at fixed position
        self.player = Player(80, 380)
        if hasattr(self, 'total_score'):
            self.player.score = self.total_score

        # Enemies
        self.enemies = []
        for (x, y, pl, pr) in data["slow_students"]:
            self.enemies.append(SlowStudent(x, y, pl, pr))
        for (x, y, pl, pr) in data["fast_students"]:
            self.enemies.append(FastStudent(x, y, pl, pr))
        for (x, y, pt, pb) in data["drones"]:
            self.enemies.append(FlyingDrone(x, y, pt, pb))

        # Collectibles
        self.chips = []
        for (x, y) in data["chips"]:
            self.chips.append(AccessChip(x, y))

        self.tokens = []
        for (x, y) in data["tokens"]:
            self.tokens.append(PatriotToken(x, y))

        # Exit
        ex, ey = data["exit"]
        self.exit_portal = ExitPortal(ex, ey)

        self.camera_x        = 0
        self.chips_collected = 0

    # ── debug menu ─────────────────────────────────────────
    def _toggle_debug(self):
        self.debug_open   = not self.debug_open
        self.debug_cursor = self.level_index

    def _debug_jump(self, index):
        """Immediately warp to any level, bypass briefing, keep score."""
        self.level_index = index
        self.total_score = self.player.score if hasattr(self, 'player') else 0
        self._load_level(index)
        self.state      = STATE_PLAYING
        self.debug_open = False

    def _draw_debug_menu(self):
        """Overlay the level-select debug panel on top of whatever is on screen."""
        font_title = pygame.font.SysFont("Arial", 18, bold=True)
        font_item  = pygame.font.SysFont("Arial", 14)
        font_hint  = pygame.font.SysFont("Arial", 11)

        row_h  = 50
        pad    = 10
        width  = 520
        height = 54 + len(LEVEL_DATA) * row_h + 36
        ox     = SCREEN_WIDTH  // 2 - width  // 2
        oy     = SCREEN_HEIGHT // 2 - height // 2

        backdrop = pygame.Surface((width, height), pygame.SRCALPHA)
        backdrop.fill((10, 10, 30, 230))
        self.screen.blit(backdrop, (ox, oy))

        pygame.draw.rect(self.screen, (20, 90, 180), (ox, oy, width, 38))
        pygame.draw.rect(self.screen, C_ACCENT,      (ox, oy, width, 38), 2)
        t = font_title.render("  DBU DEBUG  -  LEVEL SELECT   [G] close", True, C_WHITE)
        self.screen.blit(t, (ox + 10, oy + 9))

        hx, hy = ox + pad, oy + 40
        pygame.draw.line(self.screen, (50, 50, 100),
                         (hx, hy + 12), (ox + width - pad, hy + 12), 1)
        self.screen.blit(font_hint.render("LEVEL",      True, (160,160,200)), (hx + 36, hy))
        self.screen.blit(font_hint.render("BACKGROUND", True, (160,160,200)), (hx + 260, hy))

        bg_info = {row["level"] - 1: row for row in bg_status()}

        for i, data in enumerate(LEVEL_DATA):
            ry     = oy + 54 + i * row_h
            rx     = ox + pad
            rw     = width - pad * 2
            is_sel = (i == self.debug_cursor)

            pygame.draw.rect(self.screen,
                             (35,140,70) if is_sel else (28,28,58),
                             (rx, ry, rw, row_h - 4), border_radius=5)
            pygame.draw.rect(self.screen,
                             C_TOKEN if is_sel else (55,55,100),
                             (rx, ry, rw, row_h - 4), 1, border_radius=5)

            pygame.draw.rect(self.screen,
                             C_TOKEN if is_sel else (70,70,120),
                             (rx+4, ry+6, 28, 28), border_radius=4)
            num = font_title.render(str(i+1), True, C_BLACK if is_sel else C_WHITE)
            self.screen.blit(num, (rx+4+14-num.get_width()//2,
                                   ry+6+14-num.get_height()//2))

            self.screen.blit(font_item.render(data["name"], True, C_WHITE),
                             (rx+40, ry+5))

            enemies = (len(data["slow_students"]) + len(data["fast_students"])
                       + len(data["drones"]))
            tag = "chips:%d  enemies:%d%s" % (
                data["chips_needed"], enemies,
                "  <- ACTIVE" if i == self.level_index else "")
            self.screen.blit(
                font_hint.render(tag, True, C_CHIP if is_sel else (130,130,175)),
                (rx+40, ry+26))

            info   = bg_info.get(i, {"status": "none", "file": "-"})
            status = info["status"]
            fname  = info["file"]
            if status == "loaded":
                dot_col      = (50, 220, 80)
                status_label = "OK " + fname
                sub_label    = "photo BG active - parallax scroll"
                sub_col      = (100, 200, 120)
            elif status == "found (not loaded)":
                dot_col      = (255, 180, 0)
                status_label = "WARN " + fname
                sub_label    = "found but rejected (check ratio)"
                sub_col      = (220, 160, 60)
            else:
                dot_col      = (120, 120, 140)
                status_label = "no image  ->  backgrounds/level%d.*" % (i+1)
                sub_label    = "procedural BG in use"
                sub_col      = (100, 100, 130)

            pygame.draw.circle(self.screen, dot_col, (rx+262, ry+16), 5)
            self.screen.blit(font_hint.render(status_label, True, dot_col), (rx+272, ry+9))
            self.screen.blit(font_hint.render(sub_label,    True, sub_col), (rx+272, ry+24))

        hint = font_hint.render(
            "Up/Down navigate    ENTER warp to level    G close",
            True, (150,150,195))
        self.screen.blit(hint, (ox + width//2 - hint.get_width()//2,
                                oy + height - 22))

    # ── camera ─────────────────────────────────────────────
    def _update_camera(self):
        target = self.player.rect.centerx - SCREEN_WIDTH // 2
        self.camera_x = max(0, min(target, self.level_width - SCREEN_WIDTH))

    # ── collision helpers ──────────────────────────────────
    def _check_collectibles(self):
        p  = self.player
        pr = p.rect

        for chip in self.chips:
            if not chip.collected and pr.colliderect(chip.rect):
                chip.collected = True
                chip.kill()
                self.chips_collected += 1
                p.score += SCORE_CHIP
                if self.chips_collected >= self.chips_needed:
                    self.exit_portal.active = True

        for token in self.tokens:
            if not token.collected and pr.colliderect(token.rect):
                token.collected = True
                p.score += SCORE_TOKEN

        if self.exit_portal.active and pr.colliderect(self.exit_portal.rect):
            p.score += SCORE_LEVEL
            self.total_score = p.score
            if self.level_index >= len(LEVEL_DATA) - 1:
                self.state = STATE_VICTORY
            else:
                self.state = STATE_LEVEL_DONE

    def _check_enemies(self):
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.hit()

    def _check_fall_death(self):
        if self.player.rect.top > SCREEN_HEIGHT + 80:
            self.player.lives -= 1
            self.player.invincible = INVINCIBILITY_FRAMES
            if self.player.lives <= 0:
                self.player.dead = True
            else:
                self.player.rect.topleft = (80, 380)
                self.player.vel_x = 0
                self.player.vel_y = 0

    # ── main run loop ──────────────────────────────────────
    def run(self):
        running = True
        while running:
            self.tick += 1
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    # G toggles debug menu from any game state
                    if event.key == pygame.K_g:
                        self._toggle_debug()

                    elif self.debug_open:
                        # All input inside the menu
                        if event.key == pygame.K_UP:
                            self.debug_cursor = (self.debug_cursor - 1) % len(LEVEL_DATA)
                        elif event.key == pygame.K_DOWN:
                            self.debug_cursor = (self.debug_cursor + 1) % len(LEVEL_DATA)
                        elif event.key == pygame.K_RETURN:
                            self._debug_jump(self.debug_cursor)
                        elif event.key == pygame.K_ESCAPE:
                            self.debug_open = False

                    else:
                        # Normal input
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        if event.key == pygame.K_RETURN:
                            self._handle_enter()

            if self.state == STATE_PLAYING and not self.debug_open:
                self._update()

            self._draw()

            # Debug overlay drawn on top of everything
            if self.debug_open:
                self._draw_debug_menu()

            pygame.display.flip()

        pygame.quit()

    def _handle_enter(self):
        if self.state == STATE_TITLE:
            self.state = STATE_BRIEFING
        elif self.state == STATE_BRIEFING:
            self.state = STATE_PLAYING
        elif self.state == STATE_LEVEL_DONE:
            self.level_index += 1
            self._load_level(self.level_index)
            self.state = STATE_BRIEFING
        elif self.state in (STATE_GAME_OVER, STATE_VICTORY):
            self._reset_game()
            self.state = STATE_TITLE

    def _update(self):
        self.player.update(self.tiles)
        self._check_fall_death()
        self._check_enemies()
        self._check_collectibles()

        if self.player.dead:
            self.state = STATE_GAME_OVER
            return

        for enemy in self.enemies:
            enemy.update(self.tiles)

        for chip in self.chips:
            chip.update()
        for token in self.tokens:
            token.update()
        self.exit_portal.update()

        self._update_camera()

    def _draw(self):
        if self.state == STATE_TITLE:
            draw_title_screen(self.screen, self.tick)

        elif self.state == STATE_BRIEFING:
            draw_mission_briefing(self.screen,
                                  self.level_data["mission"],
                                  self.level_data["name"],
                                  self.tick)

        elif self.state == STATE_PLAYING:
            draw_background(self.screen, self.level_data, self.camera_x, self.tick)

            for tile in self.tiles:
                self.screen.blit(tile.image,
                                 (tile.rect.x - self.camera_x, tile.rect.y))

            for chip in self.chips:
                chip.draw(self.screen, self.camera_x)
            for token in self.tokens:
                token.draw(self.screen, self.camera_x)
            self.exit_portal.draw(self.screen, self.camera_x)

            for enemy in self.enemies:
                enemy.draw(self.screen, self.camera_x)

            self.player.draw(self.screen, self.camera_x)

            self.hud.draw(self.screen, self.player,
                          self.chips_collected, self.chips_needed,
                          self.level_data["name"])

            # Small debug indicator when menu is closed but debug was used
            if self.level_index > 0 or self.state != STATE_PLAYING:
                pass  # nothing extra needed

        elif self.state == STATE_LEVEL_DONE:
            draw_background(self.screen, self.level_data, self.camera_x, self.tick)
            draw_level_complete(self.screen, self.level_data["name"],
                                self.player.score, self.chips_collected, self.tick)

        elif self.state == STATE_GAME_OVER:
            draw_game_over(self.screen, self.total_score, self.tick)

        elif self.state == STATE_VICTORY:
            draw_victory(self.screen, self.total_score, self.tick)
