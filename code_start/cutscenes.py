import pygame
import sys
import math

pygame.init()

# Настройки окна
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("катсцена 1")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DIALOG_BG_COLOR = (255, 255, 224)

# Шрифты
font = pygame.font.SysFont(None, 24)

def draw_character(pos):
    # Рисуем круг персонажа
    pygame.draw.circle(screen, BLACK, (int(pos[0]), int(pos[1])), 20)

def draw_dialogue(text, pos, max_width=300):
    # Используем те же цвета, что и в draw_dialogue_box2
    bg_color = WHITE
    border_color = BLACK
    text_color = BLACK

    # Разбиваем текст на строки по ширине max_width
    words = text.split()
    lines = []
    current_line = ''
    
    for word in words:
        test_line = current_line + (' ' if current_line else '') + word
        test_surface = font.render(test_line, True, text_color)
        if test_surface.get_width() <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    # Высота каждой строки
    line_height = font.get_height()
    
    # Общая высота блока с отступами
    rect_height = line_height * len(lines) + 20  # padding: по 10 сверху и снизу
    
    # Ширина блока — максимум из ширин строк или max_width + padding
    rect_width = max([font.render(line, True, text_color).get_width() for line in lines]) + 20
    
    rect_x= pos[0] - rect_width//2
    rect_y= pos[1] -20 - rect_height -10
    
    dialog_rect=pygame.Rect(rect_x , rect_y , rect_width , rect_height )
    
    # Рисуем фон и рамку с теми же цветами
    pygame.draw.rect(screen, bg_color , dialog_rect)
    pygame.draw.rect(screen, border_color , dialog_rect ,2)
    
    # Рисуем каждую строку внутри блока
    y_offset= rect_y +10  # отступ сверху
    for line in lines:
        text_surface= font.render(line , True , text_color)
        screen.blit(text_surface , (rect_x +10 , y_offset))
        y_offset += line_height
def cut1():
    # Положение портала слева у края экрана
    portal_x = 50
    portal_y = HEIGHT // 2

    # Конечная точка — центр экрана
    target_x = WIDTH // 2
    target_y = HEIGHT // 2

    # Параметры движения по дуге
    flight_time = 1200  # время полета в миллисекундах
    start_time = None

    # Начальная позиция персонажа — у портала
    start_pos = [portal_x + 20, portal_y]

    # Текущая позиция персонажа
    character_pos = start_pos.copy()

    # Флаг запуска анимации полета (автоматический запуск)
    has_flew = False

    # Список диалогов
    dialogues_list1 = ["Мда, мягкая посадочка", "А, собственно, где я? ", "Это явно не похоже на место, куда отправляются умершие, чтобы наконец отдохнуть.", "Неужели мы с моим товарищем сделали что-то не так и я все еще не могу упокоиться?!", "Так, ладно... Наверно, сперва стоит осмотреться и найти безопасное место, а там и разберемся, что же случилось."]
    dialogue_index = -1  # Изначально ничего не выбрано

    dialogue_text = ''
    show_dialogue = False
    dialogue_display_time = 2000  # миллисекунды
    dialogue_start_time = None

    # Множество уже показанных фраз для ограничения одного показа каждой.
    shown_dialogues=set()

    # Флаг приземления и остановки анимации
    landed_and_stopped=False
    running=True
    dialogue_finished = False  # добавляем флаг завершения диалога

    while running:
        dt=clock.tick(60)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            
            elif event.type==pygame.MOUSEBUTTONDOWN:
                # При переключаемся на следующую фразу в списке.
                dialogue_index +=1
                
                if dialogue_index >= len(dialogues_list1):
                    dialogue_index=0
                
                current_phrase= dialogues_list1[dialogue_index]
                
                # Показываем только если эта фраза еще не показывалась.
                if current_phrase not in shown_dialogues:
                    dialogue_text= current_phrase
                    show_dialogue=True
                    dialogue_start_time=pygame.time.get_ticks()
                    shown_dialogues.add(current_phrase)
                else:
                    # Если фраза уже показывалась — не показываем диалог.
                    show_dialogue=False
                
                # Запускаем анимацию полета при первом клике или при необходимости.
                if not has_flew:
                    start_time=pygame.time.get_ticks()
                    has_flew=True

                    arc_height=150  # высота дуги

                    start_point= start_pos.copy()
                    end_point= [target_x , target_y]

        # Автоматический запуск полета при старте программы.
        if not has_flew:
            start_time=pygame.time.get_ticks()
            has_flew=True

            arc_height=150  # высота дуги

            start_point= start_pos.copy()
            end_point= [target_x , target_y]

        screen.fill(WHITE)

        # Рисуем портал слева у края экрана
        pygame.draw.circle(screen,(100,100,255),(portal_x , portal_y),30)

        # Анимация полета — только если еще не приземлились.
        if has_flew and not landed_and_stopped:
            current_time=pygame.time.get_ticks()
            elapsed= current_time - start_time

            t= min(elapsed / flight_time ,1) # прогресс от 0 до 1

            x= start_point[0] + (end_point[0] - start_point[0]) * t
            y_base= start_point[1] + (end_point[1] - start_point[1]) * t
            y_offset= arc_height * math.sin(math.pi * t)
            y= y_base - y_offset

            character_pos=[x,y]

            if t>=1:
                character_pos=[end_point[0], end_point[1]]
                landed_and_stopped=True

        else:
            if landed_and_stopped:
                character_pos=[end_point[0], end_point[1]]

        draw_character(character_pos)

        if show_dialogue:
            draw_dialogue(dialogue_text , character_pos )

        # Проверяем завершение диалога
        if show_dialogue:
            current_time = pygame.time.get_ticks()
            if current_time - dialogue_start_time > dialogue_display_time:
                show_dialogue=False
        else:
            # Если диалог не показывается и все фразы показаны (или по вашему условию),
            # можно завершить функцию.
            if len(shown_dialogues) >= len(dialogues_list1):
                dialogue_finished = True

        # Если диалог завершен — выходим из цикла и функции
        if dialogue_finished:
            break

        pygame.display.flip()

