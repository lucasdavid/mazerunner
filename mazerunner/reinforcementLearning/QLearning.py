"""Reinforcement Learning functions

Authors: Karina e Agnaldo

"""
import numpy as np
import random
import math

class QLearning(goalPosition, percept):
#goalPosition eh um vetor de duas posicoes:x,y (tipo float)
#percept eh um vetor de 5 posicoes:x_atual_NAO, y_atual_NAO, sonar_frente, sonar_atras, sonar_ombroD, sonarOmbroE (tipo float)
	
	def __init__(self):
		self.gp = goalPosition
		self.numStates = 1024
		self.numAction = 4
		self.alpha = 0.2
		self.gamma = 0.75
		self.atualA = 0		# inicia com um valor qq -- vai ser atualiza na primeira chamada de getAction
		self.E = 0.2		# 20 cm -- Usado para determinar se o NAO mudou significativamente de posicao
		self.atualS_binary = self.stateDiscretization(percept)
		self.atualS = int(self.atualS_binary, 2)  # binay -> int
		self.oldDist = getDist(percept[0],percept[1])
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
		self.atualA = np.argmax(Q[atualS])
		return self.atualA

	# Atualiza a tabela Q e estados apos realizar a acao instruida pelo getAction
	def setState(self, percept):
		r = self.reward(self.atualS_binary,self.oldA)
		newS_binary = self.stateDiscretization(percept)
		newS = int(newS_binary, 2)    #binary --> int
		Q[self.atualS][self.atualA] = (1-self.alpha)*(Q[self.atualS][self.atualA]) + self.alpha*(r + self.gamma*(np.max(Q[newS])))
		# atualizacoes
		self.atualS = newS
		self.atualS_binary = newS_binary
		self.oldDist = getDist(percept[0],percept[1])
		return 

	#funcao para discretizar o estado correspondente aa 'percept' --- gera uma string de bits 0s e 1s
	def stateDiscretization(self, p):
		s = ''
		deltaDist = self.oldDist - self.getDist(p[0],p[1])
		s = s + self.auxStateDisc(deltaDist, (-1)*self.E, self.E) # s=xx -> aproximou/manteve/recuou
		s = s + self.auxStateDisc(p[2], 0.2, 0.5)   # s=xxyy  -> acrescimo: sonar da frente
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
	def getDist(self, x, y):
		return math.sqrt((self.gp[0]-x)**2 + (self.gp[1]-y)**2)

	#funcao de recompensa
	def reward(self, s, a):
		soma = 0.0
		if (s == 'colisao'):
			soma += -500
		#Falta terminar
		return 0
	
	
	
