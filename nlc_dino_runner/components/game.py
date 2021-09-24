import pygame
import random
from nlc_dino_runner.components.life_manager import LifeManager
from nlc_dino_runner.components.powerups.power_up_manager import PowerUpManager
from nlc_dino_runner.utils import text_utils
from nlc_dino_runner.components.obstacles.obstaclesManager import ObstaclesManager
from nlc_dino_runner.utils.constants import TITLE, ICON, SCREEN_WIDTH, SCREEN_HEIGHT, BG, FPS, SOUND_GAME_LOOP, \
    SOUND_GAME_OVER, RESET_IMG, GAME_OVER_IMG, DARK_MODE, NORMAL_MODE, CLOUD
from nlc_dino_runner.components.dinosaur import Dinosaur


class Game:
    def __init__(self):

        self.separation = random.randint(350, 450)
        self.x_pos_cloud1 = 0 + self.separation
        self.x_pos_cloud2 = 0 + self.separation * 2
        self.x_pos_cloud3 = 0 + self.separation * 3
        self.x_pos_cloud4 = 0 + self.separation * 4
        self.y_pos_cloud1 = random.randint(100, 250)
        self.y_pos_cloud2 = random.randint(100, 250)
        self.y_pos_cloud3 = random.randint(100, 250)
        self.y_pos_cloud4 = random.randint(100, 250)
        self.separation = 250

        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstaclesManager()
        self.power_up_manager = PowerUpManager()
        self.points = 0
        self.running = True
        self.death_count = 0
        self.life_manager = LifeManager()

        self.dark = False

    def run(self):
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups(self.points, self.player)
        self.points = 0
        self.playing = True
        self.life_manager.refull_lifes()
        #GAME LOOP: event, update, draw
        SOUND_GAME_LOOP.play()
        while self.playing:  #3 segundos
            self.event()
            self.update()
            self.draw()
        self.game_speed = 20
        SOUND_GAME_OVER.play()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self, self.screen)
        self.power_up_manager.update(self.points, self.game_speed, self.player)

    def draw(self):
        self.clock.tick(FPS)

        if self.points % 1000 == 0:
            if (self.points / 1000) % 2 == 0:
                self.dark = False
            else:
                self.dark = True
        if self.dark:
            self.screen.fill(DARK_MODE)
        else:
            self.screen.fill(NORMAL_MODE)

        self.score()
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.life_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
        score_element, score_element_rect = text_utils.get_score_element(self.points)
        self.screen.blit(score_element, score_element_rect)
        self.player.check_invincibility(self.screen)

    def draw_background(self):
        image_width = BG.get_width()
        #para dibujar imagen "blit"
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))

        #La imagen se mueve
        self.screen.blit(BG, (self.x_pos_bg + image_width, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (self.x_pos_bg + image_width, self.y_pos_bg))
            self.x_pos_bg = 0

        self.x_pos_bg -= self.game_speed
        self.draw_clouds()

    def draw_clouds(self):  # drawing the clouds
        self.screen.blit(CLOUD, (self.x_pos_cloud1, self.y_pos_cloud1))
        self.screen.blit(CLOUD, (self.x_pos_cloud2, self.y_pos_cloud2))
        self.screen.blit(CLOUD, (self.x_pos_cloud3, self.y_pos_cloud3))
        self.screen.blit(CLOUD, (self.x_pos_cloud4, self.y_pos_cloud4))
        self.x_pos_cloud1 -= self.game_speed // 2
        self.x_pos_cloud2 -= self.game_speed // 2
        self.x_pos_cloud3 -= self.game_speed // 2
        self.x_pos_cloud4 -= self.game_speed // 2
        if self.x_pos_cloud1 <= -SCREEN_WIDTH // 4:
            self.x_pos_cloud1 = SCREEN_WIDTH
            self.y_pos_cloud1 = random.randint(100, 250)
        if self.x_pos_cloud2 <= -SCREEN_WIDTH // 4:
            self.x_pos_cloud2 = SCREEN_WIDTH
            self.y_pos_cloud2 = random.randint(100, 250)
        if self.x_pos_cloud3 <= -SCREEN_WIDTH // 4:
            self.x_pos_cloud3 = SCREEN_WIDTH
            self.y_pos_cloud3 = random.randint(100, 250)
        if self.x_pos_cloud4 <= -SCREEN_WIDTH // 4:
            self.x_pos_cloud4 = SCREEN_WIDTH
            self.y_pos_cloud4 = random.randint(100, 250)

    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()
                SOUND_GAME_LOOP.stop()

    def show_menu(self):
        self.running = True

        white_color = (255, 255, 255)
        self.screen.fill(white_color)

        self.print_menu_elements()
        pygame.display.update()
        self.handle_key_events_on_menu()

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()

    def print_menu_elements(self):
        half_screen_height = SCREEN_HEIGHT // 2

        if self.death_count < 1:
            text, text_rect = text_utils.get_centered_message("Press any key to Start")
        else:
            pygame.time.delay(900)

            #IMAGEN RESTART y GAME OVER
            self.screen.blit(GAME_OVER_IMG, ((SCREEN_WIDTH // 2) - 200, (SCREEN_HEIGHT // 2) - 220))
            self.screen.blit(RESET_IMG, ((SCREEN_WIDTH // 2) - 40, (SCREEN_HEIGHT // 2) + 25))

            text, text_rect = text_utils.get_centered_message("Press any key to Restart")

            death_score, death_score_rect = text_utils.get_centered_message("Death count: " + str(self.death_count), height=half_screen_height + 120)
            self.screen.blit(death_score, death_score_rect)

            score, score_rect = text_utils.get_centered_message("FINAL SCORE: " + str(self.points), height=half_screen_height + 160)
            self.screen.blit(score, score_rect)
        self.screen.blit(text, text_rect)

        self.screen.blit(ICON, ((SCREEN_WIDTH // 2) - 40, (SCREEN_HEIGHT // 2) - 150))
