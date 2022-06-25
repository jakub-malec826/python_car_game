import random
import pygame

pygame.init()

fps = 60
FPS = pygame.time.Clock()


SIZE = X, Y = 400, 700

WINDOW = pygame.display.set_mode(SIZE)

SCORE = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("./graphic/player_car.png")
        self.surf = pygame.Surface((80, 180))
        self.rect = self.surf.get_rect(center=(250, 500))

    def update(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_a] and self.rect.left > 0:
            self.rect.centerx -= 15
        if key[pygame.K_d] and self.rect.right < SIZE[0]:
            self.rect.centerx += 15


class EnemyDown(pygame.sprite.Sprite):
    def __init__(self, y):
        super(EnemyDown, self).__init__()

        self.Y = y
        self.image = pygame.image.load("./graphic/car_enemy.png")
        self.surf = pygame.Surface((80, 180))
        self.rect = self.surf.get_rect(center=(random.choice((50, 150, 250, 350)), self.Y))
        self.speed = 6

    def update(self):
        global SCORE
        self.rect.centery += self.speed
        if self.rect.top > SIZE[1]:
            SCORE += 1
            self.rect.top = self.Y
            self.rect.x = random.choice((0, 100, 200, 300))
            self.speed += 1


class Road:
    def __init__(self):
        self.road = pygame.image.load("./graphic/road.png")
        self.rect = self.road.get_rect()

        self.X1, self.Y1 = 0, 0
        self.X2, self.Y2 = 0, self.rect.height
        self.speed = 5

    def update(self):
        self.Y1 += self.speed
        self.Y2 += self.speed
        if self.Y1 >= self.rect.height:
            self.Y1 = -self.rect.height

        if self.Y2 >= self.rect.height:
            self.Y2 = -self.rect.height

    def render(self):
        WINDOW.blit(self.road, (self.X1, self.Y1))
        WINDOW.blit(self.road, (self.X2, self.Y2))
        self.update()


def main():
    font = pygame.font.SysFont('arial', 40, True)

    background = Road()

    player = Player()
    enemy_down = EnemyDown(-400)
    enemy_down2 = EnemyDown(-800)

    enemy_cars = pygame.sprite.Group(enemy_down, enemy_down2)
    all_cars = pygame.sprite.Group(enemy_down, enemy_down2, player)

    game_over = font.render("GAME OVER", True, 'black')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

        background.render()
        for cars in all_cars:
            WINDOW.blit(cars.image, cars.rect)
            cars.update()
        rendered = font.render("SCORE: " + str(SCORE), True, 'white')
        WINDOW.blit(rendered, (0, 0))
        pygame.display.flip()

        if pygame.sprite.spritecollideany(player, enemy_cars):
            WINDOW.blit(background.road, (0, 0))
            WINDOW.blit(game_over, (70, 300))

            pygame.display.update()
            for cars in all_cars:
                cars.kill()
            pygame.time.wait(2000)
            pygame.quit()

        pygame.display.update()
        FPS.tick(fps)


if __name__ == "__main__":
    main()
