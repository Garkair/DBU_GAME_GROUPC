# ─────────────────────────────────────────────────────────────
#  scoreboard.py  –  username entry + persistent leaderboard
#  Scores saved to  saves/scoreboard.json
# ─────────────────────────────────────────────────────────────
import os, json, pygame
from .constants import *

_ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SAVE_DIR  = os.path.join(_ROOT, "saves")
_SAVE_FILE = os.path.join(_SAVE_DIR, "scoreboard.json")
MAX_ENTRIES = 10


# ── Persistence ───────────────────────────────────────────────
def _load() -> list:
    try:
        os.makedirs(_SAVE_DIR, exist_ok=True)
        with open(_SAVE_FILE) as f:
            return json.load(f)
    except Exception:
        return []


def _save(entries: list) -> None:
    os.makedirs(_SAVE_DIR, exist_ok=True)
    with open(_SAVE_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def add_score(name: str, score: int) -> None:
    entries = _load()
    entries.append({"name": name.strip()[:16] or "AGENT", "score": score})
    entries.sort(key=lambda e: e["score"], reverse=True)
    entries = entries[:MAX_ENTRIES]
    _save(entries)


def get_scores() -> list:
    return _load()


# ── Name-entry widget ─────────────────────────────────────────
class NameEntry:
    """
    Blocking name-entry screen.  Call .run(screen, clock, score) →
    returns the entered name string (or "AGENT" if empty).
    """
    MAX_LEN = 12

    def __init__(self):
        self.font_big  = pygame.font.SysFont("Impact", 48)
        self.font_med  = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_sm   = pygame.font.SysFont("Arial", 16)
        self.name      = ""
        self.tick      = 0

    def run(self, screen, clock, score: int) -> str:
        self.name = ""
        while True:
            self.tick += 1
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.name or "AGENT"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.name.strip() or "AGENT"
                    elif event.key == pygame.K_ESCAPE:
                        return self.name.strip() or "AGENT"
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif len(self.name) < self.MAX_LEN:
                        ch = event.unicode
                        if ch.isprintable() and ch not in '"\\/':
                            self.name += ch
            self._draw(screen, score)
            pygame.display.flip()

    def _draw(self, screen, score):
        screen.fill((10, 10, 30))
        # Stars
        import math
        for i in range(40):
            bri = int(60 + 60 * math.sin(self.tick * 0.04 + i))
            pygame.draw.circle(screen, (bri, bri, bri+40),
                               ((i*173+50)%SCREEN_WIDTH, (i*97+40)%SCREEN_HEIGHT), 1)

        t = self.font_big.render("MISSION COMPLETE!", True, C_GREEN)
        screen.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2, 80))

        sc = self.font_med.render(f"Score: {score:,}", True, C_TOKEN)
        screen.blit(sc, (SCREEN_WIDTH//2 - sc.get_width()//2, 155))

        prompt = self.font_med.render("Enter your name:", True, C_WHITE)
        screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, 220))

        # Input box
        box_w, box_h = 320, 48
        bx = SCREEN_WIDTH//2 - box_w//2
        by = 260
        pygame.draw.rect(screen, (30, 30, 60), (bx, by, box_w, box_h), border_radius=6)
        pygame.draw.rect(screen, C_ACCENT,     (bx, by, box_w, box_h), 2, border_radius=6)
        cursor = "|" if (self.tick // 18) % 2 == 0 else ""
        name_txt = self.font_med.render(self.name + cursor, True, C_WHITE)
        screen.blit(name_txt, (bx + 12, by + 10))

        hint = self.font_sm.render("ENTER to confirm  |  ESC to skip", True, (140,140,180))
        screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, 325))


# ── Scoreboard draw helper ────────────────────────────────────
def draw_scoreboard(surface, tick):
    import math
    surface.fill((8, 8, 25))
    for i in range(50):
        bri = int(50 + 50 * math.sin(tick*0.03 + i*0.7))
        pygame.draw.circle(surface, (bri, bri, bri+50),
                           ((i*137+30)%SCREEN_WIDTH, (i*97+20)%SCREEN_HEIGHT), 1)

    font_title = pygame.font.SysFont("Impact", 42)
    font_head  = pygame.font.SysFont("Arial", 16, bold=True)
    font_row   = pygame.font.SysFont("Arial", 18)
    font_hint  = pygame.font.SysFont("Arial", 14)

    t = font_title.render("LEADERBOARD", True, C_TOKEN)
    surface.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2, 30))
    pygame.draw.line(surface, C_ACCENT, (80, 85), (SCREEN_WIDTH-80, 85), 2)

    # Column headers
    surface.blit(font_head.render("#",     True, (160,160,200)), (100, 95))
    surface.blit(font_head.render("NAME",  True, (160,160,200)), (145, 95))
    surface.blit(font_head.render("SCORE", True, (160,160,200)), (680, 95))
    pygame.draw.line(surface, (40,40,80), (80, 115), (SCREEN_WIDTH-80, 115), 1)

    entries = get_scores()
    if not entries:
        msg = font_row.render("No scores yet – finish a game to appear here!", True, (120,120,160))
        surface.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 200))
    else:
        medal = {0:(255,215,0), 1:(192,192,192), 2:(205,127,50)}
        for rank, e in enumerate(entries):
            ry   = 122 + rank * 32
            col  = medal.get(rank, C_WHITE)
            if rank % 2 == 0:
                row_bg = pygame.Surface((SCREEN_WIDTH-160, 28), pygame.SRCALPHA)
                row_bg.fill((255,255,255,12))
                surface.blit(row_bg, (80, ry))
            surface.blit(font_row.render(f"{rank+1}.", True, col),        (100, ry+2))
            surface.blit(font_row.render(e["name"],    True, col),        (145, ry+2))
            sc = font_row.render(f"{e['score']:,}",    True, col)
            surface.blit(sc, (680 + 80 - sc.get_width(), ry+2))

    blink = (tick // 30) % 2
    if blink:
        h = font_hint.render("ENTER or ESC to return to main menu", True, C_TOKEN)
        surface.blit(h, (SCREEN_WIDTH//2 - h.get_width()//2, SCREEN_HEIGHT - 40))
