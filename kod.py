import pygame
import random
import pygame_menu
import time
from math import sqrt
from pygame import mixer
from pygame_menu import sound

from classes import item

pygame.init()
counter = 0

#definiowanie okna gry
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#rozmiar obrazków
IMG_SIZE = 64

#maxX
MAX_X = SCREEN_WIDTH - IMG_SIZE

#muzyka w tle
mixer.music.load('sounds/AutumnDay.mp3')
mixer.music.play(-1)

# wyświetlanie okna gry
pygame.display.set_caption("Mr. Hedgehog's Adventures")

#zmiana ikony okna gry
icon = pygame.image.load('images/hedgehog32.png')
pygame.display.set_icon(icon)

#ikonki jako stringi
hedgehogRight = "images/hedgehog.png"
hedgehogLeft = "images/hedgehog_rev.png"
appleImg = "images/apple.png"
pearImg = "images/pear.png"
stoneImg = "images/stone.png"


#gracz (jeż)
hedgehog = item( (SCREEN_WIDTH - IMG_SIZE) / 2, SCREEN_HEIGHT - 120 - (IMG_SIZE / 2), pygame.image.load(hedgehogRight), 0, mixer.Sound('sounds/StoneHit.wav'))

hedgehog_speed = 3.6
hedgehog_mul = 1.0

# jablko
apple = item([random.randint(0, MAX_X), random.randint(0, MAX_X), random.randint(0, MAX_X)], [-110, -210, -310], pygame.image.load(appleImg), [3.02, 2.74, 2.88], mixer.Sound('sounds/AppleBite.wav'))

# gruszka
pear = item(random.randint(0, MAX_X), -10, pygame.image.load(pearImg), 3.31, mixer.Sound('sounds/PearBite.wav'))

#kamień
stone = item([random.randint(0, MAX_X)], [-400], pygame.image.load(stoneImg), [2.88], mixer.Sound('sounds/StoneHit.wav'))

#wynik
score_val = 0

#czcionka
font = pygame.font.Font('fonts/Lato-Bold.ttf', 32)

textX = 5
textY = 5

timeX = 5
timeY = 42

#gracz
nick = ""

def text_object(text, color, font):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def show_time(x, y, t):
    timee = font.render("Time: " + str(t), True, (255,255,255))
    screen.blit(timee, (x, y))

def show_score(x, y):
    score = font.render("Score: " + str(score_val), True, (255,255,255))
    screen.blit(score, (x, y))

def hedgehog_move():

    global hedgehog

    hedgehog.X += hedgehog.change
        
    if hedgehog.X <= 0:
        hedgehog.X = 0
    elif hedgehog.X >= MAX_X:
        hedgehog.X = MAX_X
    draw(hedgehog.X, hedgehog.Y, hedgehog.Img)

def apple_move():

    global apple

    for i in range(3):
        item_m(apple.X, apple.Y, apple.change, i, apple)
        if apple.Y[i] > SCREEN_HEIGHT:
            apple.X[i] = random.randint(0, MAX_X)
            apple.Y[i] = -10 + (i * -100)
            item_m(apple.X, apple.Y, apple.change, i, apple)

def item_m(X, Y, C, i,item):

    draw(X[i], Y[i], item.Img)
    Y[i] += C[i]

def stone_move():

    global stone

    for i in range(len(stone.X)):
        item_m(stone.X, stone.Y, stone.change, i, stone)
        if stone.Y[i] > SCREEN_HEIGHT:
            stone.X[i] = random.randint(0, MAX_X)
            stone.Y[i] = -10 + (i * -100)
            item_m(stone.X, stone.Y, stone.change, i, stone)


def pear_move():

    global pear
    global counter

    draw(pear.X, pear.Y, pear.Img)
    pear.Y += pear.change
    if pear.Y > SCREEN_HEIGHT:
        pear.X = random.randint(0, MAX_X)
        counter = 0
        pear.Y = -10

def draw(x, y, Img):
    screen.blit(Img, (x, y))

def get_speed():

    global pear
    global hedgehog

    if hedgehog.X > pear.X-64 and hedgehog.X < pear.X+64 and pear.Y+64-hedgehog.Y <= 64 and pear.Y+64-hedgehog.Y > 0:
        return True
    else:
        return False

