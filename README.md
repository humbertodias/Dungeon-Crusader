# Dungeon-Crusader

Start run.bat to play (run.py not working currently)

Required modules: pygame (https://www.pygame.org/wiki/GettingStarted)

Requires python 3.x

### Controls:
| key | action|
|-----|-------|
| ARROW KEYS| move the player|
| Z (Y on QWERTZ keyboard)| Item A |
| X | Item B |
| ENTER | Interact (Doors, Chest etc.) |
| ESC | open inventory |
| F6 | quicksave (might crash the game!)|
| F9| quickload |
| H | debug mode |

### Controls in debug mode:
| key | action|
|-----|-------|
|F4 | slow motion mode (5 FPS)|
|PAGEUP/PAGEDOWN | add/remove items|
|F12 | save dungeon image as png (freezes the game) |
| V | Display/hide enemy aggro radius|
| K | kill all enemies on the screen |


Install
```
pip3 install -r requirements.txt 
```

Run

```
python3 modules/main.py
```

Format
```
pip3 install yapf
yapf -i game.py
```

# Tools

[Tiled](https://www.mapeditor.org)
