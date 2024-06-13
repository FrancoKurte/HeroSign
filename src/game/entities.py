from pygame.sprite import Sprite
from .sprites import get_frame, get_len, adjust_pos
from pathlib import Path
from .utils import margin_range
from .sfx import get_sfx
import random, string
import pygame as pg

BASE_DIR = Path(__file__).parent.parent.parent / ""
ASSETS_DIR = BASE_DIR / "assets"

class Physics():
    def __init__(self):
        self.movement = {
            "left": False,
            "right": False,
        }
        self.velocity = {
            "x": 1,
        }
        self.objective_reached = False

    def set_velocity(self, x=1) -> None:
        self.velocity["x"] = x

    def check_objective_reached(self, objective):
            if objective:
                from_distance = 100
                objective = (objective.rect.x + objective.rect.w)
                minimum_distance = margin_range(objective, from_distance)
                if not self.rect.x in minimum_distance:
                    self.objective_reached = False
                else:
                    self.objective_reached = True

    def move(self, objective) -> None:
        if self.current_health_points <= 0:
            return
        if self.not_static():
            frame_movement = {
                "left": self.movement["left"] * self.velocity["x"],
                "right": self.movement["right"] * self.velocity["x"],
            }
            if objective:
                from_distance = 100
                objective = (objective.rect.x + objective.rect.w)
                minimum_distance = margin_range(objective, from_distance)
                if not self.rect.x in minimum_distance:
                    self.movement["left"] = True
                else:
                    self.movement["left"] = False
                self.pos["x"] -= self.movement["left"] * self.velocity["x"]
                self.rect.x = self.pos["x"]
            else:
                self.pos["x"] += -frame_movement["left"] + frame_movement["right"]
                self.rect.x = self.pos["x"]

    def not_static(self):
        return not self.entity in ("WITCH", "SORCERER")

class Animation(Physics):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity
        self.attack_sfx = get_sfx(self.entity)

    def death(self, flip=False) -> None:
        if self.current_health_points <= 0:
            self.set_action("death", flip)

    def damage(self, flip=False) -> None:
        if self.current_health_points > 0:
            self.current_health_points -= 1   
            self.set_action("damage", flip)

    def run(self, flip=False) -> None:
        if self.current_health_points > 0:
            if self.not_static():
                self.set_action("run", flip)
    
    def attack(self, flip=False) -> None:
        if self.can_attack:
            if self.current_health_points > 0:
                self.set_action("attack", flip)
                if self.attack_sfx:
                    self.attack_sfx.play()

    def idle(self, flip=False) -> None:
        if self.current_health_points > 0:
            self.set_action("idle", flip)
            if self.attack_sfx:
                self.attack_sfx.stop()

