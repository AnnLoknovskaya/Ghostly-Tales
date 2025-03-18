from settings import *
from sprites import Sprite, MovingSprite
from player import Player

# Создание уровня
class Level:
	def __init__(self, tmx_map):
		# Получаем поверхность экрана для отображения
		self.display_surface = pygame.display.get_surface()

		# Группы спрайтов для управления рендерингом и взаимодействием объектов
		self.all_sprites = pygame.sprite.Group() # Все спрайты
		self.collision_sprites = pygame.sprite.Group() # Спрайты, с которыми происходят коллизии
		self.semi_collision_sprites = pygame.sprite.Group() # Спрайты с частичными коллизиями

		# Инициализация уровня с использованием карты tmx
		self.setup(tmx_map)

	# Метод для создания тайлов (плиток) на основе слоя Terrain
	def setup(self, tmx_map):
		# Проходим по всем плиткам и создаем спрайты
		for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
			# Создаем статичный спрайт и добавляем его в соответствующие группы
			Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))

		# Создание объектов на основе слоя Objects
		for obj in tmx_map.get_layer_by_name('Objects'):
			# Если объект - игрок, создаем экземпляр класса Player
			if obj.name == 'player':
				Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.semi_collision_sprites)

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

	# Метод обновления и отрисовки уровня в каждом кадре
	def run(self, dt):
		# Заполняем экран черным цветом перед отрисовкой след кадра
		self.display_surface.fill('black')

		# Обновляем все спрайты с учетом времени dt (используется для плавности движения)
		self.all_sprites.update(dt)

		# Отрисовываем все спрайты на экране
		self.all_sprites.draw(self.display_surface)



