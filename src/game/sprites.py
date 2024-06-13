from .utils import load_img
from os import listdir
from pygame import transform
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent.parent / ""
CHAR_DIR =  BASE_DIR / "assets\characters"

def adjust_pos(frame, x, y):
    rect = frame.get_rect()
    rect.x = x
    rect.y = y - rect.height
    return rect

def get_frame(entity, action, index=0, flip=False):
    frame = SPRITES[entity][action][index]
    if flip and entity != "SHADOW" and entity != "ASSASSIN":
        return transform.flip(frame, flip, False)
    return frame

def get_len(entity, action):
    return len(SPRITES[entity][action])

def load_all_frames(path, factor) -> list:
    frames = [load_img(f"{CHAR_DIR / path / frame}", factor)
               for frame in listdir(CHAR_DIR / path)]
    return frames

FACTORS = {
    "PLAYER": 4,
    "HARVESTER": 0.8,
    "SHADOW": 1.5,
    "WITCH": 3.3,
    "SKULL": 2.5,
    "ASSASSIN": 3.5,
    "VOIDWARRIOR": 2,
    "SORCERER": 3,
}

SPRITES = {
    "PLAYER": {
        "idle": load_all_frames("hero\idle", factor=FACTORS["PLAYER"]),
        "attack": load_all_frames(r"hero\attack", factor=FACTORS["PLAYER"]),
        "run": load_all_frames(r"hero\run", factor=FACTORS["PLAYER"]),
        "damage": load_all_frames("hero\damage", factor=FACTORS["PLAYER"]),
        "death": load_all_frames("hero\death", factor=FACTORS["PLAYER"]),
    },
    "HARVESTER": {
        "idle": load_all_frames(r"harvester\idle", factor=FACTORS["HARVESTER"]),
        "attack": load_all_frames(r"harvester\attack", factor=FACTORS["HARVESTER"]),
        "run": load_all_frames(r"harvester\run", factor=FACTORS["HARVESTER"]),
        "damage": load_all_frames("harvester\damage", factor=FACTORS["HARVESTER"]),
        "death": load_all_frames("harvester\death", factor=FACTORS["HARVESTER"]),
    },
    "SHADOW": {
        "idle": load_all_frames(r"shadow\idle", factor=FACTORS["SHADOW"]),
        "attack": load_all_frames(r"shadow\attack", factor=FACTORS["SHADOW"]),
        "run": load_all_frames(r"shadow\run", factor=FACTORS["SHADOW"]),
        "death": load_all_frames("shadow\death", factor=FACTORS["SHADOW"]),
    },
    "SKULL": {
        "idle": load_all_frames(r"skull\run", factor=FACTORS["SKULL"]),
        "run": load_all_frames(r"skull\run", factor=FACTORS["SKULL"]),
        "attack": load_all_frames(r"skull\run", factor=FACTORS["SKULL"]),
        "death": load_all_frames(r"skull\death", factor=FACTORS["SKULL"]),
    },
    "WITCH": {
        "idle": load_all_frames(r"witch\idle", factor=FACTORS["WITCH"]),
        "attack": load_all_frames(r"witch\attack", factor=FACTORS["WITCH"]),
        "run": load_all_frames(r"witch\idle", factor=FACTORS["WITCH"]),
        "death": load_all_frames(r"witch\death", factor=FACTORS["WITCH"]),
    },
    "VOIDWARRIOR": {
        "idle": load_all_frames(r"voidwarrior\idle", factor=FACTORS["VOIDWARRIOR"]),
        "attack": load_all_frames(r"voidwarrior\attack", factor=FACTORS["VOIDWARRIOR"]),
        "run": load_all_frames(r"voidwarrior\run", factor=FACTORS["VOIDWARRIOR"]),
        "damage": load_all_frames("voidwarrior\damage", factor=FACTORS["VOIDWARRIOR"]),
        "death": load_all_frames("voidwarrior\death", factor=FACTORS["VOIDWARRIOR"]),
    },
    "ASSASSIN": {
        "idle": load_all_frames(r"assassin\idle", factor=FACTORS["ASSASSIN"]),
        "attack": load_all_frames(r"assassin\attack", factor=FACTORS["ASSASSIN"]),
        "run": load_all_frames(r"assassin\run", factor=FACTORS["ASSASSIN"]),
        "damage": load_all_frames("assassin\damage", factor=FACTORS["ASSASSIN"]),
        "death": load_all_frames("assassin\death", factor=FACTORS["ASSASSIN"]),
    },
    "SORCERER": {
        "idle": load_all_frames(r"sorcerer\idle", factor=FACTORS["SORCERER"]),
        "attack": load_all_frames(r"sorcerer\attack", factor=FACTORS["SORCERER"]),
        "death": load_all_frames(r"sorcerer\death", factor=FACTORS["SORCERER"]),
        "run": load_all_frames(r"sorcerer\idle", factor=FACTORS["SORCERER"]),
    }
}


if __name__== "__main__":
    pass