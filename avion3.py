import pygame, sys, random, os

carpeta_juego= os.path.dirname(__file__)

carpeta_assets = os.path.join(carpeta_juego, "assets")
carpeta_imagenes = os.path.join(carpeta_assets, "images")
carpeta_sonidos = os.path.join(carpeta_assets, "sounds")

pygame.init()

HEIGHT =600
WIDTH = 800
WHITE =  (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (125, 125, 125)
size = (WIDTH, HEIGHT)

#crear ventana
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

#coordenadas
cord_x = -80
cord_y = 0

min_edif = 3
max_edif = 5

#velocidad a la que se movera
speed_x = 2
speed_y = 3
Vidas = 3
you_win = False

#Icono y titulo
pygame.display.set_caption("Avioncito")
icono=pygame.image.load("assets/images/avion5.png")
pygame.display.set_icon(icono)


def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

class Edificio(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(carpeta_imagenes, "edificio.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

class Avion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(carpeta_imagenes, "avion4.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = cord_x
        self.rect.y = cord_y
        self.speed_x = 0

    def changespeed(self, x):
        self.speed_x += x

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x > 800:
            self.rect.x = -80
            self.rect.y += 40    
        if self.rect.y > HEIGHT - 80:
            self.image = pygame.image.load(os.path.join(carpeta_imagenes, "avion5.png")).convert()
            self.image.set_colorkey(WHITE)
            if self.rect.x > WIDTH - 160:
                self.speed_x = 0
                avioneta.stop()
                aplauso.play()
                draw_text(screen, "You Win, Congratulation", 40, WIDTH //2, HEIGHT // 2)
                you_win = True
        
class Bomba(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(carpeta_imagenes, "bomba.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y += 3

background = pygame.image.load(os.path.join(carpeta_imagenes, "cielo.png")).convert()

all_sprite_list = pygame.sprite.Group()
avion_list = pygame.sprite.Group()
bomba_list = pygame.sprite.Group()
pygame.mixer.init()
avioneta = pygame.mixer.Sound(os.path.join(carpeta_sonidos, "avioneta.mp3"))
explosion = pygame.mixer.Sound(os.path.join(carpeta_sonidos, "explosion.mp3"))
aplauso = pygame.mixer.Sound(os.path.join(carpeta_sonidos, "aplauso.mp3"))
edif_list = []
for x in range(50, 750, 50):
    y = HEIGHT
    alt = random.randint(min_edif, max_edif)
    for j in range(alt):
        y -= 50
        edif_list.append([x, y])

edificio_list = pygame.sprite.Group()
for cord in edif_list:
    x = cord[0]
    y = cord[1]
    edificio = Edificio()
    edificio.rect.x = x
    edificio.rect.y = y
    edificio_list.add(edificio)
    all_sprite_list.add(edificio)
    
avion = Avion()
all_sprite_list.add(avion)
avion.changespeed(3)
avioneta.play()

game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if (len(bomba_list) == 0):

                    bomba = Bomba()
                    bomba.rect.x = avion.rect.x + 40
                    bomba.rect.y = avion.rect.y + 20

                all_sprite_list.add(bomba)
                bomba_list.add(bomba)

    for bomba in bomba_list:
        edificio_hit_list = pygame.sprite.spritecollide(bomba, edificio_list, True)
        for edificio in edificio_hit_list:
            explosion.play()
            all_sprite_list.remove(bomba)
            bomba_list.remove(bomba)
            edificio_list.remove(edificio)
            
        if bomba.rect.y > HEIGHT:
            all_sprite_list.remove(bomba)
            bomba_list.remove(bomba)

    all_sprite_list.update()

    avion_list.add(avion)
   
    avion_hit_list = pygame.sprite.spritecollide(avion, edificio_list, True)
                    
    if avion_hit_list:
        game_over = True


    
    screen.blit(background, [0,0])
    all_sprite_list.draw(screen)

    if you_win:
        draw_text(screen, "You Win, Congratulation", 40, WIDTH //2, HEIGHT // 2)
    draw_text(screen, str(Vidas), 25, WIDTH // 2, 10)
    #actualizar pantalla
    pygame.display.flip()
    clock.tick(60)
pygame.quit()