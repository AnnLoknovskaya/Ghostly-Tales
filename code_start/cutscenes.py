import pygame
import sys
import math
from settings import *
from final_credits import *

pygame.init()

# Настройки окна
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("катсцена 1")
clock = pygame.time.Clock()

# Загрузка кадров портала
portal_frames = [
    pygame.image.load('portal/idle/1.png').convert_alpha(),
    pygame.image.load('portal/idle/2.png').convert_alpha(),
    pygame.image.load('portal/idle/3.png').convert_alpha(),
    pygame.image.load('portal/idle/4.png').convert_alpha(),
    pygame.image.load('portal/idle/5.png').convert_alpha(),
    pygame.image.load('portal/idle/6.png').convert_alpha(),
    pygame.image.load('portal/idle/7.png').convert_alpha(),
    pygame.image.load('portal/idle/8.png').convert_alpha()
]
for i in range(len(portal_frames)):
    portal_frames[i] = pygame.transform.scale(portal_frames[i], (TILE_SIZE*6, TILE_SIZE*6))

# Загрузка кадров падающего персонажа
gg_fall_frames = [
    pygame.image.load('gg/fall/1.png').convert_alpha(),
    pygame.image.load('gg/fall/2.png').convert_alpha(),
    pygame.image.load('gg/fall/3.png').convert_alpha(),
    pygame.image.load('gg/fall/4.png').convert_alpha(),
    pygame.image.load('gg/fall/5.png').convert_alpha()
]
for i in range(len(gg_fall_frames)):
    gg_fall_frames[i] = pygame.transform.scale(gg_fall_frames[i], (TILE_SIZE*4, TILE_SIZE*4))

gg_fall_water_frames = [
    pygame.image.load('gg/fall_water/1.png').convert_alpha(),
    pygame.image.load('gg/fall_water/2.png').convert_alpha()
]
for i in range(len(gg_fall_water_frames)):
    gg_fall_water_frames[i] = pygame.transform.scale(gg_fall_water_frames[i], (TILE_SIZE*3, TILE_SIZE*3))

gg_run_frames = [
    pygame.image.load('gg/run/1.png').convert_alpha(),
    pygame.image.load('gg/run/2.png').convert_alpha(),
    pygame.image.load('gg/run/3.png').convert_alpha(),
    pygame.image.load('gg/run/4.png').convert_alpha(),
    pygame.image.load('gg/run/5.png').convert_alpha(),
    pygame.image.load('gg/run/6.png').convert_alpha(),
    pygame.image.load('gg/run/7.png').convert_alpha(),
    pygame.image.load('gg/run/8.png').convert_alpha()
]
for i in range(len(gg_run_frames)):
    gg_run_frames[i] = pygame.transform.scale(gg_run_frames[i], (TILE_SIZE*3, TILE_SIZE*3))

gg_jump_frames = [
    pygame.image.load('gg/jump/1.png').convert_alpha(),
    pygame.image.load('gg/jump/2.png').convert_alpha(),
    pygame.image.load('gg/jump/3.png').convert_alpha(),
    pygame.image.load('gg/jump/4.png').convert_alpha(),
    pygame.image.load('gg/jump/5.png').convert_alpha(),
    pygame.image.load('gg/jump/6.png').convert_alpha(),
    pygame.image.load('gg/jump/7.png').convert_alpha(),
    pygame.image.load('gg/jump/8.png').convert_alpha()
]
for i in range(len(gg_jump_frames)):
    gg_jump_frames[i] = pygame.transform.scale(gg_jump_frames[i], (TILE_SIZE*3, TILE_SIZE*3))

gg_idle_frames = [
    pygame.image.load('gg/idle/1.png').convert_alpha(),
    pygame.image.load('gg/idle/2.png').convert_alpha(),
    pygame.image.load('gg/idle/3.png').convert_alpha()
]
for i in range(len(gg_idle_frames)):
    gg_idle_frames[i] = pygame.transform.scale(gg_idle_frames[i], (TILE_SIZE*3, TILE_SIZE*3))

