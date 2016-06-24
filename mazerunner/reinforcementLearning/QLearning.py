"""Reinforcement Learning functions

Authors: Karina  --- 
		 Agnaldo --- agnaldo.esmael@ic.unicamp.br

"""
import numpy as np
import random
import math

# A classe QLearning -- determina as acoes do robo NAO
# Actions = {0,1,2,3}, onde 0=ir para frente, 1=ir para tras, 2=vire aa Dir, 3=vire aa Esq.
# percept eh um vetor float de 5 posicoes com as seguintes distancias em metros: 
#   percept[0]= distancia(NAO, objetivo)
#   percept[1]= distancia captada pelo sonar_frente
#   percept[2]= distancia captada pelo sonar_atras
#   percept[3]= distancia captada pelo sonar_ombroDir
#   percept[4]= distancia captada pelo sonar_ombroEsq

class QLearning(object):
	
	def __init__(self, percept):
		self.numStates = 1024
		self.numAction = 4
		self.alpha = 0.2
		self.gamma = 0.75
		self.action = None
		self.E = 0.2			# 20 cm -- Usado para determinar se o NAO mudou significativamente de posicao
		self.state_binary = self.stateDiscretization(percept)
		self.state_int = int(self.state_binary, 2)  # binay -> int
		self.distNAOtoObj = percept[0] # recebe a distancia q o NAO estah do objetivo
		self.Q = self.initQ()

	def initQ(self):
		mat = np.zeros((self.numStates,self.numAction))
		# inicializar com valores aleatorios [0.0, 1.0)
		# informando a semente da funcao radom
		random.seed(73)
		for i in range(self.numStates):
			for j in range(self.numAction):
				mat[i][j] = random.random()
		return mat

	#Lucas requisita uma nova acao 
	def getAction(self):
		self.action = np.argmax(Q[self.state_int])
		return self.action

	# Atualiza a tabela Q e estados apos realizar a acao instruida pelo getAction
	def setState(self, percept):
		r = self.reward(self.state_binary, self.action)
		newS_binary = self.stateDiscretization(percept)
		newS_int = int(newS_binary, 2)    #binary --> int
		Q[self.state_int][self.action] = (1-self.alpha)*(Q[self.state_int][self.action]) + self.alpha*(r + self.gamma*(np.max(Q[newS_int])))
		# atualizacoes
		self.state_int = newS_int
		self.state_binary = newS_binary
		self.distNAOtoObj = percept[0]
		return 

	#funcao para discretizar o estado correspondente aa 'percept' --- gera uma string de bits 0s e 1s
	def stateDiscretization(self, p):
		s = ''
		deltaDist = self.distNAOtoObj - p[0]
		s = s + self.auxStateDisc(deltaDist, (-1)*self.E, self.E) # s=xx -> 00-aproximou, 01-manteve, 10-recuou 
		s = s + self.auxStateDisc(p[2], 0.2, 0.5)   # s=xxyy  -> acrescimo: sonar da frente --> 00-longe, 01-perto, 10-colisao
		s = s + self.auxStateDisc(p[3], 0.2, 0.5)   # s=xxyyzz  -> acrescimo: sonar de tras
		s = s + self.auxStateDisc(p[4], 0.1, 0.3)   # s=xxyyzzdd  -> acrescimo: sonar direita
		s = s + self.auxStateDisc(p[5], 0.1, 0.3)   # s=xxyyzzddee  -> acrescimo: sonar esquerda
		return s

	def auxStateDisc(self, value, minVal, maxVal):
		b = '00'
		if(value < minVal):
			b = '10'
			else if( value >= minVal && value <= maxVal):
				b = '01'
		return b

	# calcula a distancia do NAO ate o objetivo
	#def getDist(self, x, y):
	#	return math.sqrt((self.gp[0]-x)**2 + (self.gp[1]-y)**2)

	#funcao de recompensa
	def reward(self, s, a):
		soma = 0.0
		if (s == 'colisao'):
			soma += -500
		#Falta terminar
		return 0
	
	
	
