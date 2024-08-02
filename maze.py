from random import choice
from pygame import *
import pygame_menu

init()
font.init()
font1 = font.SysFont("Impact", 100)
game_over_text = font1.render("GAME OVER", True, (150, 0, 0))
mixer.init()
mixer.music.load('jungles.ogg')
# mixer.music.play()
mixer.music.set_volume(0.2)

MAP_WIDTH, MAP_HEIGHT = 25, 20 # ширина і висота карти
TILESIZE = 40 #розмір квадратика карти
WIDTH, HEIGHT = MAP_WIDTH*TILESIZE, MAP_HEIGHT*TILESIZE

window = display.set_mode((WIDTH,HEIGHT))
FPS = 90
clock = time.Clock()

bg = image.load('background.jpg')
bg = transform.scale(bg,(WIDTH,HEIGHT))

player_img = image.load("hero_01.png")
cyborg_img = image.load("pngwing.com.png")
wall_img = image.load("transparent-bg-tiles (2).png")
gold_img = image.load("transparent-bg-tiles (4).png")
all_sprites = sprite.Group()

class Sprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect   = Rect(x,y, width, height)
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)

class Player(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.hp = 100
        self.speed = 2
        self.dir = "r"

    def update(self):
        key_pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if key_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
            self.dir = "u"
        if key_pressed[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            self.dir = "d"
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.dir = "l"
        if key_pressed[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
            self.dir = "r"
        
        collide_list = sprite.spritecollide(self, walls, False, sprite.collide_mask) 
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_pos
        
        enemy_collide = sprite.spritecollide(self, enemys, False, sprite.collide_mask)
        if len(enemy_collide) > 0:
            self.hp -= 100

    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery +15, self)      


class Enemy(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.damage = 100
        self.speed = 2
        self.dir_list = ['right', 'left', "up", "down"]
        self.dir = choice(self.dir_list)

    def update(self):
        old_pos = self.rect.x, self.rect.y # зберігаємо позицію
        if self.dir == "right":
            self.rect.x += self.speed
        elif self.dir == "left":
            self.rect.x -= self.speed
        elif self.dir == "up":
            self.rect.y -= self.speed
        elif self.dir == "down":
            self.rect.y += self.speed

        collide_list = sprite.spritecollide(self, walls, False, sprite.collide_mask) 
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_pos #якщо торкнуися стіни - крок назад
            self.dir = choice(self.dir_list)

bullets = sprite.Group()
class Bullet(Sprite):
    def __init__(self, x, y, player):
        img = Surface((10,10))
        img.fill((255,0,0))
        super().__init__(img, 10, 10, x, y)
        self.rect.centerx = x
        self.rect.bottom = y
        self.damage = 100
        self.speed = 10
        bullets.add(self)
        self.dir = player.dir
    def update(self):
        if self.rect.bottom < 0:
            self.kill()


        if self.dir == "r":
            self.rect.x += self.speed
        elif self.dir == "l":
            self.rect.x -= self.speed
        elif self.dir == "u":
            self.rect.y -= self.speed
        elif self.dir == "d":
            self.rect.y += self.speed
        


player = Player(player_img, TILESIZE-5, TILESIZE-5, 300, 300)
walls = sprite.Group()
enemys = sprite.Group()

with open("map.txt", "r") as f:
    map = f.readlines()
    x = 0
    y = 0
    for line in map:
        for symbol in line:
            if symbol == "w": # стіни
                walls.add(Sprite(wall_img, TILESIZE, TILESIZE, x, y ))
            if symbol == "p": # гравець
                player.rect.x = x
                player.rect.y = y
            if symbol == "g": # стіни
                gold = Sprite(gold_img, 70, 70, x, y )
            if symbol == "e": 
                enemys.add(Enemy(cyborg_img, TILESIZE-5, TILESIZE-5, x, y ))
            x += TILESIZE
        y += TILESIZE
        x = 0
        





def set_difficulty(selected, value):
    """
    Set the difficulty of the game.
    """
    print(f'Set difficulty to {selected[0]} ({value})')

def start_the_game():
    # Do the job here !
    global run
    run = True
    menu.disable()


#створюємо власну тему - копію стандартної
mytheme = pygame_menu.themes.THEME_DARK.copy()
# колір верхньої панелі (останній параметр - 0 робить її прозорою)
mytheme.title_background_color=(255, 255, 255, 0) 
#задаємо картинку для фону

menu = pygame_menu.Menu('Fight maze', WIDTH, HEIGHT,
                       theme=mytheme)   

user_name = menu.add.text_input("Ім'я :", default='Анонім')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(window)

run = True
finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e. type == KEYDOWN:
            if e.key == K_ESCAPE:
                menu.enable()
                menu.mainloop(window)
            if e.key == K_q:
                player.fire()
    window.fill((252, 199, 50))
    if player.hp <= 0:
        finish = True

    if sprite.collide_mask(player, gold):
        finish = True
        game_over_text = font1.render("YOU WIN", True, (0, 150, 0))

    all_sprites.draw(window)
    if not finish: 
        all_sprites.update()
    if finish:
        window.blit(game_over_text, (300, 300))
    display.update()
    clock.tick(FPS)