import random

import pygame.time

from nlc_dino_runner.components.obstacles.bird import Bird
from nlc_dino_runner.components.obstacles.cactus import Cactus
from nlc_dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD


class ObstaclesManager:

    def __init__(self):
        self.obstacles_list = []

    def update(self, game):
        self.aleatorio = random.randint(0,2)
        if len(self.obstacles_list) == 0:
            if self.aleatorio == 0:
                self.obstacles_list.append(Cactus(SMALL_CACTUS))
            if self.aleatorio == 1:
                self.obstacles_list.append(Cactus(LARGE_CACTUS))
            if self.aleatorio == 2:
                self.obstacles_list.append(Bird(BIRD))

        for obstacle in self.obstacles_list:
            obstacle.update(game.game_speed, self.obstacles_list)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.shield:
                    self.obstacles_list.remove(obstacle)
                elif game.life_manager.life_counter() == 1:
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    break
                else:
                    game.life_manager.delete_life()
                    self.obstacles_list.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles_list:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles_list = []