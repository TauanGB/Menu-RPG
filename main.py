import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy import Config
Config.set('graphics', 'multisamples', '0')

from kivy import Config
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.popup import Popup
from tkinter import filedialog as Fd
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import threading
import json


class Tela_inicial(MDScreen):
	def __init__(self, **kwargs):
		self.name = 'Tela_principal'
		self.Jogadores = {}
		self.Ordem_jogadores = []
		self.Sounds = {}
		self.Rodadas = 0
		self.Batalha_togle = False
		super().__init__(**kwargs)

		try:
			Musicas = [i for i in os.listdir('.\\Musicas') if os.path.isfile(os.path.join('.\\Musicas', i))]
		except:
			os.makedirs('Musicas')
			Musicas = [i for i in os.listdir('.\\Musicas') if os.path.isfile(os.path.join('.\\Musicas', i))]
		for i in Musicas:
			if '.mp' in i :
				i = Audio_box(i,self)

		with open('Monstros.json','w') as ARQ:
			self.Cenario = {"Cenario":"","Monstros":['']}
			json.dump(self.Cenario,ARQ)

		with open('Cenario Grade.json','w') as ARQ:
			json.dump('',ARQ)

		self.Thread_reserva = threading.Thread(target=self.Add_Musicas,args=(True,))
		self.Thread_reserva.start()
	
	def Adicionar_musica(self):
		Musica = Fd.askopenfilename(filetypes=[("Musicas",".mp3")])
		if Musica != "":
			Classe_Musica = [Audio_box(Musica,self),Musica]
			self.Thread_reserva = threading.Thread(target=self.Add_Musicas,args=(False,Classe_Musica))
			self.Thread_reserva.start()

	def Trocar_tela(self):
		if self.ids.Scree_Manager_Configs.current == 'Tela_ini':
			self.ids.Scree_Manager_Configs.current = 'Tela_Audio'
		else:
			self.ids.Scree_Manager_Configs.current = 'Tela_ini'

	def select_cenario(self,source):
		self.ids.img_cenario.source = source
		with open('Monstros.json','w') as ARQ:
			self.Cenario["Cenario"] = source
			json.dump(self.Cenario,ARQ)
	
	def select_cenario_2(self,source): 
		with open('Cenario Grade.json','w') as ARQ:
			json.dump(source,ARQ)

	def Adicionar_Cenarios_2(self):
		Diretorio_monstros = Fd.askdirectory()
		if Diretorio_monstros != "":
			Cenarios = [i for i in os.listdir(Diretorio_monstros) if os.path.isfile(os.path.join(Diretorio_monstros, i))]
			for i in Cenarios:
				self.ids.Box_cenarios_2.add_widget(Box_cenario_2(Diretorio_monstros+'/'+i,i.split('.')[0]))
			
	def Adicionar_Cenarios(self):
		Diretorio_monstros = Fd.askdirectory()
		if Diretorio_monstros != "":
			Cenarios = [i for i in os.listdir(Diretorio_monstros) if os.path.isfile(os.path.join(Diretorio_monstros, i))]
			for i in Cenarios:
				self.ids.Box_cenarios.add_widget(Box_cenario(Diretorio_monstros+'/'+i,i.split('.')[0]))

	def Add_Musicas(self,Boole,Musica=[]):
		if Boole == True :
			for i in range(len(list(self.Sounds.keys()))):
				print('Associando...')
				list(self.Sounds.keys())[i-1].Audio = SoundLoader.load(self.Sounds[list(self.Sounds.keys())[i-1]])
				print(f'{i+1}° item, Associado')
		else:
			print('Associando...')
			Musica[0].Audio = SoundLoader.load(Musica[1])
			print('item, Associado')

	def Adicionar_monstros(self):
		Diretorio_monstros = Fd.askdirectory()
		if Diretorio_monstros != "":
			Monstros = [i for i in os.listdir(Diretorio_monstros) if os.path.isfile(os.path.join(Diretorio_monstros, i))]
			for i in Monstros:
				if ".png" in i or ".jpg" in i or ".jpeg" in i:
					self.ids.Box_List_monstros.add_widget(Box_monstros(Diretorio_monstros+'/'+i,i.split('.')[0]))
			self.ids.Bt_adc_mosntros.width: self.ids.Box_List_monstros.widt *0.3

	def Ativar_monstro(self,source,nome):
		self.ids.Box_monstros_hp.add_widget(Monstro_Ativo(source,nome))
	
	def Adicionar_a_iniciativa(self,monstro):
		if monstro.ids.life.value >  0:
			if self.Batalha_togle == False:
				monstro.ids.Nome.text += ' N  %i'%self.ids.Box_monstros_hp.children.index(monstro)
				monstro.Nome += ' N  %i'%self.ids.Box_monstros_hp.children.index(monstro)
				self.ids.Box_Ordem_player.add_widget(Na_fila(monstro))
				monstro.remove_widget(monstro.ids.Buton_ad_iniciativa)
				monstro.Refer_Cenario = monstro.source+","+monstro.ids.Nome.text
				
			else:
				self.ids.Box_Ordem_player.children[self.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0.5,0.5,0.5,1]
				self.Turn_atual_jgdr += 1
				self.ids.Box_Ordem_player.add_widget(Na_fila(monstro))
				monstro.remove_widget(monstro.ids.Buton_ad_iniciativa)
				self.ids.Box_Ordem_player.children[self.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0,1,0,1]
				self.Refer_Cenario = monstro.source+","+' ,'+monstro.ids.Nome.text
		else:
			Pop_alerta('Adicione a vida maxima')
		

	def Adicionar_ao_cenario(self,monstro):
		if monstro.ids.life.value >  0:
			print(monstro.source)
			print(type(monstro.source))
			with open('Monstros.json','w') as ARQ:
				self.Cenario["Monstros"].append(monstro.source)
				json.dump(self.Cenario,ARQ)
				
			monstro.remove_widget(monstro.ids.Buton_ad_cenario)
				

		else:
			Pop_alerta('Adicione a vida maxima')

	def Adicionar_personagem(self,jogador):
		if jogador not in self.Jogadores.keys() and jogador != '':
			if self.Batalha_togle == False:
				self.Ordem_jogadores.append(jogador)
				jogador = Jogador(jogador,self.Ordem_jogadores.index(jogador))
				self.Jogadores[jogador.Nome] = jogador
				self.ids.Box_Players_dano.add_widget(No_dano(jogador))
				self.ids.Box_Ordem_player.add_widget(Na_fila(jogador))
				self.ids.Input_nome_perso.text = ''
			else:
				self.ids.Box_Ordem_player.children[self.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0.5,0.5,0.5,1]
				self.Turn_atual_jgdr += 1
				self.Ordem_jogadores.append(jogador)
				jogador = Jogador(jogador,self.Ordem_jogadores.index(jogador))
				self.Jogadores[jogador.Nome] = jogador
				self.ids.Box_Players_dano.add_widget(No_dano(jogador))
				self.ids.Box_Ordem_player.add_widget(Na_fila(jogador))
				self.ids.Input_nome_perso.text = ''
				self.ids.Box_Ordem_player.children[self.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0,1,0,1]
	
	def Pos_Antecedente(self,Box_referente):
		self.posição = self.ids.Box_Ordem_player.children.index(Box_referente)

		if self.posição >= len(self.ids.Box_Ordem_player.children)-1:
			self.ids.Box_Ordem_player.children[0],self.ids.Box_Ordem_player.children[self.posição]=self.ids.Box_Ordem_player.children[self.posição],self.ids.Box_Ordem_player.children[0]
		else:
			self.ids.Box_Ordem_player.children[self.posição+1],self.ids.Box_Ordem_player.children[self.posição]=self.ids.Box_Ordem_player.children[self.posição],self.ids.Box_Ordem_player.children[self.posição+1]
			
	def Pos_decendente(self,Box_referente):
		self.posição = self.ids.Box_Ordem_player.children.index(Box_referente)
		self.ids.Box_Ordem_player.children[self.posição-1],self.ids.Box_Ordem_player.children[self.posição]=self.ids.Box_Ordem_player.children[self.posição],self.ids.Box_Ordem_player.children[self.posição-1]

	def Iniciar_batalha(self):
		if len(self.ids.Box_Ordem_player.children) != 0 :
			if 	self.ids.Bt_Comandar_batalha.text != 'Encerrar Batalha':
				self.Turn_atual_jgdr = len(self.ids.Box_Ordem_player.children) -1
				self.ids.Box_Ordem_player.children[self.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0,1,0,1]
				self.ids.Bt_Comandar_batalha.text = 'Encerrar Batalha'
				self.Rodadas = 0
				self.Batalha_togle = True
			else:
				self.ids.Box_Ordem_player.children[self.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0.5,0.5,0.5,1]
				self.ids.Bt_Comandar_batalha.text = 'Iniciar Batalha'
				self.Batalha_togle = False
				for Index in self.ids.Box_Ordem_player.children:
					if Index.Cooldown != 0:
						Index.Cooldown = [0,0]
						Index.md_bg_color = [0.2,0.2,0.2,1]
					
	
	def Turno_Prox(self):
		if self.Batalha_togle == True:
			self.ids.Box_Ordem_player.children[self.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0.5,0.5,0.5,1]##mudando a cor pra padrap
			Pos = (self.Turn_atual_jgdr -1 )if self.Turn_atual_jgdr != 0 else len(self.ids.Box_Ordem_player.children)-1
			
			if Pos == len(self.ids.Box_Ordem_player.children)-1:
				self.Rodadas += 1
				self.ids.Rodada_label.text = str(self.Rodadas)

			
			self.ids.Box_Ordem_player.children[Pos].ids.BcgNome.md_bg_color = [0,1,0,1]
			self.Turn_atual_jgdr = Pos
			
			if self.ids.Box_Ordem_player.children[Pos].Cooldown[1] < self.Rodadas:
				if self.ids.Box_Ordem_player.children[Pos].Cooldown[0] == 1:
					self.ids.Box_Ordem_player.children[Pos].md_bg_color = [0.2,0.2,0.2,1]
					self.ids.Box_Ordem_player.children[Pos].Cooldown[0] -= 1
					self.ids.Box_Ordem_player.children[Pos].Cooldown[1] = self.Rodadas
				
				else:
					self.ids.Box_Ordem_player.children[Pos].Cooldown[0] -= 1
					self.ids.Box_Ordem_player.children[Pos].Cooldown[1] = self.Rodadas


		
	def Turno_Anter(self):
		if self.Batalha_togle == True:
			if self.Turn_atual_jgdr < len(self.ids.Box_Ordem_player.children)-1:
				self.ids.Box_Ordem_player.children[self.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0.5,0.5,0.5,1]##mudando a cor pra padrao
				self.Turn_atual_jgdr += 1
				self.ids.Box_Ordem_player.children[self.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0,1,0,1]

			else:
				self.ids.Box_Ordem_player.children[len(self.ids.Box_Ordem_player.children)-1].ids.BcgNome.md_bg_color = [0.5,0.5,0.5,1]
				self.Turn_atual_jgdr = 0
				self.Rodadas -= 1
				self.ids.Rodada_label.text = str(self.Rodadas)
				self.ids.Box_Ordem_player.children[self.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0,1,0,1]

