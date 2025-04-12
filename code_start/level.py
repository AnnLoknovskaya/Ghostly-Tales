import pygame.sprite

from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite
from player import Player
from groups import AllSprites
from enemies import Tooth, Shell

# Создание уровня
class Level:
	def __init__(self, tmx_map, level_frames):
		# Получаем поверхность экрана для отображения
		self.display_surface = pygame.display.get_surface()

		# Группы спрайтов для управления рендерингом и взаимодействием объектов
		self.all_sprites = AllSprites()  # Все спрайты
		self.collision_sprites = pygame.sprite.Group() # Спрайты, с которыми происходят коллизии
		self.semi_collision_sprites = pygame.sprite.Group() # Спрайты с частичными коллизиями
		self.damage_sprites = pygame.sprite.Group()
		self.tooth_sprites = pygame.sprite.Group()

		# Инициализация уровня с использованием карты tmx
		self.setup(tmx_map, level_frames)

	# Метод для создания тайлов (плиток) на основе слоя Terrain
	def setup(self, tmx_map, level_frames):
		# Проходим по всем плиткам и создаем спрайты
		for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
			for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
				groups = [self.all_sprites]
				if layer == 'Terrain': groups.append(self.collision_sprites)
				if layer == 'Platforms': groups.append(self.semi_collision_sprites)

				match layer:
					case 'BG': z = Z_LAYERS['bg tiles']
					case 'FG': z = Z_LAYERS['bg tiles']
					case _: z = Z_LAYERS['main']
				# Создаем статичный спрайт и добавляем его в соответствующие группы
				Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)

		# Создание объектов на основе слоя Objects
		for obj in tmx_map.get_layer_by_name('Objects'):
			# Если объект - игрок, создаем экземпляр класса Player
			if obj.name == 'player':
				self.player = Player(
					pos = (obj.x, obj.y),
					groups = self.all_sprites,
					collision_sprites = self.collision_sprites,
					semi_collision_sprites = self.semi_collision_sprites,
					frames = level_frames['player'])
			else:
				# Объекты без анимации
				if obj.name in ('barrel', 'crate'):
					Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
				else:
					if 'palm' not in obj.name:
						frames = level_frames[obj.name]
						AnimatedSprite((obj.x, obj.y), frames, self.all_sprites)

		# Создание движущихся объектов на основе слоя Moving Objects
		for obj in tmx_map.get_layer_by_name('Moving Objects'):
			if obj.name == 'helicopter':
				# Определяем направление движения в зависимости от размеров объекта
				if obj.width > obj.height: #Если ширина больше высоты, движение горизонтальное
					move_dir = 'x'
					start_pos = (obj.x, obj.y + obj.height / 2)
					end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
				else: # Иначе вертикальное
					move_dir = 'y'
					start_pos = (obj.x + obj.width / 2, obj.y)
					end_pos = (obj.x + obj.width / 2, obj.y + obj.height)

				# Получаем скорость движения из свойств объекта
				speed = obj.properties['speed']

				#Создаем движущийся спрайт и добавляем его в соответствующие группы
				MovingSprite((self.all_sprites, self.semi_collision_sprites), start_pos, end_pos, move_dir, speed)

		# Злодеи
		for obj in tmx_map.get_layer_by_name('Enemies'):
			if obj.name == 'tooth':
				Tooth((obj.x, obj.y), level_frames['tooth'], (self.all_sprites, self.damage_sprites, self.tooth_sprites), self.collision_sprites)
			if obj.name == 'shell':
				# Пример добавления смещения к позициям (например, смещение на 10 пикселей вправо и вниз)
				shell_pos = (obj.x + 10, obj.y + 10)  # Сдвиг на 10 пикселей
				Shell(shell_pos, level_frames['shell'], (self.all_sprites, self.collision_sprites))


	# Метод обновления и отрисовки уровня в каждом кадре
	def run(self, dt):
		# Заполняем экран черным цветом перед отрисовкой след кадра
		self.display_surface.fill('black')

		# Обновляем все спрайты с учетом времени dt (используется для плавности движения)
		self.all_sprites.update(dt)

		# Отрисовываем все спрайты на экране
		self.all_sprites.draw(self.player.hitbox_rect.center)