def draw_dialogue_box2(text, speaker_position, speaker_side):
    padding = 10
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render(text, True, BLACK)
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()

    box_width = text_width + 2 * padding
    box_height = text_height + 2 * padding

    if speaker_side == 'left':
        box_x = speaker_position[0] + 50
        box_y = speaker_position[1] - box_height - 20
    else:
        box_x = speaker_position[0] - box_width - 50
        box_y = speaker_position[1] - box_height - 20

    # Ограничение по границам экрана
    if box_x < 0:
        box_x=0
    if box_x + box_width > WIDTH:
        box_x=WIDTH - box_width
    if box_y <0:
        box_y=0

    # Рисуем окно и текст
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height),1)
    screen.blit(text_surface,(box_x + padding ,box_y + padding))

def cut2():
    # Позиции персонажей
    character1_x=50
    character1_y=HEIGHT//2+100

    character2_x=WIDTH-150
    character2_y=HEIGHT//2+100

    # Положение обрыва (в центре)
    cliff_x=WIDTH//2
    cliff_y=HEIGHT//2+50

    # Диалоги: список кортежей (имя_говорящего, текст)
    dialogues=[
        ('Персонаж1', "И куда теперь?!"),
        ('Персонаж2', "Не тормози, прыгай!"),
        ('Персонаж1', "Ты с ума сошел? Я не допрыгну!"),
        ('Персонаж2', "Вниз прыгай, я его задержу"),
        ('Персонаж1', "Выбор у меня невелик...")
    ]

    current_dialogue_idx=0

    scene_stage='approach'   # стадии: approach -> dialogue -> jump -> завершение
    show_dialogue=False

    jump_initiated=False
    jump_start_time=None
    jump_duration=1000

    moving_to_quarter=True

    character1_pos=[character1_x , character1_y]

    running=True

    while running:
        dt=clock.tick(60)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

            elif event.type==pygame.MOUSEBUTTONDOWN:
                if scene_stage=='approach':
                    scene_stage='dialogue'
                    show_dialogue=True
                elif scene_stage=='dialogue':
                    current_dialogue_idx+=1
                    if current_dialogue_idx>=len(dialogues):
                        # Все диалоги показаны — начинаем прыжок
                        scene_stage='jump'
                        jump_start_time=pygame.time.get_ticks()
                        jump_start_pos=list(character1_pos)
                        jump_initiated=False

        screen.fill(WHITE)

        # Рисуем обрыв
        pygame.draw.rect(screen,(139,69,19),(cliff_x -50 , cliff_y ,100 ,20))

        # Всегда рисуем персонажа1
        draw_character(character1_pos)

        # Всегда рисуем персонажа2
        draw_character([character2_x , character2_y])

        if scene_stage=='approach':
            if moving_to_quarter:
                target_x= WIDTH*0.25
                if character1_pos[0]<target_x:
                    character1_pos[0]+=6
                else:
                    moving_to_quarter=False

        elif scene_stage=='dialogue':
            speaker_name,text= dialogues[current_dialogue_idx]
            if speaker_name=='Персонаж1':
                speaker_side='left'
                speaker_pos=[character1_pos[0], character1_pos[1]]
            else:
                speaker_side='right'
                speaker_pos=[character2_x , character2_y]
            draw_dialogue_box2(text,speaker_pos,speaker_side)

        elif scene_stage == 'jump':
            if not jump_initiated:
                jump_initiated = True
                jump_start_time = pygame.time.get_ticks()
                jump_phase = 'up'
                fall_speed = 0

            elapsed = pygame.time.get_ticks() - jump_start_time
            t = min(elapsed / jump_duration, 1)

            # Путь по дуге прыжка
            x = jump_start_pos[0] + (cliff_x - jump_start_pos[0]) * t
            y_base = jump_start_pos[1] + (cliff_y - jump_start_pos[1]) * t
            arc_height = 150
            y_offset = arc_height * math.sin(math.pi * t)
            y = y_base - y_offset

            if t >= 1 and jump_phase == 'up':
                # Завершили прыжок по дуге — начинаем падение
                jump_phase = 'fall'
                fall_speed = 0  # сбрасываем скорость для падения

            if jump_phase == 'fall':
                fall_speed += 10  # гравитация
                y += fall_speed

                if y >= HEIGHT:
                    return  # персонаж упал за границы экрана

            character1_pos = [x, y]
            draw_character(character1_pos)

        pygame.display.flip()

