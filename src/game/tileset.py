from pathlib import Path
import pygame as pg

BASE_DIR = Path(__file__).parent.parent.parent / ""
TILESET_DIR =  BASE_DIR / r"assets\tileset"

FLOOR = {
    1:695,
    2:680,
    3:695,
    4:695,
    5:625,
    6:555,
}

MAPS = {
    1:rf"{TILESET_DIR}\background\map1\map1.png",
    2:rf"{TILESET_DIR}\background\map2\map2.png",
    3:rf"{TILESET_DIR}\background\map3\map3.png",
    4:rf"{TILESET_DIR}\background\map4\map4.jpg",
    5:rf"{TILESET_DIR}\background\map5\map5.jpg",
    6:rf"{TILESET_DIR}\background\map6\map6.jpg",
}

DECORATORS = {
    3: rf"{TILESET_DIR}\background\decorator.png",
    4: rf"{TILESET_DIR}\background\decorator.png",
}


def load_tile(dict, key, width, height):
    if dict == "MAPS":
        path = MAPS[key]
    elif dict == "DECORATORS":
        path = DECORATORS[key]

    img = pg.image.load(path)    
    return pg.transform.scale(img, (width, height))