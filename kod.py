import pygame
import random
import pygame_menu
import time

from pygame import mixer
from pygame_menu import sound

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
mixer.music.load('AutumnDay.mp3')
pygame.mixer.music.play(-1)


# wyświetlanie okna gry
pygame.display.set_caption("Przygody Pana Jeżyka")

class item:
    def __init__(self, X, Y, Img, change):
        self.X = X
        self.Y = Y
        self.Img = Img
        self.change = change

#gracz (jeż)
hedgehog = item( (SCREEN_WIDTH - IMG_SIZE) / 2, SCREEN_HEIGHT - 120 - (IMG_SIZE / 2), pygame.image.load("hedgehog.png"), 0)

hedgehog_speed = 2.5
hedgehog_mul = 1.0

# jablko
apple = item([random.randint(0, MAX_X), random.randint(0, MAX_X), random.randint(0, MAX_X)], [-110, -210, -310], pygame.image.load("apple.png"), [2.1, 1.9, 2.0])

# gruszka
pear = item(random.randint(0, MAX_X), -10, pygame.image.load("pear.png"), 2.3)

#kamień
stone = item([random.randint(0, MAX_X)], [-400], pygame.image.load("stone3.png"), [2.0])

#wynik
score_val = 0

#czcionka
font = pygame.font.Font('Lato-Bold.ttf', 32)

textX = 5
textY = 5

timeX = 5
timeY = 42

#gracz
nick = ""

def show_time(x, y, t):
    timee = font.render("Czas: " + str(t), True, (255,255,255))
    screen.blit(timee, (x, y))

def show_score(x, y):
    score = font.render("Wynik: " + str(score_val), True, (255,255,255))
    screen.blit(score, (x, y))

def hedgehog_move():
    global hedgehog

    hedgehog.X += hedgehog.change
        
    if hedgehog.X <= 0:
        hedgehog.X = 0
    elif hedgehog.X >= MAX_X:
        hedgehog.X = MAX_X
    draw(hedgehog.X, hedgehog.Y, hedgehog.Img)

def apple_m(X, Y, C, i):

    global apple

    draw(X[i], Y[i], apple.Img)
    Y[i] += C[i]

def apple_move():

    global apple

    for i in range(3):
        apple_m(apple.X, apple.Y, apple.change, i)
        if apple.Y[i] > SCREEN_HEIGHT:
            apple.X[i] = random.randint(0, MAX_X)
            apple.Y[i] = -10 + (i * -100)
            apple_m(apple.X, apple.Y, apple.change, i)

def stone_m(X, Y, C, i):

    global stone

    draw(X[i], Y[i], stone.Img)
    Y[i] += C[i]

def stone_move():

    global stone

    for i in range(len(stone.X)):
        stone_m(stone.X, stone.Y, stone.change, i)
        if stone.Y[i] > SCREEN_HEIGHT:
            stone.X[i] = random.randint(0, MAX_X)
            stone.Y[i] = -10 + (i * -100)
            stone_m(stone.X, stone.Y, stone.change, i)


def pear_move():
    global pear
    global counter
    draw(pear.X, pear.Y, pear.Img)
    pear.Y += pear.change
    if pear.Y > SCREEN_HEIGHT:
        pear.X = random.randint(0, MAX_X)
        counter = 0
        pear.Y = -10
        print("Gruszka przeleciala")

def draw(x, y, Img):
    screen.blit(Img, (x, y))

def get_speed():
    global pear
    global hedgehog

    if hedgehog.X > pear.X-64 and hedgehog.X < pear.X+64 and pear.Y+64-hedgehog.Y <= 64 and pear.Y+64-hedgehog.Y > 0:
        return True
    else:
        return False

def get_point(i):

    global apple
    global hedgehog

    if hedgehog.X > apple.X[i]-64 and hedgehog.X < apple.X[i]+64 and apple.Y[i]+64-hedgehog.Y <= 64 and apple.Y[i]+64-hedgehog.Y > 0:
        return True
    else:
        return False

def get_hit(i):

    global stone
    global hedgehog

    if hedgehog.X > stone.X[i]-64 and hedgehog.X < stone.X[i]+64 and stone.Y[i]+64-hedgehog.Y <= 64 and stone.Y[i]+64-hedgehog.Y > 0:
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
    global stone

    stone = item([random.randint(0, MAX_X)], [-400], pygame.image.load("stone3.png"), [2.0])

    counter = 0
    score_val = 0
    pear.Y = -20
    for i in range(3):
        apple.Y[i] = (i+1) * -100
    hedgehog.X = (SCREEN_WIDTH - IMG_SIZE) / 2
    hedgehog_speed = 2.5


