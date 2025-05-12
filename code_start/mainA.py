import pygame
import sys
from button import ImageButton

# Импорт необходимых модулей
from settings import *
from level import Level
# Импорт функции загрузки карт TMX (карты, созданные в Tiled)
from pytmx.util_pygame import load_pygame
# Импорт функции для объединения путей (удобно для загрузки файлов)
from os.path import join

from support import *
from data import Data
from debug import debug
from ui import UI
from overworld import Overworld
from main import Game

pygame.init()

# HEIGHT/8  HEIGHT*3/8  HEIGHT*7/8

button_up = []
button_med = []
button_low = []

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Ghostly Tales")
main_background = pygame.image.load("image/menu1920.jpg")

cursor = pygame.image.load("image/cursor.png")
pygame.mouse.set_visible(False)

def main_menu():
    new_game_button = ImageButton(WIDTH/20, HEIGHT/8, 307, 123, "", "image/button1920/start.png", "image/button1920/start_hover.png")
    settings_button = ImageButton(WIDTH/20, HEIGHT*3/8, 460, 119, "", "image/button1920/settings.png", "image/button1920/settings_hover.png")
    quit_button = ImageButton(WIDTH/20, HEIGHT*4/5, 292, 129, "", "image/button1920/quit.png", "image/button1920/quit_hover.png")

    button_up.append(new_game_button)
    button_med.append(settings_button)
    button_low.append(quit_button)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == new_game_button:
                general_game()

            if event.type == pygame.USEREVENT and event.button == settings_button:
                settings_menu()

            if event.type == pygame.USEREVENT and event.button == quit_button:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [new_game_button, settings_button, quit_button]:
                btn.handle_event(event)

        for btn in [new_game_button, settings_button, quit_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x, y))

        pygame.display.flip()

def settings_menu():
    audio_button = ImageButton(WIDTH/20, HEIGHT/8, 274, 116, "", "image/button1920/audio.png", "image/button1920/audio_hover.png")
    video_button = ImageButton(WIDTH/20,  HEIGHT*3/8, 273, 115, "", "image/button1920/video.png", "image/button1920/video_hover.png")
    back_set_button = ImageButton(WIDTH/20, HEIGHT*4/5, 272, 117, "", "image/button1920/back.png", "image/button1920/back_hover.png")

    button_up.append(audio_button)
    button_med.append(video_button)
    button_low.append(back_set_button)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_set_button:
                running = False

            if event.type == pygame.USEREVENT and event.button == video_button:
                video_settings()

            for btn in [audio_button, video_button, back_set_button]:
                btn.handle_event(event)

        for btn in [audio_button, video_button, back_set_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x, y))
        
        pygame.display.flip()

def video_settings():
    windowed_button = ImageButton(WIDTH/20, HEIGHT/8, 389, 119, "", "image/button1920/windowed.png", "image/button1920/windowed_hover.png")
    fullscreen_button = ImageButton(WIDTH/20,  HEIGHT*3/8, 663, 119, "", "image/button1920/fullscreen.png", "image/button1920/fullscreen_hover.png")
    back_vid_button = ImageButton(WIDTH/20, HEIGHT*4/5, 272, 117, "", "image/button1920/back.png", "image/button1920/back_hover.png")
    
    button_up.append(windowed_button)
    button_med.append(fullscreen_button)
    button_low.append(back_vid_button)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_vid_button:
                running = False

            if event.type == pygame.USEREVENT and event.button == windowed_button:
                change_video_mode(1280, 720)
                running = False

            if event.type == pygame.USEREVENT and event.button == fullscreen_button:
                change_video_mode(1920, 1080, pygame.FULLSCREEN)
                running = False

            for btn in [windowed_button, fullscreen_button, back_vid_button]:
                btn.handle_event(event)

        for btn in [windowed_button, fullscreen_button, back_vid_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x, y))
        
        pygame.display.flip()

def general_game():
    newgame_button = ImageButton(WIDTH/20, HEIGHT/8, 463, 119, "", "image/button1920/newgame.png", "image/button1920/newgame_hover.png")
    loadgame_button = ImageButton(WIDTH/20, HEIGHT*3/8, 707, 119, "", "image/button1920/loadgame.png", "image/button1920/loadgame_hover.png")
    back_gg_button = ImageButton(WIDTH/20, HEIGHT*4/5, 272, 117, "", "image/button1920/back.png", "image/button1920/back_hover.png")

    button_up.append(newgame_button)
    button_med.append(loadgame_button)
    button_low.append(back_gg_button)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == newgame_button:
                fade()
                new_game()

            if event.type == pygame.USEREVENT and event.button == loadgame_button:
                fade()
                new_game()

            if event.type == pygame.USEREVENT and event.button == back_gg_button:
                running = False

            for btn in [newgame_button, loadgame_button, back_gg_button]:
                btn.handle_event(event)

        for btn in [newgame_button, loadgame_button, back_gg_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(screen)

        x, y = pygame.mouse.get_pos()
        screen.blit(cursor, (x, y))

        pygame.display.flip()

def new_game():
    game = Game()
    game.run()
    # back_game_button = ImageButton(WIDTH/20, HEIGHT*4/5, 272, 117, "", "image/button1920/back.png", "image/button1920/back_hover.png")
    # button_low.append(back_game_button)

    # running = True
    # while running:
    #     screen.fill((0, 0, 0))
        
    #     font = pygame.font.Font(None, 72)
    #     text_surface = font.render("Добро пожаловать в игру!", True, (255, 255, 255))
    #     text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
    #     screen.blit(text_surface, text_rect)

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #             pygame.quit()
    #             sys.exit()

        #     if event.type == pygame.USEREVENT and event.button == back_game_button:
        #         fade()
        #         running = False

        #     for btn in [back_game_button]:
        #         btn.handle_event(event)

        # for btn in [back_game_button]:
        #         btn.check_hover(pygame.mouse.get_pos())
        #         btn.draw(screen)

        # x, y = pygame.mouse.get_pos()
        # screen.blit(cursor, (x, y))
        
        # pygame.display.flip()

def fade():
    running = True
    fade_alpha = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        fade_alpha += 5
        if fade_alpha >= 255:
            fade_alpha = 255
            running = False

        pygame.display.flip()

def change_video_mode(w, h, fullscreen = 0):
    global WIDTH, HEIGHT, screen, main_background, button_lst

    WIDTH, HEIGHT = w, h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), fullscreen)

    main_background = pygame.image.load(f'image/menu{WIDTH}.jpg')

    for btn in button_up:
        btn.set_pos(WIDTH/20, HEIGHT/8)

    for btn in button_med:
        btn.set_pos(WIDTH/20, HEIGHT*3/8)

    for btn in button_low:
        btn.set_pos(WIDTH/20, HEIGHT*4/5)       

if __name__ == "__main__":
    main_menu()