def collision(item, i):

    global hedgehog

    d = (item.X[i] - hedgehog.X)*(item.X[i] - hedgehog.X) + (item.Y[i] - hedgehog.Y)*(item.Y[i] - hedgehog.Y)
    if sqrt(d) < 48:
        return True
    else:
        return False

def quit_the_game():
    quit()

def reset():

    global counter
    global score_val
    global pear
    global apple
    global hedgehog
    global hedgehog_speed
    global hedgehog_mul
    global stone
    global dead
    global hedgehogRight
    global hedgehogLeft
    global appleImg
    global pearImg

    stone = item([random.randint(0, MAX_X)], [-400], pygame.image.load(stoneImg), [2.88], mixer.Sound('sounds/StoneHit.wav'))
    apple.X = [random.randint(0, MAX_X), random.randint(0, MAX_X), random.randint(0, MAX_X)]

    counter = 0
    score_val = 0
    pear.Y = -20
    for i in range(3):
        apple.Y[i] = (i+1) * -100
    hedgehog.X = (SCREEN_WIDTH - IMG_SIZE) / 2
    hedgehog_speed = 3.6
    hedgehog_mul = 1.0
    hedgehog.change = 0

    hedgehogRight = "images/hedgehog.png"
    hedgehogLeft = "images/hedgehog_rev.png"
    appleImg = "images/apple.png"
    pearImg = "images/pear.png"

    hedgehog.Img = pygame.image.load(hedgehogRight)
    apple.Img = pygame.image.load(appleImg)
    pear.Img = pygame.image.load(pearImg)



def show(x, y, DANE, i):
    font = pygame.font.Font('fonts/Lato-Regular.ttf', 32)

    imie = font.render(str(i+1) + "." + " " + str(DANE[i][1]), True, (255,255,255))
    punkty = font.render( str(DANE[i][0]), True, (255,255,255))

    screen.blit(imie, (x, y+i*42))
    screen.blit(punkty, (x+200, y+i*42))

def moving():
    
    global hedgehog

    #klawisze
    keys = pygame.key.get_pressed()
    #zwraca stan klawiszy na klawiaturze jako wartość logiczną
    if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
        hedgehog.change = 0
    elif keys[pygame.K_RIGHT]:
        hedgehog.change = hedgehog_speed * hedgehog_mul
        hedgehog.Img = pygame.image.load(hedgehogRight)
        screen.blit(hedgehog.Img, (hedgehog.X, hedgehog.Y))
    elif keys[pygame.K_LEFT]:
        hedgehog.change = -1 * hedgehog_speed * hedgehog_mul
        hedgehog.Img = pygame.image.load(hedgehogLeft)
        screen.blit(hedgehog.Img, (hedgehog.X, hedgehog.Y))
    else:
        hedgehog.change = 0

        #zamykanie gry
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            reset()
            return False
            
    return True

def game_end(T):
    global dead
    global run
    if score_val == 45 or dead == True:
        your_time = round(T, 2)
        reset()

        #ekran pokazujący czas
        while run:
            if dead == False:
                screen.fill((10,92,43))
                timeSurf, timeRect = text_object("Your Time: " + str(your_time), (255,255,255), pygame.font.Font('fonts/Lato-Bold.ttf', 64))
                timeRect.center = (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2-96)
                pressSurf, pressRect = text_object("Press [space] to see highscores", (255,255,255), pygame.font.Font('fonts/Lato-Bold.ttf', 32))
                pressRect.center = (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2)
                screen.blit(timeSurf, timeRect)
                screen.blit(pressSurf, pressRect)
                pygame.display.update()
            else:
                screen.fill((255,255,255))
                obitSurf, obitRect = text_object("You are dead, " + str(nick.get_value()), (0,0,0), pygame.font.Font('fonts/Antraxja-Gothic.ttf', 128))
                obitRect.center = (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2-96)
                timeSurf, timeRect = text_object("You've lived for: " + str(your_time) + " seconds", (0,0,0), pygame.font.Font('fonts/Antraxja-Gothic.ttf', 64))
                timeRect.center = (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2+24)
                pressSurf, pressRect = text_object("Press [space] to see highscores", (0,0,0), pygame.font.Font('fonts/Lato-Bold.ttf', 32))
                pressRect.center = (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2+184)
                screen.blit(obitSurf, obitRect)
                screen.blit(timeSurf, timeRect)
                screen.blit(pressSurf, pressRect)
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:

                        highscores = []
                        if dead == False:
                            your_score = str(your_time) + " " + nick.get_value() + "\n"
                            f = open("scores.txt", "a")
                            f.write(your_score)
                            f.close()
                        f = open("scores.txt", "r")
                        for line in f:
                            x = line.split()
                            x[0] = float(x[0])
                            highscores.append(x)
                        highscores.sort()

                        #ekran pokazujący HS
                        run = True
                        while run:

                            for event in pygame.event.get():

                                    #zamykanie gry
                                    if event.type == pygame.QUIT:
                                        run = False

                            screen.fill((0,82,33))

                            HSSurf, HSRect = text_object("HIGHSCORES:", (235,235,235), pygame.font.Font('fonts/Lato-Black.ttf', 64))
                            HSRect.center = (SCREEN_WIDTH/2), (SCREEN_HEIGHT/2-280)
                            screen.blit(HSSurf, HSRect)

                            for i in range(min(10, len(highscores))):
                                show(401, 150, highscores, i)

                            pygame.display.update()