def show(x, y, DANE, i):
    font = pygame.font.Font('Lato-Regular.ttf', 32)

    imie = font.render(str(i+1) + "." + " " + str(DANE[i][1]), True, (255,255,255))
    punkty = font.render( str(DANE[i][0]), True, (255,255,255))

    screen.blit(imie, (x, y+i*42))
    screen.blit(punkty, (x+200, y+i*42))    


def start_the_game():

    global hedgehog
    global hedgehog_speed
    global hedgehog_mul

    global apple
    global stone
    global pear

    global nick

    global score_val
    global counter

    bite_sound = mixer.Sound('AppleBite.wav')

    dead = False

    delta = 0
    T = 0
    max_tps = 144

    clock = pygame.time.Clock()

    ready_pear = random.randint(460, 840)

    run = True

    #pętla główna
    while run:
        screen.fill((0,82,33))
        pygame.draw.rect(screen, (87,65,47), (0, SCREEN_HEIGHT - 120 - (IMG_SIZE / 2) + 57, SCREEN_WIDTH, 100))

        for event in pygame.event.get():

            #klawisze
            keys = pygame.key.get_pressed()
            #zwraca stan klawiszy na klawiaturze jako wartość logiczną
            if keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]:
                hedgehog.change = 0
            elif keys[pygame.K_RIGHT]:
                hedgehog.change = hedgehog_speed * hedgehog_mul
                hedgehog.Img = pygame.image.load("hedgehog.png")
                screen.blit(hedgehog.Img, (hedgehog.X, hedgehog.Y))
            elif keys[pygame.K_LEFT]:
                hedgehog.change = -1 * hedgehog_speed * hedgehog_mul
                hedgehog.Img = pygame.image.load("hedgehog_rev.png")
                screen.blit(hedgehog.Img, (hedgehog.X, hedgehog.Y))
            else:
                hedgehog.change = 0

            #zamykanie gry
            if event.type == pygame.QUIT:
                run = False
                reset()


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
            if round(T, 2) % 18 == 0:
                stone.X.append(random.randint(0, MAX_X))
                stone.Y.append(-400)
                stone.change.append(2.0)


            #zjadanie jablka
            for i in range(3):
                if get_point(i):
                    bite_sound.play()
                    apple.Y[i] = SCREEN_HEIGHT + 1
                    score_val += 1

            #zjadanie kamienia
            for i in range(len(stone.X)):
                if get_hit(i):
                    #hit_sound.play()
                    stone.Y[i] = SCREEN_HEIGHT + 1
                    #score_val += 1
                    screen.fill((255,255,255))
                    obituary = font.render("Umarłes " + str(nick.get_value()), True, (0,0,0))
                    screen.blit(obituary, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                    pygame.display.update()
                    time.sleep(5)
                    dead = True
                    reset()   

            #znikniecie gruszki
            if pear.Y > SCREEN_HEIGHT:
                pear.X = random.randint(0, MAX_X)
                counter = 0
                pear.Y = -10
                print("Gruszka przeleciala")

            #wypuszczenie gruszki
            if counter == ready_pear:
                #ruch gruszki
                counter = ready_pear - 1
                pear_move()

            #zjedzenie gruszki
            if get_speed():
                hedgehog_mul += 0.15
                pear.Y = SCREEN_HEIGHT + 1
                pear.Y = -10
                pear.X = random.randint(0, MAX_X)
                counter = 0
                ready_pear = random.randint(460, 840)
                print("Gruszka zjedzona")

            #pokazuj wynik
            show_score(textX, textY)
            #pokazuj czas
            show_time(timeX, timeY, round(T, 2))


            #koniec gry
            if score_val == 100 or dead == True:
                your_time = round(T, 2)
                reset()
                #ekran pokazujący czas
                while run:
                    screen.fill((10,92,43))
                    show_time(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, round(T, 2))
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
                                    fontHS = pygame.font.Font('Lato-Black.ttf', 42)
                                    screen.blit(fontHS.render("HIGHSCORES:", True, (235,235,235)), (390, 100))
                                    for i in range(min(10, len(highscores))):
                                        show(390, 150, highscores, i)

                                    pygame.display.update()

            pygame.display.update()

    pass

#menu
menu = pygame_menu.Menu(300, 400, 'Witaj', theme=pygame_menu.themes.THEME_BLUE)
nick = menu.add_text_input('Imię: ', default='John')
menu.add_button('Graj', start_the_game)
menu.add_button('Wyjdź', quit_the_game)
menu.mainloop(screen, fps_limit=144)

