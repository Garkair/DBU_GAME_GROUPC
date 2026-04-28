# ─────────────────────────────────────────────────────────────
#  audio_manager.py
#
#  Three separate audio categories:
#
#  INTRO STINGS  (assets/sounds/intro/levelN.ogg)
#    Played ONCE on the mission-briefing splash screen.
#    Loaded as pygame.Sound so they never loop.
#
#  ONE-SHOT SFX  (assets/sounds/)
#    hit_prof / hit_students / hit_drones – fired on enemy contact.
#    opening / level_complete / game_completion – state transitions.
#
#  BGM  (assets/music/levelN_bgm.ogg)   ← drop files here when ready
#    Looping background music during gameplay.
#    If the file doesn't exist the game just runs silently.
# ─────────────────────────────────────────────────────────────

import os
import pygame

# ── Paths ─────────────────────────────────────────────────────
_ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SFX_DIR   = os.path.join(_ROOT, "assets", "sounds")
_INTRO_DIR = os.path.join(_ROOT, "assets", "sounds", "intro")
_MUSIC_DIR = os.path.join(_ROOT, "assets", "music")

# ── Manifests ─────────────────────────────────────────────────

# One-shot SFX played via pygame.mixer.Sound (never loop)
_SFX_FILES = {
    "hit_prof":       "hit_prof.ogg",
    "hit_students":   "hit_students.ogg",
    "hit_drones":     "hit_drones.ogg",
    "opening":        "opening.ogg",
    "level_complete": "level_complete.ogg",
    "game_completion":"game_completion.ogg",
}

# Level intro stings – play once on briefing splash, no loop
_INTRO_FILES = {
    1: "level1.ogg",
    2: "level2.ogg",
    3: "level3.ogg",
    4: "level4.ogg",
    5: "level5.ogg",
}

# BGM files – looped during gameplay (optional, loaded from assets/music/)
_BGM_FILES = {
    1: "level1_bgm.ogg",
    2: "level2_bgm.ogg",
    3: "level3_bgm.ogg",
    4: "level4_bgm.ogg",
    5: "level5_bgm.ogg",
}

# Enemy class name → sfx key
_ENEMY_SFX = {
    "Prof":        "hit_prof",
    "SlowStudent": "hit_students",
    "FastStudent": "hit_students",
    "FlyingDrone": "hit_drones",
}

# ── State ─────────────────────────────────────────────────────
_sfx_cache:   dict  = {}   # key → pygame.Sound  (SFX + intros)
_enabled:     bool  = True
_sfx_volume:  float = 0.9
_music_volume:float = 0.7
_mixer_ok:    bool  = False
_current_bgm: str   = ""   # path of currently looping BGM


# ── Init ──────────────────────────────────────────────────────

def init() -> None:
    """Initialise mixer and preload all SFX / intro stings."""
    global _mixer_ok
    if _mixer_ok:
        return
    try:
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        _mixer_ok = True
        _preload_sfx()
        _preload_intros()
        print("[Audio] Mixer initialised OK")
    except Exception as exc:
        print(f"[Audio] Mixer unavailable – running silent ({exc})")
        _mixer_ok = False


def _preload_sfx() -> None:
    for key, fname in _SFX_FILES.items():
        path = os.path.join(_SFX_DIR, fname)
        if os.path.isfile(path):
            try:
                snd = pygame.mixer.Sound(path)
                snd.set_volume(_sfx_volume)
                _sfx_cache[key] = snd
                print(f"[Audio] SFX loaded: {key}")
            except Exception as exc:
                print(f"[Audio] SFX load failed '{key}': {exc}")
        else:
            print(f"[Audio] SFX missing: {path}")


def _preload_intros() -> None:
    for level_num, fname in _INTRO_FILES.items():
        path = os.path.join(_INTRO_DIR, fname)
        if os.path.isfile(path):
            try:
                snd = pygame.mixer.Sound(path)
                snd.set_volume(_sfx_volume)
                _sfx_cache[f"intro_{level_num}"] = snd
                print(f"[Audio] Intro loaded: level {level_num}")
            except Exception as exc:
                print(f"[Audio] Intro load failed level {level_num}: {exc}")
        else:
            print(f"[Audio] Intro missing: {path}")


# ── Intro stings ──────────────────────────────────────────────

def play_level_intro(level_index: int) -> None:
    """
    Play the level intro sting ONCE (no loop) on the briefing splash.
    level_index is 0-based.
    """
    if not _mixer_ok or not _enabled:
        return
    key = f"intro_{level_index + 1}"
    snd = _sfx_cache.get(key)
    if snd:
        snd.stop()   # stop if somehow already playing
        snd.play(loops=0)


# ── BGM (gameplay loop) ───────────────────────────────────────

def play_level_bgm(level_index: int) -> None:
    """
    Start looping BGM for gameplay.  If no file exists, stops any
    current music silently so the game never crashes.
    level_index is 0-based.
    """
    global _current_bgm
    if not _mixer_ok:
        return
    fname = _BGM_FILES.get(level_index + 1)
    path  = os.path.join(_MUSIC_DIR, fname) if fname else ""
    if not path or not os.path.isfile(path):
        # No BGM yet – stop whatever is playing and continue silently
        pygame.mixer.music.stop()
        _current_bgm = ""
        return
    if path == _current_bgm and pygame.mixer.music.get_busy():
        return  # already playing, don't restart
    try:
        pygame.mixer.music.fadeout(400)
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(_music_volume)
        pygame.mixer.music.play(loops=-1, fade_ms=600)
        _current_bgm = path
        print(f"[Audio] BGM started: {fname}")
    except Exception as exc:
        print(f"[Audio] BGM failed: {exc}")


def stop_bgm(fade_ms: int = 600) -> None:
    global _current_bgm
    if _mixer_ok:
        pygame.mixer.music.fadeout(fade_ms)
    _current_bgm = ""


# ── One-shot SFX ──────────────────────────────────────────────

def play_sfx(key: str) -> None:
    if not _mixer_ok or not _enabled:
        return
    snd = _sfx_cache.get(key)
    if snd:
        snd.play(loops=0)


def play_hit_sfx(enemy) -> None:
    key = _ENEMY_SFX.get(type(enemy).__name__, "hit_students")
    play_sfx(key)


def play_level_complete() -> None:
    stop_bgm(fade_ms=300)
    play_sfx("level_complete")


def play_game_completion() -> None:
    stop_bgm(fade_ms=300)
    play_sfx("game_completion")


def play_opening() -> None:
    stop_bgm(fade_ms=0)
    play_sfx("opening")


# ── Volume ────────────────────────────────────────────────────

def set_music_volume(vol: float) -> None:
    global _music_volume
    _music_volume = max(0.0, min(1.0, vol))
    if _mixer_ok:
        pygame.mixer.music.set_volume(_music_volume)


def set_sfx_volume(vol: float) -> None:
    global _sfx_volume
    _sfx_volume = max(0.0, min(1.0, vol))
    for snd in _sfx_cache.values():
        snd.set_volume(_sfx_volume)


def toggle_mute() -> bool:
    """Toggle mute. Returns True if now muted."""
    global _enabled
    _enabled = not _enabled
    if _mixer_ok:
        vol = _music_volume if _enabled else 0.0
        pygame.mixer.music.set_volume(vol)
        sfx_vol = _sfx_volume if _enabled else 0.0
        for snd in _sfx_cache.values():
            snd.set_volume(sfx_vol)
    return not _enabled


def is_enabled() -> bool:
    return _enabled


def quit() -> None:
    if _mixer_ok:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
