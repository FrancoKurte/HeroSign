from PIL import Image
import pygame as pg


def trim_img(path):
    img = Image.open(path)
    if img.mode not in ['RGB', 'RGBA']:
        img = img.convert('RGBA')
    img = img.crop(img.getbbox())
    return img.tobytes(), img.size, img.mode

def scale(old_width, old_height, factor=1) -> tuple:
    new_width = old_width * factor
    new_height = old_height * factor

    return int(new_width), int(new_height)

def load_img(path, factor=1, flip=False):        
    data, size, mode = trim_img(path)
    img = pg.image.fromstring(data, size, mode)
    img = pg.transform.scale(img, scale(img.get_size()[0], img.get_size()[1], factor))
    if flip: 
        return pg.transform.flip(img, flip, False)
    return img

def margin_range(center, margin=1):
    return list(range(int(center)-int(margin), int(center)+int(margin+1)))

def parallel_range(value=1):
    return list(range(-int(value), int(value+1)))