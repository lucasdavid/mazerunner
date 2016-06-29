"""Q-learning Algorithm.

Authors:
    Agnaldo     -- <agnaldo.esmael@ic.unicamp.br>
    Karina      -- <karina.bogdan@gmail.com>
    Lucas David -- <ld492@drexel.edu>


License: MIT (c) 2016

"""
import logging
import math
import numpy as np

from ..constants import Actions, AgentStates, MAX_LEARNING_CYCLES
from .. import utils

logger = logging.getLogger('mazerunner')


def binary_code(value, min_value, max_value):
    return ('10' if value < min_value else
            '01' if min_value <= value <= max_value else
            '00')


def weight_for_distance(distance):
    return 1 - distance / 28


def weight_for_cycle(cycle):
    return 1 - cycle / MAX_LEARNING_CYCLES


def decode_state(state, sonar):
    """Function that returns the state from (two)bit-information,
    considering if the state is obtained from sonar information
    or not (e.g. NAO moved to the goal).

    :param state: current state (binary representation)
    :param sonar: boolean indicating if the state is from a sonar or not
    :return: int
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
    """Q-learning.

    Q-learning algorithm for RoboticAgents' walk.

    :param n_states: int, default=1024
        Number of possible states considered by the agent.

    :param n_actions: int, default=4
        Number of possible actions considered by the agent.
        Must match `constants.Actions` enumeration.

    :param alpha: float, default=.1
        Learning rate of the algorithm.

    :param gamma: float, default=.75
        Discount factor.

    :param strategy: str, default='greedy'
        Strategy used when selecting actions. Options are:
        --- 'greedy': selects the best option available.
        --- 'e-greedy': selects a random action with probability `epsilon`
            and the best action available with probability `1-epsilon`.

    :param epsilon: float, default=.5
        Probability of randomly selecting a action when strategy is 'e-greedy'.

    :param front_sonar_min_value:
    :param front_sonar_max_value:
    :param side_sonar_min_value:
    :param side_sonar_max_value:

    :param checkpoint: int, default=None
        If an integer, it will save a snapshot of the current model
        (the table Q) every `checkpoint` iterations.

    :param saving_name: str, default='snapshot.model.gz'
        File name used to save the model's snapshot. Used when persisting
        multiple models (E.g.: training multiple agents).

    :param random_state: RandomState-like
        Used to control the randomness of QLearning objects.

    """

    IMMEDIATE_REWARD = {
        Actions.FORWARD: 1,
        Actions.BACKWARD: 1,
        Actions.CLOCKWISE: 1,
        Actions.CCLOCKWISE: 1,
        'collision': -10,
        'closetothegoal': 5,
    }

    DELTA_MOVE_DETECTION_THRESHOLD = .2

    def __init__(self, n_states=1024, n_actions=4,
                 alpha=0.1, gamma=0.75,
                 strategy='greedy', epsilon=.5,
                 Q=None,
                 front_sonar_min_value=.2, front_sonar_max_value=.5,
                 side_sonar_min_value=.2, side_sonar_max_value=.5,
                 checkpoint=None,
                 saving_name='snapshot.model.gz',
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
        self.checkpoint = checkpoint

        self.saving_name = saving_name
        self.random_state = random_state or np.random.RandomState()

        self.Q_ = (Q if Q is not None else
                   self.random_state.rand(self.n_states, self.n_actions))

        self.cycle_ = 1
        self.action_ = Actions.FORWARD
        self.distance_to_goal_ = 17
        self.state_code_ = self.discretize(5 * [np.inf])

    def update(self, percept):
        """Update the table Q after the execution of the current action, which
        produced a new perception of the environment; then find which action
        should be executed next.

        :param percept: array-like, the current perception of the environment.
        """
        logger.info('perception received: %s', percept)
        logger.info('current iteration: %i', self.cycle_)
        random = self.random_state

        Q, old_state, a = self.Q_, int(self.state_code_, 2), self.action_
        r = self.reward(self.state_code_, a, self.distance_to_goal_)

        state_code = self.discretize(percept)
        state = int(state_code, 2)

        Q[old_state, a] = ((1 - self.alpha) * Q[old_state, a] +
                           self.alpha * (r + self.gamma * np.max(Q[state])))

        self.distance_to_goal_ = percept[0]
        old_state_code = self.state_code_
        self.state_code_ = state_code

        if self.strategy == 'greedy' or random.rand() > (
                self.epsilon * weight_for_cycle(self.cycle_)):
            self.action_ = np.argmax(self.Q_[state])

        elif self.strategy == 'e-greedy':
            self.action_ = random.randint(0, self.n_actions)
            logger.info('%i was randomly chosen. (e=%f)', self.action_, (
                self.epsilon * weight_for_cycle(self.cycle_)))

        else:
            raise ValueError('Incorrect value for strategy: %s'
                             % self.strategy)

        if self.checkpoint and self.cycle_ % self.checkpoint == 0:
            logger.info('saving snapshot of Q-learning model...')
            utils.ModelStorage.save(self.Q_, name=self.saving_name)

        self.cycle_ += 1

        logger.info('\nepsilon-e-greedy: %f, weight:%f\n'
                    'previous and current actions: %i, %i\n'
                    'Q[old_state]: %s\n'
                    'Q[state]: %s\n'
                    'old_state: %i, state: %i\n'
                    'old_state_code: %s, state_code: %s',
                    self.epsilon * weight_for_cycle(self.cycle_),
                    weight_for_cycle(self.cycle_),
                    a, self.action_, Q[old_state], Q[state], old_state, state,
                    old_state_code, state_code)

        return self

    def discretize(self, p):
        """Discretize a perception `p`, generating the current state of the
        agent.

        :param p: current perception of the environment by the agent.
        :return: str, a binary sequence that describes the perception.
            E.g.: 0110110010 and 1110011011.

        """
        return (
            binary_code(self.distance_to_goal_ - p[0],
                        (-1) * self.DELTA_MOVE_DETECTION_THRESHOLD,
                        self.DELTA_MOVE_DETECTION_THRESHOLD) +
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
        reward = 0
        chunks = [state[start: start + 2] for start in range(0, len(state), 2)]

        for i, chunk in enumerate(chunks):
            decoded_state = decode_state(chunk, sonar=i)

            if decoded_state == -1:
                logger.error('[IREWARD] decoded state is incorrect')

            # rewards related to states
            if decoded_state == AgentStates.COLLISION:
                reward += self.IMMEDIATE_REWARD['collision']

            elif decoded_state == AgentStates.CLOSE_TO_GOAL:
                reward_proximity = (self.IMMEDIATE_REWARD['closetothegoal'] *
                                    weight_for_distance(distance_to_goal))
                reward += reward_proximity
                logger.info('distance: %f, reward-proximity: %f',
                            distance_to_goal, reward_proximity)

        # rewards related to actions.
        reward += self.IMMEDIATE_REWARD[action]

        logger.info('reward: %f', reward)
        return reward
