from nlc_dino_runner.components.life import Life

class LifeManager:
    def __init__(self):
        self.life_list = []

    def refull_lifes(self):
        pos_x = 10 #Distancia entre vidas
        for i in range(0, 5):
            self.life_list.append(Life(pos_x))
            pos_x += 30

    def draw(self, screen):
        for life in self.life_list:
            life.draw(screen)

    def delete_life(self):
        self.life_list.pop()

    def life_counter(self):
        return len(self.life_list)
