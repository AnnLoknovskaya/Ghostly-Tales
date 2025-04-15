import pygame
from timer import Timer
from os.path import join
from settings import *

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, semi_collision_sprites, frames):
        super().__init__(groups)
        self.z = Z_LAYERS['main']

        # Создание изображения игрока
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'idle_girl', True
        self.image = self.frames[self.state][self.frame_index]

        # Определение прямоугольников для коллизий
        self.rect = self.image.get_rect(topleft=pos) # Прямоугольник на позиции pos
        self.hitbox_rect = self.rect.inflate(-30, 2)
        # self.hitbox_rect = self.rect.inflate(-60, -20)
        self.old_rect = self.hitbox_rect.copy() # Хранит предыдущее положение для коллизий

        # Движения
        self.direction = vector() # Вектор направления движения
        self.speed = 500 # Скорость передвижения
        self.gravity = 3000 #Гравитация
        self.jump = False # Флаг для прыжка
        self.jump_height = 1700 # Сила прыжка
        self.attacking = False

        # Коллизии
        self.collision_sprites = collision_sprites # Спрайты с полной коллизией
        self.semi_collision_sprites = semi_collision_sprites # Спрайты с частичной коллизией (платформы)
        self.on_surface = {'floor': False, 'left': False, 'right': False}  # Статус контакта с поверхностями
        self.platform = None # Платформа, на которой стоит игрок

        # Таймеры для механик прыжков и взаимодействий
        self.timers = {
            'wall jump': Timer(400),
            'wall slide block': Timer(500),
            'platform skip': Timer(50),
            'attack block': Timer(500)
        }

    # Метод для обработки ввода от игрока
    def input(self):
        # Получаем состояние клавиш
        keys = pygame.key.get_pressed()
        # Разрешаем горизонтальное движение (всегда)
        input_vector = vector(0, 0)
        if not self.timers['wall jump'].active:

            if keys[pygame.K_RIGHT]:
                input_vector.x += 1 # Движение вправо
                self.facing_right = True

            if keys[pygame.K_LEFT]:
                input_vector.x -= 1 # Движение влево
                self.facing_right = False

            # Активировать таймер для пропуска платформы (если нажата стрелка вниз)
            if keys[pygame.K_DOWN]:
                self.timers['platform skip'].activate()

            if keys[pygame.K_x]:
                self.attack()

            # Нормализуем горизонтальное направление для плавности движения
            self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        # Обработка прыжка
        if keys[pygame.K_SPACE]:
            self.jump = True # Устанавливаем True, если нажат space

        # if keys[pygame.K_DOWN]:
        #     self.timers['platform skip'].activate()

    def attack(self):
        if not self.timers['attack block'].active:  # Проверяем, что атака не активна
            self.attacking = True  # Начинаем атаку
            self.frame_index = 0  # Сброс индекса кадров для анимации атаки
            self.timers['attack block'].activate()


    # Метод для обработки движений игрока
    def move(self, dt):
        # Применяем горизонтальное движение сразу
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        # Проверка на горизонтальные коллизии
        self.collision('horizontal')

        # Применяем вертикальное движение (гравитация и прыжки)
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not \
        self.timers['wall slide block'].active:
            # Если игрок не стоит на поверхности, но касается стены (и нет блокировки скольжения)
            self.direction.y = 0 # Останавливаем вертикальное движение
            self.hitbox_rect.y += self.gravity / 10 * dt # Применяем замедленную гравитацию
        else: # Иначе
            self.direction.y += self.gravity * dt # Применяем полную гравитацию
            self.hitbox_rect.y += self.direction.y * dt # Перемещаем игрока по вертикали

        # # Добавим параметр для скольжения по стене
        # self.wall_slide_speed = 50  # Ускорение падения при скольжении по стене
        #
        # # Обработка вертикального движения (прыжок и падение)
        # if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])):
        #     # Если игрок не стоит на поверхности, но касается стены
        #     if self.direction.y > 0:  # Если игрок падает вниз
        #         # Применяем ускоренную гравитацию для скольжения по стенам
        #         self.direction.y = min(self.direction.y + self.wall_slide_speed * dt, self.gravity)
        #     else:
        #         self.direction.y = 0  # Если игрок не падает, то вертикальная скорость 0
        #     self.hitbox_rect.y += self.direction.y * dt
        # else:
        #     # Если игрок на земле, то применяем нормальную гравитацию
        #     self.direction.y += self.gravity * dt
        #     self.hitbox_rect.y += self.direction.y * dt

        # Обработка прыжка
        if self.jump:
            # Если игрок на земле
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height # Устанавливаем вертикальное движение вверх
                self.timers['wall slide block'].activate() # Блокируем скольжение по стене
                self.hitbox_rect.bottom -= 1  # Корректируем положение игрока
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers[
                'wall slide block'].active:  # Если игрок прыгает от стены
                self.timers['wall jump'].activate() # Активируем таймер прыжка по стене
                self.direction.y = -self.jump_height # Прыжок вверх
                self.direction.x = 1 if self.on_surface['left'] else -1 # Прыжок в сторону стены
            self.jump = False # Сбрасываем флаг прыжка

        # Проверка вертикальных коллизий
        self.collision('vertical')
        # Проверка частичных коллизий с платформами
        self.semi_collision()
        self.rect.center = self.hitbox_rect.center

    # Метод для движения вместе с платформой
    def platform_move(self, dt):
        if self.platform:
            # Перемещаем игрока вместе с платформой
            self.hitbox_rect.topleft += self.platform.direction * self.platform.speed * dt

    # Проверка контакта с платформами и проверка коллизий
    def check_contact(self):
        # Прямоугольник пола
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        # Прямоугольник правой стороны
        right_rect = pygame.Rect(self.hitbox_rect.topright + vector(0, self.hitbox_rect.height / 4), (2, self.hitbox_rect.height / 2))
        # Прямоугольник левой стороны
        left_rect = pygame.Rect(self.hitbox_rect.topleft + vector(-2, self.hitbox_rect.height / 4), (2, self.hitbox_rect.height / 2))
        # Прямоугольники с полной коллизией
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        # Прямоугольники с частичной коллизией
        semi_collide_rect = [sprite.rect for sprite in self.semi_collision_sprites]

        # Проверка коллизий с полом
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 or floor_rect.collidelist(semi_collide_rect) >= 0 and self.direction.y >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False

        # Проверка платформы, на которой стоит игрок
        self.platform = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            # Если прямоугольник пола сталкивается с платформой
            if sprite.rect.colliderect(floor_rect):
                self.platform = sprite # Привязываем игрока к платформе

    # Метод для обработки коллизий
    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal':  # Горизонтальные коллизии
                    # Если столкновение с левой стороной
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(
                            sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right
                        self.direction.x = 0  # Останавливаем движение по оси X
                    # Если столкновение с правой стороной
                    elif self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(
                            sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left
                        self.direction.x = 0  # Останавливаем движение по оси X
                else:  # Вертикальные коллизии
                    # Если столкновение с верхней стороной
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(
                            sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom
                        self.direction.y = 0  # Останавливаем вертикальное движение
                    # Если столкновение с нижней стороной
                    elif self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(
                            sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.direction.y = 0  # Останавливаем вертикальное движение

    # Метод для проверки частичных коллизий (с платформами)
    def semi_collision(self):
        # Если таймер пропуска платформы не активен
        if not self.timers['platform skip'].active:
            for sprite in self.semi_collision_sprites:
                # Если прямоугольник игрока сталкивается с платформой
                if sprite.rect.colliderect(self.hitbox_rect):
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = sprite.rect.top # Корректируем положение игрока на платформе
                        if self.direction.y > 0:
                            self.direction.y = 0 # Останавливаем вертикальное движение

    # Обновление таймеров
    def update_timers(self):
        for timer in self.timers.values():
            timer.update() # Обновление состояния таймеров

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        # Проверяем, завершена ли анимация атаки
        if self.state == 'attack_girl' and self.frame_index >= len(self.frames[self.state]):
            self.state = 'idle_girl'  # Возвращаем состояние в idle после завершения атаки
            self.attacking = False  # Сбрасываем флаг атаки

        # Обновление изображения на основе состояния
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)

        if self.attacking and self.frame_index > len(self.frames[self.state]):
            self.attacking = False

    def get_state(self):
        if self.on_surface['floor']:
            if self.attacking:
                self.state = 'attack_girl'
            else:
                self.state = 'idle_girl' if self.direction.x == 0 else 'run_girl'
        else:
            if self.attacking:
                self.state = 'air_attack_girl'
            else:
                if any((self.on_surface['left'], self.on_surface['right'])):
                    self.state == 'wall'
                else:
                    self.state = 'jump_girl' if self.direction.y < 0 else 'fall_girl'

    # Основной метод обновления
    def update(self, dt):
        self.old_rect = self.hitbox_rect.copy() # Сохраняем текущую позицию для коллизий
        self.update_timers() # Обновляем таймеры


        self.input() # Обрабатываем ввод
        self.move(dt) # Перемещаем игрока
        self.platform_move(dt) # Перемещаем игрока вместе с платформой (если он на ней)
        self.check_contact() # Проверяем контакт с коллизиями и платформами

        self.get_state()
        self.animate(dt)