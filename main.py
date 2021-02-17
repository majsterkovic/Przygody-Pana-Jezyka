import pygame
import random
import pygame_menu
from pygame import mixer

pygame.init()

clock = pygame.time.Clock()
clock.tick(60)

# definiowanie okna gry
screen = pygame.display.set_mode((1080, 720))
mixer.music.load('AutumnDay.mp3')
pygame.mixer.music.play(-1)

# wyświetlanie okna gry
pygame.display.set_caption("Przygody Pana Jeżyka")

# gracz
playerImg = pygame.image.load("hedgehog.png")
#rozmiar 64x64
playerX = 508
playerY = 568
playerX_change = 0

# jablko
appleImg = pygame.image.load("apple.png")
#rozmiar 64x64
appleX = random.randint(0, 1014)
appleY = -5
appleY_change = 0.15

# gruszka
pearImg = pygame.image.load("pear.png")
#rozmiar 64x64

#wynik
score_val = 0
font = pygame.font.Font('SyneMono-Regular.ttf', 32)
textX = 5
textY = 5

def show_score(x, y):
    score = font.render("Wynik: " + str(score_val), True, (255,255,255))
    screen.blit(score, (x, y))

def player_move():

    global playerX
    global playerY
    global playerX_change

    playerX += playerX_change
        
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1014:
        playerX = 1014

    player(playerX, playerY)

def apple_m():
        
    global appleX
    global appleY
    global appleX_change

    apple(appleX, appleY)
    appleY += appleY_change

def apple_move():
    global appleY
    global appleX
    apple_m()
    if appleY > 1080:
        appleX = random.randint(0, 1014)
        appleY = -5
        apple_m()

def player(x, y):
    screen.blit(playerImg, (x, y))

def apple(x, y):
    screen.blit(appleImg, (x, y))

def get_point():
    global appleX
    global appleY
    global playerX
    global playerY

    if playerX > appleX-64 and playerX < appleX+64 and appleY+64-playerY <= 64 and appleY+64-playerY > 0:
        return True

def start_the_game():

    global playerX_change
    global appleY
    global score_val
    global playerX
    global playerY
    global playerImg

    run = True
    while run:

        screen.fill((0,82,33))

        for event in pygame.event.get():

            #zamykanie gry
            if event.type == pygame.QUIT:
                run = False

            #klawisze

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.2
                    playerImg = pygame.image.load("hedgehog_rev.png")
                    screen.blit(playerImg, (playerX, playerY))
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.2
                    playerImg = pygame.image.load("hedgehog.png")
                    screen.blit(playerImg, (playerX, playerY))

            else:
                playerX_change = 0


        #ruch gracza
        player_move()

        

        #ruch jabłka
        apple_move()
        

        if get_point():
            appleY = 1081
            score_val += 1

        show_score(textX, textY)
        pygame.display.update()

    pass

#menu
menu = pygame_menu.Menu(300, 400, 'Witaj',
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add_text_input('Imię: ', default='Jacuś')
menu.add_button('Graj', start_the_game)
menu.add_button('Wyjdź', pygame_menu.events.EXIT)

menu.mainloop(screen)