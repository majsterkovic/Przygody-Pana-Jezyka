import pygame 

#definiowanie okna gry
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.init()


def show(x, y, DANE, i):
    font = pygame.font.Font('Lato-Bold.ttf', 32)

    imie = font.render(str(i+1) + "." + " " + str(DANE[i][1]), True, (255,255,255))
    punkty = font.render( str(DANE[i][0]), True, (255,255,255))

    screen.blit(imie, (x, y+i*42))
    screen.blit(punkty, (x+200, y+i*42))

highscores = []
f = open("scores.txt", "a")
f.write("\n100 Daniel")
f.close()
f = open("scores.txt", "r")
for line in f:
    x = line.split()
    x[0] = int(x[0])
    highscores.append(x)
highscores.sort(reverse=True)

print(highscores)

run = True
while run:

    for event in pygame.event.get():

            #zamykanie gry
            if event.type == pygame.QUIT:
                run = False

    screen.fill((0,82,33))
    font = pygame.font.Font('Lato-Bold.ttf', 42)
    screen.blit(font.render("HIGHSCORES:", True, (255,255,255)), (390, 100))
    for i in range(10):
        show(390, 150, highscores, i)

    pygame.display.update()