import pygame as pg
import random
from game.entities import Player, Shadow, Harvester, Skull, Voidwarrior, Assassin, Witch, Sorcerer
from game.tileset import load_tile, FLOOR
from game.utils import margin_range
from game.sfx import get_music
from vision.inference_classifier import HandGestureClassifier

class Game:
    def __init__(self):
        pg.init()
        from game.fonts import FONTS
        self.FONTS = FONTS
        self.font = self.FONTS["MAGO1"]
        pg.display.set_caption("HeroSign: Una Aventura de Señas")
        self.screen_size = [1366, 768]
        self.screen = pg.display.set_mode(self.screen_size, pg.HWSURFACE | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        self.map = 1
        self.background = load_tile("MAPS", self.map, width=self.screen_size[0], height=self.screen_size[1])
        self.decorator = pg.transform.flip(load_tile("DECORATORS", 3, self.screen_size[0], 500), False, True)
        self.player = Player(self.screen, "idle", (100, FLOOR[self.map]))
        self.entities = pg.sprite.Group(self.player)
        self.target = None
        self.current_character = ""
        self.NPCs = {
            3: Witch(self.screen, "idle", (1000, FLOOR[3])),
            6: Sorcerer(self.screen, "idle", (1000, FLOOR[6])), 
        }
        self.enemies = {
            1: (3, [Harvester]),
            2: (4, [Shadow, Harvester, Harvester, Harvester]),
            3: (5, [Skull, Harvester, Harvester]),
            4: (5, [Voidwarrior, Harvester, Harvester]),
            5: (3, [Assassin, Harvester, Harvester]),
            6: (5, [Shadow, Harvester, Skull, Voidwarrior, Assassin, Harvester, Harvester, Harvester]),
        }
        self.timer = {
            1: 3000,
            2: 3000,
            3: 1000,
            4: 1500,
            5: 2000,
            6: 1500,
        }
        self.music = get_music(self.map)
        self.music.set_volume(0.3)
        self.music.play(-1)
        self.win = False
        self.hand_classifier = HandGestureClassifier()

    def controller(self):
        if self.player.current_character == "A":
            self.player.movement["left"] = False
            self.player.movement["right"] = False
            self.player.can_attack = False
            self.player.idle()
            if self.target:
                self.target.can_attack = False
                self.target.idle(flip=True)

    def collision(self, *objects) -> None:
        subj = objects[0]
        objects = objects[1:]
        for obj in objects:
            if type(obj) != type(subj):
                if subj.movement["left"] and subj.rect.x in margin_range(obj.rect.x + obj.rect.w, 15):
                    subj.movement["left"] = False
                if subj.movement["right"] and (subj.rect.x + subj.rect.w) in margin_range(obj.rect.x, 15):
                    subj.movement["right"] = False

    def collision_enemies(self):
        enemies = [entity for entity in self.entities.sprites() if isinstance(entity, (Shadow, Harvester, Skull, Voidwarrior, Assassin))]
        enemies.sort(key=lambda e: e.rect.x)
        for i in range(1, len(enemies)):
            prev_enemy = enemies[i - 1]
            curr_enemy = enemies[i]
            if curr_enemy.rect.colliderect(prev_enemy.rect):
                overlap = prev_enemy.rect.right - curr_enemy.rect.left
                curr_enemy.rect.x += overlap + 1
                curr_enemy.pos['x'] = curr_enemy.rect.x
                prev_enemy.movement["right"] = False
                curr_enemy.movement["left"] = False

    def generate_enemies(self, count, enemy_classes, interval) -> None:
        self.enemy_count = count
        self.enemy_classes = enemy_classes
        self.enemy_interval = interval
        pg.time.set_timer(pg.USEREVENT + 1, interval)

    def spawn_enemy(self) -> None:
        if self.enemy_count > 0:
            enemy_class = random.choice(self.enemy_classes)
            if enemy_class.__name__ == "Skull":
                height = FLOOR[self.map] - 130
            else:
                height = FLOOR[self.map]
            enemy = enemy_class(self.screen, "idle", (self.screen_size[0] + 100, height))
            enemy.update_character()  # Generate the enemy's character
            self.entities.add(enemy)
            self.enemy_count -= 1

    def reset_player_position(self):
        self.player.pos["x"] = 100
        self.player.rect.x = self.player.pos["x"]

    def next_map(self) -> None:
        self.reset_player_position()
        self.target = None
        if self.map < 6:
            self.map += 1
            self.background = load_tile("MAPS", self.map, width=self.screen_size[0], height=self.screen_size[1])
            self.entities = pg.sprite.Group(self.player)
            self.generate_enemies(self.enemies[self.map][0], self.enemies[self.map][1], self.timer[self.map])
            self.player.pos["y"] = FLOOR[self.map]
            self.player.current_character = ""
            self.music.stop()
            self.music = get_music(self.map)
            self.music.play(-1)
        try:
            self.entities.add(self.NPCs[self.map])
        except:
            pass

    def render_hud(self):
        player_health_text = self.font.render(f'HP: {self.player.current_health_points}', True, (255, 255, 255))
        self.screen.blit(player_health_text, (100, 50))
        
        score_text = self.font.render(f'Score: {self.player.score["points"]}', True, (255, 255, 255))
        self.screen.blit(score_text, (100, 100))
        
        if self.target and self.target.current_health_points >= 0:
            enemy_health_text = self.font.render(f'Enemy HP: {self.target.current_health_points}', True, (255, 25, 25))
            self.screen.blit(enemy_health_text, (800, 50))

    def render_entity_character(self, entity):
        if entity.current_character:
            char_text = self.FONTS["MAGO3"].render(entity.current_character, True, (50, 10, 10))
            char_rect = char_text.get_rect(center=(entity.rect.centerx, entity.rect.top - 20))            
            cube_width, cube_height = char_rect.width + 30, char_rect.height + 20
            cube_rect = pg.Rect(
                char_rect.centerx - cube_width // 2,
                char_rect.centery - cube_height // 2,
                cube_width,
                cube_height
            )
            pg.draw.rect(self.screen, (255, 255, 255), cube_rect, border_radius=10)
            self.screen.blit(char_text, char_rect)

    def battle(self):
        if not self.target:
            return
        if self.player.current_character != "":
            if self.player.current_character == self.target.current_character:
                self.player.can_attack = True
                self.target.can_attack = False
                self.player.render_next(self.target)
                self.player.attack()
            else:
                self.player.can_attack = False
                if not self.target.has_been_attacked:
                    self.target.can_attack = True
                    self.target.render_next(self.player)
                    self.target.attack(flip=True)
                else:
                    self.target.idle(flip=True)

    def check_level(self):
        level_thresholds = [3, 7, 12, 17, 20]
        for points in level_thresholds:
            if self.player.score["points"] == points and self.map == (level_thresholds.index(points) + 1):
                self.next_map()
                break 
        if self.player.score["points"] == 25:
            self.win = True


    def main_menu(self):
        self.screen.fill((0, 0, 0))
        main_menu_title = self.font.render("HeroSign: Una Aventura de Señas", True,  (255, 255, 255))
        main_menu_text = self.font.render("Press SPACE to start", True, (255, 255, 255))
        text_width, text_height = main_menu_text.get_size()
        center_x = self.screen_size[0] // 2 - text_width // 2
        center_y = 400
        self.screen.blit(main_menu_title, (center_x, center_y-50))
        self.screen.blit(main_menu_text, (center_x, center_y))
        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        pg.quit()
                        quit()
                    if event.key == pg.K_SPACE:
                        return
            pg.display.update()
            self.clock.tick(120)

    def game_over(self):
        self.entities = []
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render("Press Enter to quit", True, (255, 255, 255))
        score_text = self.font.render(f'Score: {self.player.score["points"]}', True, (255, 255, 255))
        game_over_width, game_over_height = game_over_text.get_size()
        score_width, score_height = score_text.get_size()
        center_x = self.screen_size[0] // 2 - game_over_width // 2
        center_y = 300
        self.screen.blit(game_over_text, (center_x, center_y))
        center_x = self.screen_size[0] // 2 - score_width // 2
        score_y = center_y + game_over_height + 100
        self.screen.blit(score_text, (center_x, score_y))

        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        pg.quit()
                        quit()
            pg.display.update()
            self.clock.tick(120)

    def victory(self):
        self.entities = []
        self.screen.fill((0, 0, 0))
        victory_text = self.font.render("Has Ganado, Felicitaciones!", True, (255, 255, 255))
        score_text = self.font.render(f'Score: {self.player.score["points"]}', True, (255, 255, 255))
        game_over_width, game_over_height = victory_text.get_size()
        score_width, score_height = score_text.get_size()
        center_x = self.screen_size[0] // 2 - game_over_width // 2
        center_y = 300
        self.screen.blit(victory_text, (center_x, center_y))
        center_x = self.screen_size[0] // 2 - score_width // 2
        score_y = center_y + game_over_height + 100
        self.screen.blit(score_text, (center_x, score_y))

        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        pg.quit()
                        quit()
            pg.display.update()
            self.clock.tick(120)

    def run(self) -> None:
        pg.display.update()
        self.main_menu()
        self.generate_enemies(self.enemies[self.map][0], self.enemies[self.map][1], self.timer[1])
        while not self.win:
            self.check_level()
            if self.player.death_animation_completed:
                    break
            if self.player.current_health_points <= 0:
                self.player.death()
            if self.target:
                if self.target.current_health_points <= 0:
                    self.target.death()
                    self.target = None     
            pg.sprite.spritecollideany(self.player, self.entities, self.collision)
            self.screen.blit(self.background, (0, 0))
            if self.map in {3, 4}:
                self.screen.blit(self.decorator, (0, FLOOR[self.map] - 10))

            self.collision_enemies()

            for entity in self.entities.sprites()[1:]:
                entity.check_objective_reached(objective=self.player)
                if entity.objective_reached:
                    if self.map == 3 or self.map == 6:
                        if len(self.entities.sprites()[1:]) >=2:
                            self.target = self.entities.sprites()[1:][1]
                        else:
                            self.target = self.entities.sprites()[1:][0]
                    else:
                        self.target = self.entities.sprites()[1:][0]               
                    self.render_entity_character(entity)
                    entity.render_next()
                else:
                    self.player.can_attack = False
                    entity.move(objective=self.player)
                    entity.run(flip=True)
                    entity.render_next()

            predicted_char = self.hand_classifier.get_prediction()
            if predicted_char:
                self.player.current_character = predicted_char
                print(self.player.current_character)
                if self.target:
                    self.target.has_been_attacked = False

            self.controller()
            self.battle()
            self.player.move(None)
            self.player.render_next()           

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

                if event.type == pg.USEREVENT + 1:
                    self.spawn_enemy()
                    if self.map in [3, 6]:
                        self.NPCs[self.map].attack(True)

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        pg.quit()
                        quit()
                    if event.key == pg.K_SPACE:
                        self.next_map()

            self.render_hud()
            pg.display.update()
            self.clock.tick(120)
        if self.win:
            self.victory()
            self.hand_classifier.release()
        else:
            self.game_over()

if __name__ == "__main__":
    Game().run()