kaira_idle2_frames = [
    pygame.image.load('kaira/idle2/1.png').convert_alpha(),
    pygame.image.load('kaira/idle2/2.png').convert_alpha(),
    pygame.image.load('kaira/idle2/3.png').convert_alpha(),
    pygame.image.load('kaira/idle2/4.png').convert_alpha()
]
for i in range(len(kaira_idle2_frames)):
    kaira_idle2_frames[i] = pygame.transform.scale(kaira_idle2_frames[i], (TILE_SIZE*3.5, TILE_SIZE*3.5))

kaira_fall_water_frames = [
    pygame.image.load('kaira/fall_water/1.png').convert_alpha(),
    pygame.image.load('kaira/fall_water/2.png').convert_alpha()
]
for i in range(len(kaira_fall_water_frames)):
    kaira_fall_water_frames[i] = pygame.transform.scale(kaira_fall_water_frames[i], (TILE_SIZE*3.5, TILE_SIZE*3.5))

kaira_run_frames = [
    pygame.image.load('kaira/run/1.png').convert_alpha(),
    pygame.image.load('kaira/run/2.png').convert_alpha(),
    pygame.image.load('kaira/run/3.png').convert_alpha(),
    pygame.image.load('kaira/run/4.png').convert_alpha(),
    pygame.image.load('kaira/run/5.png').convert_alpha(),
    pygame.image.load('kaira/run/6.png').convert_alpha(),
    pygame.image.load('kaira/run/7.png').convert_alpha(),
    pygame.image.load('kaira/run/8.png').convert_alpha()
]
for i in range(len(kaira_run_frames)):
    kaira_run_frames[i] = pygame.transform.scale(kaira_run_frames[i], (TILE_SIZE*3.5, TILE_SIZE*3.5))

boss_run_frames = [
    pygame.image.load('boss_run/1.png').convert_alpha(),
    pygame.image.load('boss_run/2.png').convert_alpha(),
    pygame.image.load('boss_run/3.png').convert_alpha(),
    pygame.image.load('boss_run/4.png').convert_alpha(),
    pygame.image.load('boss_run/5.png').convert_alpha(),
    pygame.image.load('boss_run/6.png').convert_alpha(),
    pygame.image.load('boss_run/7.png').convert_alpha(),
    pygame.image.load('boss_run/8.png').convert_alpha()
]
for i in range(len(boss_run_frames)):
    boss_run_frames[i] = pygame.transform.scale(boss_run_frames[i], (TILE_SIZE*15, TILE_SIZE*15))


all_sprites = pygame.sprite.Group()

class AnimSprite(pygame.sprite.Sprite):
    def __init__(self, pos, frames, group=None, animation_speed=10, loop=True):
        super().__init__(group)
        self.frames = frames
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=pos)
        self.animation_speed = animation_speed
        self.counter = 0
        self.loop = loop
        self.animation_finished = False

    def update(self):
        if self.animation_finished:
            return  # анимация закончилась, перестаём обновлять

        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.frames):
                if self.loop:
                    self.index = 0
                else:
                    self.index = len(self.frames) - 1
                    self.animation_finished = True
            self.image = self.frames[self.index]

portal_sprite = None

def create_portal(pos, group):
    global portal_sprite
    portal_sprite = AnimSprite(pos=pos, frames=portal_frames, group=group, animation_speed=10, loop=True)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифты
font = pygame.font.SysFont(None, 24)

