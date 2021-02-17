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

#gracz (jeż)
hedgehogImg = pygame.image.load("hedgehog.png")
IMG_SIZE = 64
hedgehogX = SCREEN_WIDTH / 2 - (IMG_SIZE / 2)
hedgehogY = SCREEN_HEIGHT - 120 - (IMG_SIZE / 2) #568
hedgehogX_change = 0
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
    global hedgehogX
    global hedgehogY
    global hedgehogX_change
    global hedgehogImg

    hedgehogX += hedgehogX_change
        
    if hedgehogX <= 0:
        hedgehogX = 0
    elif hedgehogX >= MAX_X:
        hedgehogX = MAX_X
    draw(hedgehogX, hedgehogY, hedgehogImg)

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
    global hedgehogX
    global hedgehogY

    if hedgehogX > pearX-64 and hedgehogX < pearX+64 and pearY+64-hedgehogY <= 64 and pearY+64-hedgehogY > 0:
        return True
    else:
        return False

def get_point(i):

    global appleX
    global appleY
    global hedgehogX
    global hedgehogY

    if hedgehogX > appleX[i]-64 and hedgehogX < appleX[i]+64 and appleY[i]+64-hedgehogY <= 64 and appleY[i]+64-hedgehogY > 0:
        return True
    else:
        return False


def start_the_game():

    global hedgehogX
    global hedgehogY
    global hedgehogX_change
    global hedgehogImg
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
                    hedgehogX_change = -1 * hedgehog_speed* hedgehog_mul
                    hedgehogImg = pygame.image.load("hedgehog_rev.png")
                    screen.blit(hedgehogImg, (hedgehogX, hedgehogY))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    hedgehogX_change = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    hedgehogX_change = hedgehog_speed * hedgehog_mul
                    hedgehogImg = pygame.image.load("hedgehog.png")
                    screen.blit(hedgehogImg, (hedgehogX, hedgehogY))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    hedgehogX_change = 0

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