from math import sin, cos, radians
from random import randint

import pygame

from settings import *

# Класс простого статического спрайта
class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf=pygame.Surface((TILE_SIZE,TILE_SIZE)), groups=None, z = Z_LAYERS['main']):
		super().__init__(groups)
		self.image = surf # Изображение спрайта
		self.rect = self.image.get_rect(topleft = pos) # Прямоугольник, определяющий положение спрайта
		self.old_rect = self.rect.copy() # Сохранение предыдущего положения (для обработки коллизий)
		self.z = z

class AnimatedSprite(Sprite):
	def __init__(self, pos, frames, groups, z = Z_LAYERS['main'], animation_speed = ANIMATION_SPEED):
		self.frames, self.frame_index = frames, 0
		super().__init__(pos, self.frames[self.frame_index], groups, z)
		self.animation_speed = animation_speed

	def animate(self, dt):
		self.frame_index += self.animation_speed * dt
		self.image = self.frames[int(self.frame_index % len(self.frames))]

	def update(self, dt):
		self.animate(dt)

class Item(AnimatedSprite):
	def __init__(self, item_type, pos, frames, groups, data):
		super().__init__(pos, frames, groups)
		self.rect.center = pos
		self.item_type = item_type
		self.data = data

	def activate(self):
		if self.item_type == 'gold':
			self.data.coins += 5
		if self.item_type == 'silver':
			self.data.coins += 1
		if self.item_type == 'diamond':
			self.data.coins += 20
		if self.item_type == 'skull':
			self.data.coins += 50
		if self.item_type == 'potion':
			self.data.health += 1

class ParticleEffectSprite(AnimatedSprite):
	def __init__(self, pos, frames, groups):
		super().__init__(pos, frames, groups)
		self.rect.center = pos
		self.z = Z_LAYERS['fg']

	def animate(self, dt):
		self.frame_index += self.animation_speed * dt
		if self.frame_index < len(self.frames):
			self.image = self.frames[int(self.frame_index)]
		else:
			self.kill()

# Класс движущегося спрайта (например, платформы)
class MovingSprite(AnimatedSprite):
	def __init__(self, frames, groups, start_pos, end_pos, move_dir, speed, flip = False):
		# Создание поверхности спрайта
		# surf = pygame.Surface((170, 50))
		super().__init__(start_pos, frames, groups)
		# self.image.fill('gray')

		# Установка начального положения
		if move_dir == 'x': # Если движение по горизонтали
			self.rect.midleft = start_pos # Привязываем к левой середине позиции
		else: # Если движение по вертикали
			self.rect.midtop = start_pos # Привязываем к верхней середине позиции

		# Параметры движения
		self.start_pos = start_pos # Начальная точка движения
		self.end_pos = end_pos # Конечная точка движения
		self.speed = speed * 5 # Скорость движения (умножаем для масштабирования)

		# Логика движения
		self.moving = True # Флаг, указывающий, движется ли объект
		self.direction = vector(1, 0) if move_dir == 'x' else vector(0, 1) # Определение направления движения
		self.move_dir = move_dir # Сохранение оси движения ('x' или 'y')
		self.flip = flip
		self.reverse = {'x': False, 'y': False}

	# Метод проверки границ движения (чтобы объект двигался в пределах start_pos и end_pos)
	def check_border(self):
		if self.move_dir == 'x': # Если движение по горизонтали
			# Если объект достиг конечной точки справа, меняем направление влево
			if self.rect.right >= self.end_pos[0] and self.direction.x == 1:
				self.direction.x = -1
				self.rect.right = self.end_pos[0] # Фиксируем позицию, чтобы избежать застревания
			# Если объект достиг начальной точки слева, меняем направление вправо
			if self.rect.left <= self.start_pos[0] and self.direction.x == -1:
				self.direction.x = 1
				self.rect.left = self.start_pos[0]
			self.reverse['x'] = True if self.direction.x < 0 else False

		else: # Если движение по вертикали
			# Если объект достиг конечной точки внизу, меняем направление вверх
			if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
				self.direction.y = -1
				self.rect.bottom = self.end_pos[1]
			# Если объект достиг начальной точки вверху, меняем направление вниз
			if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
				self.direction.y = 1
				self.rect.top = self.start_pos[1]
			self.reverse['y'] = True if self.direction.y > 0 else False

	# Метод обновления позиции спрайта
	def update(self, dt):
		self.old_rect = self.rect.copy() # Сохраняем предыдущее положение для обработки коллизий
		self.rect.topleft += self.direction * self.speed * dt # Перемещаем объект в заданном направлении
		self.check_border() # Проверяем границы движения и меняем направление, если необходимо
		self.animate(dt)
		if self.flip:
			self.image = pygame.transform.flip(self.image, self.reverse['x'], self.reverse['y'])