def draw_dialogue(text, pos, max_width=300):
    bg_color = WHITE
    border_color = BLACK
    text_color = BLACK

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
    
    line_height = font.get_height()
    rect_height = line_height * len(lines) + 20
    rect_width = max([font.render(line, True, text_color).get_width() for line in lines]) + 20
    
    rect_x = pos[0] - rect_width // 2
    rect_y = pos[1] - 20 - rect_height - 10
    
    dialog_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
    
    pygame.draw.rect(screen, bg_color, dialog_rect)
    pygame.draw.rect(screen, border_color, dialog_rect, 2)
    
    y_offset = rect_y + 10
    for line in lines:
        text_surface = font.render(line, True, text_color)
        screen.blit(text_surface, (rect_x + 10, y_offset))
        y_offset += line_height

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + ('' if current_line == '' else ' ') + word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def cut1():
    background_image = pygame.image.load("bg_cut1.jpg").convert()
    # Если нужно подогнать размер под экран, то:
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    portal_x = 50
    portal_y = HEIGHT // 2 - 150
    create_portal((portal_x, portal_y), all_sprites)

    gg_fall_sprite = AnimSprite(
        pos=(portal_x + 20, portal_y),
        frames=gg_fall_frames,
        group=all_sprites,
        animation_speed=10
    )

    target_x = portal_x + WIDTH // 3
    target_y = HEIGHT // 2 - 120
    flight_time = 2500
    start_time = None
    start_point = [portal_x + 20, portal_y]
    end_point = [target_x, target_y]
    arc_height = 100

    has_flew = False
    landed_and_stopped = False

    dialogues_list1 = [
        "Мда, мягкая посадочка",
        "А, собственно, где я? ",
        "Это явно не похоже на место, куда отправляются умершие, чтобы наконец отдохнуть.",
        "Неужели мы с моим товарищем сделали что-то не так и я все еще не могу упокоиться?!",
        "Так, ладно... Наверно, сперва стоит осмотреться и найти безопасное место, а там и разберемся, что же случилось."
    ]
    dialogue_index = -1
    dialogue_text = ''
    show_dialogue = False
    dialogue_start_time = None
    shown_dialogues = set()
    dialogue_finished = False

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                dialogue_index += 1
                if dialogue_index >= len(dialogues_list1):
                    dialogue_index = 0
                current_phrase = dialogues_list1[dialogue_index]
                if current_phrase not in shown_dialogues:
                    dialogue_text = current_phrase
                    show_dialogue = True
                    dialogue_start_time = pygame.time.get_ticks()
                    shown_dialogues.add(current_phrase)
                else:
                    show_dialogue = False

                if not has_flew:
                    start_time = pygame.time.get_ticks()
                    has_flew = True

        if not has_flew:
            start_time = pygame.time.get_ticks()
            has_flew = True

        screen.blit(background_image, (0, 0))

        if portal_sprite:
            portal_sprite.update()

        if has_flew and not landed_and_stopped:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - start_time
            t_raw = min(elapsed / flight_time, 1)

            t = 0.5 - 0.5 * math.cos(math.pi * t_raw)

            x = start_point[0] + (end_point[0] - start_point[0]) * t
            y_base = start_point[1] + (end_point[1] - start_point[1]) * t
            y_offset = arc_height * math.sin(math.pi * t)
            y = y_base - y_offset

            gg_fall_sprite.rect.center = (x, y)

            frame_index = int(t_raw * (len(gg_fall_frames) - 1))
            gg_fall_sprite.index = frame_index
            gg_fall_sprite.image = gg_fall_frames[frame_index]

            if t_raw >= 1:
                landed_and_stopped = True
                gg_fall_sprite.rect.center = (end_point[0], end_point[1])
        else:
            gg_fall_sprite.index = len(gg_fall_frames) - 1
            gg_fall_sprite.image = gg_fall_frames[-1]
            gg_fall_sprite.rect.center = (end_point[0], end_point[1])

        all_sprites.draw(screen)

        if show_dialogue:
            # Используем draw_dialogue_box2 вместо draw_dialogue
            draw_dialogue_box2(dialogue_text, (gg_fall_sprite.rect.centerx, gg_fall_sprite.rect.top - 10), align='left')

        if not show_dialogue:
            if len(shown_dialogues) >= len(dialogues_list1):
                dialogue_finished = True

        pygame.display.flip()

        if dialogue_finished:
            break

    all_sprites.empty()

