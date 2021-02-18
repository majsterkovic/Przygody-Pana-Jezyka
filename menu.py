import pygame_menu

from functions import *

#menu
menu = pygame_menu.Menu(300, 400, 'Witaj', theme=pygame_menu.themes.THEME_BLUE)
menu.add_text_input('Imię: ', default='Jacuś')
menu.add_button('Graj', start_the_game(score_val_and_counter))
menu.add_button('Wyjdź', pygame_menu.events.EXIT)
menu.mainloop(screen)