class Spike(Sprite):
	def __init__(self, pos, surf, groups, radius, speed, start_angle, end_angle, z = Z_LAYERS['main']):
		self.center = pos
		self.radius = radius
		self.speed = speed
		self.start_angle = start_angle
		self.end_angle = end_angle
		self.angle = self.start_angle
		self.direction = 1
		self.full_circle = True if self.end_angle == -1 else False

		# Тригонометрия
		y = self.center[1] + sin(radians(self.angle)) * self.radius
		x = self.center[0] + cos(radians(self.angle)) * self.radius

		super().__init__((x, y), surf, groups, z)

	def update(self, dt):
		self.angle += self.direction * self.speed * dt

		if not self.full_circle:
			if self.angle >= self.end_angle:
				self.direction = -1
			if self.angle < self.start_angle:
				self.direction = 1

		y = self.center[1] + sin(radians(self.angle)) * self.radius
		x = self.center[0] + cos(radians(self.angle)) * self.radius
		self.rect.center = (x, y)

class Cloud(Sprite):
	def __init__(self, pos, surf, groups, z = Z_LAYERS['clouds']):
		super().__init__(pos, surf, groups, z)
		self.speed = randint(50, 120)
		self.direction = -1
		self.rect.midbottom = pos
	def update(self, dt):
		self.rect.x += self.direction * self.speed * dt

		if self.rect.right <= 0:
			self.kill()


class Node(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, level, data, paths):
		super().__init__(groups)
		self.image = surf
		#####
		self.rect = self.image.get_rect(center = (pos[0] + TILE_SIZE / 2, pos[1] + TILE_SIZE / 2))
		self.z = Z_LAYERS['path']
		self.level = level
		self.data = data
		self.paths = paths
		self.grid_pos = (int(pos[0] / TILE_SIZE), int(pos[1] / TILE_SIZE))

	def can_move(self, direction):
		if direction in list(self.paths.keys()) and int(self.paths[direction][0][0]) <= self.data.unlocked_level:
			# print(self.paths[direction][0][0])
			return direction in self.paths

class Icon(pygame.sprite.Sprite):
	def __init__(self, pos, groups, frames):
		super().__init__(groups)
		self.icon = True
		self.path = None
		self.direction = vector()
		self.speed = 400

		#image
		self.frames, self.frame_index = frames, 0
		self.state = 'idle_girl'
		self.image = self.frames[self.state][self.frame_index]
		self.z = Z_LAYERS['main']

		# rect
		###########
		self.rect = self.image.get_rect(center = pos)

	def start_move(self, path):
		self.rect.center = path[0]
		self.path = path[1:]
		self.find_path()

	def find_path(self):
		if self.path:
			if self.rect.centerx == self.path[0][0]: # vertical
				self.direction = vector(0, 1 if self.path[0][1] > self.rect.centery else -1)
			else: #horizontal
				self.direction = vector(1 if self.path[0][0] > self.rect.centerx else -1, 0)
		else:
			self.direction = vector()

	def point_collision(self):
		if self.direction.y == 1 and self.rect.centery >= self.path[0][1] or \
				self.direction.y == -1 and self.rect.centery <= self.path[0][1]	:
			self.rect.centery = self.path[0][1]
			del self.path[0]
			self.find_path()

		if self.direction.x == 1 and self.rect.centerx >= self.path[0][0] or \
				self.direction.x == -1 and self.rect.centerx <= self.path[0][0]:
			self.rect.centerx = self.path[0][0]
			del self.path[0]
			self.find_path()

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]

	def get_state(self):
		self.state = 'idle_girl'
		if self.direction == vector(1, 0):
			self.state = 'right_girl'
		if self.direction == vector(-1, 0):
			self.state = 'left_girl'
		if self.direction == vector(0, 1):
			self.state = 'down_girl'
		if self.direction == vector(0, -1):
			self.state = 'up_girl'

	def update(self, dt):
		if self.path:
			self.point_collision()
			self.rect.center += self.direction * self.speed * dt
		self.get_state()
		self.animate(dt)

class PathSprite(Sprite):
	def __init__(self, pos, surf, groups, level):
		super().__init__(pos, surf, groups, Z_LAYERS['path'])
		self.level = level

