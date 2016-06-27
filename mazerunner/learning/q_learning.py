"""QLearning Algorithm.

Authors: Karina  --- <karina.bogdan@gmail.com>
         Agnaldo --- <agnaldo.esmael@ic.unicamp.br>

License: MIT (c) 2016

"""
import math
import numpy as np
from mazerunner.constants import ACTIONS, AGENT_STATES, ACTION_SELECTION


def aux_state_discretization(value, min_value, max_value):
    binary = '00'
    if value < min_value:
        binary = '10'
    elif min_value <= value <= max_value:
        binary = '01'
    return binary


def get_weight_from(distance):
    weight = 1 / math.exp(distance)
    return weight


class QLearning(object):
    """
    # A classe QLearning -- determina as acoes do robo NAO
    # Actions = {0,1,2,3}, onde 0=ir para frente, 1=ir para tras, 2=vire aa Dir, 3=vire aa Esq.
    # percept eh um vetor float de 5 posicoes com as seguintes distancias em metros:
    #   percept[0]= distancia(NAO, objetivo)
    #   percept[1]= distancia captada pelo sonar_frente
    #   percept[2]= distancia captada pelo sonar_atras
    #   percept[3]= distancia captada pelo sonar_ombroDir
    #   percept[4]= distancia captada pelo sonar_ombroEsq
    """

    IMMEDIATE_REWARD = {
        'collision': -100,
        'backwards': 1,
        'forward': 1,
        'clockwise': 1,
        'cclockwise': 1,
        'closetothegoal': 10
    }

    def __init__(self, num_states=1024, num_action=4,
                 alpha=0.1, gamma=0.75, epsilon=0.2,
                 front_sonar_min_value=0.2, front_sonar_max_value=0.5, side_sonar_min_value=0.1, side_sonar_max_value=0.3,
                 action_selection=ACTION_SELECTION.greedy, action_selection_epsilon=0.5):
        self._num_states = num_states
        self._num_action = num_action

        # parameters for q-learning rule
        self._alpha = alpha   # learning rate
        self._gamma = gamma   # discount factor

        self._epsilon = epsilon  # 20 cm -- Usado para determinar se o NAO mudou significativamente de posicao

        # parameters in order to define the states: 'close to obstacle', 'faraway', and 'collision state'
        # front-back (sonar)
        self._front_sonar_min_value = front_sonar_min_value
        self._front_sonar_max_value = front_sonar_max_value
        # side (sonar)
        self._side_sonar_min_value = side_sonar_min_value
        self._side_sonar_max_value = side_sonar_max_value

        self._action_selection = action_selection
        self._action_selection_epsilon = action_selection_epsilon  #parameter for e-greedy selection

        # Q table
        self.random_state = np.random.RandomState(0)
        self.Q = self.random_state.rand(self._num_states, self._num_action)



    # initiates the q-learning algorithm with an initial percept
    def start_learning(self, percept):
        # current status of NAO
        self._action = None
        self.distance_NAO_to_goal = percept[0]  # recebe a distancia q o NAO esta do objetivo
        self.state_binary = self.discretize(percept)
        self.state_int = int(self.state_binary, 2)  # binay -> int


    def action(self):
        """
        Returns the action to be executed considering the selection method chosen.
        :return: the next action to be executed by the agent
        """
        if (self._action_selection == ACTION_SELECTION.greedy):
            self._action = np.argmax(self.Q[self.state_int])
        elif (self._action_selection == ACTION_SELECTION.e_greedy):
            probability_q = self.random_state.random_sample(1)[0]

            if (probability_q <= self._action_selection_epsilon):
                random_index = self.random_state.randint(0, self._num_action)
                print('random action = ', random_index)

                new_action = None
                if (random_index == ACTIONS.forward):
                    new_action = ACTIONS.forward
                elif (random_index == ACTIONS.backward):
                    new_action = ACTIONS.backward
                elif (random_index == ACTIONS.clockwise):
                    new_action = ACTIONS.clockwise
                elif (random_index == ACTIONS.cclockwise):
                    new_action = ACTIONS.cclockwise

                self._action = new_action
            else:
                self._action = np.argmax(self.Q[self.state_int])

        return self._action



    def set_state(self, percept):
        """
         Update the table Q after the execution of the current action producing a new percept (percept)
        :param percept: percept generate after the current action
        :return: new state(t+1) of the agent
        """
        r = self.reward(self.state_binary, self._action, self.distance_NAO_to_goal)

        new_state_binary = self.discretize(percept)
        new_state_int = int(new_state_binary, 2)  # binary --> int

        self.Q[self.state_int][self._action] = (1 - self._alpha) * (
            self.Q[self.state_int][self._action]) + self._alpha * (
            r + self._gamma * (np.max(self.Q[new_state_int])))
        print('current_action=', self._action, ', tabelaQold=', self.Q[self.state_int])
        print('current_action=', self._action, ', tabelaQnew=', self.Q[new_state_int])

        # atualizacoes
        self.state_int = new_state_int
        self.state_binary = new_state_binary
        self.distance_NAO_to_goal = percept[0]
        return



    def discretize(self, p):
        """
         Discretization of the percept p, generating the current state of the agent.
        :param p: current percept of the environment by the agent.
        :return: String composed by 0s and 1s - concatenation of the binary values of each state produced by the percept p.
        """
        s = ''
        delta_distance = self.distance_NAO_to_goal - p[0]
        s = s + aux_state_discretization(delta_distance, (-1) * self._epsilon, self._epsilon)  # s=xx -> 00-aproximou, 01-manteve, 10-recuou
        s = s + aux_state_discretization(p[1], self._front_sonar_min_value, self._front_sonar_max_value)  # s=xxyy  -> acrescimo: sonar da frente --> 00-longe, 01-perto, 10-colisao
        s = s + aux_state_discretization(p[2], self._front_sonar_min_value, self._front_sonar_max_value)  # s=xxyyzz  -> acrescimo: sonar de tras
        s = s + aux_state_discretization(p[3], self._side_sonar_min_value, self._side_sonar_max_value)  # s=xxyyzzdd  -> acrescimo: sonar direita
        s = s + aux_state_discretization(p[4], self._side_sonar_min_value, self._side_sonar_max_value)  # s=xxyyzzddee  -> acrescimo: sonar esquerda

        print('s=', s)
        return s


    def get_translated_state(self, state, sonar):
        """
          Function that returns the state from (two)bit-information,
          considering if the state is obtained from sonar information or not (e.g. NAO moved to the goal)
        :param state: current state (binary representation)
        :param sonar: boolean indicating if the state is from a sonar or not
        :return:
        """
        dec_from_binary = int(state, 2)
        state_translated = -1

        if (sonar):
            if (dec_from_binary == 0):  # close to obstacle
                state_translated = AGENT_STATES.close
            elif (dec_from_binary == 1):  # far away
                state_translated = AGENT_STATES.faraway
            elif (dec_from_binary == 2):  # collision state
                state_translated = AGENT_STATES.collision
        else:
            # estados da aproximacao
            if (dec_from_binary == 0):  # is close to the goal
                state_translated = AGENT_STATES.closetogoal
            elif (dec_from_binary == 1):  # same place
                state_translated = AGENT_STATES.sameplace
            elif (dec_from_binary == 2):  # moved away
                state_translated = AGENT_STATES.movedaway

        return state_translated


    def reward(self, state, action, distance_to_goal):
        """
         Immediate reward function
        :param state:
        :param action:
        :param distance_to_goal:
        :return: the reward value for either an action or state passed by parameter
        """
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
            t_state = self.get_translated_state(state_list[index], (False if index == 0 else True))

            if (t_state == -1): print('[IREWARD] Translated state is incorrect')

            # rewards related to states
            if (t_state == AGENT_STATES.collision):
                total_reward += self.IMMEDIATE_REWARD['collision']
            if (t_state == AGENT_STATES.closetogoal):
                reward_weight = get_weight_from(distance_to_goal)
                total_reward += (self.IMMEDIATE_REWARD['closetothegoal'] * reward_weight)
            index = index + 1

        # rewards related to actions
        if (action == ACTIONS.forward):
            total_reward += self.IMMEDIATE_REWARD['forward']
        elif (action == ACTIONS.backward):
            total_reward += self.IMMEDIATE_REWARD['backwards']
        elif (action == ACTIONS.cclockwise):
            total_reward += self.IMMEDIATE_REWARD['cclockwise']
        elif (action == ACTIONS.clockwise):
            total_reward += self.IMMEDIATE_REWARD['clockwise']

        print('total reward=', total_reward)
        return total_reward



# # exemplo de como seria a execucao
# print('pra frente essa coisa', ACTIONS.forward)
# x = ACTIONS.forward
# print(x)
percept = [2.0, 0.6, 0.5, 0.4, 0.4]
objeto = QLearning()
print(objeto.IMMEDIATE_REWARD['collision'])



# # TODO definir se chegou no objetivo ou alcancou um numero maximo de iteracoes
objeto.start_learning(percept)
for i in range(5):
    action = objeto.action()
    print('action=', action)

    # so exemplo mudando a distancia do objetivo e o sensor da frente
    percept[1] -= 0.1
    percept[0] -= 0.1

    objeto.set_state(percept)
