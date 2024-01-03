import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy import Config
Config.set('graphics', 'multisamples', '0')

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import os
import json

class Cenario_box(BoxLayout):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

class Cenario_2(MDApp):
	def build(self):
		super().build()
		self.last_size = self.get_file_size('Cenario Grade.json')
		Evento = Clock.schedule_interval(self.Montiramento,3)
	
		self.root = Cenario_box()
		self.ultima_Jogada = ''


	def Full_Screen(self):
		if Window.fullscreen == False:
			Window.fullscreen = True
		else:
			Window.fullscreen = False

	def Montiramento(self,value):
		current_size = self.get_file_size('Cenario Grade.json')
		if current_size != self.last_size:
			self.last_size = current_size
			print("O arquivo foi modificado!")
			with open('Cenario Grade.json','r') as ARQ:
				self.Cenario = json.load(ARQ)
		
			self.root.ids.Img_cenario.source = self.Cenario

			


	def get_file_size(self,file_path):
		return os.stat(file_path).st_size

if __name__ == "__main__":
	global app
	app = Cenario_2().run()