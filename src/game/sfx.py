import pygame as pg
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent.parent / "assets/sfx/"
CHAR_DIR = BASE_DIR / "characters/"
EXTRA_DIR = BASE_DIR / "extra/"
MAPS_DIR = BASE_DIR / "maps/"

pg.mixer.init()

def load_sfx(file_path, volume=0.6):
    sound = pg.mixer.Sound(os.fspath(file_path))
    sound.set_volume(volume)
    return sound

def get_sfx(entity):
    return SFX["CHARACTERS"].get(entity.upper(), {}).get("attack", None)

def get_music(map):
    return SFX["MAPS"].get(map, None)

SFX = {
    "CHARACTERS": {
        "PLAYER": {
            "attack": load_sfx(CHAR_DIR / "hero/attack/attack.mp3", volume=0.8),
        },
        "HARVESTER": {
            "attack": load_sfx(CHAR_DIR / "harvester/attack/attack.mp3", volume=0.45),
        },
        "SHADOW": {
            "attack": load_sfx(CHAR_DIR / "shadow/attack/attack.mp3", volume=0.5),
        },
        "SKULL": {
            "attack": load_sfx(CHAR_DIR / "skull/attack/attack.mp3", volume=0.5),
        },
        "WITCH": {
            "attack": load_sfx(CHAR_DIR / "witch/attack/attack.mp3", volume=0.7),
        },
        "VOIDWARRIOR": {
            "attack": load_sfx(CHAR_DIR / "voidwarrior/attack/attack.mp3", volume=0.5),
        },
        "ASSASSIN": {
            "attack": load_sfx(CHAR_DIR / "assassin/attack/attack.mp3", volume=0.5),
        },
        "SORCERER": {
            "attack": load_sfx(CHAR_DIR / "sorcerer/attack/attack.mp3", volume=0.7),
        },
    },
    "EXTRA": {
        "CRYSTAL": load_sfx(EXTRA_DIR / "crystal/crystal.mp3"),
    },
    "MAPS": {
        1: load_sfx(MAPS_DIR / "map1/music.mp3"),
        2: load_sfx(MAPS_DIR / "map2/music.mp3"),
        3: load_sfx(MAPS_DIR / "map3/music.mp3"),
        4: load_sfx(MAPS_DIR / "map4/music.mp3"),
        5: load_sfx(MAPS_DIR / "map5/music.mp3"),
        6: load_sfx(MAPS_DIR / "map6/music.mp3"),
    }
}

# Set default volume for music
for music in SFX["MAPS"].values():
    music.set_volume(1.0)