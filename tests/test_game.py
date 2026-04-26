"""
tests/test_game.py  –  headless smoke tests for Operation DBU: Reloaded
Run with:  python -m pytest tests/ -v
"""

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pytest
import pygame

pygame.init()
pygame.display.set_mode((960, 540))


# ── Imports ───────────────────────────────────────────────────
from game.constants import *
from game.player      import Player
from game.enemies     import SlowStudent, FastStudent, FlyingDrone
from game.collectibles import AccessChip, PatriotToken, ExitPortal
from game.levels      import LEVEL_DATA, build_tiles
from game.sprites     import (make_player_sprite, make_slow_student,
                               make_fast_student, make_drone,
                               make_access_chip, make_patriot_token)


# ── Constants ─────────────────────────────────────────────────
def test_screen_dimensions():
    assert SCREEN_WIDTH  == 960
    assert SCREEN_HEIGHT == 540
    assert TILE_SIZE     == 40


# ── Sprites ───────────────────────────────────────────────────
@pytest.mark.parametrize("fn,expected_w,expected_h", [
    (make_player_sprite,  28, 40),
    (make_slow_student,   26, 38),
    (make_fast_student,   26, 36),
    (make_drone,          34, 28),
    (make_access_chip,    22, 22),
    (make_patriot_token,  20, 20),
])
def test_sprite_size(fn, expected_w, expected_h):
    surf = fn(0)
    assert surf.get_size() == (expected_w, expected_h)


# ── Player ────────────────────────────────────────────────────
def test_player_initial_state():
    p = Player(80, 380)
    assert p.lives  == PLAYER_MAX_LIVES
    assert p.score  == 0
    assert not p.dead
    assert p.invincible == 0


def test_player_hit_reduces_lives():
    p = Player(80, 380)
    p.hit()
    assert p.lives == PLAYER_MAX_LIVES - 1
    assert p.invincible == INVINCIBILITY_FRAMES


def test_player_invincibility_prevents_double_hit():
    p = Player(80, 380)
    p.hit()
    p.hit()  # should be blocked by invincibility
    assert p.lives == PLAYER_MAX_LIVES - 1


def test_player_dies_at_zero_lives():
    p = Player(80, 380)
    for _ in range(PLAYER_MAX_LIVES):
        p.invincible = 0
        p.hit()
    assert p.dead


def test_player_update_with_tiles():
    tiles = build_tiles(0)
    p = Player(80, 380)
    for _ in range(10):
        p.update(tiles)
    # Player should land on ground (level 1 ground is at y=460)
    assert p.rect.bottom <= 465


# ── Enemies ───────────────────────────────────────────────────
def test_slow_student_stays_in_patrol():
    enemy = SlowStudent(400, 420, 300, 700)
    tiles = build_tiles(0)
    for _ in range(300):
        enemy.update(tiles)
    assert enemy.patrol_left <= enemy.rect.left
    assert enemy.rect.right <= enemy.patrol_right


def test_fast_student_speed_greater_than_slow():
    assert FAST_STUDENT_SPEED > SLOW_STUDENT_SPEED


def test_drone_stays_in_vertical_patrol():
    drone = FlyingDrone(400, 200, 100, 400)
    tiles = []
    for _ in range(300):
        drone.update(tiles)
    assert drone.patrol_top    <= drone.rect.top
    assert drone.rect.bottom   <= drone.patrol_bottom


# ── Collectibles ──────────────────────────────────────────────
def test_access_chip_initial_state():
    chip = AccessChip(100, 100)
    assert not chip.collected


def test_patriot_token_initial_state():
    token = PatriotToken(100, 100)
    assert not token.collected


def test_exit_portal_initially_locked():
    portal = ExitPortal(500, 300)
    assert not portal.active


def test_chip_animation_advances():
    chip = AccessChip(100, 100)
    for _ in range(5):
        chip.update()
    assert chip.frame_timer >= 0  # just ensure no crash


# ── Level data ────────────────────────────────────────────────
def test_all_levels_exist():
    assert len(LEVEL_DATA) == 5


@pytest.mark.parametrize("index", range(5))
def test_level_structure(index):
    data = LEVEL_DATA[index]
    assert "name"      in data
    assert "mission"   in data
    assert "tiles"     in data
    assert "chips"     in data
    assert "exit"      in data
    assert len(data["chips"]) == data["chips_needed"]


@pytest.mark.parametrize("index", range(5))
def test_level_builds_tiles(index):
    tiles = build_tiles(index)
    assert len(tiles) > 0
    for tile in tiles:
        assert tile.rect.width  == TILE_SIZE
        # ground tiles are full height, platform tiles may vary
        assert tile.rect.height >= TILE_SIZE // 2


def test_level5_has_most_enemies():
    l5 = LEVEL_DATA[4]
    l1 = LEVEL_DATA[0]
    enemies_5 = len(l5["slow_students"]) + len(l5["fast_students"]) + len(l5["drones"])
    enemies_1 = len(l1["slow_students"]) + len(l1["fast_students"]) + len(l1["drones"])
    assert enemies_5 > enemies_1


def test_level5_chips_needed():
    assert LEVEL_DATA[4]["chips_needed"] == 5


def test_level1_chips_needed():
    assert LEVEL_DATA[0]["chips_needed"] == 3


# ── Score ─────────────────────────────────────────────────────
def test_score_constants_positive():
    from game.game_engine import SCORE_CHIP, SCORE_TOKEN, SCORE_LEVEL
    assert SCORE_CHIP  > 0
    assert SCORE_TOKEN > 0
    assert SCORE_LEVEL > 0
