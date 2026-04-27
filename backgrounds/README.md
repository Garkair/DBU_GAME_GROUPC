# backgrounds/

Drop your photo backgrounds here.  The game auto-detects and loads them at startup.

## Naming

| File name        | Used for |
|-----------------|----------|
| `level1.png/jpg` | Level 1 – Entrance: Mountain Creek Pkwy |
| `level2.png/jpg` | Level 2 – Collins Learning Center       |
| `level3.png/jpg` | Level 3 – Mahler Student Center         |
| `level4.png/jpg` | Level 4 – Dorm Zone                     |
| `level5.png/jpg` | Level 5 – Control Center                |

Supported formats: `.png`  `.jpg`  `.jpeg`  `.bmp`  `.webp`

## Required Aspect Ratio

The image must be one of:

| Ratio  | Example resolutions                |
|--------|------------------------------------|
| 16:9   | 1920×1080, 1280×720, 3840×2160     |
| 16:10  | 1920×1200, 1280×800                |
| 4:3    | 1024×768, 1280×960                 |

A ±6 % tolerance is applied, so phone photos typically work fine.
Images with other ratios (e.g. portrait shots) are rejected and the
procedural background is used instead.  The console will print why.

## What the game does automatically

1. **Validates** the aspect ratio on first run
2. **Scales** the image to fit the game window (960×490) with letterboxing
3. **Compresses** it to a `.cache.jpg` (≈ quality 72) next to the source –
   subsequent launches use the cache so startup is instant
4. The cache is **regenerated** automatically if you replace the source file

## Parallax scrolling

Photo backgrounds scroll at 25 % of the foreground speed, giving a
natural depth effect as the player moves through the level.
A subtle dark tint is applied so sprites always pop over bright photos.

## Tips

- Campus photos work great (buildings, fields, hallways)
- Landscape / outdoor shots suit Levels 1 & 4 (sky bg_type)
- Indoor corridor shots suit Levels 2 & 3 (indoor bg_type)
- Dark/techy images suit Level 5 (final bg_type)
- If Pillow (`pip install pillow`) is installed the cache is smaller;
  otherwise pygame's default compression is used
