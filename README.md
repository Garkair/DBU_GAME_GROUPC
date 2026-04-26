# Operation DBU: Reloaded 🎮

A 2D platform game set on the campus of **Dallas Baptist University**.
You play as **Agent Patriot**, a student turned undercover agent who must
navigate five campus locations, collect Access Chips, and restore the
campus system.

---

## Project Structure

```
operation_dbu/
├── main.py                  # Entry point – run this to start the game
├── README.md
└── game/
    ├── __init__.py
    ├── constants.py         # All tunable values (speed, colours, physics)
    ├── sprites.py           # Procedural pixel-art – no external images needed
    ├── player.py            # Agent Patriot: movement, gravity, collision
    ├── enemies.py           # SlowStudent, FastStudent, FlyingDrone
    ├── collectibles.py      # AccessChip, PatriotToken, ExitPortal
    ├── levels.py            # Tile-map data for all 5 levels + Tile sprite
    ├── hud.py               # On-screen HUD (lives, score, chip counter)
    ├── screens.py           # Title, briefing, game-over, victory screens
    └── game_engine.py       # State machine & main game loop
```

---

## Requirements

| Dependency | Version   |
|------------|-----------|
| Python     | 3.9 +     |
| pygame     | 2.0 +     |

No other libraries are required.  All art is drawn procedurally at runtime.

---

## Installation

### 1 – Clone / download the project

```bash
git clone <repo-url>
cd operation_dbu
```

### 2 – Create a virtual environment (recommended)

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3 – Install pygame

```bash
pip install pygame
```

---

## Running the Game

```bash
python main.py
```

The game opens a **960 × 540** window at 60 FPS.

---

## Controls

| Key                   | Action              |
|-----------------------|---------------------|
| ← / A                 | Move left           |
| → / D                 | Move right          |
| Space / W / ↑        | Jump                |
| Enter                 | Confirm / Advance   |
| Esc                   | Quit                |

---

## Gameplay Overview

### Objective
Collect all **Access Chips** on each level, then reach the **EXIT portal**.

### Collectibles
| Item          | Points | Purpose                           |
|---------------|--------|-----------------------------------|
| Access Chip   | 500    | Required to unlock the exit       |
| Patriot Token | 100    | Bonus score / exploration reward  |

### Enemies
| Enemy         | Movement   | Levels present |
|---------------|------------|----------------|
| Slow Student  | Horizontal | 1 – 5          |
| Fast Student  | Horizontal | 3 – 5          |
| Flying Drone  | Vertical   | 2 – 5          |

Touching an enemy costs **one life**; you have a brief invincibility window
after each hit.  Falling off the bottom of the screen also costs a life.

### Levels
| #  | Location                          | Chips | Special mechanic            |
|----|-----------------------------------|-------|-----------------------------|
| 1  | Entrance – Mountain Creek Pkwy    | 3     | Tutorial / open space       |
| 2  | Collins Learning Center           | 3     | Vertical platforming        |
| 3  | Mahler Student Center             | 3     | More enemies, faster pace   |
| 4  | Dorm Zone                         | 3     | Narrow platforms / precision|
| 5  | Final Mission: Control Center     | 5     | All challenges combined     |

---

## Running Tests

A headless smoke test verifies all modules load and core logic works without
a display (useful in CI environments):

```bash
python -m pytest tests/ -v
```

Or run the built-in manual smoke test:

```bash
python -c "
import os; os.environ['SDL_VIDEODRIVER']='dummy'; os.environ['SDL_AUDIODRIVER']='dummy'
from game.game_engine import Game
from game.levels import build_tiles, LEVEL_DATA
for i in range(5):
    t = build_tiles(i)
    print(f'Level {i+1}: {len(t)} tiles OK')
print('All levels OK')
"
```

---

## Customisation

All game-feel values live in `game/constants.py`:

```python
GRAVITY        = 0.55    # increase for heavier feel
JUMP_FORCE     = -13     # more negative = higher jump
PLAYER_SPEED   = 4       # pixels per frame
SLOW_STUDENT_SPEED = 1.2
FAST_STUDENT_SPEED = 2.5
DRONE_SPEED    = 1.5
PLAYER_MAX_LIVES = 3
```

Level layouts (platform positions, enemy patrols, chip locations) are
defined as plain Python data structures in `game/levels.py` – easy to
edit without touching game logic.

---

## Architecture Notes

- **No external assets** – all sprites are drawn procedurally in `sprites.py`
  using `pygame.draw` primitives, keeping the project self-contained.
- **OOP design** – `Player`, `SlowStudent`, `FastStudent`, `FlyingDrone`,
  `AccessChip`, `PatriotToken`, `ExitPortal`, and `Tile` are all
  `pygame.sprite.Sprite` subclasses.
- **Camera system** – horizontal scrolling via a `camera_x` offset applied
  at draw time; no world-space transformations required.
- **State machine** – `game_engine.py` drives `STATE_TITLE → STATE_BRIEFING →
  STATE_PLAYING → STATE_LEVEL_DONE → …` transitions cleanly.
- **Modular levels** – adding a new level requires only a new dict entry in
  `LEVEL_DATA`; the engine picks it up automatically.

---

## Team Collaboration

Version-control workflow (as specified in the project document):

```
main        – stable, tested builds
dev         – integration branch
feature/*   – individual features (e.g. feature/drone-enemy, feature/level3)
```

Suggested split by module:
- **Gameplay mechanics** → `player.py`, `constants.py`
- **Level design** → `levels.py`
- **Enemy AI** → `enemies.py`
- **Art / visual polish** → `sprites.py`, `screens.py`
- **Testing / QA** → `tests/`

---

*Go Patriots! 🦅*
