import pygame

from timer import Timer
from settings import *

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, semi_collision_sprites):
        super().__init__(groups)
        # Создание изображения игрока
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')

        # Определение прямоугольников для коллизий
        self.rect = self.image.get_rect(topleft=pos) # Прямоугольник на позиции pos
        self.old_rect = self.rect.copy() # Хранит предыдущее положение для коллизий

        # Движения
        self.direction = vector() # Вектор направления движения
        self.speed = 280 # Скорость передвижения
        self.gravity = 3000 #Гравитация
        self.jump = False # Флаг для прыжка
        self.jump_height = 1400 # Сила прыжка

        # Коллизии
        self.collision_sprites = collision_sprites # Спрайты с полной коллизией
        self.semi_collision_sprites = semi_collision_sprites # Спрайты с частичной коллизией (платформы)
        self.on_surface = {'floor': False, 'left': False, 'right': False}  # Статус контакта с поверхностями
        self.platform = None # Платформа, на которой стоит игрок

        # Таймеры для механик прыжков и взаимодействий
        self.timers = {
            'wall jump': Timer(400),
            'wall slide block': Timer(250),
            'platform skip': Timer(300)
        }

    # Метод для обработки ввода от игрока
    def input(self):
        # Получаем состояние клавиш
        keys = pygame.key.get_pressed()

        # Разрешаем горизонтальное движение (всегда)
        input_vector = vector(0, 0)
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1 # Движение вправо
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1 # Движение влево
        # Активировать таймер для пропуска платформы (если нажата стрелка вниз)
        if keys[pygame.K_DOWN]:
            self.timers['platform skip'].activate()

        # Нормализуем горизонтальное направление для плавности движения
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

        # Обработка прыжка
        if keys[pygame.K_SPACE]:
            self.jump = True # Устанавливаем True, если нажат space

    # Метод для обработки движений игрока
    def move(self, dt):
        # Применяем горизонтальное движение сразу
        self.rect.x += self.direction.x * self.speed * dt
        # Проверка на горизонтальные коллизии
        self.collision('horizontal')

        # Применяем вертикальное движение (гравитация и прыжки)
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not \
        self.timers['wall slide block'].active:
            # Если игрок не стоит на поверхности, но касается стены (и нет блокировки скольжения)
            self.direction.y = 0 # Останавливаем вертикальное движение
            self.rect.y += self.gravity / 10 * dt # Применяем замедленную гравитацию
        else: # Иначе
            self.direction.y += self.gravity * dt # Применяем полную гравитацию
            self.rect.y += self.direction.y * dt # Перемещаем игрока по вертикали

        # Обработка прыжка
        if self.jump:
            # Если игрок на земле
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height # Устанавливаем вертикальное движение вверх
                self.timers['wall slide block'].activate() # Блокируем скольжение по стене
                self.rect.bottom -= 1  # Корректируем положение игрока
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

    # Метод для движения вместе с платформой
    def platform_move(self, dt):
        if self.platform:
            # Перемещаем игрока вместе с платформой
            self.rect.topleft += self.platform.direction * self.platform.speed * dt

    # Проверка контакта с платформами и проверка коллизий
    def check_contact(self):
        # Прямоугольник пола
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 7))
        # Прямоугольник правой стороны
        right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4), (2, self.rect.height / 2))
        # Прямоугольник левой стороны
        left_rect = pygame.Rect(self.rect.topleft + vector(-2, self.rect.height / 4), (2, self.rect.height / 2))
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

    # Метод для проверки коллизий по осям
    def collision(self, axis):
        for sprite in self.collision_sprites:
            # Если прямоугольник игрока сталкивается с прямоугольником другого объекта
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal': # Горизонтальные коллизии
                    # Если столкновение с левой стороной
                    if self.rect.left <= sprite.rect.right and int(self.old_rect.left) >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # Если столкновение с правой стороной
                    if self.rect.right >= sprite.rect.left and int(self.old_rect.right) <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                else:  # Вертикальные коллизии
                    # Если столкновение с верхней стороной
                    if self.rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        if hasattr(sprite, 'moving'): # Если объект двигается
                            self.rect.top += 8 # Корректируем положение игрока
                    # Если столкновение с нижней стороной
                    if self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0 # Останавливаем вертикальное движение

    # Метод для проверки частичных коллизий (с платформами)
    def semi_collision(self):
        # Если таймер пропуска платформы не активен
        if not self.timers['platform skip'].active:
            for sprite in self.semi_collision_sprites:
                # Если прямоугольник игрока сталкивается с платформой
                if sprite.rect.colliderect(self.rect):
                    if self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top # Корректируем положение игрока на платформе
                        if self.direction.y > 0:
                            self.direction.y = 0 # Останавливаем вертикальное движение

    # Обновление таймеров
    def update_timers(self):
        for timer in self.timers.values():
            timer.update() # Обновление состояния таймеров

    # Основной метод обновления
    def update(self, dt):
        self.old_rect = self.rect.copy() # Сохраняем текущую позицию для коллизий
        self.update_timers() # Обновляем таймеры
        self.input() # Обрабатываем ввод
        self.move(dt) # Перемещаем игрока
        self.platform_move(dt) # Перемещаем игрока вместе с платформой (если он на ней)
        self.check_contact() # Проверяем контакт с коллизиями и платформами
