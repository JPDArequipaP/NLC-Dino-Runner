import random

from nlc_dino_runner.components.obstacles.obstacles import Obstacles

#Clase hija
class Bird(Obstacles):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 250
        self.FPS = 0

    def draw(self, screen):
        if self.FPS > 5:
            screen.blit(self.image[0], self.rect)
        else:
            screen.blit(self.image[1], self.rect)

        if self.FPS >= 9:
            self.FPS = 0

        self.FPS += 1.5