class Box_cenario(MDBoxLayout):
	def __init__(self,source,nome, **kwargs):
		self.Nome = nome
		self.source =source
		super().__init__(**kwargs)

class Box_cenario_2(MDBoxLayout):
	def __init__(self,source,nome, **kwargs):
		self.Nome = nome
		self.source =source
		super().__init__(**kwargs)

class Box_monstros(MDBoxLayout):
	def __init__(self,source,nome, **kwargs):
		super().__init__(**kwargs)
		self.ids.Nome.text=nome
		self.ids.img.source=source

class Monstro_Ativo(MDBoxLayout):
	def __init__(self,source,nome, **kwargs):
		super().__init__(**kwargs)
		self.ids.Nome.text = nome 
		self.Refer_Cenario = ''
		self.ids.img.source = source
		self.Nome = nome
		self.source = source
		self.Box_referentes = {}

	def Add_vida(self,valor):
		try:
			valor = float(valor)
			if valor !='':
				self.ids.life.value = float(valor) + int(self.ids.life.value)
				self.ids.life_label.text = str(int(self.ids.life.value))
				self.ids.Hit_setado.text = ''

		except ValueError:
			Pop_alerta("Apenas numeros")

	def Definir_vida(self,valor):
		try:
			valor = float(valor)
			if valor != '':
				self.ids.life.max = float(valor)
				self.ids.life.value = float(valor)
				self.ids.life_label.text = str(int(self.ids.life.value))
				self.ids.Hit_setado.text = ''
		except:
			Pop_alerta("Apenas numeros")
		
	def Excluir_monstro(self,Tela):
		if len(self.Box_referentes.keys()) != 0:
			if Tela.Batalha_togle == True:
				if Tela.Turn_atual_jgdr == self.Box_referentes['Fila'].parent.children.index(self.Box_referentes['Fila']):
					if Tela.Turn_atual_jgdr == 0:
						Tela.ids.Box_Ordem_player.children[Tela.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0.5,0.5,0.5,1]
						Tela.Turn_atual_jgdr = len(self.Box_referentes['Fila'].parent.children)-2
						Tela.ids.Box_Ordem_player.children[Tela.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0,1,0,1]
					else:
						Tela.ids.Box_Ordem_player.children[Tela.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0.5,0.5,0.5,1]
						Tela.Turn_atual_jgdr -= 1
						Tela.ids.Box_Ordem_player.children[Tela.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0,1,0,1]

			Tela.ids.Box_Ordem_player.remove_widget(self.Box_referentes['Fila'])

			with open('Monstros.json','w') as ARQ:
				Tela.Cenario["Monstros"].pop(Tela.Cenario["Monstros"].index(self.source))
				json.dump(Tela.Cenario,ARQ)

		Tela.ids.Box_monstros_hp.remove_widget(self)

	def Dano_levado(self,valor,Tela):
		try:
			valor = float(valor)
			if valor != '' and self.ids.life.value > 0.2:
				self.ids.life.value -= valor
				if self.ids.life.value == 0:##apenas para desbugar a barra
					self.ids.life.value = 0.1
				self.ids.life_label.text = str(int(self.ids.life.value))
				self.ids.Hit_setado.text = ''
				if 'Encerrar Batalha' in Tela.ids.Bt_Comandar_batalha.text:
					if 'Historico' not in self.Box_referentes.keys():
						Tela.ids.Historico_batalha_box.add_widget(Monstro_historico(self))
						self.Box_referentes['Historico'].ids.His_hit_levado.add_widget(Box_label_contagem(Tela,valor,self.Box_referentes['Historico']))
						with open('Batalha.txt','a') as Arq:
							Arq.write(f'Spawnow Monstro: {self.Nome}\n')
							Arq.close()
					else:
						if Tela.ids.Box_Ordem_player.children[Tela.Turn_atual_jgdr].ids.Nome.text in self.Box_referentes['Historico'].Dano_ref_players.keys():
							Nome_player = Tela.ids.Box_Ordem_player.children[Tela.Turn_atual_jgdr].ids.Nome.text
							Var_dano = self.Box_referentes['Historico'].Dano_ref_players[Nome_player].ids.Dano.text.split('.')[0]
							self.Box_referentes['Historico'].Dano_ref_players[Nome_player].ids.Dano.text = str(int(Var_dano) + int(valor))
							with open('Batalha.txt','a') as Arq:
								Arq.write(f'{Nome_player} atacou mosntro {self.Nome} com {valor} de dano\n')
								Arq.close()
		
						else:
							self.Box_referentes['Historico'].ids.His_hit_levado.add_widget(Box_label_contagem(Tela,valor,self.Box_referentes['Historico']))
							with open('Batalha.txt','a') as Arq:
								Arq.write(f'{Tela.ids.Box_Ordem_player.children[Tela.Turn_atual_jgdr].ids.Nome.text} atacou mosntro {self.Nome} com {valor} de dano \n')
								Arq.close()
		except:
			Pop_alerta("Apenas numeros")
		
