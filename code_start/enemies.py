from random import choice

import pygame.sprite

from settings import *
from timer import Timer

class Tooth(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites, health=3):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        ####
        self.rect = self.image.get_rect(topleft = pos)
        self.z = Z_LAYERS['main']

        self.direction = choice((-1, 1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.speed = 500
        self.health = health

        self.hit_timer = Timer(250)

    def reverse(self):
        if not self.hit_timer.active:
            self.direction *= -1
            self.hit_timer.activate()

    def take_damage(self, amount=1):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        # Можно добавить анимацию смерти, звук и т.п.
        self.kill()

    def update(self, dt):
        self.hit_timer.update()

        # Анимация
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

        # Перемещение
        self.rect.x += self.direction * self.speed * dt

        # Смена направления
        ######
        # Проверка, есть ли пол под ногами
        floor_rect_right = pygame.Rect(self.rect.bottomright, (2, 2))
        floor_rect_left = pygame.Rect((self.rect.bottomleft[0] - 2, self.rect.bottomleft[1]), (2, 2))

        # Проверка на столкновение со стенами
        wall_rect = pygame.Rect(self.rect.topleft + vector(-1, 0), (self.rect.width + 2, self.rect.height))

        # Если нет пола или упёрся в стену — меняем направление
        if (floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0) or \
                (floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0) or \
                (wall_rect.collidelist(self.collision_rects) != -1):
            self.reverse()

class Shell(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, reverse, player, create_pearl, health=3):
        super().__init__(groups)

        if reverse:
            self.frames = {}
            for key, surfs in frames.items():
                self.frames[key] = [pygame.transform.flip(surf, True, False) for surf in surfs]
                self.bullet_direction = -1
        else:
            self.frames = frames
            self.bullet_direction = 1

        self.frame_index = 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        #####
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']
        self.player = player
        self.health = health
        self.shoot_timer = Timer(3000)
        self.has_fired = False
        self.create_pearl = create_pearl

    def state_management(self):
        player_pos, shell_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = shell_pos.distance_to(player_pos) < 500
        player_front = shell_pos.x < player_pos.x if self.bullet_direction > 0 else shell_pos.x > player_pos.x
        player_level = abs(shell_pos.y - player_pos.y) < 60

        if player_near and player_front and player_level and not self.shoot_timer.active:
            self.state = 'fire'
            self.frame_index = 0
            self.shoot_timer.activate()

    def take_damage(self, amount=1):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        # Можно добавить анимацию смерти, звук и т.п.
        self.kill()

    def update(self, dt):
        self.shoot_timer.update()
        self.state_management()

        # Анимация и атаки
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frame_index)]

            # Атака
            if self.state == 'fire' and int(self.frame_index) == 4 and not self.has_fired:
                self.create_pearl(self.rect.center, self.bullet_direction)
                self.has_fired = True

        else:
            self.frame_index = 0
            if self.state == 'fire':
                self.state = 'idle'
                self.has_fired = False

class Pearl(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf, direction, speed):
        self.pearl = True
        super().__init__(groups)
        self.image = surf
        ######
        self.rect = self.image.get_rect(center = pos + vector(50 * direction, 0))
        self.direction = direction
        self.speed = speed
        self.z = Z_LAYERS['main']
        self.timers = {'lifetime': Timer(5000), 'reverse': Timer(250)}
        self.timers['lifetime'].activate()

    def reverse(self):
        if not self.timers['reverse'].active:
            self.direction *= -1
            self.timers['reverse'].activate()

    def update(self, dt):
        for timer in self.timers.values():
            timer.update()

        #!!! Поменяла скорость движения пули
        self.rect.x += self.direction * self.speed * dt * 3
        if not self.timers['lifetime'].active:
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, health=20, z=Z_LAYERS['main']):
        super().__init__(groups)
        self.hurt_timer = Timer(400)
        self.frame_index = 0

        # Масштабируем кадры анимаций
        scale_factor = 9  # увеличиваем размер до 9 * TILE_SIZE
        self.frames = {}
        for key in frames:
            self.frames[key] = [
                pygame.transform.scale(surf, (TILE_SIZE * scale_factor, TILE_SIZE * scale_factor))
                for surf in frames[key]
            ]

        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z

        self.player = player
        self.health = health
        self.direction = pygame.math.Vector2(-1, 0)
        self.speed = 5

        self.attack_timer = Timer(2000)
        self.attack_timer.activate()

        self.animation_timer = 0
        self.animation_speed = 0.15

        self.has_attacked = False

    def attack(self):
        if self.state == 'attack':
            if int(self.frame_index) == 4 and not self.has_attacked:
                if hasattr(self.player, 'take_damage'):
                    self.player.take_damage()
                self.has_attacked = True

    def take_damage(self, amount=1):
        if not self.hurt_timer.active:
            self.health -= amount
            if self.health > 0:
                self.state = 'hurt'
                self.frame_index = 0
                self.hurt_timer.activate()
            else:
                self.die()

    def die(self):
        self.kill()

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index += 1

            frames_count = len(self.frames[self.state])
            if self.frame_index >= frames_count:
                self.frame_index = 0
                if self.state == 'attack':
                    self.state = 'idle'
                    self.has_attacked = False

            self.image = self.frames[self.state][self.frame_index]

    def state_management(self):
        if self.state == 'hurt':
            return

        if not self.attack_timer.active and self.state != 'attack':
            self.state = 'attack'
            self.frame_index = 0
            self.has_attacked = False
            self.attack_timer.activate()

    def move(self, dt, collision_sprites):
        self.rect.x += self.direction.x * self.speed * dt * 60

        floor_rect_right = pygame.Rect(self.rect.bottomright, (2, 2))
        floor_rect_left = pygame.Rect((self.rect.bottomleft[0] - 2, self.rect.bottomleft[1]), (2, 2))

        collision_rects = [sprite.rect for sprite in collision_sprites]

        if self.direction.x > 0:
            wall_rect = pygame.Rect(self.rect.right + 1, self.rect.top, 2, self.rect.height)
        else:
            wall_rect = pygame.Rect(self.rect.left - 3, self.rect.top, 2, self.rect.height)

        no_floor_right = floor_rect_right.collidelist(collision_rects) == -1 and self.direction.x > 0
        no_floor_left = floor_rect_left.collidelist(collision_rects) == -1 and self.direction.x < 0
        hit_wall = wall_rect.collidelist(collision_rects) != -1

        if no_floor_right or no_floor_left or hit_wall:
            self.direction.x *= -1

    def update(self, dt, collision_sprites):
        self.attack_timer.update()
        self.hurt_timer.update()

        if not self.hurt_timer.active and self.state == 'hurt':
            self.state = 'idle'
            self.frame_index = 0

        self.state_management()
        self.attack()
        self.animate(dt)

        if self.state not in ['hurt', 'attack']:
            self.move(dt, collision_sprites)


