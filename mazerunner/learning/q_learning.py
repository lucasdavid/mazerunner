"""QLearning Algorithm.

Authors:
    Agnaldo     -- <agnaldo.esmael@ic.unicamp.br>
    Karina      -- <karina.bogdan@gmail.com>
    Lucas David -- <ld492@drexel.edu>


License: MIT (c) 2016

"""
import logging
import math
import numpy as np

from ..constants import Actions, AgentStates

logger = logging.getLogger('mazerunner')


def binary_code(value, min_value, max_value):
    return ('10' if value < min_value else
            '01' if min_value <= value <= max_value else
            '00')


def get_weight_from(distance):
    weight = 1 / math.exp(distance)
    return weight


def decode_state(state, sonar):
    """Function that returns the state from (two)bit-information,
    considering if the state is obtained from sonar information
    or not (e.g. NAO moved to the goal).

    :param state: current state (binary representation)
    :param sonar: boolean indicating if the state is from a sonar or not
    :return:
    """
    dec_from_binary = int(state, 2)
    state_translated = -1

    if sonar:
        if dec_from_binary == 0:  # close to obstacle
            state_translated = AgentStates.CLOSE
        elif dec_from_binary == 1:  # far away
            state_translated = AgentStates.FARAWAY
        elif dec_from_binary == 2:  # collision state
            state_translated = AgentStates.COLLISION
    else:
        # estados da aproximacao
        if dec_from_binary == 0:  # is close to the goal
            state_translated = AgentStates.CLOSE_TO_GOAL
        elif dec_from_binary == 1:  # same place
            state_translated = AgentStates.SOME_PLACE
        elif dec_from_binary == 2:  # moved away
            state_translated = AgentStates.MOVED_AWAY

    return state_translated


class QLearning(object):
    """QLearning.

    Q-learning algorithm for RoboticAgents' walk.

    """

    IMMEDIATE_REWARD = {
        Actions.BACKWARD: 1,
        Actions.FORWARD: 1,
        Actions.CLOCKWISE: 1,
        Actions.CCLOCKWISE: 1,
        'collision': -100,
        'closetothegoal': 10,
    }
    DELTA_MOVE_THRESHOLD = .2

    def __init__(self, n_states=1024, n_actions=4,
                 alpha=0.1, gamma=0.75,
                 strategy='greedy', epsilon=.5,
                 front_sonar_min_value=.2, front_sonar_max_value=.5,
                 side_sonar_min_value=.2, side_sonar_max_value=.5,
                 random_state=None):
        self.n_states = n_states
        self.n_actions = n_actions

        # learning rate
        self.alpha = alpha
        # discount factor
        self.gamma = gamma

        # parameters in order to define the states:
        # 'close to obstacle', 'faraway', and 'collision state'
        # front-back (sonar)
        self._front_sonar_min_value = front_sonar_min_value
        self._front_sonar_max_value = front_sonar_max_value
        # side (sonar)
        self._side_sonar_min_value = side_sonar_min_value
        self._side_sonar_max_value = side_sonar_max_value

        self.strategy = strategy
        self.epsilon = epsilon

        self.random_state = random_state or np.random.RandomState()
        self.Q_ = self.random_state.rand(self.n_states, self.n_actions)

        self.action = Actions.FORWARD
        self.distance_to_goal = np.inf
        self.state_code = self.discretize(5 * [np.inf])

    def update(self, percept):
        """Update the table Q after the execution of the current action, which
        produced a new perception of the environment; then find which action
        should be executed next.

        :param percept: array-like, the current perception of the environment.
        """
        random = self.random_state

        Q, old_state, a = self.Q_, int(self.state_code, 2), self.action
        r = self.reward(self.state_code, a, self.distance_to_goal)

        state_code = self.discretize(percept)
        state = int(state_code, 2)

        Q[old_state, a] = ((1 - self.alpha) * Q[old_state, a] +
                           self.alpha * (r + self.gamma * np.max(Q[state])))

        self.distance_to_goal = percept[0]
        self.state_code = state_code

        if self.strategy == 'greedy' or random.rand() > self.epsilon:
            self.action = np.argmax(self.Q_[state])

        elif self.strategy == 'e-greedy':
            self.action = random.randint(0, self.n_actions)
            logger.info('%i was randomly chosen.', self.action)

        else:
            raise ValueError('Incorrect value for strategy: %s'
                             % self.strategy)

        logger.info('\nprevious action: %i\n'
                    'current action: %i\n'
                    'Q[old_state]: %s\n'
                    'Q[state]: %s\n'
                    'state_code: %s',
                    a, self.action, Q[old_state], Q[state], state_code)

        return self

    def discretize(self, p):
        """Discretize a perception `p`, generating the current state of the
        agent.

        :param p: current perception of the environment by the agent.
        :return: str, a binary sequence that describes the perception.
            E.g.: 0110110010 and 1110011011.

        """
        return (
            binary_code(self.distance_to_goal - p[0],
                        (-1) * self.DELTA_MOVE_THRESHOLD,
                        self.DELTA_MOVE_THRESHOLD) +
            binary_code(p[1], self._front_sonar_min_value,
                        self._front_sonar_max_value) +
            binary_code(p[2], self._front_sonar_min_value,
                        self._front_sonar_max_value) +
            binary_code(p[3], self._side_sonar_min_value,
                        self._side_sonar_max_value) +
            binary_code(p[4], self._side_sonar_min_value,
                        self._side_sonar_max_value)
        )

    def reward(self, state, action, distance_to_goal):
        """Immediate Reward Function."""
        reward = 0.0
        chunks = [state[start: start + 2] for start in range(0, len(state), 2)]

        for i, chunk in enumerate(chunks):
            decoded_state = decode_state(chunk, sonar=i)

            if decoded_state == -1:
                logger.error('[IREWARD] decoded state is incorrect')

            # rewards related to states
            if decoded_state == AgentStates.COLLISION:
                reward += self.IMMEDIATE_REWARD['collision']

            elif decoded_state == AgentStates.CLOSE_TO_GOAL:
                reward += (self.IMMEDIATE_REWARD['closetothegoal'] *
                           get_weight_from(distance_to_goal))

        # rewards related to actions.
        reward += self.IMMEDIATE_REWARD[action]

        logger.info('reward: %i', reward)
        return reward