class Jogador():
	def __init__(self,Nome,iniciativa):
		self.Nome = Nome
		self.iniciativa = iniciativa
		self.Box_referentes = {}
	
class No_dano(MDBoxLayout):
	def __init__(self,Jogador, **kwargs):
		super().__init__(**kwargs)
		self.ids.Nome.text = Jogador.Nome
		self.JGdr = Jogador
		Jogador.Box_referentes['Dano'] = self
	
	def excluir_person(self,Tela):
		if len(self.JGdr.Box_referentes.keys()) != 0: 
			if Tela.Batalha_togle == True:
				if Tela.Turn_atual_jgdr == self.JGdr.Box_referentes['Fila'].parent.children.index(self.JGdr.Box_referentes['Fila']):
					if Tela.Turn_atual_jgdr == 0:
						Tela.ids.Box_Ordem_player.children[Tela.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0.5,0.5,0.5,1]
						Tela.Turn_atual_jgdr = self.Box_referentes['Fila'].parent.children -1
						Tela.ids.Box_Ordem_player.children[Tela.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0,1,0,1]
					else:
						Tela.ids.Box_Ordem_player.children[Tela.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0.5,0.5,0.5,1]
						Tela.Turn_atual_jgdr -= 1
						Tela.ids.Box_Ordem_player.children[Tela.Turn_atual_jgdr].ids.BcgNome.md_bg_color = [0,1,0,1]
				else:
					if Tela.Turn_atual_jgdr == 0:
						Tela.Turn_atual_jgdr = self.Box_referentes['Fila'].parent.children -1
					else:
						Tela.Turn_atual_jgdr -= 1
				
						
			Tela.ids.Box_Ordem_player.remove_widget(self.JGdr.Box_referentes['Fila'])
		self.parent.remove_widget(self)

