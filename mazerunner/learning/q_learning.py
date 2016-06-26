"""QLearning Algorithm.

Authors: Karina  --- <karina.bogdan@gmail.com>
         Agnaldo --- <agnaldo.esmael@ic.unicamp.br>

License: MIT (c) 2016

"""
import math
import numpy as np

from ..constants import ACTIONS


class QLearning(object):
    """QLearning.

    Determines a model which describes the actions taken by a RoboticAgent.

    # Actions = {0,1,2,3}, onde 0=ir para frente, 1=ir para tras, 2=vire aa Dir, 3=vire aa Esq.
    # percept eh um vetor float de 5 posicoes com as seguintes distancias em metros:
    #   percept[0]= distancia(NAO, objetivo)
    #   percept[1]= distancia captada pelo sonar_frente
    #   percept[2]= distancia captada pelo sonar_atras
    #   percept[3]= distancia captada pelo sonar_ombroDir
    #   percept[4]= distancia captada pelo sonar_ombroEsq
    """

    def __init__(self, percept, n_states=1024):
        self.n_states = n_states
        self.n_actions = len(ACTIONS)

        # parameters for q-learning rule
        self.alpha = 0.2  # learning rate
        self.gamma = 0.75  # discount factor

        self.epsilon = 0.2  # 20 cm -- Usado para determinar se o NAO mudou significativamente de posicao

        # parameters in order to define the states: 'close to obstacle', 'faraway', and 'collision state'
        # front-back (sonar)
        self.fs_min_value = 0.2
        self.fs_max_value = 0.5
        # side (sonar)
        self.ss_min_value = 0.1
        self.ss_max_value = 0.3

        # reward function parameters
        self.ireward_collision = -100
        self.ireward_backwards = 1
        self.ireward_forward = 1
        self.ireward_turnright = 1
        self.ireward_turnleft = 1
        self.ireward_closetothegoal = 10

        # environment actions:
        self.action_forward = 0
        self.action_turnright = 1
        self.action_turnleft = 2
        self.action_backwards = 3

        # environment states
        self.state_close = 0
        self.state_faraway = 1
        self.state_collision = 2
        self.state_closetogoal = 10
        self.state_sameplace = 11
        self.state_movedaway = 12

        # Q table
        self.random_state = np.random.RandomState(0)
        self.Q = self.random_state.rand(self.n_states, self.n_actions)

        # current status of NAO
        self.action = None
        self.distNAOtoObj = percept[
            0]  # recebe a distancia q o NAO esta do objetivo
        self.state_binary = self.discretize(percept)
        self.state_int = int(self.state_binary, 2)  # binay -> int

    # Requisicao de uma nova acao
    def getAction(self):
        self.action = np.argmax(self.Q[self.state_int])
        return self.action

    # Atualiza a tabela Q e estados apos realizar a acao instruida pelo getAction
    def setState(self, percept):
        r = self.reward(self.state_binary, self.action, self.distNAOtoObj)

        newS_binary = self.discretize(percept)
        newS_int = int(newS_binary, 2)  # binary --> int

        self.Q[self.state_int][self.action] = (1 - self.alpha) * (
            self.Q[self.state_int][self.action]) + self.alpha * (
            r + self.gamma * (np.max(self.Q[newS_int])))
        print(
            'current_action=', self.action, ', tabelaQold=',
            self.Q[self.state_int])
        print('current_action=', self.action, ', tabelaQnew=', self.Q[newS_int])

        # atualizacoes
        self.state_int = newS_int
        self.state_binary = newS_binary
        self.distNAOtoObj = percept[0]
        return

    def discretize(self, p):
        # funcao para discretizar o estado correspondente aa 'percept' --- gera uma string de bits 0s e 1s
        s = ''
        deltaDist = self.distNAOtoObj - p[0]
        s = s + self.auxStateDisc(deltaDist, (-1) * self.epsilon,
                                  self.epsilon)  # s=xx -> 00-aproximou, 01-manteve, 10-recuou
        s = s + self.auxStateDisc(p[1], self.fs_min_value,
                                  self.fs_max_value)  # s=xxyy  -> acrescimo: sonar da frente --> 00-longe, 01-perto, 10-colisao
        s = s + self.auxStateDisc(p[2], self.fs_min_value,
                                  self.fs_max_value)  # s=xxyyzz  -> acrescimo: sonar de tras
        s = s + self.auxStateDisc(p[3], self.ss_min_value,
                                  self.ss_max_value)  # s=xxyyzzdd  -> acrescimo: sonar direita
        s = s + self.auxStateDisc(p[4], self.ss_min_value,
                                  self.ss_max_value)  # s=xxyyzzddee  -> acrescimo: sonar esquerda

        print('s=', s)
        return s

    def auxStateDisc(self, value, minVal, maxVal):
        b = '00'
        if value < minVal:
            b = '10'
        elif minVal <= value <= maxVal:
            b = '01'
        return b

    # calcula a distancia do NAO ate o objetivo
    # def getDist(self, x, y):
    #	return math.sqrt((self.gp[0]-x)**2 + (self.gp[1]-y)**2)


    # function that returns the state from (two)bit-information,
    # considering if the state is obtained from sonar information or not (e.g. NAO moved to the goal)
    def getTState(self, state, sonar):
        dec_from_binary = int(state, 2)
        state_translated = -1

        if (sonar):
            if (dec_from_binary == 0):  # close to obstacle
                state_translated = self.state_close
            elif (dec_from_binary == 1):  # far away
                state_translated = self.state_faraway
            elif (dec_from_binary == 2):  # collision state
                state_translated = self.state_collision
        else:
            # estados da aproximacao
            if (dec_from_binary == 0):  # is close to the goal
                state_translated = self.state_closetogoal
            elif (dec_from_binary == 1):  # same place
                state_translated = self.state_sameplace
            elif (dec_from_binary == 2):  # moved away
                state_translated = self.state_movedaway

        return state_translated

    # get weight for the reward considering the distance to the goal.
    def getRWeight(self, distance):
        weight = 1 / math.exp(distance)
        return weight

    # immediate reward function
    def reward(self, state, action, distance_to_goal):
        total_reward = 0.0
        state_list = []
        size = len(state)
        start = 0
        end = 0

        while (end < size):
            end = end + 2
            current_state = state[start:end]
            state_list.append(current_state)
            start = end

        size_list = len(state_list)
        index = 0
        while (index < size_list):
            t_state = self.getTState(state_list[index],
                                     (False if index == 0 else True))

            if (t_state == -1): print('[IREWARD] Translated state is incorrect')

            # rewards related to states
            if (t_state == self.state_collision):
                total_reward += self.ireward_collision
            if (t_state == self.state_closetogoal):
                reward_weight = self.getRWeight(distance_to_goal)
                total_reward += (self.ireward_closetothegoal * reward_weight)
            index = index + 1

        # rewards related to actions
        if (action == self.action_forward):
            total_reward += self.ireward_forward
        elif (action == self.action_backwards):
            total_reward += self.ireward_backwards
        elif (action == self.action_turnleft):
            total_reward += self.ireward_turnleft
        elif (action == self.action_turnright):
            total_reward += self.ireward_turnright

        return total_reward