class Entity(Sprite, Animation):
    def __init__(self, surface, entity, action, pos, flip=False):
        Sprite.__init__(self)
        Animation.__init__(self, entity)
        self.entity = entity
        self.is_dead = False
        self.can_attack = False
        self.surface = surface
        self.action = action
        self.pos = {
            "x": pos[0],
            "y": pos[1]
        }
        self.current_character = ""
        self.current = 0
        self.len = get_len(self.entity, self.action)
        self.frames = [get_frame(self.entity, self.action, index=i, flip=flip) for i in range(self.len)]
        self.img = self.frames[self.current]
        self.rect = adjust_pos(self.img, self.pos["x"], self.pos["y"])
        self.base_width = self.rect.width
        self.attack_sfx = get_sfx(entity)

    def render_next(self, entity=None) -> None:
        if self.current >= self.len - 1:                
            self.current = 0
            if self.current_health_points <= 0:
                self.kill()
                self.remove()
                if self.__class__.__name__ == "Player":
                    self.death_animation_completed = True
                    self.current = self.len - 1
            if entity:
                self.do_damage(entity)
            
        self.img = self.frames[int(self.current)]
        frame_width = self.img.get_width()
        self.rect = adjust_pos(self.img, self.pos["x"] - (frame_width - self.base_width) // 2, self.pos["y"])
        self.current += 0.12
        self.surface.blit(self.img, self.rect)

    def set_action(self, action, flip) -> None:
        if self.action != action:
            self.action = action
            self.len = get_len(self.entity, self.action)
            self.frames = [get_frame(self.entity, self.action, index=i, flip=flip) for i in range(self.len)]
            self.current = 0
            self.img = self.frames[self.current]
            self.rect = adjust_pos(self.img, self.pos["x"], self.pos["y"])
            self.base_width = self.rect.width
    
    def do_damage(self, entity=None):
        if self.current_health_points <= 0:
            return
        if self.__class__.__name__ == "Player" and entity:
            if self.can_attack:
                entity.current_health_points -= self.power
                if entity.current_health_points <= 0:
                    self.add_points(kill=True)
                    self.can_attack = False
                    self.current_character = ""
                    self.idle()
        else:
            if entity and self.can_attack and not self.has_been_attacked:
                entity.current_health_points -= self.power
                self.can_attack = False
                self.has_been_attacked = True

class Player(Entity):
    def __init__(self, surface, action, pos=(0, 0), flip=False):
        super().__init__(surface, "PLAYER", action, pos, flip)
        self.set_velocity(x=2)
        self.max_health_points = 30
        self.current_health_points = self.max_health_points
        self.power = 1
        self.score = {
            "points": 0,
            "crystals": 0,
        }
        self.death_animation_completed = False

    def heal(self) -> None:
        self.current_health_points = self.max_health_points

    def update_character(self, char):
        self.current_character = char

    def add_points(self, kill=False):
        if kill:
            self.score["points"] += 1

    def add_crystal(self, kill=False):
        if kill:
            self.scocre["crustals"] += 1

    def get_score(self):
        return (self.score["points"], self.score["crystals"])

    def reset(self) -> None:
        self.current_health_points = self.max_health_points
        self.score["points"] = 0
        self.score["crystals"] = 0

class Enemy():
    def __init__(self, power=1):
        self.power = power
        self.excluded_keys = "MNQPRA"
        self.has_been_attacked = True

    def update_character(self):
        uppercase_letters = "".join(char for char in string.ascii_uppercase if char not in self.excluded_keys)
        random_index = random.randint(0, len(uppercase_letters) - 1)
        self.current_character = uppercase_letters[random_index]

class Harvester(Entity, Enemy):
    def __init__(self, surface, action, pos=(0, 0), flip=True):
        super().__init__(surface, "HARVESTER", action, pos, flip=True)
        Enemy.__init__(self, power=1)
        self.set_velocity(x=1)
        self.max_health_points = 1
        self.current_health_points = self.max_health_points

class Shadow(Entity, Enemy):
    def __init__(self, surface, action, pos=(0, 0), flip=False):
        super().__init__(surface, "SHADOW", action, pos, flip)
        Enemy.__init__(self, power=1)
        self.set_velocity(x=2)
        self.max_health_points = 1
        self.current_health_points = self.max_health_points

class Skull(Entity, Enemy):
    def __init__(self, surface, action, pos=(0, 0), flip=False):
        super().__init__(surface, "SKULL", action, pos, flip)
        Enemy.__init__(self, power=1)
        self.set_velocity(x=2)
        self.max_health_points = 1
        self.current_health_points = self.max_health_points

class Witch(Entity, Enemy):
    def __init__(self, surface, action, pos=(0, 0), flip=True):
        super().__init__(surface, "WITCH", action, pos, flip)
        Enemy.__init__(self, power=1)
        self.max_health_points = 1
        self.current_health_points = self.max_health_points

class Voidwarrior(Entity, Enemy):
    def __init__(self, surface, action, pos=(0, 0), flip=False):
        super().__init__(surface, "VOIDWARRIOR", action, pos, flip)
        Enemy.__init__(self, power=1)
        self.set_velocity(x=2)
        self.max_health_points = 1
        self.current_health_points = self.max_health_points

class Assassin(Entity, Enemy):
    def __init__(self, surface, action, pos=(0, 0), flip=False):
        super().__init__(surface, "ASSASSIN", action, pos, flip)
        Enemy.__init__(self, power=1)
        self.set_velocity(x=1)
        self.max_health_points = 1
        self.current_health_points = self.max_health_points

class Sorcerer(Entity, Enemy):
    def __init__(self, surface, action, pos=(0, 0), flip=True):
        super().__init__(surface, "SORCERER", action, pos, flip)
        Enemy.__init__(self, power=1)
        self.max_health_points = 1
        self.current_health_points = self.max_health_points