def cut1_5():
    # Начальные параметры
    start_pos = [70, HEIGHT // 2]

    #---------------СЮДА НАДО ДОБАВИТЬ ФРАЗЫ БУДЕТ

    # Текущая позиция персонажа
    character_pos = start_pos.copy()  # старт слева у края
    target_x = WIDTH // 2  # середина экрана
    speed = 7

    state = "running"  # состояния: running, waiting_for_jump, jumping, jumping_sequence, on_platform, fleeing
    wait_start_time = None

    jump_count = 0
    max_jumps = 3

    jump_start_time = None
    jump_duration = 600  # длительность прыжка в мс
    jump_start_pos = None
    jump_end_pos = None

    on_platform_time_start = None
    platform_wait_time = 2000  # задержка на платформе в миллисекундах

    fleeing_speed_multiplier=2

    running=True

    while running:
        dt=clock.tick(60)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

        current_time=pygame.time.get_ticks()

        # Логика по состояниям
        if state=="running":
            if character_pos[0]<target_x:
                character_pos[0]+=speed
            else:
                state="waiting_for_jump"
                wait_start_time=current_time

        elif state=="waiting_for_jump":
            if current_time - wait_start_time >=1000:
                # начинаем прыжок вверх
                state="jumping"
                jump_start_time=current_time
                jump_start_pos=character_pos.copy()
                jump_end_pos=[character_pos[0], character_pos[1]-150]

        elif state=="jumping":
            elapsed = current_time - jump_start_time
            t = min(elapsed / jump_duration, 1)
            x = jump_start_pos[0] + (jump_end_pos[0] - jump_start_pos[0]) * t
            
            y_base = jump_start_pos[1]
            arc_height = 150
            y_offset = arc_height * math.sin(math.pi * t)
            y = y_base - y_offset

            character_pos[0] = x
            character_pos[1] = y

            if t >= 1:
                # Завершение прыжка
                jump_count += 1
                if jump_count < max_jumps:
                    state="waiting_for_next_jump"
                    wait_start_time=current_time
                else:
                    # Возвращаемся на землю или фиксируем позицию на вершине
                    #character_pos[1]=HEIGHT-50  # на земле
                    state="on_platform"
                    on_platform_time_start=current_time

        elif state=="waiting_for_next_jump":
            if current_time - wait_start_time >=500:
                state="jumping"
                jump_start_time=current_time
                jump_start_pos=character_pos.copy()
                jump_end_pos=[character_pos[0], character_pos[1]-150]

        elif state=="on_platform":
            # персонаж стоит на вершине некоторое время (например, 2 секунды)
            if current_time - on_platform_time_start >= platform_wait_time:
                # после этого убегает за границы экрана справа
                state="flee"

        elif state=="flee":
            character_pos[0]+=speed*fleeing_speed_multiplier

        # Проверка выхода за границы экрана справа — завершение сцены или остановка.
        if character_pos[0]>WIDTH+50:
            running=False

        # Рисуем сцену
        screen.fill(WHITE)
        pygame.draw.circle(screen, (0, 0, 255), (int(character_pos[0]), int(character_pos[1])),20)

        pygame.display.flip()

if __name__ == "__main__":
    cut1_5()