def draw_dialogue_box2(text, pos, align='left'):
    font = pygame.font.SysFont('arial', 24)
    max_width = 400  # максимальная ширина текста в пикселях
    lines = wrap_text(text, font, max_width)

    line_height = font.get_linesize()
    box_width = max([font.size(line)[0] for line in lines]) + 20
    box_height = line_height * len(lines) + 20

    x, y = pos
    y -= box_height + 10
    if align == 'left':
        rect = pygame.Rect(x, y, box_width, box_height)
    else:
        rect = pygame.Rect(x - box_width, y, box_width, box_height)

    # Белый фон с чёрной рамкой
    pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=8)

    # Чёрный текст
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, (0, 0, 0))
        if align == 'left':
            screen.blit(text_surface, (rect.x + 10, rect.y + 10 + i * line_height))
        else:
            line_width = font.size(line)[0]
            screen.blit(text_surface, (rect.x + box_width - line_width - 10, rect.y + 10 + i * line_height))

def cut2():
    background_image = pygame.image.load("bg_cut2.jpg").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    character1_x = 50
    character1_y = HEIGHT // 3 + 130

    character2_x = WIDTH - 250
    character2_y = HEIGHT // 3 + 110

    cliff_x = WIDTH // 2
    cliff_y = HEIGHT // 3 + 50

    dialogues = [
        ('Персонаж1', "И куда теперь?!"),
        ('Персонаж2', "Не тормози, прыгай!"),
        ('Персонаж1', "Ты с ума сошел? Я не допрыгну!"),
        ('Персонаж2', "Вниз прыгай, я его задержу"),
        ('Персонаж1', "Выбор у меня невелик...")
    ]

    current_dialogue_idx = 0
    scene_stage = 'run'   # run -> stop -> dialogue -> jump
    show_dialogue = False

    moving_to_quarter = True
    target_x = WIDTH * 0.25

    # Создаем спрайт gg для персонажа1 с бегом сначала
    gg_sprite = AnimSprite(
        pos=(character1_x, character1_y),
        frames=gg_run_frames,
        group=all_sprites,
        animation_speed=5
    )

    # Создаем спрайт kaira для персонажа2 (idle анимация)
    kaira_sprite = AnimSprite(
        pos=(character2_x, character2_y),
        frames=kaira_idle2_frames,
        group=all_sprites,
        animation_speed=10
    )

    jump_start_time = None
    jump_duration = 1000
    jump_phase = None
    fall_speed = 0

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if scene_stage == 'stop':
                    scene_stage = 'dialogue'
                    show_dialogue = True
                elif scene_stage == 'dialogue':
                    current_dialogue_idx += 1
                    if current_dialogue_idx >= len(dialogues):
                        scene_stage = 'jump'
                        jump_start_time = pygame.time.get_ticks()
                        jump_start_pos = list(gg_sprite.rect.center)
                        jump_phase = 'up'
                        fall_speed = 0

        screen.blit(background_image, (0, 0))


        kaira_sprite.update()

        if scene_stage == 'run':
            if gg_sprite.rect.centerx < target_x:
                gg_sprite.rect.centerx += 6
                gg_sprite.update()
            else:
                scene_stage = 'stop'
                gg_sprite.frames = gg_idle_frames
                gg_sprite.index = 0
                gg_sprite.animation_speed = 10
                gg_sprite.counter = 0

        elif scene_stage == 'stop':
            gg_sprite.update()

        elif scene_stage == 'dialogue':
            gg_sprite.update()  # Важно: анимация не останавливается в диалоге
            # Диалог рисуем после отрисовки спрайтов

        elif scene_stage == 'jump':
            elapsed = pygame.time.get_ticks() - jump_start_time
            t = min(elapsed / jump_duration, 1)

            x = jump_start_pos[0] + (cliff_x - jump_start_pos[0]) * t
            y_base = jump_start_pos[1] + (cliff_y - jump_start_pos[1]) * t
            arc_height = 150
            y_offset = arc_height * math.sin(math.pi * t)
            y = y_base - y_offset

            frame_index = int(t * (len(gg_jump_frames) - 1))
            gg_sprite.index = frame_index
            gg_sprite.image = gg_jump_frames[frame_index]
            gg_sprite.rect.center = (x, y)

            if t >= 1 and jump_phase == 'up':
                jump_phase = 'fall'
                fall_speed = 0

            if jump_phase == 'fall':
                fall_speed += 10
                y += fall_speed
                gg_sprite.rect.center = (x, y)
                if y >= HEIGHT:
                    all_sprites.empty()
                    return

        all_sprites.draw(screen)  # рисуем персонажей

        if scene_stage == 'dialogue':
            speaker_name, text = dialogues[current_dialogue_idx]
            if speaker_name == 'Персонаж1':
                speaker_pos = gg_sprite.rect.midtop
            else:
                speaker_pos = kaira_sprite.rect.midtop
            draw_dialogue_box2(text, speaker_pos, 'left' if speaker_name == 'Персонаж1' else 'right')

        pygame.display.flip()

    all_sprites.empty()

