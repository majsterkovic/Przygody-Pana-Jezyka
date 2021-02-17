import pygame
import random
import pygame_menu
from pygame import mixer

pygame.init()

counter = 0

# definiowanie okna gry
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#muzyka w tle
mixer.music.load('AutumnDay.mp3')
pygame.mixer.music.play(-1)

# wyświetlanie okna gry
pygame.display.set_caption("Przygody Pana Jeżyka")

class obiekt:
    def __init__(self, X, Y, Img, change):
        self.X = X
        self.Y = Y
        self.Img = Img
        self.change = change

#gracz (jeż)
IMG_SIZE = 64
hedgehog = obiekt(SCREEN_WIDTH / 2 - (IMG_SIZE / 2), SCREEN_HEIGHT - 120 - (IMG_SIZE / 2), pygame.image.load("hedgehog.png"), 0)
hedgehog.Img = pygame.image.load("hedgehog.png")


hedgehog_speed = 0.3
hedgehog_mul = 1.0

#maxX
MAX_X = SCREEN_WIDTH - IMG_SIZE

# jablko
appleImg = pygame.image.load("apple.png")
#rozmiar 64x64
appleX = [random.randint(0, MAX_X), random.randint(0, MAX_X), random.randint(0, MAX_X)]
appleY = [-10, -110, -210]
appleY_change = [0.2, 0.2, 0.2]

# gruszka
pearImg = pygame.image.load("pear.png")
#rozmiar 64x64
pearX = random.randint(0, MAX_X)
pearY = -10
pearY_change = 0.23

#wynik
score_val = 0
font = pygame.font.Font('SyneMono-Regular.ttf', 32)
textX = 5
textY = 5

def show_score(x, y):
    score = font.render("Wynik: " + str(score_val), True, (255,255,255))
    screen.blit(score, (x, y))

def hedgehog_move():
    global MAX_X
    global hedgehog

    hedgehog.X += hedgehog.change
        
    if hedgehog.X <= 0:
        hedgehog.X = 0
    elif hedgehog.X >= MAX_X:
        hedgehog.X = MAX_X
    draw(hedgehog.X, hedgehog.Y, hedgehog.Img)

def apple_m(X, Y, C, i):

    global appleImg

    draw(X[i], Y[i], appleImg)
    Y[i] += C[i]

def apple_move():

    global appleY
    global appleX
    global MAX_X
    global SCREEN_HEIGHT

    for i in range(3):
        apple_m(appleX, appleY, appleY_change, i)
        if appleY[i] > SCREEN_HEIGHT:
            appleX[i] = random.randint(0, MAX_X)
            appleY[i] = -10 + (i * -100)
            apple_m(appleX, appleY, appleY_change, i)

def pear_m(): 
    global pearX
    global pearY
    global pearY_change
    global pearImg
    draw(pearX, pearY, pearImg)
    pearY += pearY_change

def pear_move():
    global pearY
    global pearX
    global counter
    global SCREEN_HEIGHT
    pear_m()
    if pearY > SCREEN_HEIGHT:
        pearX = random.randint(0, MAX_X)
        counter = 0
        pearY = -10
        pear_m()


def draw(x, y, Img):
    screen.blit(Img, (x, y))

def get_speed():
    global pearX
    global pearY

    global hedgehog

    if hedgehog.X > pearX-64 and hedgehog.X < pearX+64 and pearY+64-hedgehog.Y <= 64 and pearY+64-hedgehog.Y > 0:
        return True
    else:
        return False

def get_point(i):

    global appleX
    global appleY

    global hedgehog

    if hedgehog.X > appleX[i]-64 and hedgehog.X < appleX[i]+64 and appleY[i]+64-hedgehog.Y <= 64 and appleY[i]+64-hedgehog.Y > 0:
        return True
    else:
        return False


def start_the_game():

    global hedgehog
    global hedgehog_speed
    global hedgehog_mul

    global appleX
    global appleY
    global appleX_change
    global appleImg

    global pearX
    global pearY

    global score_val
    global SCREEN_HEIGHT
    global counter

    
    #is_pear = False
    ready_pear = random.randint(7000, 30000)


    run = True
    while run:

        counter += 1
        screen.fill((0,82,33))
        pygame.draw.rect(screen, (87,65,47), (0, SCREEN_HEIGHT - 120 - (IMG_SIZE / 2) + 57, SCREEN_WIDTH, 100))

        for event in pygame.event.get():

            #zamykanie gry
            if event.type == pygame.QUIT:
                run = False

            #klawisze
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hedgehog.change = -1 * hedgehog_speed* hedgehog_mul
                    hedgehog.Img = pygame.image.load("hedgehog_rev.png")
                    screen.blit(hedgehog.Img, (hedgehog.X, hedgehog.Y))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    hedgehog.change = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    hedgehog.change = hedgehog_speed * hedgehog_mul
                    hedgehog.Img = pygame.image.load("hedgehog.png")
                    screen.blit(hedgehog.Img, (hedgehog.X, hedgehog.Y))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    hedgehog.change = 0

        #ruch gracza
        hedgehog_move()
        #ruch jabłka
        apple_move()

        for i in range(3):
            if get_point(i):
                appleY[i] = SCREEN_HEIGHT + 1
                score_val += 1

        if counter == ready_pear:
            #ruch gruszki
            counter = ready_pear - 1
            pear_move()


        if get_speed():
            hedgehog_mul += 0.015
            pearY = SCREEN_HEIGHT + 1
            pearY = -10
            pearX = random.randint(0, MAX_X)

            counter = 0
            ready_pear = random.randint(7000, 30000)
 

        show_score(textX, textY)
        pygame.display.update()

    pass

#menu
menu = pygame_menu.Menu(300, 400, 'Witaj', theme=pygame_menu.themes.THEME_BLUE)
menu.add_text_input('Imię: ', default='Jacuś')
menu.add_button('Graj', start_the_game)
menu.add_button('Wyjdź', pygame_menu.events.EXIT)
menu.mainloop(screen)