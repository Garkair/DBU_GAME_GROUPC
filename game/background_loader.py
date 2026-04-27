# ─────────────────────────────────────────────────────────────
#  background_loader.py
#
#  Loads, validates, compresses and caches custom background
#  images from  <project_root>/backgrounds/
#
#  Naming convention:
#    level1.png / level1.jpg   →  Level 1
#    level2.png / level2.jpg   →  Level 2
#    ...
#    level5.png / level5.jpg   →  Level 5
#
#  Accepted aspect ratios:   16:9  (±5 %)   e.g. 1920×1080
#                            16:10 (±5 %)   e.g. 1920×1200
#                            4:3   (±5 %)   e.g. 1280×960
#  Any other ratio is rejected and the procedural BG is used.
#
#  On first load the image is:
#    1. Validated for aspect ratio
#    2. Scaled to SCREEN_WIDTH × (SCREEN_HEIGHT - HUD_HEIGHT)
#       preserving aspect ratio with letterbox/pillarbox fill
#    3. Saved as a compressed .cache.jpg next to the source
#       (quality 72, so even 6 MB PNGs become ~200 KB)
#  Subsequent launches read the cache file directly.
# ─────────────────────────────────────────────────────────────

import os
import pygame
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, HUD_HEIGHT

# ── Target render size ────────────────────────────────────────
BG_W = SCREEN_WIDTH
BG_H = SCREEN_HEIGHT - HUD_HEIGHT   # don't paint behind the HUD

# ── Accepted aspect ratios (w/h) with ±tolerance ─────────────
_RATIOS = [
    (16 / 9,   "16:9"),
    (16 / 10,  "16:10"),
    (4  / 3,   "4:3"),
]
_TOLERANCE = 0.06   # 6 % slack

# ── Supported source extensions (in priority order) ───────────
_EXTS = [".png", ".jpg", ".jpeg", ".bmp", ".webp"]

# ── In-memory cache  {level_index: Surface | None} ───────────
_cache: dict[int, pygame.Surface | None] = {}


def _backgrounds_dir() -> str:
    """Return the absolute path to the backgrounds/ folder."""
    here = os.path.dirname(os.path.abspath(__file__))          # game/
    return os.path.join(os.path.dirname(here), "backgrounds")  # project root


def _find_source(level_index: int) -> str | None:
    """Find the first matching source file for a given level."""
    folder = _backgrounds_dir()
    stem   = f"level{level_index + 1}"
    for ext in _EXTS:
        path = os.path.join(folder, stem + ext)
        if os.path.isfile(path):
            return path
    return None


def _cache_path(source_path: str) -> str:
    base, _ = os.path.splitext(source_path)
    return base + ".cache.jpg"


def _check_ratio(w: int, h: int) -> tuple[bool, str]:
    """Return (ok, description).  ok=False means reject."""
    if h == 0:
        return False, "zero height"
    ratio = w / h
    for target, name in _RATIOS:
        if abs(ratio - target) / target <= _TOLERANCE:
            return True, name
    return False, f"{w}×{h} ({ratio:.2f}) — not 16:9 / 16:10 / 4:3"


