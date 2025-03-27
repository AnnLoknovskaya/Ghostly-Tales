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


# Класс движущегося спрайта (например, платформы)
class MovingSprite(Sprite):
	def __init__(self, groups, start_pos, end_pos, move_dir, speed):
		# Создание поверхности спрайта
		surf = pygame.Surface((200, 50))
		super().__init__(start_pos, surf, groups)
		self.image.fill('white')

		# Установка начального положения
		if move_dir == 'x': # Если движение по горизонтали
			self.rect.midleft = start_pos # Привязываем к левой середине позиции
		else: # Если движение по вертикали
			self.rect.midtop = start_pos # Привязываем к верхней середине позиции

		# Параметры движения
		self.start_pos = start_pos # Начальная точка движения
		self.end_pos = end_pos # Конечная точка движения
		self.speed = speed * 4.8 # Скорость движения (умножаем для масштабирования)

		# Логика движения
		self.moving = True # Флаг, указывающий, движется ли объект
		self.direction = vector(1, 0) if move_dir == 'x' else vector(0, 1) # Определение направления движения
		self.move_dir = move_dir # Сохранение оси движения ('x' или 'y')

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

		else: # Если движение по вертикали
			# Если объект достиг конечной точки внизу, меняем направление вверх
			if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
				self.direction.y = -1
				self.rect.bottom = self.end_pos[1]
			# Если объект достиг начальной точки вверху, меняем направление вниз
			if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
				self.direction.y = 1
				self.rect.top = self.start_pos[1]

	# Метод обновления позиции спрайта
	def update(self, dt):
		self.old_rect = self.rect.copy() # Сохраняем предыдущее положение для обработки коллизий
		self.rect.topleft += self.direction * self.speed * dt # Перемещаем объект в заданном направлении
		self.check_border() # Проверяем границы движения и меняем направление, если необходимо