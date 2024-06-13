from pathlib import Path
from os import fspath
import pygame as pg

BASE_DIR = Path(__file__).parent.parent.parent / ""
FONTS_DIR = BASE_DIR / "assets/extra/fonts"

def load_font(file_path, size=32):
    font = pg.font.Font(fspath(file_path), size)
    return font

FONTS = {
    "MAGO1": load_font(FONTS_DIR / "mago1.ttf"),
    "MAGO2": load_font(FONTS_DIR / "mago1.ttf", size=64),
    "MAGO3": load_font(FONTS_DIR / "mago1.ttf", size=82),
}