class Na_fila(MDBoxLayout):
	def __init__(self,Jogador, **kwargs):
		super().__init__(**kwargs)
		self.Cooldown = [0,0]
		self.ids.Nome.text = Jogador.Nome
		Jogador.Box_referentes['Fila'] = self
	
	def Setar_coldown(self,Tela):
		self.Cooldown = [2,Tela.Rodadas]
		self.md_bg_color = [1,0,0,1]

class Monstro_historico(MDBoxLayout):
	def __init__(self,Monstro, **kwargs):
		super().__init__(**kwargs)
		self.ids.nome.text = Monstro.Nome
		Monstro.Box_referentes['Historico'] = self
		self.Dano_ref_players = {}

class Box_label_contagem(MDBoxLayout):
	def __init__(self, Tela, valor,Box, **kwargs):
		super().__init__(**kwargs)
		self.ids.nome.text = Tela.ids.Box_Ordem_player.children[Tela.Turn_atual_jgdr].ids.Nome.text
		self.ids.Dano.text = str(valor)
		Box.Dano_ref_players[self.ids.nome.text] = self

class Pop_alerta(Popup):
	def	__init__(self,Alerta, **kwargs):
		super().__init__(**kwargs)
		self.ids.Alerta.text = Alerta
		self.open()

class Audio_box(MDBoxLayout):
	def __init__(self, Name_tag, Tela,**kwargs):
		super().__init__(**kwargs)
		#Propiedades
		self.Mute,self.Musica_on = False , ''
		self.name = Name_tag
		self.tela = Tela
		self.Audio = SoundLoader()
		self.Link_som, Bar_event = '',''

		self.ids.Switch_mute.bind(active=self.replay)
		Tela.Sounds[self] = '.\\Musicas\\'+self.name
		self.Bt_referente = BT_Aba(self.name,Tela)
		Tela.ids.Abas_audio.add_widget(self)
	
	def Play_Pause(self):
		if self.Musica_on != '':
			if self.Audio.state == 'play':
				self.ids.Buton_play.icon='play'
				self.Audio.stop()
			else:
				self.Audio.play()
				self.ids.Buton_play.icon='pause'
		else:
			self.Audio.play()
			self.Musica_on = True
			self.ids.Buton_play.icon='pause'

			if self.ids.Switch_mute.active == True:
				self.Audio.loop = True
			else:
				self.Audio.loop = False
	## instance e o box que foi apertado, e value e o valor que fica e enviado
	def replay(self,instace,value):
		if value == True:
			self.Audio.loop = True
		else:
			self.Audio.loop = False
	
	def Volume_Slider(self,Value):	
		self.Audio.volume = int("%.0f"%Value)/100

	def Mutar(self):
		if self.Mute == False:
			self.ids.Volume_progess.value=0
			self.ids.Volume_progess.disabled = True
			self.Audio.volume = 0
			self.Mute = True
			self.ids.Bt_Mute.icon='volume-low'
		else:
			self.ids.Volume_progess.value=100
			self.ids.Volume_progess.disabled = False
			self.Audio.volume = 1
			self.Mute = False
			self.ids.Bt_Mute.icon='volume-high'

class BT_Aba(MDBoxLayout):
	def __init__(self,name,Tela , **kwargs):
		self.text = name
		self.Box_Audio = Tela.ids.Box_Audio
		super().__init__(**kwargs)

class main(MDApp):
	def build(self):
		return Tela_inicial()

if __name__ == "__main__":
	global app
	app = main().run()