from random import uniform

import pygame.sprite

from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Item, ParticleEffectSprite, Spike
from player import Player
from groups import AllSprites
from enemies import Tooth, Shell, Pearl, Boss

from cutscenes import *

# Создание уровня
class Level:
	def __init__(self, tmx_map, level_frames, audio_files, data, switch_stage, bg_music):
		# Получаем поверхность экрана для отображения
		self.display_surface = pygame.display.get_surface()
		self.data = data
		self.switch_stage = switch_stage
		self.bg_music = bg_music
		self.boss = None

		# Данные уровня
		self.level_width = tmx_map.width * TILE_SIZE
		self.level_bottom = tmx_map.height * TILE_SIZE
		tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
		self.level_unlock = tmx_level_properties['level_unlock']
		if tmx_level_properties['bg']:
			bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
		else:
			bg_tile = None

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
		self.setup(tmx_map, level_frames, audio_files)

		# frames
		self.pearl_surf = level_frames['pearl']
		self.particle_frames = level_frames['particle']

		# Звук
		self.coin_sound = audio_files['coin']
		self.coin_sound.set_volume(0.1)
		self.damage_sound = audio_files['damage']
		self.damage_sound.set_volume(0.2)
		self.pearl_sound = audio_files['pearl']

	def setup(self, tmx_map, level_frames, audio_files):
		# tiles
		for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
			for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
				groups = [self.all_sprites]
				if layer == 'Terrain': groups.append(self.collision_sprites)
				if layer == 'Platforms': groups.append(self.semi_collision_sprites)
				match layer:
					case 'BG':
						z = Z_LAYERS['bg tiles']
					case 'FG':
						z = Z_LAYERS['bg tiles']
					case _:
						z = Z_LAYERS['main']

				Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, z)


		# objects
		for obj in tmx_map.get_layer_by_name('Objects'):
			if obj.name == 'player':
				self.player = Player(
					pos=(obj.x, obj.y),
					groups=self.all_sprites,
					collision_sprites=self.collision_sprites,
					semi_collision_sprites=self.semi_collision_sprites,
					frames=level_frames['player'],
					data=self.data,
					attack_sound=audio_files['attack'],
					jump_sound=audio_files['jump'])
			else:
				if obj.name in ('barrel', 'crate'):
					Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
				else:
					if 'palm' not in obj.name:
						frames = level_frames[obj.name]
						if obj.name == 'floor_spike' and obj.properties['inverted']:
							frames = [pygame.transform.flip(frame, False, True) for frame in frames]

						# groups
						groups = [self.all_sprites]
						if obj.name in ('saw', 'floor_spike'): groups.append(self.damage_sprites)

						# z index
						z = Z_LAYERS['main'] if not 'bg' in obj.name else Z_LAYERS['bg details']

						# animation speed
						animation_speed = ANIMATION_SPEED if not 'palm' in obj.name else ANIMATION_SPEED + uniform(-1, 1)
						AnimatedSprite((obj.x, obj.y), frames, groups, z, animation_speed)
			if obj.name == 'flag':
				self.level_finish_rect = pygame.Rect((obj.x, obj.y), (obj.width, obj.height))

		# moving objects
		for obj in tmx_map.get_layer_by_name('Moving Objects'):
			if obj.name == 'spike':
				Spike(
					pos=(obj.x + obj.width / 2, obj.y + obj.height / 2),
					surf=level_frames['spike'],
					radius=obj.properties['radius'],
					speed=obj.properties['speed'],
					start_angle=obj.properties['start_angle'],
					end_angle=obj.properties['end_angle'],
					groups=(self.all_sprites, self.damage_sprites))
				for radius in range(0, obj.properties['radius'], 20):
					Spike(
						pos=(obj.x + obj.width / 2, obj.y + obj.height / 2),
						surf=level_frames['spike_chain'],
						radius=radius,
						speed=obj.properties['speed'],
						start_angle=obj.properties['start_angle'],
						end_angle=obj.properties['end_angle'],
						groups=self.all_sprites,
						z=Z_LAYERS['bg details'])

			else:
				frames = level_frames[obj.name]
				groups = (self.all_sprites, self.semi_collision_sprites) if obj.properties['platform'] else (
				self.all_sprites, self.damage_sprites)
				if obj.width > obj.height:  # horizontal
					move_dir = 'x'
					start_pos = (obj.x, obj.y + obj.height / 2)
					end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
				else:  # vertical
					move_dir = 'y'
					start_pos = (obj.x + obj.width / 2, obj.y)
					end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
				speed = obj.properties['speed']
				MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed, obj.properties['flip'])

				if obj.name == 'saw':
					if move_dir == 'x':
						y = start_pos[1] - level_frames['saw_chain'].get_height() / 2
						left, right = int(start_pos[0]), int(end_pos[0])
						for x in range(left, right, 20):
							Sprite((x, y), level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details'])
					else:
						x = start_pos[0] - level_frames['saw_chain'].get_width() / 2
						top, bottom = int(start_pos[1]), int(end_pos[1])
						for y in range(top, bottom, 20):
							Sprite((x, y), level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details'])

		# enemies
		for obj in tmx_map.get_layer_by_name('Enemies'):
			if obj.name == 'tooth':
				Tooth((obj.x, obj.y), level_frames['tooth'],
					  (self.all_sprites, self.damage_sprites, self.tooth_sprites), self.collision_sprites)
			if obj.name == 'shell':
				Shell(
					pos=(obj.x, obj.y),
					frames=level_frames['shell'],
					groups=(self.all_sprites, self.collision_sprites),
					reverse=obj.properties['reverse'],
					player=self.player,
					create_pearl=self.create_pearl)
			elif obj.name == 'boss':
				self.boss = Boss(
					pos=(obj.x, obj.y),
					frames=level_frames['boss'],
					groups=(self.all_sprites, self.damage_sprites),
					player=self.player,
					health=obj.properties.get('health', 20))

				self.player.boss = self.boss  # ПОМОГИТЕ

		# items
		for obj in tmx_map.get_layer_by_name('Items'):
			Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name],
				 (self.all_sprites, self.item_sprites), self.data)

		# water
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
		self.pearl_sound.play()

	def pearl_collision(self):
		for sprite in self.collision_sprites:
			sprite = pygame.sprite.spritecollide(sprite, self.pearl_sprites, True)
			if sprite:
				ParticleEffectSprite((sprite[0].rect.center), self.particle_frames, self.all_sprites)

	def hit_collision(self):
		for sprite in self.damage_sprites:
			if sprite.rect.colliderect(self.player.hitbox_rect):
				self.player.get_damage()
				self.damage_sound.play()
				if hasattr(sprite, 'pearl'):
					sprite.kill()
					ParticleEffectSprite((sprite.rect.center), self.particle_frames, self.all_sprites)

	def item_collision(self):
		if self.item_sprites:
			item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
			if item_sprites:
				item_sprites[0].activate()
				ParticleEffectSprite((item_sprites[0].rect.center), self.particle_frames, self.all_sprites)
				self.coin_sound.play()

	#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	def attack_collision(self):
		# Проверяем все объекты класса Shell
		for target in self.tooth_sprites.sprites() + [s for s in self.collision_sprites if isinstance(s, Shell)]:
			facing_target = (self.player.rect.centerx < target.rect.centerx and self.player.facing_right) or \
							(self.player.rect.centerx > target.rect.centerx and not self.player.facing_right)
			if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
				target.take_damage(1)

		# Проверяем босса отдельно, если он существует
		if self.boss:
			facing_boss = (self.player.rect.centerx < self.boss.rect.centerx and self.player.facing_right) or \
						  (self.player.rect.centerx > self.boss.rect.centerx and not self.player.facing_right)

			# ✅ Проверка: босс не в состоянии "hurt"
			if (
					self.boss.rect.colliderect(self.player.rect) and
					self.player.attacking and
					facing_boss and
					self.boss.state != 'hurt'  # 💥 не атаковать, если уже ранен
			):
				self.boss.take_damage(1)
				self.boss.state = 'hurt'
				self.boss.hurt_timer.activate()  # ⏱️ запускаем таймер неуязвимости

	def check_constraint(self):
		# Влево и вправо
		if self.player.hitbox_rect.left <= 0:
			self.player.hitbox_rect.left = 0
		if self.player.hitbox_rect.right >= self.level_width:
			self.player.hitbox_rect.right = self.level_width

		# bottom border — если упал, теряем жизнь и возвращаемся в оверворлд
		if self.player.hitbox_rect.bottom > self.level_bottom:
			self.data.health -= 1  # Уменьшаем здоровье
			self.switch_stage('overworld', -1)

		# Успех — достигли финишного флага
		if self.player.hitbox_rect.colliderect(self.level_finish_rect):
			if self.data.current_level == 19:  # если последний уровень
				self.bg_music.stop()
				self.switch_stage('overworld', 19)  # завершаем игру
			#-------------------------------------------------------------------------------извените сь это мое
			elif self.data.current_level == 0:
				#fade()
				cut1_5()
				#fade()
				cut2()
				#fade()
				cut2_5()
				self.switch_stage('overworld', self.level_unlock)
			else:
				self.switch_stage('overworld', self.level_unlock)

	# Метод обновления и отрисовки уровня в каждом кадре
	def run(self, dt):
		# Заполняем экран черным цветом перед отрисовкой след кадра
		self.display_surface.fill('black')

		# Обновляем все спрайты с учетом времени dt (используется для плавности движения)
		for sprite in self.all_sprites:
			if isinstance(sprite, Boss):
				sprite.update(dt, self.collision_sprites)
			else:
				sprite.update(dt)
		self.pearl_collision()
		self.hit_collision()
		self.item_collision()
		self.attack_collision()
		self.check_constraint()

		# Отрисовываем все спрайты на экране
		self.all_sprites.draw(self.player.hitbox_rect.center, dt)



