# Импорт необходимых модулей
import sys

from code_start.final_credits import final_credits
from mainA import main_menu, fade, play_music, stop_music
import pygame

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
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN) # Создание окна игры
		pygame.display.set_caption('Game') # Установка заголовка окна
		self.clock = pygame.time.Clock() # Создание игрового таймера для контроля FPS
		self.import_assets()


		self.ui = UI(self.font, self.ui_frames)
		self.data = Data(self.ui)
		# Загрузка карты уровня из TMX файла
		#AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
		self.tmx_maps = {
			# Обучение прыжкам
			0: load_pygame(join('..', 'data', 'levels', '0.tmx')),
			# Обучение сбору монет
			1: load_pygame(join('..', 'data', 'levels', '1.tmx')),
			# Обучение атакам на монстров
			2: load_pygame(join('..', 'data', 'levels', '2.tmx')),
			# Средний уровень №1
			3: load_pygame(join('..', 'data', 'levels', '3.tmx')),
			# Средний уровень №2
			4: load_pygame(join('..', 'data', 'levels', '4.tmx')),
			# Средний уровень №3
			5: load_pygame(join('..', 'data', 'levels', '5.tmx')),
			# Средний уровень №4
			6: load_pygame(join('..', 'data', 'levels', '6.tmx')),
			# Средний уровень №5
			7: load_pygame(join('..', 'data', 'levels', '7.tmx')),
			# Средний уровень №6
			8: load_pygame(join('..', 'data', 'levels', '8.tmx')),
			# Средний уровень №7
			9: load_pygame(join('..', 'data', 'levels', '9.tmx')),
			# Средний уровень №8
			10: load_pygame(join('..', 'data', 'levels', '10.tmx')),
			# Средний уровень №9
			11: load_pygame(join('..', 'data', 'levels', '11.tmx')),
			# Средний уровень №10
			12: load_pygame(join('..', 'data', 'levels', '12.tmx')),
			# Средний уровень №11
			13: load_pygame(join('..', 'data', 'levels', '13.tmx')),
			# Средний уровень №12
			14: load_pygame(join('..', 'data', 'levels', '14.tmx')),
			# Сложный уровень №1
			15: load_pygame(join('..', 'data', 'levels', '15.tmx')),
			# Сложный уровень №2
			16: load_pygame(join('..', 'data', 'levels', '16.tmx')),
			# Сложный уровень №3
			17: load_pygame(join('..', 'data', 'levels', '17.tmx')),
			# Финальный уровень
			18: load_pygame(join('..', 'data', 'levels', '18.tmx'))
		} # Загружаем карту и сохраняем в словарь

		self.bg_music = pygame.mixer.Sound(join('..', 'audio', 'my_roman_empire.mp3'))
		self.tmx_overworld = load_pygame(join('..', 'data', 'overworld', 'overworld.tmx'))
		self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage, self.bg_music) # Создаём объект Level с загруженной картой
		# self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames)
		#self.bg_music.play(-1)
		self.bg_music.set_volume(0.2)
		self.running = True

	def check_game_over(self):
		if self.data.health <= 0:
			self.bg_music.stop()
			self.running = False
			return True

		elif self.data.current_level == 19:
			self.data.coins = 0
			self.data.health = 5
			self.data.unlocked_level = 0
			self.data.current_level = 0
			self.data.save()
			self.bg_music.stop()
			self.running = False
			return True

		return False

	def switch_stage(self, target, unlock=0):
		if target == 'level':

			self.current_stage = Level(
				self.tmx_maps[self.data.current_level],
				self.level_frames,
				self.audio_files,
				self.data,
				self.switch_stage,
				self.bg_music
			)
		else:
			# <-- Эта проверка только для успешного завершения уровня
			if unlock > 0:
				self.data.unlocked_level = max(self.data.unlocked_level, unlock)
				if unlock == 19:
					self.running = False
					self.data.save()
					self.bg_music.stop()
					final_credits()
					return

			# Возвращаем в overworld на текущем уровне (даже если он не был пройден)
			self.current_stage = Overworld(
				self.tmx_overworld,
				self.data,
				self.overworld_frames,
				self.switch_stage
			)

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
			'candle_light': import_folder('..', 'graphics', 'level', 'candle light'),
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
			'spike_chain': import_image('..', 'graphics', 'enemies', 'spike_ball', 'spiked_chain'),
			'boss': import_sub_folders('..', 'graphics', 'enemies', 'boss')
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

		self.audio_files = {
			'coin': pygame.mixer.Sound(join('..', 'audio', 'coin.wav')),
			'attack': pygame.mixer.Sound(join('..', 'audio', 'attack.wav')),
			'jump': pygame.mixer.Sound(join('..', 'audio', 'jumpp.mp3')),
			'damage': pygame.mixer.Sound(join('..', 'audio', 'damage.wav')),
			'pearl': pygame.mixer.Sound(join('..', 'audio', 'pearl.wav')),
		}

	# def check_game_over(self):
	# 	if self.data.health <= 0:
	# 		self.bg_music.stop()
	# 		self.running = False

	def run(self):
		play_music()
		self.running = True
		while self.running:
			dt = self.clock.tick() / 1000
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.data.save()  # сохраняем прогресс
					pygame.quit()
					sys.exit()

				#-------------временный вариант выхода из игры в главное меню-------------------------
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						stop_music()
						self.data.save()  # сохраняем прогресс
						fade()
						main_menu()

			# Проверка условий завершения игры
			if self.check_game_over():
				fade()  # Можно сделать плавное затухание экрана
				main_menu()  # Возврат в главное меню
				break  # Выходим из игрового цикла


			# self.check_game_over()
			self.current_stage.run(dt)
			self.ui.update(dt)
			pygame.display.update()

# Запуск игры
# if __name__ == '__main__':
# 	game = Game() # Создаём экземпляр класса Game
# 	game.run() # Запускаем главный цикл игры