def _fit_surface(img: pygame.Surface) -> pygame.Surface:
    """
    Scale img to fill BG_W × BG_H, keeping aspect ratio.
    Any leftover area is filled with black (letterbox/pillarbox).
    """
    iw, ih = img.get_size()
    scale   = min(BG_W / iw, BG_H / ih)
    new_w   = int(iw * scale)
    new_h   = int(ih * scale)
    scaled  = pygame.transform.smoothscale(img, (new_w, new_h))

    canvas  = pygame.Surface((BG_W, BG_H))
    canvas.fill((0, 0, 0))
    canvas.blit(scaled, ((BG_W - new_w) // 2, (BG_H - new_h) // 2))
    return canvas


def _load_and_process(source_path: str) -> pygame.Surface | None:
    """
    Load source → validate → fit → write cache → return Surface.
    Returns None if the image is invalid.
    """
    try:
        img = pygame.image.load(source_path).convert()
    except Exception as exc:
        print(f"[BG] Could not load '{source_path}': {exc}")
        return None

    w, h = img.get_size()
    ok, desc = _check_ratio(w, h)
    if not ok:
        print(f"[BG] '{os.path.basename(source_path)}' rejected – aspect ratio {desc}. "
              f"Use 16:9, 16:10, or 4:3.")
        return None

    print(f"[BG] '{os.path.basename(source_path)}' accepted ({desc}, {w}×{h}) – processing…")
    fitted = _fit_surface(img)

    # Write compressed cache (jpeg quality 72)
    cache = _cache_path(source_path)
    try:
        pygame.image.save(fitted, cache)
        # Re-save as lower-quality JPEG via pygame (pygame saves .jpg at ~95 by default;
        # we use a temp approach to get quality=72 via the source filename trick)
        # pygame doesn't expose quality directly, so we save then reload is fine —
        # the file is already written above.  For true quality control, use Pillow if present.
        try:
            from PIL import Image as PILImage
            pil = PILImage.open(cache).convert("RGB")
            pil.save(cache, "JPEG", quality=72, optimize=True)
            print(f"[BG] Cache written (Pillow q=72): {os.path.basename(cache)}")
        except ImportError:
            print(f"[BG] Cache written (pygame default): {os.path.basename(cache)}")
    except Exception as exc:
        print(f"[BG] Warning – could not write cache: {exc}")

    return fitted


def _load_from_cache(source_path: str) -> pygame.Surface | None:
    cache = _cache_path(source_path)
    if not os.path.isfile(cache):
        return None
    # Invalidate cache if source is newer
    if os.path.getmtime(source_path) > os.path.getmtime(cache):
        print(f"[BG] Source newer than cache – regenerating…")
        return None
    try:
        surf = pygame.image.load(cache).convert()
        # Ensure correct size (in case constants changed)
        if surf.get_size() != (BG_W, BG_H):
            surf = pygame.transform.smoothscale(surf, (BG_W, BG_H))
        print(f"[BG] Loaded from cache: {os.path.basename(cache)}")
        return surf
    except Exception as exc:
        print(f"[BG] Cache read failed ({exc}), will reprocess.")
        return None


# ── Public API ────────────────────────────────────────────────

def get_background(level_index: int) -> pygame.Surface | None:
    """
    Return a scaled Surface for the given level, or None if no
    image is available.  Results are cached in memory.
    """
    if level_index in _cache:
        return _cache[level_index]

    source = _find_source(level_index)
    if source is None:
        _cache[level_index] = None
        return None

    # Try cache file first
    surf = _load_from_cache(source)
    if surf is None:
        surf = _load_and_process(source)

    _cache[level_index] = surf
    return surf


def preload_all() -> None:
    """Call once at startup to preload / validate all backgrounds."""
    folder = _backgrounds_dir()
    os.makedirs(folder, exist_ok=True)
    print(f"[BG] Scanning backgrounds/ …")
    found = 0
    for i in range(5):
        surf = get_background(i)
        if surf:
            found += 1
    print(f"[BG] {found}/5 custom backgrounds loaded.")


def clear_cache() -> None:
    """Wipe in-memory cache (e.g. after hot-swapping images at runtime)."""
    _cache.clear()


def get_status() -> list[dict]:
    """
    Return a list of dicts describing each level's BG status.
    Used by the debug menu.
    """
    rows = []
    folder = _backgrounds_dir()
    for i in range(5):
        source = _find_source(i)
        if source is None:
            rows.append({"level": i + 1, "status": "none", "file": "—"})
            continue
        cached = _cache.get(i)
        if cached is not None:
            rows.append({"level": i + 1, "status": "loaded",
                         "file": os.path.basename(source)})
        else:
            rows.append({"level": i + 1, "status": "found (not loaded)",
                         "file": os.path.basename(source)})
    return rows
