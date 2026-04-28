# assets/music/

Drop level background music files here once you have them.

## Naming convention

| File              | Plays during         |
|-------------------|----------------------|
| `level1_bgm.ogg`  | Level 1 gameplay     |
| `level2_bgm.ogg`  | Level 2 gameplay     |
| `level3_bgm.ogg`  | Level 3 gameplay     |
| `level4_bgm.ogg`  | Level 4 gameplay     |
| `level5_bgm.ogg`  | Level 5 gameplay     |

## Supported formats
`.ogg` (recommended), `.mp3`, `.wav`

## How it works
The audio manager checks this folder at startup. If a BGM file exists
for the current level it will loop automatically during gameplay.
If no file is found for a level, gameplay continues silently until
you add one — no code changes needed.
