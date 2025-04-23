import pygame.sprite
from sqlalchemy.testing import rowset
from sqlalchemy.util import column_set

from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Item, ParticleEffectSprite, Spike
from player import Player
from groups import AllSprites
from enemies import Tooth, Shell, Pearl


# Создание уровня
class Level:
	def __init__(self, tmx_map, level_frames, data):
		# Получаем поверхность экрана для отображения
		self.display_surface = pygame.display.get_surface()
		self.data = data

		# Данные уровня
		self.level_width = tmx_map.width * TILE_SIZE
		self.level_bottom = tmx_map.height * TILE_SIZE
		tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
		if tmx_level_properties['bg']:
			bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
		else:
			bg_tile = None
		print(level_frames['bg_tiles'].keys())

		# Группы спрайтов для управления рендерингом и взаимодействием объектов
		self.all_sprites = AllSprites(
			width = tmx_map.width,
			height = tmx_map.height,
			bg_tile = bg_tile,
			top_limit = tmx_level_properties['top_limit'],
			clouds = {'large': level_frames['cloud_large'], 'small': level_frames['cloud_small']},
			horizon_line = tmx_level_properties['horizon_line']) # Все спрайты

		self.collision_sprites = pygame.sprite.Group() # Спрайты, с которыми происходят коллизии
		self.semi_collision_sprites = pygame.sprite.Group() # Спрайты с частичными коллизиями
		self.damage_sprites = pygame.sprite.Group()
		self.tooth_sprites = pygame.sprite.Group()
		self.pearl_sprites = pygame.sprite.Group()
		self.item_sprites = pygame.sprite.Group()

		# Инициализация уровня с использованием карты tmx
		self.setup(tmx_map, level_frames)

		# frames
		self.pearl_surf = level_frames['pearl']
		self.particle_frames = level_frames['particle']

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
					frames = level_frames['player'],
					data = self.data)
			else:
				# Объекты без анимации
				if obj.name in ('barrel', 'crate'):
					Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
				else:
					if 'palm' not in obj.name:
						frames = level_frames[obj.name]
						AnimatedSprite((obj.x, obj.y), frames, self.all_sprites)
			if obj.name == 'flag':
				self.level_finish_rect = pygame.FRect((obj.x, obj.y), (obj.width, obj.height))

		# Создание движущихся объектов на основе слоя Moving Objects
		for obj in tmx_map.get_layer_by_name('Moving Objects'):
			if obj.name == 'spike':
				Spike(
					pos = (obj.x + obj.width / 2, obj.y + obj.height / 2),
					surf = level_frames['spike'],
					radius = obj.properties['radius'],
					speed =obj.properties['speed'],
					start_angle =obj.properties['start_angle'],
					end_angle = obj.properties['end_angle'],
					groups = (self.all_sprites, self.damage_sprites))

				for radius in range(0, obj.properties['radius'], 20):
					Spike(
						pos = (obj.x + obj.width / 2, obj.y + obj.height / 2),
						surf = level_frames['spike_chain'],
						radius = radius,
						speed = obj.properties['speed'],
						start_angle = obj.properties['start_angle'],
						end_angle = obj.properties['end_angle'],
						groups = self.all_sprites,
						z = Z_LAYERS['bg details'])

			else:
				frames = level_frames[obj.name]
				groups = (self.all_sprites, self.semi_collision_sprites) if obj.properties['platform'] else (self.all_sprites, self.damage_sprites)
				print(frames)
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
				MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed, obj.properties['flip'])

				if obj.name == 'saw':
					if move_dir == 'x':
						y = start_pos[1] - level_frames['saw_chain'].get_height() / 2
						left, right = int(start_pos[0]), int(end_pos[0])
						for x in range(left, right, 20):
							Sprite((x, y) , level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details'])
					else:
						x = start_pos[0] - level_frames['saw_chain'].get_width() / 2
						top, bottom = int(start_pos[1]), int(end_pos[1])
						for y in range(top, bottom, 20):
							Sprite((x, y), level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details'])

		# Злодеи
		for obj in tmx_map.get_layer_by_name('Enemies'):
			if obj.name == 'tooth':
				Tooth((obj.x, obj.y), level_frames['tooth'], (self.all_sprites, self.damage_sprites, self.tooth_sprites), self.collision_sprites)
			if obj.name == 'shell':
				# Пример добавления смещения к позициям (например, смещение на 10 пикселей вправо и вниз)
				shell_pos = (obj.x + 10, obj.y + 10)  # Сдвиг на 10 пикселей
				Shell(
					pos = shell_pos,
					frames = level_frames['shell'],
					groups = (self.all_sprites, self.collision_sprites),
					reverse = obj.properties['reverse'],
					player = self.player,
					create_pearl = self.create_pearl)

		# Предметы
		for obj in tmx_map.get_layer_by_name('Items'):
			Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites), self.data)

		# Вода
		for obj in tmx_map.get_layer_by_name('Water'):
			rows = int(obj.height / TILE_SIZE)
			cols = int(obj.width / TILE_SIZE)
			for row in range(rows):
				for col in range(cols):
					x = obj.x + col * TILE_SIZE
					y = obj.y + row * TILE_SIZE
					if row == 0:
						AnimatedSprite((x, y), level_frames['water_top'], self.all_sprites, Z_LAYERS['water'])
					else:
						Sprite((x, y), level_frames['water_body'], self.all_sprites, Z_LAYERS['water'])



	def create_pearl(self, pos, direction):
		Pearl(pos, (self.all_sprites, self.damage_sprites, self.pearl_sprites), self.pearl_surf, direction, 150)

	def pearl_collision(self):
		for sprite in self.collision_sprites:
			sprite = pygame.sprite.spritecollide(sprite, self.pearl_sprites, True)
			if sprite:
				ParticleEffectSprite((sprite[0].rect.center), self.particle_frames, self.all_sprites)

	def hit_collision(self):
		for sprite in self.damage_sprites:
			if sprite.rect.colliderect(self.player.hitbox_rect):
				self.player.get_damage()
				if hasattr(sprite, 'pearl'):
					sprite.kill()
					ParticleEffectSprite((sprite.rect.center), self.particle_frames, self.all_sprites)

	def item_collision(self):
		if self.item_sprites:
			item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
			if item_sprites:
				item_sprites[0].activate()
				ParticleEffectSprite((item_sprites[0].rect.center), self.particle_frames, self.all_sprites)

	def attack_collision(self):
		for target in self.pearl_sprites.sprites() + self.tooth_sprites.sprites():
			facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or \
				self.player.rect.centerx > target.rect.centerx and self.player.facing_right
			if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
				target.reverse()

	def check_constraint(self):
		# Влево и вправо
		if self.player.hitbox_rect.left <= 0:
			self.player.hitbox_rect.left = 0
		if self.player.hitbox_rect.right >= self.level_width:
			self.player.hitbox_rect.right = self.level_width

		# bottom border
		if self.player.hitbox_rect.bottom > self.level_bottom:
			pass
			# print('oi wei')

		# Успех
		if self.player.hitbox_rect.colliderect(self.level_finish_rect):
			pass
			# print('success')

	# Метод обновления и отрисовки уровня в каждом кадре
	def run(self, dt):
		# Заполняем экран черным цветом перед отрисовкой след кадра
		self.display_surface.fill('black')

		# Обновляем все спрайты с учетом времени dt (используется для плавности движения)
		self.all_sprites.update(dt)
		self.pearl_collision()
		self.hit_collision()
		self.item_collision()
		self.attack_collision()
		self.check_constraint()

		# Отрисовываем все спрайты на экране
		self.all_sprites.draw(self.player.hitbox_rect.center, dt)