def raccoon():
    
    global hedgehogRight
    global hedgehogLeft
    global appleImg
    global pearImg

    global apple
    global pear
    global hedgehog

    hedgehogRight = "images/raccoon.png"
    hedgehogLeft = "images/raccoon_rev.png"
    appleImg = "images/laundry.png"
    pearImg = "images/dishes.png"
    hedgehog.Img = pygame.image.load(hedgehogRight)
    apple.Img = pygame.image.load(appleImg)
    pear.Img = pygame.image.load(pearImg)

dead = False
run = True

def start_the_game():

    global hedgehog
    global hedgehog_speed
    global hedgehog_mul

    global apple
    global stone
    global pear

    global nick
    global dead
    global score_val
    global counter
    global run
    


    delta = 0
    T = 0
    max_tps = 100

    clock = pygame.time.Clock()

    ready_pear = random.randint(460, 840)

    run = True
    dead = False

    

    #pętla główna
    while run:

        screen.fill((0,82,33))
        pygame.draw.rect(screen, (87,65,47), (0, SCREEN_HEIGHT - 120 - (IMG_SIZE / 2) + 57, SCREEN_WIDTH, 100))

        #moving obsługuje ruch jeża
        run = moving()

        #egg
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] and keys[pygame.K_z] and keys[pygame.K_o] and keys[pygame.K_p]:
            raccoon()

        #Ticking
        delta += clock.tick()/1000.0   
        while delta > 1 / max_tps:
            counter += 1
            #print(counter)
            T += 1 / max_tps #licznik w sekundach
            #print(round(T, 2))
            delta -= 1 / max_tps 

            #ruch gracza
            hedgehog_move()

            #ruch jabłka
            apple_move()

            #ruch kaminia
            stone_move()

            #dodanie kamienia
            if round(T, 2) % 15 == 0:
                stone.X.append(random.randint(0, MAX_X))
                stone.Y.append(-400)
                stone.change.append(2.0)


            #zjadanie jablka
            for i in range(3):
                if collision(apple, i):
                    apple.snd.play()
                    apple.Y[i] = SCREEN_HEIGHT + 1
                    score_val += 1

            #zjadanie kamienia
            for i in range(len(stone.X)):
                if collision(stone, i):
                    stone.snd.play()
                    dead = True
                    reset()
                    break   

            #znikniecie gruszki
            if pear.Y > SCREEN_HEIGHT:
                pear.X = random.randint(0, MAX_X)
                counter = 0
                pear.Y = -10

            #wypuszczenie gruszki
            if counter == ready_pear:
                #ruch gruszki
                counter = ready_pear - 1
                pear_move()

            #zjedzenie gruszki
            if get_speed():
                pear.snd.play()
                hedgehog_mul += 0.15
                pear.Y = SCREEN_HEIGHT + 1
                pear.Y = -10
                pear.X = random.randint(0, MAX_X)
                counter = 0
                ready_pear = random.randint(460, 840)

            #pokazuj wynik
            show_score(textX, textY)
            #pokazuj czas
            show_time(timeX, timeY, round(T, 2))

            game_end(T)

            pygame.display.update()

    pass

#menu
menu = pygame_menu.Menu(300, 400, 'Hello', theme=pygame_menu.themes.THEME_BLUE)
nick = menu.add_text_input('Name: ', default='Jacuś')
menu.add_button('Play', start_the_game)
menu.add_button('Quit', quit_the_game)
menu.mainloop(screen, fps_limit=100)