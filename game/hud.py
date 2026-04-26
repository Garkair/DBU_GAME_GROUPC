# ─────────────────────────────────────────────────────────────
#  hud.py
# ─────────────────────────────────────────────────────────────
import pygame
from .constants import *
from .sprites import make_access_chip, make_patriot_token, make_player_sprite


class HUD:
    def __init__(self):
        pygame.font.init()
        self.font_lg = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_sm = pygame.font.SysFont("Arial", 14)
        self.chip_icon  = pygame.transform.scale(make_access_chip(0),  (18, 18))
        self.token_icon = pygame.transform.scale(make_patriot_token(0),(16, 16))
        self.heart_surf = self._make_heart()

    @staticmethod
    def _make_heart():
        s = pygame.Surface((16, 14), pygame.SRCALPHA)
        pygame.draw.polygon(s, (220, 50, 50),
                            [(8, 13), (1, 5), (1, 3), (3, 1), (5, 1),
                             (8, 4), (11, 1), (13, 1), (15, 3), (15, 5)])
        return s

    def draw(self, surface, player, chips_collected, chips_needed, level_name):
        # Background bar
        pygame.draw.rect(surface, C_HUD, (0, 0, SCREEN_WIDTH, HUD_HEIGHT))
        pygame.draw.line(surface, C_ACCENT, (0, HUD_HEIGHT), (SCREEN_WIDTH, HUD_HEIGHT), 2)

        # Lives
        for i in range(player.lives):
            surface.blit(self.heart_surf, (10 + i * 22, 16))

        # Score
        score_txt = self.font_lg.render(f"SCORE  {player.score:06d}", True, C_TOKEN)
        surface.blit(score_txt, (120, 12))

        # Chip counter
        surface.blit(self.chip_icon, (340, 15))
        chip_txt = self.font_lg.render(
            f"{chips_collected}/{chips_needed}", True, C_CHIP)
        surface.blit(chip_txt, (362, 12))

        # Level name
        name_txt = self.font_sm.render(level_name, True, C_WHITE)
        surface.blit(name_txt, (SCREEN_WIDTH // 2 - name_txt.get_width() // 2, 16))

        # DBU branding
        brand = self.font_sm.render("DBU OPERATION", True, C_ACCENT)
        surface.blit(brand, (SCREEN_WIDTH - brand.get_width() - 10, 16))
