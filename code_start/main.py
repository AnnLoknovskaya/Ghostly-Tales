# Импорт необходимых модулей
from settings import *
from level import Level
# Импорт функции загрузки карт TMX (карты, созданные в Tiled)
from pytmx.util_pygame import load_pygame
# Импорт функции для объединения путей (удобно для загрузки файлов)
from os.path import join

from support import *
from data import Data
from debug import debug
from ui import UI
from overworld import Overworld

# Класс Game — управляет всей игрой
class Game:
	def __init__(self):
		pygame.init() # Инициализация Pygame
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Создание окна игры
		pygame.display.set_caption('Game') # Установка заголовка окна
		self.clock = pygame.time.Clock() # Создание игрового таймера для контроля FPS
		self.import_assets()

		self.ui = UI(self.font, self.ui_frames)
		self.data = Data(self.ui)
		# Загрузка карты уровня из TMX файла
		self.tmx_maps = {
			0: load_pygame(join('..', 'data', 'levels', '0.tmx')),
			1: load_pygame(join('..', 'data', 'levels', '1.tmx')),
			2: load_pygame(join('..', 'data', 'levels', '2.tmx')),
			3: load_pygame(join('..', 'data', 'levels', '3.tmx')),
			4: load_pygame(join('..', 'data', 'levels', '4.tmx')),
			5: load_pygame(join('..', 'data', 'levels', '5.tmx')),
		} # Загружаем карту и сохраняем в словарь

		self.tmx_overworld = load_pygame(join('..', 'data', 'overworld', 'overworld.tmx'))
		self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.data, self.switch_stage) # Создаём объект Level с загруженной картой
		# self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames)

	def switch_stage(self, target, unlock=0):
		if target == 'level':
			self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.data,
									   self.switch_stage)
		else:
			if unlock > 0:
				self.data.unlocked_level = max(self.data.unlocked_level, unlock)  # ← важно: берем максимум!
			else:
				self.data.health -= 1
			self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)

	def import_assets(self):
		self.level_frames = {
			'flag': import_folder('..', 'graphics', 'level', 'flag'),
			'saw': import_folder('..', 'graphics', 'enemies', 'saw', 'animation'),
			'floor_spike': import_folder('..', 'graphics', 'enemies', 'floor_spikes'),
			'palms': import_sub_folders('..', 'graphics', 'level', 'palm'),
			'candle': import_folder('..', 'graphics', 'level', 'candle'),
			'window': import_folder('..', 'graphics', 'level', 'window'),
			'big_chain': import_folder('..', 'graphics', 'level', 'big_chain'),
			'small_chain': import_folder('..', 'graphics', 'level', 'small_chain'),
			'candle_light': import_folder('..', 'graphics', 'level', 'candle_light'),
			'player': import_sub_folders('..', 'graphics', 'player'),
			'tooth': import_folder('..', 'graphics', 'enemies', 'tooth', 'run'),
			'shell': import_sub_folders('..', 'graphics', 'enemies', 'shell'),
			'pearl': import_image('..', 'graphics', 'enemies', 'bullets', 'pearl'),
			'items': import_sub_folders('..', 'graphics', 'items'),
			'particle': import_folder('..', 'graphics', 'effects', 'particle'),
			'water_top': import_folder('..', 'graphics', 'level', 'water', 'top'),
			'water_body': import_image('..', 'graphics', 'level', 'water', 'body'),
			'boat': import_folder('..', 'graphics', 'objects', 'boat'),
			'bg_tiles': import_folder_dict('..', 'graphics', 'level', 'bg', 'tiles'),
			'cloud_small': import_folder('..', 'graphics', 'level', 'clouds', 'small'),
			'cloud_large': import_image('..', 'graphics', 'level', 'clouds', 'large_cloud'),
			'helicopter': import_folder('..', 'graphics', 'level', 'helicopter'),
			'saw_chain': import_image('..', 'graphics', 'enemies', 'saw', 'saw_chain'),
			'spike': import_image('..', 'graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
			'spike_chain': import_image('..', 'graphics', 'enemies', 'spike_ball', 'spiked_chain')
		}

		self.font = pygame.font.Font(join('..', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
		self.ui_frames = {
			'heart': import_folder('..', 'graphics', 'ui', 'heart'),
			'coin': import_image('..', 'graphics', 'ui', 'coin')
		}
		self.overworld_frames = {
			'palms': import_folder('..', 'graphics', 'overworld', 'palm'),
			'water': import_folder('..', 'graphics', 'overworld', 'water'),
			'path': import_folder_dict('..', 'graphics', 'overworld', 'path'),
			'icon': import_sub_folders('..', 'graphics', 'overworld', 'icon')
		}

	# Главный игровой цикл
	def run(self):
		while True:
			dt = self.clock.tick() / 1000 # Ограничение FPS и расчёт времени между кадрами (delta time)
			for event in pygame.event.get(): # Обрабатываем все события (например, нажатия клавиш, выход)
				if event.type == pygame.QUIT: # Если нажата кнопка закрытия окна
					pygame.quit() # Закрываем Pygame
					sys.exit() # Выходим из программы

			# Запуск обновления и отрисовки текущего уровня
			self.current_stage.run(dt)
			self.ui.update(dt)
			# Обновление экрана (отрисовка нового кадра)
			pygame.display.update()

# Запуск игры
if __name__ == '__main__':
	game = Game() # Создаём экземпляр класса Game
	game.run() # Запускаем главный цикл игры