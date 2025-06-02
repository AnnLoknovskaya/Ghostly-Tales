import pygame
import sys
from settings import *

def final_credits():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 30)
    
    # Текст титров — список строк
    credits = [
        "Поздравляем с прохождением 1 Акта!",
        "",
        "Продолжение следует...",
        "",
        "Разработка:",
        "Анна Локновская",
        "Ирина Кусякина",
        "",
        "Специальные благодарности:",
        "Вам, игрокам!",
        "",
        "THE END"
    ]
    
    # Преобразуем строки в рендеренные поверхности
    credit_surfaces = [font.render(line, True, (255, 255, 255)) for line in credits]
    
    # Начальная позиция текста — внизу экрана (можно чуть ниже)
    y = WINDOW_HEIGHT
    
    speed = 1  # скорость прокрутки
    
    running = True
    while running:
        screen.fill((0, 0, 0))  # черный фон
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # Можно прервать титры нажатием клавиши или кнопкой мыши
                running = False
        
        # Отрисовка каждой строки, сдвинутой по Y
        for i, surf in enumerate(credit_surfaces):
            rect = surf.get_rect(center=(WINDOW_WIDTH // 2, y + i * 40))
            screen.blit(surf, rect)
        
        y -= speed  # сдвиг текста вверх
        
        # Если весь текст вышел за верх экрана, завершаем титры
        if y + len(credit_surfaces) * 40 < 0:
            running = False
        
        pygame.display.flip()
        clock.tick(60)
    