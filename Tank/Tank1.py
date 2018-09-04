import sys, pygame, time
from pygame.locals import *
from random import randint


class TankMain:
    width = 600
    height = 500

    def start_game(self):
        pygame.init()
        screem = pygame.display.set_mode((TankMain.width, TankMain.height), 0, 32)
        pygame.display.set_caption("坦克大战")
        my_tank = MyTank(screem)
        enemy_list = [Enemy(screem) for i in range(5)]
        while True:
            screem.fill((200, 200, 200))
            screem.blit(self.write_text(), (0, 3))
            self.get_event(my_tank)
            my_tank.display()
            my_tank.move()
            for e in enemy_list:
                e.display()
                e.random_move()
            time.sleep(0.03)
            pygame.display.update()

    def get_event(self, my_tank):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.stop_game()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    my_tank.direction = "L"
                if event.key == K_RIGHT:
                    my_tank.direction = "R"
                if event.key == K_UP:
                    my_tank.direction = "U"
                if event.key == K_DOWN:
                    my_tank.direction = "D"
                if event.key == K_ESCAPE:
                    self.stop_game()
                my_tank.stop = False
            if event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT:
                    my_tank.stop = True
            if event.type == MOUSEBUTTONDOWN:
                pass

    def stop_game(self):
        sys.exit()

    def write_text(self):
        font = pygame.font.SysFont('华文楷体', 16)  # 设置字体
        text_sf = pygame.font.Font.render(font, "敌方坦克数量为：5", True, (158, 65, 84))  # 根据字体创建图像
        return text_sf


class Item(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Tank(Item):
    width = 50
    height = 50

    def __init__(self, screem, left, top, img):
        super().__init__()
        self.speed = 5
        self.stop = False
        self.screem = screem
        self.direction = "D"
        self.images = {}
        self.images["L"] = pygame.image.load(img + "L.png")
        self.images["D"] = pygame.image.load(img + "D.png")
        self.images["R"] = pygame.image.load(img + "R.png")
        self.images["U"] = pygame.image.load(img + "U.png")
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.live = True

    def display(self):
        self.image = self.images[self.direction]
        self.screem.blit(self.image, self.rect)

    def move(self):
        if not self.stop:
            if self.direction == "L":
                if self.rect.left > 0:
                    self.rect.left -= self.speed
                else:
                    self.rect.left = 0
            elif self.direction == "R":
                if self.rect.right < TankMain.width:
                    self.rect.right += self.speed
                else:
                    self.rect.right = TankMain.width
            elif self.direction == "U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.rect.top = 0
            elif self.direction == "D":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom += self.speed
                else:
                    self.rect.bottom = TankMain.height

    def fire(self):
        pass


class MyTank(Tank):
    def __init__(self, screem):
        super().__init__(screem, 275, 400, "material/Tank")
        self.stop = True


class Enemy(Tank):
    def __init__(self, screem):
        super().__init__(screem, randint(1, 5) * 100, 100, "material/EnemyTank")
        self.get_direction()
        self.step = self.get_step()

    def get_direction(self):
        r = randint(0, 4)
        if r == 4:
            self.stop = True
        else:
            self.stop = False
            if r == 0:
                self.direction = 'L'
            elif r == 1:
                self.direction = 'U'
            elif r == 2:
                self.direction = 'D'
            elif r == 3:
                self.direction = 'R'

    def get_step(self):
        return randint(3, 5)

    def random_move(self):
        if self.live:
            if self.step == 0:
                self.get_direction()
                self.step = self.get_step()
            else:
                self.move()
                self.step -= 1


screem = TankMain()
screem.start_game()
