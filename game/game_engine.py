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
        self.hud    = HUD()
        self.state  = STATE_TITLE
        self.tick   = 0
        self.level_index = 0
        self._reset_game()

    # ── setup helpers ──────────────────────────────────────
    def _reset_game(self):
        self.level_index = 0
        self.total_score = 0
        self._load_level(self.level_index)

    def _load_level(self, index):
        data = LEVEL_DATA[index]
        self.level_data  = data
        self.level_width = data["width"]
        self.chips_needed = data["chips_needed"]

        # Tiles
        self.tiles = build_tiles(index)
        self.tile_group = pygame.sprite.Group(self.tiles)

        # Player – spawn at fixed position
        self.player = Player(80, 380)
        if hasattr(self, 'total_score'):
            self.player.score = self.total_score  # carry score

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

        self.camera_x     = 0
        self.chips_collected = 0

    # ── camera ─────────────────────────────────────────────
    def _update_camera(self):
        target = self.player.rect.centerx - SCREEN_WIDTH // 2
        self.camera_x = max(0, min(target, self.level_width - SCREEN_WIDTH))

    # ── collision helpers ──────────────────────────────────
    def _check_collectibles(self):
        p = self.player
        pr = p.rect

        # Chips
        for chip in self.chips:
            if not chip.collected and pr.colliderect(chip.rect):
                chip.collected = True
                chip.kill()
                self.chips_collected += 1
                p.score += SCORE_CHIP
                if self.chips_collected >= self.chips_needed:
                    self.exit_portal.active = True

        # Tokens
        for token in self.tokens:
            if not token.collected and pr.colliderect(token.rect):
                token.collected = True
                p.score += SCORE_TOKEN

        # Exit
        if self.exit_portal.active and pr.colliderect(self.exit_portal.rect):
            p.score += SCORE_LEVEL
            self.total_score = p.score
            if self.level_index >= len(LEVEL_DATA) - 1:
                self.state = STATE_VICTORY
            else:
                self.state = STATE_LEVEL_DONE

    def _check_enemies(self):
        p = self.player
        for enemy in self.enemies:
            if p.rect.colliderect(enemy.rect):
                p.hit()

    def _check_fall_death(self):
        if self.player.rect.top > SCREEN_HEIGHT + 80:
            self.player.lives -= 1
            self.player.invincible = INVINCIBILITY_FRAMES
            if self.player.lives <= 0:
                self.player.dead = True
            else:
                # Respawn
                self.player.rect.topleft = (80, 380)
                self.player.vel_x = 0
                self.player.vel_y = 0

    # ── main run loop ──────────────────────────────────────
    def run(self):
        running = True
        while running:
            self.tick += 1
            dt = self.clock.tick(FPS)

            # ─ Events ─────────────────────────────────────
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_RETURN:
                        self._handle_enter()

            # ─ Update ─────────────────────────────────────
            if self.state == STATE_PLAYING:
                self._update()

            # ─ Draw ───────────────────────────────────────
            self._draw()
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
        # Player
        self.player.update(self.tiles)
        self._check_fall_death()
        self._check_enemies()
        self._check_collectibles()

        if self.player.dead:
            self.state = STATE_GAME_OVER
            return

        # Enemies
        for enemy in self.enemies:
            enemy.update(self.tiles)

        # Collectibles
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

            # Tiles
            for tile in self.tiles:
                self.screen.blit(tile.image,
                                 (tile.rect.x - self.camera_x, tile.rect.y))

            # Collectibles
            for chip in self.chips:
                chip.draw(self.screen, self.camera_x)
            for token in self.tokens:
                token.draw(self.screen, self.camera_x)
            self.exit_portal.draw(self.screen, self.camera_x)

            # Enemies
            for enemy in self.enemies:
                enemy.draw(self.screen, self.camera_x)

            # Player
            self.player.draw(self.screen, self.camera_x)

            # HUD (on top)
            self.hud.draw(self.screen, self.player,
                          self.chips_collected, self.chips_needed,
                          self.level_data["name"])

        elif self.state == STATE_LEVEL_DONE:
            draw_background(self.screen, self.level_data, self.camera_x, self.tick)
            draw_level_complete(self.screen, self.level_data["name"],
                                self.player.score, self.chips_collected, self.tick)

        elif self.state == STATE_GAME_OVER:
            draw_game_over(self.screen, self.total_score, self.tick)

        elif self.state == STATE_VICTORY:
            draw_victory(self.screen, self.total_score, self.tick)