def cut1_5():
    background_image = pygame.image.load("bg_cut1_5.jpg").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    bg_x = 0
    bg_speed = 5  # скорость движения фона в пикселях за кадр

    start_pos = [WIDTH // 2 - 100, HEIGHT // 2 - 90]
    boss_start_x = -100  # за экраном слева
    boss_pos = [boss_start_x, HEIGHT // 2 - 250]

    platform_height = HEIGHT // 2 - 90
    current_platform_height = platform_height
    jump_height = 150
    jump_duration = 600
    speed = 5
    fleeing_speed_multiplier = 2
    boss_speed = 2  # скорость босса при выползании

    target_x = start_pos[0] + 150

    state = "dialogue_before_run"
    wait_start_time = None

    jump_count = 0
    max_jumps = 5

    jump_start_time = None
    jump_start_pos = None
    jump_end_pos = None

    on_platform_time_start = None
    platform_wait_time = 2000

    pre_run_dialogues = [
        "Что это?",
        "Черт, оно совсем рядом, надо бежать"
    ]
    dialogue_index = 0
    show_dialogue = True

    gg_sprite = AnimSprite(
        pos=start_pos,
        frames=gg_idle_frames,  # анимация стояния
        group=all_sprites,
        animation_speed=6
    )

    boss_sprite = None

    running = True
    clock = pygame.time.Clock()

    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == "dialogue_before_run" and show_dialogue:
                    dialogue_index += 1
                    if dialogue_index >= len(pre_run_dialogues):
                        show_dialogue = False
                        # Диалог закончился — добавляем босса в группу, меняем состояние
                        boss_sprite = AnimSprite(
                            pos=[0 + 50, HEIGHT // 2 - 200],
                            frames=boss_run_frames,
                            group=all_sprites,  # ОБЯЗАТЕЛЬНО передаём группу!
                            animation_speed=8
                        )
                        state = "boss_appearing"
                    else:
                        pass

        current_time = pygame.time.get_ticks()

        # --- Движение фона ---
        if state != "dialogue_before_run":
            bg_x -= bg_speed
            if bg_x <= -WIDTH:
                bg_x = 0

        # Рисуем фон дважды для бесшовности
        screen.blit(background_image, (bg_x, 0))
        screen.blit(background_image, (bg_x + WIDTH, 0))

        # --- Основная логика по состояниям ---
        if state == "dialogue_before_run":
            # idle анимация
            if gg_sprite.frames != gg_idle_frames:
                gg_sprite.frames = gg_idle_frames
                gg_sprite.current_frame = 0
            gg_sprite.update()

        elif state == "boss_appearing":
            # во время появления босса герой стоит (idle)
            if gg_sprite.frames != gg_idle_frames:
                gg_sprite.frames = gg_idle_frames
                gg_sprite.current_frame = 0

            # Босс движется вправо с края экрана к своей стартовой позиции
            if boss_sprite.rect.centerx < boss_pos[0] + 150:
                boss_sprite.rect.centerx += boss_speed
            else:
                # Босс занял позицию, начинается бег игрока
                state = "running"
                target_x = start_pos[0] + 150

            boss_sprite.update()
            gg_sprite.update()

        elif state in ["running", "waiting_for_jump", "waiting_for_next_jump", "running_on_platform", "flee"]:
            # беговая анимация
            if gg_sprite.frames != gg_run_frames:
                gg_sprite.frames = gg_run_frames
                gg_sprite.current_frame = 0

            if state == "running":
                if gg_sprite.rect.centerx < target_x:
                    gg_sprite.rect.centerx += speed
                else:
                    state = "waiting_for_jump"
                    wait_start_time = current_time

            elif state == "waiting_for_jump":
                if current_time - wait_start_time >= 700:
                    state = "jumping"
                    jump_start_time = current_time
                    jump_start_pos = [gg_sprite.rect.centerx, gg_sprite.rect.centery]
                    jump_end_pos = [jump_start_pos[0] + 30, current_platform_height]

            elif state == "waiting_for_next_jump":
                if current_time - wait_start_time >= 600:
                    state = "jumping"
                    jump_start_time = current_time
                    jump_start_pos = [gg_sprite.rect.centerx, gg_sprite.rect.centery]
                    jump_end_pos = [jump_start_pos[0] + 30, current_platform_height]

            elif state == "running_on_platform":
                if gg_sprite.rect.centerx < target_x:
                    gg_sprite.rect.centerx += speed
                else:
                    if on_platform_time_start is None:
                        on_platform_time_start = current_time
                    if current_time - on_platform_time_start >= platform_wait_time:
                        state = "flee"

            elif state == "flee":
                gg_sprite.rect.centerx += speed * fleeing_speed_multiplier

            gg_sprite.update()
            boss_sprite.update()

        elif state == "jumping":
            # прыжковая анимация
            if gg_sprite.frames != gg_jump_frames:
                gg_sprite.frames = gg_jump_frames
                gg_sprite.current_frame = 0

            elapsed = current_time - jump_start_time
            t = min(elapsed / jump_duration, 1)

            x = jump_start_pos[0] + (jump_end_pos[0] - jump_start_pos[0]) * t

            y_start = jump_start_pos[1]
            y_end = jump_end_pos[1]

            y = y_start + (y_end - y_start) * t - jump_height * math.sin(math.pi * t)

            gg_sprite.rect.center = (x, y)

            gg_sprite.update()
            boss_sprite.update()

            if t >= 1:
                jump_count += 1
                current_platform_height -= 150

                if jump_count < max_jumps:
                    if jump_count < 3:
                        state = "waiting_for_next_jump"
                        wait_start_time = current_time
                    else:
                        state = "running_on_platform"
                        target_x = gg_sprite.rect.centerx + 150
                else:
                    state = "flee"

        if gg_sprite.rect.left > WIDTH + 50:
            running = False

        all_sprites.draw(screen)

        if state == "dialogue_before_run" and show_dialogue:
            draw_dialogue_box2(pre_run_dialogues[dialogue_index], (gg_sprite.rect.centerx, gg_sprite.rect.top - 10), align='left')

        pygame.display.flip()

    all_sprites.empty()

def cut2_5():
    water_y = HEIGHT - 100  # уровень воды (примерно)
    shore_y = water_y - 30  # береговая линия

    character1_start = [WIDTH // 4, -100]
    character2_start = [WIDTH // 2, -150]

    character1_shore = [WIDTH // 4, shore_y]
    character2_shore = [WIDTH // 2, shore_y]

    dialogues = [
        ('Персонаж1', "Пронесло? Я больше не слышу погони"),
        ('Персонаж2', "Все в порядке, он не сможет сюда добраться. Даже если решится прыгнуть, утонет. Эти твари, к счастью, не умеют плавать."),
        ('Персонаж1', "Определенно, это радует"),
        ('Персонаж2', "Ты в порядке? Руки, ноги на месте?"),
        ('Персонаж1', "Вроде бы да"),
        ('Персонаж2', "Тогда нам нужно скорее уходить"),
        ('Персонаж1', "Ты же сказал, что этот монстр не умеет плавать"),
        ('Персонаж2', "Так тут и похуже существа бывают"),
        ('Персонаж1', "Что з..."),
        ('Персонаж2', "Я отведу тебя в безопасное место и там отвечу на все твои вопросы. Пойдем скорее"),
        ('Персонаж1', "Ну хорошо")
    ]

    state = 'fall1'
    current_dialogue_idx = 0
    show_dialogue = False

    gg_sprite = AnimSprite(pos=character1_start, frames=gg_fall_water_frames, group=all_sprites, animation_speed=8)
    kaira_sprite = AnimSprite(pos=character2_start, frames=kaira_fall_water_frames, group=all_sprites, animation_speed=8)

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_dialogue:
                    current_dialogue_idx += 1
                    if current_dialogue_idx >= len(dialogues):
                        show_dialogue = False
                        state = 'walk_right'
                        # Переключаем анимацию GG и Кайры на бег
                        gg_sprite.frames = gg_run_frames
                        gg_sprite.index = 0
                        gg_sprite.animation_speed = 10

                        kaira_sprite.frames = kaira_run_frames
                        kaira_sprite.index = 0
                        kaira_sprite.animation_speed = 10

        screen.fill(WHITE)
        pygame.draw.rect(screen, (0, 100, 255), (0, water_y, WIDTH, HEIGHT - water_y))

        if state == 'fall1':
            gg_sprite.rect.centery += 8
            if gg_sprite.rect.centery >= water_y:
                gg_sprite.rect.centery = water_y
                state = 'out_of_water1'
                gg_sprite.frames = gg_idle_frames
                gg_sprite.index = 0
                gg_sprite.animation_speed = 8
            gg_sprite.update()

        elif state == 'out_of_water1':
            gg_sprite.rect.centery -= 3
            if gg_sprite.rect.centery <= shore_y:
                gg_sprite.rect.centery = shore_y
                state = 'fall2'
                kaira_sprite.rect.center = character2_start
                kaira_sprite.frames = kaira_fall_water_frames
                kaira_sprite.index = 0
                kaira_sprite.animation_speed = 8
            gg_sprite.update()

        elif state == 'fall2':
            kaira_sprite.rect.centery += 8
            if kaira_sprite.rect.centery >= water_y:
                kaira_sprite.rect.centery = water_y
                state = 'out_of_water2'
                kaira_sprite.frames = kaira_idle2_frames
                kaira_sprite.index = 0
                kaira_sprite.animation_speed = 8
            kaira_sprite.update()
            gg_sprite.update()

        elif state == 'out_of_water2':
            kaira_sprite.rect.centery -= 3
            if kaira_sprite.rect.centery <= shore_y:
                kaira_sprite.rect.centery = shore_y
                state = 'dialogue'
                show_dialogue = True
                current_dialogue_idx = 0
            kaira_sprite.update()
            gg_sprite.update()

        elif state == 'dialogue':
            gg_sprite.update()
            kaira_sprite.update()

            speaker_name, text = dialogues[current_dialogue_idx]
            if speaker_name == 'Персонаж1':
                speaker_pos = gg_sprite.rect.midtop
                align = 'left'
            else:
                speaker_pos = kaira_sprite.rect.midtop
                align = 'right'

            draw_dialogue_box2(text, speaker_pos, align)

        elif state == 'walk_right':
            gg_sprite.rect.centerx += 5
            kaira_sprite.rect.centerx += 5
            gg_sprite.update()
            kaira_sprite.update()

            if gg_sprite.rect.left > WIDTH and kaira_sprite.rect.left > WIDTH:
                running = False

        all_sprites.draw(screen)
        pygame.display.flip()

    all_sprites.empty()


if __name__ == "__main__":
    cut2()
    #final_credits()
    