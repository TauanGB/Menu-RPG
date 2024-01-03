import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy import Config
Config.set('graphics', 'multisamples', '0')

from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
import os
import json

class Cenario_box(MDBoxLayout):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

class Mosntro(MDBoxLayout):
	def __init__(self,Destino, *args, **kwargs):
		self.Destino = Destino
		super().__init__(*args, **kwargs)


class Cenario(MDApp):
	def build(self):
		super().build()
		self.last_size = self.get_file_size('Monstros.json')
		Evento = Clock.schedule_interval(self.Montiramento,4)
		self.root = Cenario_box()
		self.ultima_Jogada = ''
		return self.root
	
	def Full_Screen(self):
		if Window.fullscreen == False:
			Window.fullscreen = True
		else:
			Window.fullscreen = False
	
	def Montiramento(self,value):
		current_size = self.get_file_size('Monstros.json')
		if current_size != self.last_size:
			self.last_size = current_size

			self.root.ids.Grade_monstros.clear_widgets()


			print("O arquivo foi modificado!")
			with open('Monstros.json','r') as ARQ:
				self.Dados = json.load(ARQ)
		
			self.root.ids.Img_cenario.source = self.Dados["Cenario"]
			self.Monstros = self.Dados["Monstros"]
			
			if self.ultima_Jogada not in self.Monstros and self.ultima_Jogada != '' :
				self.ultima_Jogada = self.ultima_Jogada[0].split(',')
				if self.ultima_Jogada[2] in self.Dict_Monstrs_atual.keys():
					self.root.ids[self.ultima_Jogada[2]].ids.Estado.md_bg_color = [0.5,0.5,0.5,1]

			for Monst in self.Monstros:
				if Monst != '':
					MOSTRN_TMP = Mosntro(Monst)
					self.root.ids.Grade_monstros.add_widget(MOSTRN_TMP)
					
				
	
			


	def get_file_size(self,file_path):
		return os.stat(file_path).st_size

if __name__ == "__main__":
	global app
	app = Cenario().run()