"""Reinforcement Learning functions

Authors: Karina e Agnaldo

"""
import numpy as np
import random

class QLearning(goalPosition, percept):
#goalPosition eh um vetor de duas posicoes:x,y (tipo float)
#percept eh um vetor de 5 posicoes:x_atual, y_atual, sonar_frente, sonar_atras, sonar_ombroD, sonarOmbroE (tipo float)
	self.gp = goalPosition
	self.Q = self.initQ()
	self.numStates = 1024
	self.numAction = 4
	self.alpha = 0.2
	self.gamma = 0.75
	self.oldS = 0  # estado em t-1  --- comeca com valor aleatorio
	self.oldA = 0  # acao tomada em t-1  --- comeca com valor aleatorio

	def initQ(self):
		mat = np.zeros((self.numStates,self.numAction))
		# inicializar com valores aleatorios [0.0, 1.0)
		# informando a semente da funcao radom
		random.seed(73)
		for i in range(self.numStates):
			for j in range(self.numAction):
				mat[i][j] = random.random()
		return mat

	#Lucas requisita uma nova acao passando 'percept'
	#'percept' eh usado para obter o estado atual: atualS
	def getAction(self, percept):
		atualS = self.getState(percept)
		Q[self.oldS][self.oldA] = (1-self.alpha)*(Q[self.oldS][self.oldA]) + self.alpha*(self.reward(self.atualS,self.oldA) + self.gamma*(np.max(Q[atualS])))
		newA = np.argmax(Q[atualS])
		self.oldS = atualS
		self.oldA = newA
		return newA

	#funcao para localizar qual linha de Q corresponde ao estado que obtemos de 'percept'
	def getState(self, p):
		#falta terminar
		return 0
	
	#funcao de recompensa
	def reward(self, s, a):
		soma = 0.0
		if (s == 'colisao'):
			soma += -500
		#Falta terminar
		return 0
	
	#funcao para determinar o estado (0 ... 1023) de 'percept'
	# '0000000000' = Q[0] entao deve retornar 0.
	#


	
